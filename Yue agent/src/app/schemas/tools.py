import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    ═══════════════════════════════════════════════════
                        工具 Schema
    ═══════════════════════════════════════════════════

    config 接受三种常见写法，统一规范化为
        {"mcpServers": {"name": {"command": ..., "args": [...]}}}
"""

SLUG_PATTERN = r"^[a-z0-9][a-z0-9_-]*$"


# —————————把上传的配置片段规范化成 {"mcpServers": {...}}————————
def normalize_mcp_config(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        raise ValueError("请粘贴或上传 MCP 配置")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"不是合法的 JSON：{exc.msg}") from None

    if not isinstance(data, dict):
        raise ValueError("配置顶层必须是 JSON 对象")

    # Claude Desktop 完整配置、servers 别名、或直接是服务名映射
    servers = data.get("mcpServers") or data.get("servers")
    if servers is None:
        # 顶层本身就是服务名 → 配置 的映射
        servers = data
    if not isinstance(servers, dict) or not servers:
        raise ValueError("配置里没有任何 MCP 服务")

    cleaned: dict = {}
    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            raise ValueError(f"服务「{name}」的配置必须是 JSON 对象")
        if not cfg.get("command") and not cfg.get("url"):
            raise ValueError(f"服务「{name}」缺少 command 或 url")
        cleaned[str(name)] = cfg

    return json.dumps({"mcpServers": cleaned}, ensure_ascii=False, indent=2)


class ToolCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str = Field(min_length=1, max_length=50, pattern=SLUG_PATTERN)
    name: str = Field(min_length=1, max_length=100)
    description: str = ""
    config: str = Field(min_length=1)
    enabled: bool = True

    @field_validator("config")
    @classmethod
    def _normalize_config(cls, v: str) -> str:
        return normalize_mcp_config(v)


class ToolUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=SLUG_PATTERN
    )
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    config: str | None = None
    enabled: bool | None = None

    @field_validator("config")
    @classmethod
    def _normalize_config(cls, v: str | None) -> str | None:
        return normalize_mcp_config(v) if v is not None else None


class ToolOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    description: str
    config: str
    available_tools: str
    enabled: bool
    created_at: datetime
    updated_at: datetime
    tools_checked_at: datetime | None


# —————————公开接口：不返回原始 config（可能含密钥 / 路径）————————
class ToolPublicOut(BaseModel):
    id: str
    slug: str
    name: str
    description: str
    enabled: bool
    servers: list[str]
    available_tools: list[dict]
    tools_checked_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, tool) -> "ToolPublicOut":
        return cls(
            id=tool.id,
            slug=tool.slug,
            name=tool.name,
            description=tool.description,
            enabled=tool.enabled,
            servers=server_names(tool.config),
            available_tools=parse_available_tools(tool.available_tools),
            tools_checked_at=tool.tools_checked_at,
            created_at=tool.created_at,
            updated_at=tool.updated_at,
        )


# —————————给员工挂载工具：tool_names 为空表示全量————————
class ToolMount(BaseModel):
    tool_id: str = Field(min_length=1)
    tool_names: list[str] | None = None


class AgentToolsUpdate(BaseModel):
    tools: list[ToolMount] = []


class ToolMountOut(BaseModel):
    tool_id: str
    slug: str
    name: str
    enabled: bool
    tool_names: list[str] | None


# —————————解析已拉取的工具清单————————
def parse_available_tools(raw: str | None) -> list[dict]:
    try:
        data = json.loads(raw or "[]")
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return [
        item
        for item in data
        if isinstance(item, dict) and item.get("name")
    ]


# —————————从挂载记录里解析选中的工具名————————
def parse_tool_names(raw: str | None) -> list[str]:
    try:
        data = json.loads(raw or "[]")
    except Exception:
        return []
    return [str(n) for n in data] if isinstance(data, list) else []


# —————————从配置里取出服务名，列表页展示用————————
def server_names(config: str) -> list[str]:
    try:
        data = json.loads(config)
    except Exception:
        return []
    servers = data.get("mcpServers") or data.get("servers") or {}
    return list(servers) if isinstance(servers, dict) else []
