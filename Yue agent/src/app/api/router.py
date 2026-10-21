from fastapi import APIRouter

from app.api.endpoints import (
    Yue_agent_roles,
    Yue_chat,
    Yue_memories,
    Yue_providers,
    Yue_sessions,
    Yue_skills,
    Yue_tools,
    Yue_workspaces,
)

"""
    ═══════════════════════════════════════════════════
                          路由整合
    ═══════════════════════════════════════════════════
"""

api_router = APIRouter()

api_router.include_router(Yue_providers.router, prefix="/providers", tags=["厂商"])
api_router.include_router(Yue_tools.router, prefix="/tools", tags=["工具"])
api_router.include_router(Yue_skills.router, prefix="/skills", tags=["技能"])
api_router.include_router(Yue_memories.router, prefix="/memories", tags=["跨会话记忆"])
api_router.include_router(Yue_agent_roles.router, prefix="/agent_roles", tags=["员工/调度员"])
api_router.include_router(Yue_chat.router, prefix="/chat", tags=["对话"])
api_router.include_router(Yue_sessions.router, prefix="/sessions", tags=["会话"])
api_router.include_router(Yue_workspaces.router, prefix="/workspaces", tags=["工作区"])

