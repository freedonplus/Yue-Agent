from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    ═══════════════════════════════════════════════════
                    会话 Schema
    ═══════════════════════════════════════════════════
"""


class SessionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # 不传则由服务端生成一个 uuid
    session_id: str | None = Field(default=None, min_length=1, max_length=100)
    title: str = Field(default="", max_length=200)
    last_message: str = Field(default="", max_length=20000)
    message_count: int = Field(default=0, ge=0)
    # 会话工作目录；空字符串 = 沿用员工提示词里的默认目录
    workdir: str = Field(default="", max_length=1000)

    @field_validator("session_id", mode="before")
    @classmethod
    def _blank_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v


class SessionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, max_length=200)
    last_message: str | None = Field(default=None, max_length=20000)
    message_count: int | None = Field(default=None, ge=0)
    workdir: str | None = Field(default=None, max_length=1000)


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    title: str
    last_message: str
    message_count: int
    workdir: str
    created_at: datetime
    updated_at: datetime


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    role: str
    content: str
    name: str | None
    created_at: datetime
