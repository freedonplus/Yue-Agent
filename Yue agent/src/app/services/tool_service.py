import asyncio
import json

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.tools import (
    ToolConfigError,
    ToolNotFoundError,
    ToolSlugExistsError,
)
from app.model.tools import AgentRoleTools, Tools, utcnow
from app.schemas.tools import ToolCreate, ToolUpdate, parse_tool_names
from Yue.mcp import probe_mcp_tools

"""
    ═══════════════════════════════════════════════════
                       MCP 工具业务逻辑
    ═══════════════════════════════════════════════════
"""


# —————————工具列表：后台展示全部（含停用）————————
async def list_tools(session: AsyncSession) -> list[Tools]:
    stmt = (
        select(Tools)
        .options(selectinload(Tools.agent_roles))
        .order_by(Tools.name.asc(), Tools.created_at.asc())
    )
    items = (await session.execute(stmt)).scalars().all()
    return list(items)


# —————————获取单个工具：不存在抛 ToolNotFoundError————————
async def get_tool(session: AsyncSession, tool_id: str) -> Tools:
    tool = await session.get(Tools, tool_id)
    if tool is None:
        raise ToolNotFoundError()
    return tool


# —————————校验 slug 未被占用（更新时排除自己）————————
async def _ensure_slug_available(
    session: AsyncSession, slug: str, *, exclude_id: str | None = None
) -> None:
    stmt = select(Tools.id).where(Tools.slug == slug)
    if exclude_id:
        stmt = stmt.where(Tools.id != exclude_id)
    if await session.scalar(stmt):
        raise ToolSlugExistsError()


# —————————创建工具————————
async def create_tool(session: AsyncSession, data: ToolCreate) -> Tools:
    await _ensure_slug_available(session, data.slug)

    tool = Tools(**data.model_dump())
    session.add(tool)
    await session.commit()
    await session.refresh(tool)
    return tool


# —————————更新工具：只改传入字段————————
async def update_tool(
    session: AsyncSession, tool_id: str, data: ToolUpdate
) -> Tools:
    tool = await get_tool(session, tool_id)
    changes = data.model_dump(exclude_unset=True)

    if "slug" in changes and changes["slug"] != tool.slug:
        await _ensure_slug_available(
            session, changes["slug"], exclude_id=tool.id
        )

    # 配置变了，旧清单作废，需要重新拉取
    if "config" in changes and changes["config"] != tool.config:
        tool.available_tools = "[]"
        tool.tools_checked_at = None

    for field, value in changes.items():
        setattr(tool, field, value)

    await session.commit()
    await session.refresh(tool)
    return tool


# —————————启用 / 停用工具：公开接口使用————————
async def set_tool_enabled(
    session: AsyncSession, tool_id: str, enabled: bool
) -> Tools:
    tool = await get_tool(session, tool_id)
    tool.enabled = enabled
    await session.commit()
    await session.refresh(tool)
    return tool


# —————————删除工具：挂载关系由外键级联清理————————
async def delete_tool(session: AsyncSession, tool_id: str) -> None:
    tool = await get_tool(session, tool_id)
    await session.delete(tool)
    await session.commit()


# —————————连接 MCP 服务，拉取工具清单并落库————————
async def refresh_tool_tools(
    session: AsyncSession, tool_id: str
) -> Tools:
    tool = await get_tool(session, tool_id)

    try:
        found = await probe_mcp_tools(tool.config)
    except asyncio.TimeoutError:
        raise ToolConfigError("MCP 服务响应超时，请检查启动命令或网络") from None
    except Exception as exc:
        raise ToolConfigError(f"工具拉取失败：{exc}") from None

    tool.available_tools = json.dumps(found, ensure_ascii=False)
    tool.tools_checked_at = utcnow()
    await session.commit()
    await session.refresh(tool)
    return tool


# —————————读取某个员工已挂载的工具 id————————
async def get_agent_tool_ids(
    session: AsyncSession, agent_id: str
) -> list[str]:
    stmt = select(AgentRoleTools.tool_id).where(
        AgentRoleTools.agent_role_id == agent_id
    )
    return list((await session.execute(stmt)).scalars())


# —————————读取某个员工的挂载明细（含工具配置信息）————————
async def list_agent_mounts(
    session: AsyncSession, agent_id: str
) -> list[tuple[Tools, list[str] | None]]:
    stmt = (
        select(AgentRoleTools, Tools)
        .join(Tools, Tools.id == AgentRoleTools.tool_id)
        .where(AgentRoleTools.agent_role_id == agent_id)
        .order_by(Tools.name.asc())
    )
    rows = (await session.execute(stmt)).all()
    return [
        (
            tool,
            parse_tool_names(link.tool_names)
            if link.tool_names is not None
            else None,
        )
        for link, tool in rows
    ]


# —————————读取某个员工每个配置下选中的工具名————————
async def get_agent_tool_selection(
    session: AsyncSession, agent_id: str
) -> dict[str, list[str]]:
    stmt = select(AgentRoleTools).where(
        AgentRoleTools.agent_role_id == agent_id
    )
    links = (await session.execute(stmt)).scalars().all()
    return {
        link.tool_id: (
            parse_tool_names(link.tool_names)
            if link.tool_names is not None
            else None
        )
        for link in links
    }


# —————————覆盖式设置某个员工挂载的工具————————
async def set_agent_tools(
    session: AsyncSession,
    agent_id: str,
    tool_ids: list[str],
    selection: dict[str, list[str]] | None = None,
) -> None:
    """selection: {tool_id: [选中的工具名]}；为空表示该配置全量挂载。"""
    selection = selection or {}
    unique_ids = list(dict.fromkeys(t for t in tool_ids if t))

    if unique_ids:
        found = set(
            (
                await session.execute(
                    select(Tools.id).where(Tools.id.in_(unique_ids))
                )
            ).scalars()
        )
        missing = [t for t in unique_ids if t not in found]
        if missing:
            raise ToolNotFoundError()

    await session.execute(
        delete(AgentRoleTools).where(
            AgentRoleTools.agent_role_id == agent_id
        )
    )
    for tool_id in unique_ids:
        # key 不存在 = 未拉取清单，全都挂；key 存在 = 按选中的名字挂（可为空）
        if tool_id in selection:
            names = [
                str(n)
                for n in (selection.get(tool_id) or [])
                if isinstance(n, str) and n
            ]
            tool_names = json.dumps(names, ensure_ascii=False)
        else:
            tool_names = None

        session.add(
            AgentRoleTools(
                agent_role_id=agent_id,
                tool_id=tool_id,
                tool_names=tool_names,
            )
        )
    await session.commit()
