import json
from urllib.parse import quote
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_session
from app.core.deps import require_admin
from app.core.exceptions import AppException
from app.core.security import (
    ADMIN_COOKIE_NAME,
    create_admin_session,
    create_csrf_token,
    verify_admin_credentials,
    verify_admin_session,
    verify_csrf_token,
)
from app.model.agent_roles import AgentRoles
from app.model.providers import Providers
from app.model.tools import Tools
from app.schemas.agent_roles import (
    AgentCreate,
    AgentUpdate,
    parse_approval_tools,
)
from app.schemas.chat import ChatApprovalRequest, ChatRequest
from app.schemas.providers import ProviderCreate, ProviderUpdate
from app.schemas.skills import SkillCreate, SkillUpdate
from app.schemas.tools import (
    ToolCreate,
    ToolUpdate,
    parse_available_tools,
    server_names,
)
from app.services import (
    agent_service,
    chat_service,
    message_service,
    provider_service,
    session_service,
    skill_service,
    tool_service,
)
from Yue.agent.graph import get_graph, reset_graph
from settings import BASE_DIR, settings

"""
    ═══════════════════════════════════════════════════
                    管理后台（服务端渲染）
    ═══════════════════════════════════════════════════

    按服务划分：
        登录 / 退出
        角色管理  → app/services/agent_service.py
        厂商管理  → app/services/provider_service.py

    路由：
        GET  /admin                        重定向到角色列表
        GET  /admin/login                  登录页
        POST /admin/login                  校验账号密码，下发签名 cookie
        POST /admin/logout                 清除 cookie

        GET  /admin/roles                  角色列表
        GET  /admin/roles/new              新建角色表单
        POST /admin/roles                  创建角色
        GET  /admin/roles/{id}/edit        编辑角色表单
        POST /admin/roles/{id}/edit        更新角色
        POST /admin/roles/{id}/delete      删除角色

        GET  /admin/tools                  工具列表
        GET  /admin/tools/new              新建工具表单
        POST /admin/tools                  创建工具
        GET  /admin/tools/{id}/edit        编辑工具表单
        POST /admin/tools/{id}/edit        更新工具
        POST /admin/tools/{id}/delete      删除工具

        GET  /admin/skills                 技能列表
        GET  /admin/skills/new             新建技能表单
        POST /admin/skills                 创建技能
        POST /admin/skills/import          从 skills/ 目录导入
        GET  /admin/skills/{id}/edit       编辑技能表单
        POST /admin/skills/{id}/edit       更新技能
        POST /admin/skills/{id}/delete     删除技能

        GET  /admin/providers              厂商列表
        GET  /admin/providers/new          新建厂商表单
        POST /admin/providers              创建厂商
        GET  /admin/providers/{id}/edit    编辑厂商表单
        POST /admin/providers/{id}/edit    更新厂商
        POST /admin/providers/{id}/delete  删除厂商

        GET  /admin/sessions               会话列表（搜索 / 分页）
        GET  /admin/sessions/{session_id}  会话详情（回放消息）
        POST /admin/sessions/{id}/delete   删除会话
        POST /admin/sessions/delete        批量删除勾选的会话

        GET  /admin/playground             测试页面（SSE 对话）
        POST /admin/playground/stream      测试页面的流式接口
        POST /admin/playground/approve     人工审批后继续运行
"""

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=str(BASE_DIR / "template"))


# ————————————————————————————————————————————————
#  后台公共工具
# ————————————————————————————————————————————————


# —————————生成登录成功后的安全跳转地址————————
def _safe_next(raw: str | None) -> str:
    """只允许跳回 /admin 下的路径，避免 open redirect。"""
    if raw and raw.startswith("/admin") and not raw.startswith("//"):
        return raw
    return "/admin/roles"


# —————————读取当前请求的管理员会话 cookie————————
def _session_token(request: Request) -> str:
    return request.cookies.get(ADMIN_COOKIE_NAME, "")


# —————————生成表单 CSRF token————————
def _csrf_token(request: Request) -> str:
    return create_csrf_token(_session_token(request))


# —————————校验表单 CSRF token————————
def _csrf_ok(request: Request, token: str) -> bool:
    token_in_cookie = _session_token(request)
    return bool(token_in_cookie) and verify_csrf_token(token_in_cookie, token)


# —————————构造 303 跳转（可携带提示/错误）————————
def _redirect(
    path: str, *, msg: str | None = None, err: str | None = None
) -> RedirectResponse:
    params = []
    if msg:
        params.append(f"msg={quote(msg)}")
    if err:
        params.append(f"err={quote(err)}")
    separator = "&" if "?" in path else "?"
    url = path + (separator + "&".join(params) if params else "")
    return RedirectResponse(url=url, status_code=303)


# —————————会话列表地址：保留搜索与页码————————
def _sessions_path(q: str = "", page: int = 1) -> str:
    params = []
    if q:
        params.append(f"q={quote(q)}")
    if page > 1:
        params.append(f"page={page}")
    return "/admin/sessions" + ("?" + "&".join(params) if params else "")


# —————————解析角色表单里的工具勾选 JSON————————
def _parse_tool_selection(raw: str) -> dict[str, list[str]]:
    try:
        data = json.loads(raw or "{}")
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, list[str]] = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[str(key)] = [
                str(name) for name in value if isinstance(name, str) and name
            ]
    return result


