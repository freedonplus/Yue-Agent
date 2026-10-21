import asyncio

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from settings import settings

"""
    ═══════════════════════════════════════════════════
                    图检查点（人工审批依赖）
    ═══════════════════════════════════════════════════

    工具执行前要暂停等人确认，LangGraph 的 interrupt 必须配合
    checkpointer 才能把暂停位置保存下来。这里用一个常驻的
    SQLite 连接，审批完成后再把对应线程删掉。
"""

_saver: AsyncSqliteSaver | None = None
_conn: aiosqlite.Connection | None = None
_lock = asyncio.Lock()


async def get_checkpointer() -> AsyncSqliteSaver:
    global _saver, _conn
    if _saver is not None:
        return _saver

    async with _lock:
        if _saver is None:
            path = settings.DB_PATH.parent / "yue_checkpoints.db"
            _conn = await aiosqlite.connect(str(path))
            saver = AsyncSqliteSaver(_conn)
            await saver.setup()
            _saver = saver

    return _saver


async def close_checkpointer() -> None:
    global _saver, _conn
    if _conn is not None:
        await _conn.close()
    _conn = None
    _saver = None
