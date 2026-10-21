from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

"""
    ═══════════════════════════════════════════════════
                        memories表
    ═══════════════════════════════════════════════════

    跨会话长期记忆：一条记录 = 一条能独立理解的事实。

    与 chat_messages 的区别：
    - chat_messages 保存某个会话里的原始对话，只在该会话回放时使用；
    - memories 保存值得长期记住的信息，跨会话检索并注入运行时提示词。
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    # 记忆归属；没有账号体系时前端可以传稳定标识，默认 default
    user_id: Mapped[str] = mapped_column(
        String(100), index=True, default="default", server_default="default"
    )

    # profile / preference / decision / fact
    kind: Mapped[str] = mapped_column(
        String(20), default="fact", server_default="fact"
    )

    content: Mapped[str] = mapped_column(Text)

    # 逗号分隔的标签，便于检索和展示
    tags: Mapped[str] = mapped_column(
        String(300), default="", server_default=""
    )

    # 这条记忆是在哪个会话里产生的
    source_session_id: Mapped[str] = mapped_column(
        String(100), default="", server_default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
