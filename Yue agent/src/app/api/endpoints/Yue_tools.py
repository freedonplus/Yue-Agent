from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.common import EnabledUpdate
from app.schemas.tools import (
    ToolCreate,
    ToolPublicOut,
    ToolUpdate,
)
from app.services import tool_service
from Yue.agent.graph import reset_graph

"""
    ═══════════════════════════════════════════════════
                        MCP 工具接口
    ═══════════════════════════════════════════════════

    POST   /api/tools                  新建工具（上传 MCP 配置）
    GET    /api/tools                  工具列表
    GET    /api/tools/{id}             工具详情
    PATCH  /api/tools/{id}             修改工具
    PATCH  /api/tools/{id}/enabled     启用 / 停用
    POST   /api/tools/{id}/refresh     连接 MCP，拉取实际工具清单

    员工挂载见 /api/agent_roles/{id}/tools。
    原始 config 不对外返回，避免泄露密钥与路径；删除仍限管理后台。
"""

router = APIRouter()


# —————————新建工具：配置会被规范化，工具清单需再调 refresh————————
@router.post("", response_model=ToolPublicOut, status_code=201)
async def create_tool(
    payload: ToolCreate,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_service.create_tool(session, payload)
    reset_graph()
    return ToolPublicOut.from_model(tool)


# —————————工具列表————————
@router.get("", response_model=list[ToolPublicOut])
async def list_tools(session: AsyncSession = Depends(get_session)):
    tools = await tool_service.list_tools(session)
    return [ToolPublicOut.from_model(tool) for tool in tools]


# —————————工具详情————————
@router.get("/{tool_id}", response_model=ToolPublicOut)
async def get_tool(
    tool_id: str,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_service.get_tool(session, tool_id)
    return ToolPublicOut.from_model(tool)


# —————————修改工具：配置变化会清空旧工具清单————————
@router.patch("/{tool_id}", response_model=ToolPublicOut)
async def update_tool(
    tool_id: str,
    payload: ToolUpdate,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_service.update_tool(session, tool_id, payload)
    reset_graph()
    return ToolPublicOut.from_model(tool)


# —————————启用 / 停用工具————————
@router.patch("/{tool_id}/enabled", response_model=ToolPublicOut)
async def set_tool_enabled(
    tool_id: str,
    payload: EnabledUpdate,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_service.set_tool_enabled(
        session, tool_id, payload.enabled
    )
    reset_graph()
    return ToolPublicOut.from_model(tool)


# —————————拉取工具：连接 MCP 服务并保存实际工具清单————————
@router.post("/{tool_id}/refresh", response_model=ToolPublicOut)
async def refresh_tool(
    tool_id: str,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_service.refresh_tool_tools(session, tool_id)
    return ToolPublicOut.from_model(tool)
