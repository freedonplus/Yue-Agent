from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

"""
    ═══════════════════════════════════════════════════
                    chat_messages表
    ═══════════════════════════════════════════════════

    按会话保存用户与最终答复，供前端重新打开会话时回放。
    只存对话级消息，不保存员工子图内部的工具调用与中间消息。
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ChatMessages(Base):
    __tablename__ = "chat_messages"

    # 自增主键同时用作分页游标
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    session_id: Mapped[str] = mapped_column(String(100), nullable=False)

    # user / assistant
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 最终答复由哪个员工产出（调度员 / 输出管卡等）
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )

    __table_args__ = (
        Index("ix_chat_messages_session_id_id", "session_id", "id"),
    )