# —————————解析角色表单里的审批工具列表 JSON（数组）————————
def _parse_approval_tools(raw: str) -> list[str]:
    try:
        data = json.loads(raw or "[]")
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return list(dict.fromkeys(
        str(name) for name in data if isinstance(name, str) and name
    ))


# —————————格式化 Pydantic 校验错误————————
def _validation_errors(exc: ValidationError) -> list[str]:
    result = []
    for item in exc.errors():
        loc = ".".join(str(p) for p in item.get("loc", ()))
        result.append(f"{loc}: {item.get('msg')}" if loc else str(item.get("msg")))
    return result


# —————————渲染模板时注入的公共上下文————————
def _base_context(request: Request, **extra) -> dict:
    return {
        "app_name": settings.APP_NAME,
        "username": settings.ADMIN_USERNAME,
        "csrf": _csrf_token(request),
        **extra,
    }


# ————————————————————————————————————————————————
#  登录 / 退出
# ————————————————————————————————————————————————


# —————————后台入口，统一跳到角色列表————————
@router.get("/admin", include_in_schema=False)
async def admin_index():
    return _redirect("/admin/roles")


# —————————登录页；已登录则直接跳目标页————————
@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request, next: str = "/admin/roles"):
    if verify_admin_session(_session_token(request)):
        return _redirect(_safe_next(next))

    return templates.TemplateResponse(
        request,
        "admin/login.html",
        _base_context(
            request,
            next_path=_safe_next(next),
            error=None,
            username="",
        ),
    )


# —————————提交登录：校验账号密码并写入会话 cookie————————
@router.post("/admin/login")
async def login_submit(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    next: str = Form("/admin/roles"),
):
    if not verify_admin_credentials(username.strip(), password):
        return templates.TemplateResponse(
            request,
            "admin/login.html",
            _base_context(
                request,
                next_path=_safe_next(next),
                error="账号或密码错误",
                username=username,
            ),
            status_code=401,
        )

    response = _redirect(_safe_next(next))
    response.set_cookie(
        ADMIN_COOKIE_NAME,
        create_admin_session(settings.ADMIN_USERNAME),
        max_age=settings.ADMIN_SESSION_TTL,
        httponly=True,
        samesite="strict",
        secure=settings.ADMIN_COOKIE_SECURE,
        # 管理员会话同时用于 /api 下的管理操作（如删除会话、记忆）
        path="/",
    )
    return response


# —————————退出登录：清除会话 cookie————————
@router.post("/admin/logout")
async def logout():
    response = _redirect("/admin/login")
    response.delete_cookie(ADMIN_COOKIE_NAME, path="/")
    return response


# ————————————————————————————————————————————————
#  角色管理 → app/services/agent_service.py
# ————————————————————————————————————————————————


# —————————角色表单的初始值————————
def _empty_role_form() -> dict:
    return {
        "slug": "",
        "name": "",
        "role": "worker",
        "description": "",
        "system_prompt": "",
        "provider_id": "",
        "sort_order": 0,
        "enabled": True,
        "is_output_gate": False,
        "tool_ids": [],
        "approval_tools": [],
    }


# —————————渲染角色表单（新建/编辑共用）————————
async def _render_role_form(
    request: Request,
    session: AsyncSession,
    *,
    mode: str,
    form: dict,
    errors: list[str],
    role_id: str | None = None,
    selected_tool_ids: list[str] | None = None,
    tool_selection: dict[str, list[str]] | None = None,
    selected_approval_tools: list[str] | None = None,
    status_code: int = 200,
):
    providers = (
        await session.execute(select(Providers).order_by(Providers.name.asc()))
    ).scalars().all()
    tools = (
        await session.execute(select(Tools).order_by(Tools.name.asc()))
    ).scalars().all()

    return templates.TemplateResponse(
        request,
        "admin/role_form.html",
        _base_context(
            request,
            mode=mode,
            role_id=role_id,
            form=form,
            errors=errors,
            providers=providers,
            tools=tools,
            tool_available={
                t.id: parse_available_tools(t.available_tools) for t in tools
            },
            selected_tool_ids=selected_tool_ids or form.get("tool_ids") or [],
            tool_selection=(
                tool_selection
                if tool_selection is not None
                else form.get("tool_selection") or {}
            ),
            selected_approval_tools=(
                selected_approval_tools
                if selected_approval_tools is not None
                else form.get("approval_tools") or []
            ),
            is_supervisor=form.get("role") == "supervisor",
        ),
        status_code=status_code,
    )


