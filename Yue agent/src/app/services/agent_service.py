from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.agent_roles import (
    AgentNotFoundError,
    AgentProviderNotFoundError,
    AgentSlugExistsError,
    AgentSupervisorExistsError,
    AgentSupervisorLockedError,
)
from app.model.agent_roles import AgentRoles
from app.model.providers import Providers
from app.schemas.agent_roles import (
    AgentCreate,
    AgentUpdate,
    dump_approval_tools,
)

"""
    ═══════════════════════════════════════════════════
                员工 / 调度员业务逻辑
    ═══════════════════════════════════════════════════
"""


# —————————获取员工列表：按角色 / 厂商 / 关键字筛选————————
async def list_agents(
    session: AsyncSession,
    *,
    role: str | None = None,
    provider_id: str | None = None,
    q: str | None = None,
    include_disabled: bool = False,
) -> list[AgentRoles]:
    # 默认只对前台暴露启用的员工；管理端可传 include_disabled 查看停用项
    conditions = [] if include_disabled else [AgentRoles.enabled.is_(True)]
    if role is not None:
        conditions.append(AgentRoles.role == role)
    if provider_id is not None:
        conditions.append(AgentRoles.provider_id == provider_id)
    if q:
        like = f"%{q.strip()}%"
        conditions.append(
            or_(AgentRoles.name.ilike(like), AgentRoles.slug.ilike(like))
        )

    stmt = (
        select(AgentRoles)
        .where(*conditions)
        .order_by(AgentRoles.sort_order.asc(), AgentRoles.created_at.asc())
    )
    items = (await session.execute(stmt)).scalars().all()
    return list(items)


# —————————获取单个员工：不存在抛 AgentNotFoundError————————
async def get_agent(session: AsyncSession, agent_id: str) -> AgentRoles:
    agent = await session.get(AgentRoles, agent_id)
    if agent is None:
        raise AgentNotFoundError()
    return agent


# —————————校验 slug 未被占用（更新时排除自己）————————
async def _ensure_slug_available(
    session: AsyncSession, slug: str, *, exclude_id: str | None = None
) -> None:
    stmt = select(AgentRoles.id).where(AgentRoles.slug == slug)
    if exclude_id:
        stmt = stmt.where(AgentRoles.id != exclude_id)
    if await session.scalar(stmt):
        raise AgentSlugExistsError()


# —————————校验绑定的厂商存在————————
async def _ensure_provider_exists(
    session: AsyncSession, provider_id: str | None
) -> None:
    if provider_id is None:
        return
    if await session.get(Providers, provider_id) is None:
        raise AgentProviderNotFoundError()


# —————————最终输出管卡全局唯一：设置新的之前清掉旧的————————
async def _clear_other_output_gates(
    session: AsyncSession, *, exclude_id: str | None = None
) -> None:
    stmt = update(AgentRoles).where(AgentRoles.is_output_gate.is_(True))
    if exclude_id:
        stmt = stmt.where(AgentRoles.id != exclude_id)
    await session.execute(stmt.values(is_output_gate=False))


# —————————查询已存在的调度员 id（更新时排除自己）————————
async def _supervisor_id(
    session: AsyncSession, *, exclude_id: str | None = None
) -> str | None:
    """返回已存在的调度员 id；exclude_id 用于更新时排除自己。"""
    stmt = select(AgentRoles.id).where(AgentRoles.role == "supervisor")
    if exclude_id:
        stmt = stmt.where(AgentRoles.id != exclude_id)
    return await session.scalar(stmt)


# —————————创建员工：调度员只能有一个，唯一索引兜底并发————————
async def create_agent(session: AsyncSession, data: AgentCreate) -> AgentRoles:
    await _ensure_slug_available(session, data.slug)
    await _ensure_provider_exists(session, data.provider_id)

    if data.role == "supervisor" and await _supervisor_id(session):
        raise AgentSupervisorExistsError()

    payload = data.model_dump()
    # 调度员不参与员工执行链，不能当输出管卡
    if payload.get("role") == "supervisor":
        payload["is_output_gate"] = False
    elif payload.get("is_output_gate"):
        await _clear_other_output_gates(session)

    approval_tools = payload.pop("approval_tools", [])
    agent = AgentRoles(
        **payload,
        approval_tools=dump_approval_tools(approval_tools),
    )
    session.add(agent)
    try:
        await session.commit()
    except IntegrityError:
        # 并发下唯一索引兜底
        await session.rollback()
        if data.role == "supervisor":
            raise AgentSupervisorExistsError() from None
        raise
    await session.refresh(agent)
    return agent


# —————————更新员工：调度员不可降级 / 停用，他人不可升级为调度员————————
async def update_agent(
    session: AsyncSession, agent_id: str, data: AgentUpdate
) -> AgentRoles:
    agent = await get_agent(session, agent_id)
    changes = data.model_dump(exclude_unset=True)

    # 审批工具列表落库前转成 JSON；None 表示这次不改
    if "approval_tools" in changes:
        approval_tools = changes.pop("approval_tools")
        if approval_tools is not None:
            changes["approval_tools"] = dump_approval_tools(approval_tools)

    if "slug" in changes and changes["slug"] != agent.slug:
        await _ensure_slug_available(
            session, changes["slug"], exclude_id=agent.id
        )

    if "provider_id" in changes:
        await _ensure_provider_exists(session, changes["provider_id"])

    # 唯一调度员不可降级、不可停用
    if agent.role == "supervisor":
        if changes.get("role", agent.role) != "supervisor":
            raise AgentSupervisorLockedError()
        if changes.get("enabled", agent.enabled) is False:
            raise AgentSupervisorLockedError()
    # 其他员工不可被提升为第二个调度员
    elif changes.get("role") == "supervisor":
        if await _supervisor_id(session, exclude_id=agent.id):
            raise AgentSupervisorExistsError()

    # 输出管卡全局只保留一个；调度员不能担任
    if changes.get("role", agent.role) == "supervisor":
        changes["is_output_gate"] = False
    elif changes.get("is_output_gate") is True:
        await _clear_other_output_gates(session, exclude_id=agent.id)

    for field, value in changes.items():
        setattr(agent, field, value)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise AgentSupervisorExistsError() from None
    await session.refresh(agent)
    return agent


# —————————启用 / 停用员工：公开接口使用，调度员不可停用————————
async def set_agent_enabled(
    session: AsyncSession, agent_id: str, enabled: bool
) -> AgentRoles:
    """公开接口的启用/停用；唯一调度员不可停用。"""
    agent = await get_agent(session, agent_id)

    if agent.role == "supervisor" and not enabled:
        raise AgentSupervisorLockedError()

    agent.enabled = enabled
    await session.commit()
    await session.refresh(agent)
    return agent


# —————————删除员工：调度员是系统单例，禁止删除————————
async def delete_agent(session: AsyncSession, agent_id: str) -> None:
    agent = await get_agent(session, agent_id)

    # 调度员是系统单例，只能编辑，不能删除
    if agent.role == "supervisor":
        raise AgentSupervisorLockedError()

    await session.delete(agent)
    await session.commit()
