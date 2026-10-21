from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.chat_messages import ChatMessages

"""
    ═══════════════════════════════════════════════════
                    会话消息业务逻辑
    ═══════════════════════════════════════════════════
"""


# —————————追加一条会话消息————————
async def add_message(
    session: AsyncSession,
    session_id: str,
    role: str,
    content: str,
    name: str | None = None,
) -> ChatMessages:
    item = ChatMessages(
        session_id=session_id,
        role=role,
        content=content,
        name=name,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


# —————————读取会话消息：默认返回最近 N 条，按时间正序————————
async def list_messages(
    session: AsyncSession,
    session_id: str,
    *,
    limit: int = 200,
    before_id: int | None = None,
) -> list[ChatMessages]:
    stmt = select(ChatMessages).where(ChatMessages.session_id == session_id)

    if before_id is not None:
        stmt = stmt.where(ChatMessages.id < before_id)

    stmt = stmt.order_by(ChatMessages.id.desc()).limit(max(1, min(limit, 1000)))
    items = list((await session.execute(stmt)).scalars().all())
    items.reverse()
    return items


# —————————消息总数：传 session_id 时只统计该会话————————
async def count_messages(
    session: AsyncSession, session_id: str | None = None
) -> int:
    stmt = select(func.count()).select_from(ChatMessages)
    if session_id:
        stmt = stmt.where(ChatMessages.session_id == session_id)
    return int(await session.scalar(stmt) or 0)


# —————————删除会话时同步清理消息————————
async def delete_messages_for_session(
    session: AsyncSession, session_id: str
) -> None:
    await session.execute(
        delete(ChatMessages).where(ChatMessages.session_id == session_id)
    )


# —————————批量删除会话时同步清理消息————————
async def delete_messages_for_sessions(
    session: AsyncSession, session_ids: list[str]
) -> None:
    if not session_ids:
        return
    await session.execute(
        delete(ChatMessages).where(ChatMessages.session_id.in_(session_ids))
    )
