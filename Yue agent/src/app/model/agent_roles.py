from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.model.providers import Providers
    from app.model.tools import Tools


"""
    ═══════════════════════════════════════════════════
                        agent_roles表
    ═══════════════════════════════════════════════════
"""

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class AgentRoles(Base):
    __tablename__ = "agent_roles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    # 身份
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), index=True)   # supervisor / worker

    # 内容
    description: Mapped[str] = mapped_column(Text, default="")
    system_prompt: Mapped[str] = mapped_column(Text)

    # 需要人工审批的工具名（JSON 数组）；空数组表示直接执行
    approval_tools: Mapped[str] = mapped_column(
        Text, default="[]", server_default="[]"
    )

    # 管理
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    # 最终输出管卡：其他员工完成后，由这个员工整理成最终答复
    is_output_gate: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="0"
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    provider_id: Mapped[str | None] = mapped_column(
        ForeignKey("providers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    provider: Mapped[Providers | None] = relationship(back_populates="agent_roles")

    # 挂载到这个员工的 MCP 工具
    tools: Mapped[list["Tools"]] = relationship(
        secondary="agent_role_tools",
        back_populates="agent_roles",
    )

    # 数据库层兜底：role='supervisor' 至多一行（SQLite 部分唯一索引）
    __table_args__ = (
        Index(
            "uq_agent_roles_single_supervisor",
            "role",
            unique=True,
            sqlite_where=text("role = 'supervisor'"),
        ),
    )

