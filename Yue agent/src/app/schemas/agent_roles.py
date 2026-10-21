import json
from datetime import datetime
from typing import Iterable, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    ═══════════════════════════════════════════════════
                    员工 / 调度员 Schema
    ═══════════════════════════════════════════════════
"""

SLUG_PATTERN = r"^[a-z0-9][a-z0-9_-]*$"
AgentRole = Literal["supervisor", "worker"]


def parse_approval_tools(raw: str | None) -> list[str]:
    """把数据库里的 JSON 数组读成工具名列表；坏数据按空处理。"""
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        return []
    if not isinstance(value, list):
        return []
    return [
        name.strip()
        for name in value
        if isinstance(name, str) and name.strip()
    ]


def dump_approval_tools(names: Iterable[str] | None) -> str:
    """去重后写回 JSON 数组。"""
    return json.dumps(
        list(dict.fromkeys(n for n in (names or []) if n)),
        ensure_ascii=False,
    )


ToolNames = list[str]


class AgentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str = Field(min_length=1, max_length=50, pattern=SLUG_PATTERN)
    name: str = Field(min_length=1, max_length=100)
    role: AgentRole
    description: str = ""
    system_prompt: str = Field(min_length=1)
    enabled: bool = True
    # 最终输出管卡：任务完成后由这个员工统一整理最终答复
    is_output_gate: bool = False
    sort_order: int = 0
    provider_id: str | None = None
    # 执行前需要人工确认的工具名
    approval_tools: ToolNames = Field(default_factory=list)

    @field_validator("provider_id", mode="before")
    @classmethod
    def _blank_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("approval_tools")
    @classmethod
    def _clean_approval_tools(cls, v: list[str]) -> list[str]:
        return list(dict.fromkeys(name.strip() for name in v if name.strip()))


class AgentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=SLUG_PATTERN
    )
    name: str | None = Field(default=None, min_length=1, max_length=100)
    role: AgentRole | None = None
    description: str | None = None
    system_prompt: str | None = Field(default=None, min_length=1)
    enabled: bool | None = None
    is_output_gate: bool | None = None
    sort_order: int | None = None
    provider_id: str | None = None
    # None = 不修改；[] = 清空
    approval_tools: ToolNames | None = None

    @field_validator("provider_id", mode="before")
    @classmethod
    def _blank_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("approval_tools")
    @classmethod
    def _clean_approval_tools(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        return list(dict.fromkeys(name.strip() for name in v if name.strip()))


class AgentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    role: AgentRole
    description: str
    system_prompt: str
    enabled: bool
    is_output_gate: bool = False
    sort_order: int
    provider_id: str | None
    approval_tools: list[str]
    created_at: datetime
    updated_at: datetime

    @field_validator("approval_tools", mode="before")
    @classmethod
    def _parse_approval_tools(cls, v):
        # 数据库里存的是 JSON 字符串
        if isinstance(v, str):
            return parse_approval_tools(v)
        return v or []
