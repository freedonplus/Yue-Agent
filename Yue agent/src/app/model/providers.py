from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.model.agent_roles import AgentRoles



"""
    ═══════════════════════════════════════════════════
                        providers表
    ═══════════════════════════════════════════════════
"""

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class Providers(Base):
    __tablename__ = "providers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    base_url: Mapped[str] = mapped_column(String(255))
    api_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # 运行参数（OpenAI 兼容协议）
    temperature: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.7, server_default="0.7"
    )
    max_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, default=4096, server_default="4096"
    )
    max_retries: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3, server_default="3"
    )
    request_timeout: Mapped[int] = mapped_column(
        Integer, nullable=False, default=60, server_default="60"
    )

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    __table_args__ = (
        CheckConstraint(
            "temperature >= 0 AND temperature <= 2",
            name="ck_providers_temperature",
        ),
        CheckConstraint("max_tokens > 0", name="ck_providers_max_tokens"),
        CheckConstraint("max_retries >= 0", name="ck_providers_max_retries"),
        CheckConstraint("request_timeout > 0", name="ck_providers_request_timeout"),
    )

    agent_roles: Mapped[list["AgentRoles"]] = relationship(back_populates="provider")