# —————————角色列表：展示全部角色（含停用）及厂商名称————————
@router.get("/admin/roles", response_class=HTMLResponse)
async def roles_page(
    request: Request,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    roles = (
        await session.execute(
            select(AgentRoles)
            .options(selectinload(AgentRoles.tools))
            .order_by(
                AgentRoles.role.asc(),  # supervisor 在前
                AgentRoles.sort_order.asc(),
                AgentRoles.created_at.asc(),
            )
        )
    ).scalars().all()

    providers = (
        await session.execute(select(Providers).order_by(Providers.name.asc()))
    ).scalars().all()

    return templates.TemplateResponse(
        request,
        "admin/roles.html",
        _base_context(
            request,
            roles=roles,
            provider_names={p.id: p.name for p in providers},
            approval_counts={
                r.id: len(parse_approval_tools(r.approval_tools)) for r in roles
            },
            msg=msg,
            err=err,
        ),
    )


# —————————新建角色表单————————
@router.get("/admin/roles/new", response_class=HTMLResponse)
async def new_role_page(
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    return await _render_role_form(
        request, session, mode="create", form=_empty_role_form(), errors=[]
    )


# —————————创建角色：校验 CSRF → Pydantic → agent_service.create_agent————————
@router.post("/admin/roles")
async def create_role(
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    role: str = Form("worker"),
    description: str = Form(""),
    system_prompt: str = Form(""),
    provider_id: str = Form(""),
    sort_order: int = Form(0),
    enabled: str | None = Form(None),
    is_output_gate: str | None = Form(None),
    tool_ids: list[str] = Form([]),
    tool_selection: str = Form("{}"),
    approval_tools: str = Form("[]"),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    selection = _parse_tool_selection(tool_selection)
    approvals = _parse_approval_tools(approval_tools)
    form = {
        "slug": slug,
        "name": name,
        "role": role,
        "description": description,
        "system_prompt": system_prompt,
        "provider_id": provider_id,
        "sort_order": sort_order,
        "enabled": enabled is not None,
        "is_output_gate": is_output_gate is not None,
        "tool_ids": tool_ids,
        "tool_selection": selection,
        "approval_tools": approvals,
    }

    if not _csrf_ok(request, csrf):
        return await _render_role_form(
            request, session, mode="create", form=form,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = AgentCreate(
            slug=slug,
            name=name,
            role=role,  # type: ignore[arg-type]
            description=description,
            system_prompt=system_prompt,
            provider_id=provider_id or None,
            sort_order=sort_order,
            enabled=enabled is not None,
            is_output_gate=(
                False if role == "supervisor" else is_output_gate is not None
            ),
            approval_tools=[] if role == "supervisor" else approvals,
        )
    except ValidationError as exc:
        return await _render_role_form(
            request, session, mode="create", form=form,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        agent = await agent_service.create_agent(session, payload)
        await tool_service.set_agent_tools(
            session, agent.id, tool_ids, selection
        )
    except AppException as exc:
        return await _render_role_form(
            request, session, mode="create", form=form,
            errors=[exc.message], status_code=exc.status_code,
        )

    # 角色变更：丢弃已编译的图，下一次请求重新构建
    reset_graph()
    return _redirect("/admin/roles", msg=f"已创建角色「{name}」")


# —————————编辑角色表单：读取 agent_service.get_agent————————
@router.get("/admin/roles/{role_id}/edit", response_class=HTMLResponse)
async def edit_role_page(
    role_id: str,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        role = await agent_service.get_agent(session, role_id)
    except AppException as exc:
        return _redirect("/admin/roles", err=exc.message)

    form = {
        "slug": role.slug,
        "name": role.name,
        "role": role.role,
        "description": role.description or "",
        "system_prompt": role.system_prompt,
        "provider_id": role.provider_id or "",
        "sort_order": role.sort_order,
        "enabled": role.enabled,
        "is_output_gate": role.is_output_gate,
        "approval_tools": parse_approval_tools(role.approval_tools),
    }
    selection = await tool_service.get_agent_tool_selection(session, role.id)
    return await _render_role_form(
        request,
        session,
        mode="edit",
        form=form,
        errors=[],
        role_id=role.id,
        selected_tool_ids=list(selection),
        tool_selection=selection,
        selected_approval_tools=parse_approval_tools(role.approval_tools),
    )


# —————————更新角色：唯一调度员的角色与启用状态保持锁定————————
@router.post("/admin/roles/{role_id}/edit")
async def update_role(
    role_id: str,
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    role: str = Form("worker"),
    description: str = Form(""),
    system_prompt: str = Form(""),
    provider_id: str = Form(""),
    sort_order: int = Form(0),
    enabled: str | None = Form(None),
    is_output_gate: str | None = Form(None),
    tool_ids: list[str] = Form([]),
    tool_selection: str = Form("{}"),
    approval_tools: str = Form("[]"),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    selection = _parse_tool_selection(tool_selection)

    try:
        existing = await agent_service.get_agent(session, role_id)
    except AppException as exc:
        return _redirect("/admin/roles", err=exc.message)

    # 唯一调度员：角色与启用状态在服务层被锁死，这里保持原值
    is_supervisor = existing.role == "supervisor"
    approvals = (
        parse_approval_tools(existing.approval_tools)
        if is_supervisor
        else _parse_approval_tools(approval_tools)
    )
    form = {
        "slug": slug,
        "name": name,
        "role": "supervisor" if is_supervisor else role,
        "description": description,
        "system_prompt": system_prompt,
        "provider_id": provider_id,
        "sort_order": sort_order,
        "enabled": True if is_supervisor else enabled is not None,
        "is_output_gate": (
            False if is_supervisor else is_output_gate is not None
        ),
        "tool_ids": tool_ids,
        "tool_selection": selection,
        "approval_tools": approvals,
    }

    if not _csrf_ok(request, csrf):
        return await _render_role_form(
            request, session, mode="edit", form=form, role_id=role_id,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = AgentUpdate(
            slug=slug,
            name=name,
            role=form["role"],  # type: ignore[arg-type]
            description=description,
            system_prompt=system_prompt,
            provider_id=provider_id or None,
            sort_order=sort_order,
            enabled=form["enabled"],
            is_output_gate=form["is_output_gate"],
            approval_tools=None if is_supervisor else approvals,
        )
    except ValidationError as exc:
        return await _render_role_form(
            request, session, mode="edit", form=form, role_id=role_id,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await agent_service.update_agent(session, role_id, payload)
        # 调度员不使用工具，保存时不要清空它的历史挂载
        if not is_supervisor:
            await tool_service.set_agent_tools(
                session, role_id, tool_ids, selection
            )
    except AppException as exc:
        return await _render_role_form(
            request, session, mode="edit", form=form, role_id=role_id,
            errors=[exc.message], status_code=exc.status_code,
        )

    # 角色变更：丢弃已编译的图，下一次请求重新构建
    reset_graph()
    return _redirect("/admin/roles", msg=f"已保存角色「{name}」")


# —————————删除角色：调度员会被 agent_service 拒绝————————
@router.post("/admin/roles/{role_id}/delete")
async def delete_role(
    role_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/roles", err="页面已过期，请刷新后重试")

    try:
        await agent_service.delete_agent(session, role_id)
    except AppException as exc:
        return _redirect("/admin/roles", err=exc.message)

    # 角色变更：丢弃已编译的图，下一次请求重新构建
    reset_graph()
    return _redirect("/admin/roles", msg="角色已删除")


# ————————————————————————————————————————————————
#  工具管理 → app/services/tool_service.py
# ————————————————————————————————————————————————


# —————————工具表单的初始值————————
def _empty_tool_form() -> dict:
    return {
        "slug": "",
        "name": "",
        "description": "",
        "config": "",
        "enabled": True,
    }


# —————————渲染工具表单（新建/编辑共用）————————
async def _render_tool_form(
    request: Request,
    *,
    mode: str,
    form: dict,
    errors: list[str],
    tool_id: str | None = None,
    available: list[dict] | None = None,
    status_code: int = 200,
):
    return templates.TemplateResponse(
        request,
        "admin/tool_form.html",
        _base_context(
            request,
            mode=mode,
            tool_id=tool_id,
            form=form,
            errors=errors,
            available=available or [],
        ),
        status_code=status_code,
    )


# —————————工具列表：展示服务名、挂载的员工数————————
@router.get("/admin/tools", response_class=HTMLResponse)
async def tools_page(
    request: Request,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    tools = await tool_service.list_tools(session)

    return templates.TemplateResponse(
        request,
        "admin/tools.html",
        _base_context(
            request,
            tools=tools,
            servers={t.id: server_names(t.config) for t in tools},
            available={
                t.id: parse_available_tools(t.available_tools) for t in tools
            },
            msg=msg,
            err=err,
        ),
    )


# —————————新建工具表单————————
@router.get("/admin/tools/new", response_class=HTMLResponse)
async def new_tool_page(
    request: Request,
    _: dict = Depends(require_admin),
):
    return await _render_tool_form(
        request, mode="create", form=_empty_tool_form(), errors=[]
    )


# —————————创建工具：校验 CSRF → ToolCreate → tool_service.create_tool————————
@router.post("/admin/tools")
async def create_tool(
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    description: str = Form(""),
    config: str = Form(""),
    enabled: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    form = {
        "slug": slug,
        "name": name,
        "description": description,
        "config": config,
        "enabled": enabled is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_tool_form(
            request, mode="create", form=form,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = ToolCreate(
            slug=slug,
            name=name,
            description=description,
            config=config,
            enabled=enabled is not None,
        )
    except ValidationError as exc:
        return await _render_tool_form(
            request, mode="create", form=form,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await tool_service.create_tool(session, payload)
    except AppException as exc:
        return await _render_tool_form(
            request, mode="create", form=form,
            errors=[exc.message], status_code=exc.status_code,
        )

    # 工具变更：丢弃已编译的图
    reset_graph()
    return _redirect("/admin/tools", msg=f"已创建工具「{name}」")


# —————————编辑工具表单————————
@router.get("/admin/tools/{tool_id}/edit", response_class=HTMLResponse)
async def edit_tool_page(
    tool_id: str,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        tool = await tool_service.get_tool(session, tool_id)
    except AppException as exc:
        return _redirect("/admin/tools", err=exc.message)

    form = {
        "slug": tool.slug,
        "name": tool.name,
        "description": tool.description or "",
        "config": tool.config,
        "enabled": tool.enabled,
    }
    return await _render_tool_form(
        request,
        mode="edit",
        form=form,
        errors=[],
        tool_id=tool.id,
        available=parse_available_tools(tool.available_tools),
    )


# —————————更新工具————————
@router.post("/admin/tools/{tool_id}/edit")
async def update_tool(
    tool_id: str,
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    description: str = Form(""),
    config: str = Form(""),
    enabled: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        await tool_service.get_tool(session, tool_id)
    except AppException as exc:
        return _redirect("/admin/tools", err=exc.message)

    form = {
        "slug": slug,
        "name": name,
        "description": description,
        "config": config,
        "enabled": enabled is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_tool_form(
            request, mode="edit", form=form, tool_id=tool_id,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = ToolUpdate(
            slug=slug,
            name=name,
            description=description,
            config=config,
            enabled=enabled is not None,
        )
    except ValidationError as exc:
        return await _render_tool_form(
            request, mode="edit", form=form, tool_id=tool_id,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await tool_service.update_tool(session, tool_id, payload)
    except AppException as exc:
        return await _render_tool_form(
            request, mode="edit", form=form, tool_id=tool_id,
            errors=[exc.message], status_code=exc.status_code,
        )

    # 工具变更：丢弃已编译的图
    reset_graph()
    return _redirect("/admin/tools", msg=f"已保存工具「{name}」")


# —————————拉取工具：连接 MCP 服务，把实际工具清单存进数据库————————
@router.post("/admin/tools/{tool_id}/refresh")
async def refresh_tool(
    tool_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/tools", err="页面已过期，请刷新后重试")

    try:
        tool = await tool_service.refresh_tool_tools(session, tool_id)
    except AppException as exc:
        return _redirect("/admin/tools", err=exc.message)

    count = len(parse_available_tools(tool.available_tools))
    return _redirect("/admin/tools", msg=f"已拉取 {count} 个工具")


# —————————角色编辑页内联拉取：返回 JSON，供挂载工具列表实时展示————————
@router.post("/admin/tools/{tool_id}/probe")
async def probe_tool(
    tool_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return JSONResponse(
            {"ok": False, "msg": "页面已过期，请刷新后重试"}, status_code=400
        )

    try:
        tool = await tool_service.refresh_tool_tools(session, tool_id)
    except AppException as exc:
        return JSONResponse(
            {"ok": False, "msg": exc.message}, status_code=exc.status_code
        )

    found = parse_available_tools(tool.available_tools)
    return JSONResponse({"ok": True, "count": len(found), "tools": found})


# —————————删除工具：挂载关系一起清理————————
@router.post("/admin/tools/{tool_id}/delete")
async def delete_tool(
    tool_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/tools", err="页面已过期，请刷新后重试")

    try:
        await tool_service.delete_tool(session, tool_id)
    except AppException as exc:
        return _redirect("/admin/tools", err=exc.message)

    # 工具变更：丢弃已编译的图
    reset_graph()
    return _redirect("/admin/tools", msg="工具已删除")


# ————————————————————————————————————————————————
#  技能管理 → app/services/skill_service.py
# ————————————————————————————————————————————————


# —————————技能表单的初始值————————
def _empty_skill_form() -> dict:
    return {
        "slug": "",
        "name": "",
        "description": "",
        "content": "",
        "enabled": True,
    }


# —————————渲染技能表单（新建/编辑共用）————————
async def _render_skill_form(
    request: Request,
    *,
    mode: str,
    form: dict,
    errors: list[str],
    skill_id: str | None = None,
    status_code: int = 200,
):
    return templates.TemplateResponse(
        request,
        "admin/skill_form.html",
        _base_context(
            request,
            mode=mode,
            skill_id=skill_id,
            form=form,
            errors=errors,
        ),
        status_code=status_code,
    )


# —————————技能列表：展示全部技能及挂载员工数————————
@router.get("/admin/skills", response_class=HTMLResponse)
async def skills_page(
    request: Request,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    skills = await skill_service.list_skills(session)

    return templates.TemplateResponse(
        request,
        "admin/skills.html",
        _base_context(request, skills=skills, msg=msg, err=err),
    )


# —————————新建技能表单————————
@router.get("/admin/skills/new", response_class=HTMLResponse)
async def new_skill_page(
    request: Request,
    _: dict = Depends(require_admin),
):
    return await _render_skill_form(
        request, mode="create", form=_empty_skill_form(), errors=[]
    )


# —————————创建技能————————
@router.post("/admin/skills")
async def create_skill(
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    description: str = Form(""),
    content: str = Form(""),
    enabled: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    form = {
        "slug": slug,
        "name": name,
        "description": description,
        "content": content,
        "enabled": enabled is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_skill_form(
            request, mode="create", form=form,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = SkillCreate(
            slug=slug,
            name=name,
            description=description,
            content=content,
            enabled=enabled is not None,
        )
    except ValidationError as exc:
        return await _render_skill_form(
            request, mode="create", form=form,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await skill_service.create_skill(session, payload)
    except AppException as exc:
        return await _render_skill_form(
            request, mode="create", form=form,
            errors=[exc.message], status_code=exc.status_code,
        )

    reset_graph()
    return _redirect("/admin/skills", msg=f"已创建技能「{name}」")


# —————————从项目 skills/ 目录批量导入————————
@router.post("/admin/skills/import")
async def import_skills(
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/skills", err="页面已过期，请刷新后重试")

    try:
        result = await skill_service.import_skills_from_directory(
            session, BASE_DIR / "skills"
        )
    except AppException as exc:
        return _redirect("/admin/skills", err=exc.message)

    reset_graph()
    msg = (
        f"已导入 {result['created']} 个，更新 {result['updated']} 个"
    )
    if result["skipped"]:
        msg += f"，跳过 {len(result['skipped'])} 个"
    return _redirect("/admin/skills", msg=msg)


# —————————编辑技能表单————————
@router.get("/admin/skills/{skill_id}/edit", response_class=HTMLResponse)
async def edit_skill_page(
    skill_id: str,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        skill = await skill_service.get_skill(session, skill_id)
    except AppException as exc:
        return _redirect("/admin/skills", err=exc.message)

    form = {
        "slug": skill.slug,
        "name": skill.name,
        "description": skill.description or "",
        "content": skill.content,
        "enabled": skill.enabled,
    }
    return await _render_skill_form(
        request, mode="edit", form=form, errors=[], skill_id=skill.id
    )


# —————————更新技能————————
@router.post("/admin/skills/{skill_id}/edit")
async def update_skill(
    skill_id: str,
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    description: str = Form(""),
    content: str = Form(""),
    enabled: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    form = {
        "slug": slug,
        "name": name,
        "description": description,
        "content": content,
        "enabled": enabled is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_skill_form(
            request, mode="edit", form=form, skill_id=skill_id,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = SkillUpdate(
            slug=slug,
            name=name,
            description=description,
            content=content,
            enabled=enabled is not None,
        )
    except ValidationError as exc:
        return await _render_skill_form(
            request, mode="edit", form=form, skill_id=skill_id,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await skill_service.update_skill(session, skill_id, payload)
    except AppException as exc:
        return await _render_skill_form(
            request, mode="edit", form=form, skill_id=skill_id,
            errors=[exc.message], status_code=exc.status_code,
        )

    reset_graph()
    return _redirect("/admin/skills", msg=f"已保存技能「{name}」")


# —————————删除技能：挂载关系一起清理————————
@router.post("/admin/skills/{skill_id}/delete")
async def delete_skill(
    skill_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/skills", err="页面已过期，请刷新后重试")

    try:
        await skill_service.delete_skill(session, skill_id)
    except AppException as exc:
        return _redirect("/admin/skills", err=exc.message)

    reset_graph()
    return _redirect("/admin/skills", msg="技能已删除")


# ————————————————————————————————————————————————
#  厂商管理 → app/services/provider_service.py
# ————————————————————————————————————————————————


# —————————厂商表单的初始值————————
def _empty_provider_form() -> dict:
    return {
        "slug": "",
        "name": "",
        "base_url": "",
        "default_model": "",
        "temperature": 0.7,
        "max_tokens": 4096,
        "max_retries": 3,
        "request_timeout": 60,
        "enabled": True,
        "is_default": False,
    }


# —————————渲染厂商表单（新建/编辑共用）————————
async def _render_provider_form(
    request: Request,
    *,
    mode: str,
    form: dict,
    errors: list[str],
    provider_id: str | None = None,
    has_api_key: bool = False,
    status_code: int = 200,
):
    return templates.TemplateResponse(
        request,
        "admin/provider_form.html",
        _base_context(
            request,
            mode=mode,
            provider_id=provider_id,
            form=form,
            errors=errors,
            has_api_key=has_api_key,
        ),
        status_code=status_code,
    )


# —————————厂商列表：默认厂商置顶，密钥只显示是否配置————————
@router.get("/admin/providers", response_class=HTMLResponse)
async def providers_page(
    request: Request,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    providers = (
        await session.execute(
            select(Providers).order_by(
                Providers.is_default.desc(), Providers.name.asc()
            )
        )
    ).scalars().all()

    return templates.TemplateResponse(
        request,
        "admin/providers.html",
        _base_context(
            request,
            providers=providers,
            msg=msg,
            err=err,
        ),
    )


# —————————新建厂商表单————————
@router.get("/admin/providers/new", response_class=HTMLResponse)
async def new_provider_page(
    request: Request,
    _: dict = Depends(require_admin),
):
    return await _render_provider_form(
        request, mode="create", form=_empty_provider_form(), errors=[]
    )


# —————————创建厂商：校验 CSRF → ProviderCreate → provider_service.create_provider————————
@router.post("/admin/providers")
async def create_provider(
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    base_url: str = Form(""),
    api_key: str = Form(""),
    default_model: str = Form(""),
    temperature: str = Form("0.7"),
    max_tokens: str = Form("4096"),
    max_retries: str = Form("3"),
    request_timeout: str = Form("60"),
    enabled: str | None = Form(None),
    is_default: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    form = {
        "slug": slug,
        "name": name,
        "base_url": base_url,
        "default_model": default_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_retries": max_retries,
        "request_timeout": request_timeout,
        "enabled": enabled is not None,
        "is_default": is_default is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_provider_form(
            request, mode="create", form=form,
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    try:
        payload = ProviderCreate(
            slug=slug,
            name=name,
            base_url=base_url,
            api_key=api_key.strip() or None,
            default_model=default_model.strip() or None,
            temperature=temperature,  # type: ignore[arg-type]
            max_tokens=max_tokens,  # type: ignore[arg-type]
            max_retries=max_retries,  # type: ignore[arg-type]
            request_timeout=request_timeout,  # type: ignore[arg-type]
            enabled=enabled is not None,
            is_default=is_default is not None,
        )
    except ValidationError as exc:
        return await _render_provider_form(
            request, mode="create", form=form,
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await provider_service.create_provider(session, payload)
    except AppException as exc:
        return await _render_provider_form(
            request, mode="create", form=form,
            errors=[exc.message], status_code=exc.status_code,
        )

    # 厂商变更：模型参数可能不同，丢弃已编译的图
    reset_graph()
    return _redirect("/admin/providers", msg=f"已创建厂商「{name}」")


# —————————编辑厂商表单：读取 provider_service.get_provider————————
@router.get("/admin/providers/{provider_id}/edit", response_class=HTMLResponse)
async def edit_provider_page(
    provider_id: str,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        provider = await provider_service.get_provider(session, provider_id)
    except AppException as exc:
        return _redirect("/admin/providers", err=exc.message)

    form = {
        "slug": provider.slug,
        "name": provider.name,
        "base_url": provider.base_url,
        "default_model": provider.default_model or "",
        "temperature": provider.temperature,
        "max_tokens": provider.max_tokens,
        "max_retries": provider.max_retries,
        "request_timeout": provider.request_timeout,
        "enabled": provider.enabled,
        "is_default": provider.is_default,
    }
    return await _render_provider_form(
        request, mode="edit", form=form, errors=[],
        provider_id=provider.id, has_api_key=bool(provider.api_key),
    )


# —————————更新厂商：密钥留空表示保持原值————————
@router.post("/admin/providers/{provider_id}/edit")
async def update_provider(
    provider_id: str,
    request: Request,
    slug: str = Form(""),
    name: str = Form(""),
    base_url: str = Form(""),
    api_key: str = Form(""),
    default_model: str = Form(""),
    temperature: str = Form("0.7"),
    max_tokens: str = Form("4096"),
    max_retries: str = Form("3"),
    request_timeout: str = Form("60"),
    enabled: str | None = Form(None),
    is_default: str | None = Form(None),
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        provider = await provider_service.get_provider(session, provider_id)
    except AppException as exc:
        return _redirect("/admin/providers", err=exc.message)

    form = {
        "slug": slug,
        "name": name,
        "base_url": base_url,
        "default_model": default_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_retries": max_retries,
        "request_timeout": request_timeout,
        "enabled": enabled is not None,
        "is_default": is_default is not None,
    }

    if not _csrf_ok(request, csrf):
        return await _render_provider_form(
            request, mode="edit", form=form, provider_id=provider_id,
            has_api_key=bool(provider.api_key),
            errors=["页面已过期，请刷新后重试"], status_code=400,
        )

    changes: dict = {
        "slug": slug,
        "name": name,
        "base_url": base_url,
        "default_model": default_model.strip() or None,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_retries": max_retries,
        "request_timeout": request_timeout,
        "enabled": enabled is not None,
        "is_default": is_default is not None,
    }
    # 密钥留空表示保持原值
    if api_key.strip():
        changes["api_key"] = api_key.strip()

    try:
        payload = ProviderUpdate(**changes)  # type: ignore[arg-type]
    except ValidationError as exc:
        return await _render_provider_form(
            request, mode="edit", form=form, provider_id=provider_id,
            has_api_key=bool(provider.api_key),
            errors=_validation_errors(exc), status_code=400,
        )

    try:
        await provider_service.update_provider(session, provider_id, payload)
    except AppException as exc:
        return await _render_provider_form(
            request, mode="edit", form=form, provider_id=provider_id,
            has_api_key=bool(provider.api_key),
            errors=[exc.message], status_code=exc.status_code,
        )

    # 厂商变更：模型参数可能不同，丢弃已编译的图
    reset_graph()
    return _redirect("/admin/providers", msg=f"已保存厂商「{name}」")


# —————————删除厂商：绑定它的角色会被解绑————————
@router.post("/admin/providers/{provider_id}/delete")
async def delete_provider(
    provider_id: str,
    request: Request,
    csrf: str = Form(""),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect("/admin/providers", err="页面已过期，请刷新后重试")

    try:
        await provider_service.delete_provider(session, provider_id)
    except AppException as exc:
        return _redirect("/admin/providers", err=exc.message)

    # 厂商变更：默认厂商可能改变，丢弃已编译的图
    reset_graph()
    return _redirect("/admin/providers", msg="厂商已删除")


# ————————————————————————————————————————————————
#  会话管理 → app/services/session_service.py
# ————————————————————————————————————————————————

SESSIONS_PAGE_SIZE = 20


# —————————会话列表：搜索 + 分页 + 勾选批量删除————————
@router.get("/admin/sessions", response_class=HTMLResponse)
async def sessions_page(
    request: Request,
    q: str = "",
    page: int = 1,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    keyword = " ".join((q or "").split())[:100]
    total = await session_service.count_sessions(session, q=keyword or None)
    pages = max((total + SESSIONS_PAGE_SIZE - 1) // SESSIONS_PAGE_SIZE, 1)
    current = min(max(page, 1), pages)

    sessions = await session_service.list_sessions(
        session,
        q=keyword or None,
        limit=SESSIONS_PAGE_SIZE,
        offset=(current - 1) * SESSIONS_PAGE_SIZE,
    )
    total_messages = await message_service.count_messages(session)

    return templates.TemplateResponse(
        request,
        "admin/sessions.html",
        _base_context(
            request,
            sessions=sessions,
            total=total,
            total_messages=total_messages,
            page=current,
            pages=pages,
            page_size=SESSIONS_PAGE_SIZE,
            q=keyword,
            msg=msg,
            err=err,
        ),
    )


# —————————会话详情：回放已保存的对话消息————————
@router.get("/admin/sessions/{session_id}", response_class=HTMLResponse)
async def session_detail_page(
    session_id: str,
    request: Request,
    msg: str | None = None,
    err: str | None = None,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    try:
        item = await session_service.get_session(session, session_id)
    except AppException as exc:
        return _redirect("/admin/sessions", err=exc.message)

    messages = await message_service.list_messages(
        session, session_id, limit=1000
    )
    return templates.TemplateResponse(
        request,
        "admin/session_detail.html",
        _base_context(
            request,
            item=item,
            messages=messages,
            chars=sum(len(m.content or "") for m in messages),
            msg=msg,
            err=err,
        ),
    )


# —————————删除单个会话：连同已保存的消息一起清理————————
@router.post("/admin/sessions/{session_id}/delete")
async def delete_session_admin(
    session_id: str,
    request: Request,
    csrf: str = Form(""),
    next_q: str = Form(""),
    next_page: int = Form(1),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect(
            _sessions_path(next_q, next_page), err="页面已过期，请刷新后重试"
        )

    try:
        await session_service.delete_session(session, session_id)
    except AppException as exc:
        return _redirect(_sessions_path(next_q, next_page), err=exc.message)

    return _redirect(_sessions_path(next_q, next_page), msg="会话已删除")


# —————————批量删除：只删勾选的会话，不存在的直接忽略————————
@router.post("/admin/sessions/delete")
async def bulk_delete_sessions(
    request: Request,
    csrf: str = Form(""),
    session_ids: list[str] = Form(default=[]),
    next_q: str = Form(""),
    next_page: int = Form(1),
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, csrf):
        return _redirect(
            _sessions_path(next_q, next_page), err="页面已过期，请刷新后重试"
        )
    if not session_ids:
        return _redirect(
            _sessions_path(next_q, next_page), err="请先勾选要删除的会话"
        )

    count = await session_service.delete_sessions(session, session_ids)
    return _redirect(
        _sessions_path(next_q, next_page), msg=f"已删除 {count} 个会话"
    )


# ————————————————————————————————————————————————
#  测试页面（管理员） → app/services/chat_service.py
# ————————————————————————————————————————————————


# —————————测试页面：输入一句话，查看节点流转与流式输出————————
@router.get("/admin/playground", response_class=HTMLResponse)
async def playground_page(
    request: Request,
    _: dict = Depends(require_admin),
):
    return templates.TemplateResponse(
        request,
        "admin/playground.html",
        _base_context(request),
    )


# —————————流式测试接口：管理员 Cookie 鉴权 + CSRF 头校验————————
@router.post("/admin/playground/stream")
async def playground_stream(
    payload: ChatRequest,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, request.headers.get("x-csrf-token", "")):
        return JSONResponse(
            {"message": "CSRF 校验失败，请刷新页面后重试"},
            status_code=403,
        )

    try:
        graph = await get_graph()
    except RuntimeError as exc:
        # 没有默认厂商 / 没有唯一调度员
        return JSONResponse({"message": str(exc)}, status_code=503)

    workdir = await chat_service.resolve_workdir(
        session, payload.session_id, payload.workdir
    )
    skill = await chat_service.resolve_skill(session, payload.skill_slug)

    return StreamingResponse(
        chat_service.event_stream(
            request,
            graph,
            chat_service.to_messages(payload),
            payload.session_id,
            thread_id=uuid4().hex,
            workdir=workdir,
            skill=skill,
            user_id=payload.user_id,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# —————————人工审批：管理员在测试页批准 / 拒绝后继续运行————————
@router.post("/admin/playground/approve")
async def playground_approve(
    payload: ChatApprovalRequest,
    request: Request,
    _: dict = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    if not _csrf_ok(request, request.headers.get("x-csrf-token", "")):
        return JSONResponse(
            {"message": "CSRF 校验失败，请刷新页面后重试"},
            status_code=403,
        )

    try:
        graph = await get_graph()
    except RuntimeError as exc:
        return JSONResponse({"message": str(exc)}, status_code=503)

    if not await chat_service.has_pending_approval(graph, payload.run_id):
        return JSONResponse(
            {"message": "没有待审批的操作，可能已经处理或已过期"},
            status_code=409,
        )

    workdir = await chat_service.resolve_workdir(
        session, payload.session_id, payload.workdir
    )
    skill = await chat_service.resolve_skill(session, payload.skill_slug)

    return StreamingResponse(
        chat_service.event_stream(
            request,
            graph,
            session_id=payload.session_id,
            thread_id=payload.run_id,
            resume=payload.resume_payload,
            workdir=workdir,
            skill=skill,
            user_id=payload.user_id,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
