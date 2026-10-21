from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

"""
    ═══════════════════════════════════════════════════
                        skills表
    ═══════════════════════════════════════════════════

    技能 = 一段可复用的工作说明（SKILL.md 正文）。
    技能是全局的：所有启用的技能都会出现在前端选择列表里，
    由用户在当前会话中指定使用哪一个，不需要挂载给具体员工。
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")

    # SKILL.md 正文（frontmatter 之后的内容）
    content: Mapped[str] = mapped_column(Text)

    # 从 skills/ 目录导入时记录相对路径，便于知道来源
    source_path: Mapped[str] = mapped_column(
        String(300), default="", server_default=""
    )

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
