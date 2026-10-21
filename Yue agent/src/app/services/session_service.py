from uuid import uuid4

from sqlalchemy import delete, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.chat_sessions import SessionExistsError, SessionNotFoundError
from app.model.chat_sessions import ChatSessions
from app.schemas.chat_sessions import SessionCreate, SessionUpdate
from app.services import message_service

"""
    ═══════════════════════════════════════════════════
                    会话业务逻辑
    ═══════════════════════════════════════════════════
"""


# —————————会话列表：按最近更新排序，可按标题 / session_id 搜索————————
async def list_sessions(
    session: AsyncSession,
    *,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ChatSessions]:
    stmt = select(ChatSessions)

    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(ChatSessions.title.ilike(like), ChatSessions.session_id.ilike(like))
        )

    stmt = (
        stmt.order_by(ChatSessions.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    items = (await session.execute(stmt)).scalars().all()
    return list(items)


# —————————会话总数：管理端分页用，搜索条件与列表保持一致————————
async def count_sessions(session: AsyncSession, *, q: str | None = None) -> int:
    stmt = select(func.count()).select_from(ChatSessions)

    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(ChatSessions.title.ilike(like), ChatSessions.session_id.ilike(like))
        )

    return int(await session.scalar(stmt) or 0)


# —————————按 session_id 获取会话：不存在抛 SessionNotFoundError————————
async def get_session(session: AsyncSession, session_id: str) -> ChatSessions:
    item = await session.scalar(
        select(ChatSessions).where(ChatSessions.session_id == session_id)
    )
    if item is None:
        raise SessionNotFoundError()
    return item


# —————————读取会话工作目录：会话不存在时返回空，不影响对话————————
async def find_workdir(session: AsyncSession, session_id: str | None) -> str:
    if not session_id:
        return ""
    try:
        item = await get_session(session, session_id)
    except SessionNotFoundError:
        return ""
    return (item.workdir or "").strip()


# —————————创建会话：session_id 可由前端传入，也可由服务端生成————————
async def create_session(session: AsyncSession, data: SessionCreate) -> ChatSessions:
    session_id = data.session_id or str(uuid4())

    exists = await session.scalar(
        select(ChatSessions.id).where(ChatSessions.session_id == session_id)
    )
    if exists:
        raise SessionExistsError()

    item = ChatSessions(
        session_id=session_id,
        title=data.title,
        last_message=data.last_message,
        message_count=data.message_count,
        workdir=data.workdir,
    )
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        # 并发下唯一索引兜底
        await session.rollback()
        raise SessionExistsError() from None
    await session.refresh(item)
    return item


# —————————更新会话：标题 / 最后一条消息 / 消息数————————
async def update_session(
    session: AsyncSession,
    session_id: str,
    data: SessionUpdate,
) -> ChatSessions:
    item = await get_session(session, session_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    await session.commit()
    await session.refresh(item)
    return item


# —————————删除会话：连同已保存的对话消息一起清理————————
async def delete_session(session: AsyncSession, session_id: str) -> None:
    item = await get_session(session, session_id)
    await message_service.delete_messages_for_session(session, session_id)
    await session.delete(item)
    await session.commit()


# —————————批量删除：不存在的 session_id 直接忽略，返回实际删除条数————————
async def delete_sessions(
    session: AsyncSession, session_ids: list[str]
) -> int:
    ids = list(dict.fromkeys(
        item.strip() for item in session_ids if isinstance(item, str) and item.strip()
    ))
    if not ids:
        return 0

    await message_service.delete_messages_for_sessions(session, ids)
    result = await session.execute(
        delete(ChatSessions).where(ChatSessions.session_id.in_(ids))
    )
    await session.commit()
    return int(result.rowcount or 0)
