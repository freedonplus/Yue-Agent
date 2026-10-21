from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.model.agent_roles import AgentRoles


"""
    ═══════════════════════════════════════════════════
                        tools表
    ═══════════════════════════════════════════════════

    config 存一段 mcpServers JSON（Claude Desktop 格式），
    工具通过 agent_role_tools 多对多挂载给员工。
"""

def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# 员工 ↔ 工具：删除任意一侧时级联清理挂载关系
class AgentRoleTools(Base):
    __tablename__ = "agent_role_tools"

    agent_role_id: Mapped[str] = mapped_column(
        ForeignKey("agent_roles.id", ondelete="CASCADE"), primary_key=True
    )
    tool_id: Mapped[str] = mapped_column(
        ForeignKey("tools.id", ondelete="CASCADE"), primary_key=True
    )

    # 这个员工选中了该配置下的哪些工具（JSON 数组）；
    # 空 / NULL 表示该配置下的工具全部挂载
    tool_names: Mapped[str | None] = mapped_column(Text, nullable=True)


class Tools(Base):
    __tablename__ = "tools"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")

    # 规范化后的 {"mcpServers": {...}} JSON 文本
    config: Mapped[str] = mapped_column(Text)

    # 拉取到的工具清单（JSON 数组），元素为 {"name", "description"}
    available_tools: Mapped[str] = mapped_column(Text, default="[]")
    # 最近一次成功拉取工具的时间
    tools_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    agent_roles: Mapped[list["AgentRoles"]] = relationship(
        secondary="agent_role_tools",
        back_populates="tools",
    )
