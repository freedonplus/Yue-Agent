from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.agent_roles import AgentOut
from app.schemas.common import EnabledUpdate
from app.schemas.tools import AgentToolsUpdate, ToolMountOut
from app.services import agent_service, tool_service
from Yue.agent.graph import reset_graph

"""
    ═══════════════════════════════════════════════════
                员工 / 调度员（公开只读接口）
    ═══════════════════════════════════════════════════

    创建 / 修改 / 删除 仅限管理后台（/admin/roles）。
    这里提供查询、启用状态切换，以及工具的查看 / 挂载。
    调度员不可停用。
"""

router = APIRouter()


# —————————获取员工列表：可按角色 / 厂商 / 关键字过滤，默认只返回启用的————————
@router.get("", response_model=list[AgentOut])
async def list_agents(
    role: str | None = Query(None, pattern="^(supervisor|worker)$"),
    provider_id: str | None = Query(None),
    q: str | None = Query(None, max_length=100),
    include_disabled: bool = Query(
        False, description="true 时连同停用的员工一起返回（供管理端使用）"
    ),
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.list_agents(
        session,
        role=role,
        provider_id=provider_id,
        q=q,
        include_disabled=include_disabled,
    )


# —————————获取单个员工详情：不存在返回 404————————
@router.get("/{agent_id}", response_model=AgentOut)
async def get_agent(
    agent_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.get_agent(session, agent_id)


# —————————启用 / 停用员工：唯一调度员不可停用（409）————————
@router.patch("/{agent_id}/enabled", response_model=AgentOut)
async def set_agent_enabled(
    agent_id: str,
    payload: EnabledUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.set_agent_enabled(
        session, agent_id, payload.enabled
    )


# —————————查看员工挂载的工具：tool_names 为 None 表示全量————————
@router.get("/{agent_id}/tools", response_model=list[ToolMountOut])
async def list_agent_tools(
    agent_id: str,
    session: AsyncSession = Depends(get_session),
):
    await agent_service.get_agent(session, agent_id)
    mounts = await tool_service.list_agent_mounts(session, agent_id)
    return [
        ToolMountOut(
            tool_id=tool.id,
            slug=tool.slug,
            name=tool.name,
            enabled=tool.enabled,
            tool_names=names,
        )
        for tool, names in mounts
    ]


# —————————覆盖式挂载：不传 tool_names = 该配置下全部工具；传 [] = 一个都不给————————
@router.put("/{agent_id}/tools", response_model=list[ToolMountOut])
async def set_agent_tools(
    agent_id: str,
    payload: AgentToolsUpdate,
    session: AsyncSession = Depends(get_session),
):
    await agent_service.get_agent(session, agent_id)

    selection = {
        mount.tool_id: mount.tool_names
        for mount in payload.tools
        if mount.tool_names is not None
    }
    await tool_service.set_agent_tools(
        session,
        agent_id,
        [mount.tool_id for mount in payload.tools],
        selection,
    )
    reset_graph()

    mounts = await tool_service.list_agent_mounts(session, agent_id)
    return [
        ToolMountOut(
            tool_id=tool.id,
            slug=tool.slug,
            name=tool.name,
            enabled=tool.enabled,
            tool_names=names,
        )
        for tool, names in mounts
    ]
