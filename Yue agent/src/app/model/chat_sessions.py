from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

"""
    ═══════════════════════════════════════════════════
                    chat_sessions表
    ═══════════════════════════════════════════════════
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ChatSessions(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    # 前端生成的会话标识；同一个 session_id 只保留一行
    session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    title: Mapped[str] = mapped_column(
        String(200), nullable=False, default="", server_default=""
    )
    last_message: Mapped[str] = mapped_column(
        Text, nullable=False, default="", server_default=""
    )
    message_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    # 本次会话的工作目录；空字符串表示沿用员工提示词里的默认目录
    workdir: Mapped[str] = mapped_column(
        Text, nullable=False, default="", server_default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
