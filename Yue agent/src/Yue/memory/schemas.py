from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    ═══════════════════════════════════════════════════
                    记忆 Schema
    ═══════════════════════════════════════════════════
"""

MemoryKind = Literal["profile", "preference", "decision", "fact"]


class MemoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    user_id: str = Field(default="default", max_length=100)
    content: str = Field(min_length=1, max_length=2000)
    tags: str = Field(default="", max_length=300)
    kind: MemoryKind = "fact"
    source_session_id: str = Field(default="", max_length=100)

    @field_validator("user_id", mode="before")
    @classmethod
    def _default_user(cls, v):
        return v or "default"


class MemoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    kind: str
    content: str
    tags: str
    source_session_id: str
    created_at: datetime
    updated_at: datetime
