from typing import Literal

from langchain_core.runnables import ensure_config
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from Yue.memory.store import normalize_user_id, save_memory, search_memory_text

"""
    ═══════════════════════════════════════════════════
                    跨会话记忆工具
    ═══════════════════════════════════════════════════

    工具本身是全局的，user_id / session_id 从运行时 configurable
    读取，所以同一个图可以服务不同的用户。
"""


class SaveMemoryArgs(BaseModel):
    content: str = Field(
        max_length=2000,
        description="一条能独立理解的长期事实，例如「用户习惯称呼为阿岳」",
    )
    tags: str = Field(
        default="",
        max_length=300,
        description="可选标签，用逗号分隔，例如「偏好,写作」",
    )
    kind: Literal["profile", "preference", "decision", "fact"] = Field(
        default="fact",
        description="profile=用户档案，preference=偏好，decision=长期决定，fact=其他事实",
    )


class SearchMemoryArgs(BaseModel):
    query: str = Field(
        default="",
        max_length=200,
        description="检索关键词；留空则返回最近的记忆",
    )


def make_memory_tools() -> list:
    """为员工生成跨会话记忆的读写工具。"""

    async def save_memory_tool(
        content: str,
        tags: str = "",
        kind: str = "fact",
    ) -> str:
        config = ensure_config()
        configurable = config.get("configurable") or {}
        user_id = normalize_user_id(configurable.get("user_id"))
        session_id = str(configurable.get("session_id") or "")

        try:
            item, created = await save_memory(
                user_id,
                content,
                tags=tags,
                kind=kind,
                source_session_id=session_id,
            )
        except ValueError as exc:
            return f"没有保存：{exc}"

        action = "已记住" if created else "已更新这条记忆"
        return f"{action}：{item.content}"

    async def search_memory_tool(query: str = "") -> str:
        config = ensure_config()
        configurable = config.get("configurable") or {}
        user_id = normalize_user_id(configurable.get("user_id"))
        return await search_memory_text(user_id, query)

    return [
        StructuredTool.from_function(
            coroutine=save_memory_tool,
            name="save_memory",
            description=(
                "把值得跨会话长期记住的信息保存到记忆库。\n"
                "当用户明确告诉你称呼、偏好、长期设定、项目决策或稳定约束时，"
                "应主动保存；以后的新会话也能检索到。\n"
                "不要保存临时对话、密码 / 密钥 / 令牌、他人隐私或未经确认的猜测；"
                "一次只保存一条能独立理解的事实。"
            ),
            args_schema=SaveMemoryArgs,
        ),
        StructuredTool.from_function(
            coroutine=search_memory_tool,
            name="search_memory",
            description=(
                "搜索以前会话保存的跨会话记忆。\n"
                "用户问「你还记得……」「我之前说过……」或任务需要历史偏好时调用；"
                "留空 query 可查看最近的记忆。"
            ),
            args_schema=SearchMemoryArgs,
        ),
    ]
