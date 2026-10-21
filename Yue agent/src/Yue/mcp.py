import asyncio
import json
import logging
import os
import shutil

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

"""
    ═══════════════════════════════════════════════════
                        MCP 工具接入
    ═══════════════════════════════════════════════════

    配置来自数据库 tools 表，每个员工只加载自己挂载的工具。
    配置格式沿用 Claude Desktop 的 mcpServers JSON。

    工具按「合并后的连接配置」缓存；MCP 服务起不来时只记日志、
    返回空列表，不影响 Agent 正常对话。
"""

logger = logging.getLogger(__name__)

# key = 规范化后的连接配置 JSON，value = 加载好的工具
_cache: dict[str, list[BaseTool]] = {}


def _resolve_command(command: str) -> tuple[str, list[str]]:
    """Windows 下 npx/npm 实际是 .cmd，CreateProcess 不能直接执行，
    需要 ``cmd /c`` 包一层。其他平台原样返回。"""
    if os.name != "nt" or not command:
        return command, []

    found = shutil.which(command)
    if not found:
        return command, []

    if found.lower().endswith((".cmd", ".bat")):
        return "cmd", ["/c", found]

    return found, []


# langchain-mcp-adapters 会把连接配置里除 transport 外的键原样传给
# 各传输的构造函数，多一个未知键（例如 Claude Desktop 的 "type": "sse"）就会报错，
# 所以按传输类型只保留受支持的键。
_STDIO_KEYS = {
    "command",
    "args",
    "env",
    "cwd",
    "encoding",
    "encoding_error_handler",
    "session_kwargs",
}
_HTTP_KEYS = {
    "url",
    "headers",
    "timeout",
    "sse_read_timeout",
    "session_kwargs",
    "httpx_client_factory",
    "auth",
}
_STREAMABLE_HTTP_KEYS = _HTTP_KEYS | {"terminate_on_close"}
_WEBSOCKET_KEYS = {"url", "session_kwargs"}

_TRANSPORT_ALIASES = {
    "http": "streamable_http",
    "streamable-http": "streamable_http",
    "streamablehttp": "streamable_http",
    "ws": "websocket",
}


# —————————把单条 MCP 服务配置规范成适配器认识的连接参数————————
def _normalize_connection(cfg: dict) -> dict | None:
    cfg = dict(cfg)

    # type / transport 都可能是声明方式，统一取一个并做别名归一
    declared = cfg.pop("type", None) or cfg.pop("transport", None)
    if isinstance(declared, str):
        declared = declared.strip().lower()
        declared = _TRANSPORT_ALIASES.get(declared, declared)

    # 远程 MCP（url）
    if cfg.get("url"):
        transport = declared or "streamable_http"
        if transport == "websocket":
            allowed = _WEBSOCKET_KEYS
        elif transport == "sse":
            allowed = _HTTP_KEYS
        else:
            transport = "streamable_http"
            allowed = _STREAMABLE_HTTP_KEYS
        cfg = {k: v for k, v in cfg.items() if k in allowed}
        cfg["transport"] = transport
        return cfg

    # 本地 stdio MCP
    command = cfg.get("command")
    if not isinstance(command, str) or not command:
        return None

    cfg = {k: v for k, v in cfg.items() if k in _STDIO_KEYS}
    exe, prefix = _resolve_command(command)
    cfg["transport"] = "stdio"
    cfg["command"] = exe
    args = list(cfg.get("args") or [])
    cfg["args"] = [*prefix, *args] if prefix else args
    return cfg


def _connections_from_configs(configs: list[str]) -> dict:
    """把若干段 mcpServers JSON 合并成 MultiServerMCPClient 的连接表。"""
    connections: dict = {}

    for raw in configs:
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            logger.warning("工具配置解析失败，已跳过")
            continue

        servers = data.get("mcpServers") or data.get("servers") or {}
        if not isinstance(servers, dict):
            continue

        for name, cfg in servers.items():
            if not isinstance(cfg, dict):
                continue
            normalized = _normalize_connection(cfg)
            if normalized is None:
                logger.warning("工具配置「%s」缺少 command 或 url，已跳过", name)
                continue
            connections[name] = normalized

    return connections


async def get_mcp_tools(configs: list[str]) -> list[BaseTool]:
    """加载一组配置对应的 MCP 工具；相同配置进程内只加载一次。"""
    connections = _connections_from_configs(configs)
    if not connections:
        return []

    key = json.dumps(connections, sort_keys=True, ensure_ascii=False)
    if key in _cache:
        return _cache[key]

    try:
        client = MultiServerMCPClient(connections, tool_name_prefix=True)
        tools = await client.get_tools()
    except Exception:
        logger.exception("MCP 工具加载失败，按无 MCP 工具继续")
        _cache[key] = []
        return _cache[key]

    _cache[key] = list(tools)
    logger.info(
        "MCP 已加载 %d 个工具（%s）：%s",
        len(_cache[key]),
        ", ".join(connections),
        [tool.name for tool in _cache[key]],
    )
    return _cache[key]


async def probe_mcp_tools(config: str, timeout: float = 40.0) -> list[dict]:
    """连接一段配置里的 MCP 服务，返回工具清单（不入缓存）。

    后台「拉取工具」用，失败时抛异常由上层提示。
    """
    connections = _connections_from_configs([config])
    if not connections:
        raise ValueError("配置里没有可连接的 MCP 服务")

    client = MultiServerMCPClient(connections, tool_name_prefix=True)
    tools = await asyncio.wait_for(client.get_tools(), timeout=timeout)

    return [
        {
            "name": tool.name,
            "description": (tool.description or "").strip(),
        }
        for tool in tools
    ]


def reset_mcp_tools() -> None:
    """工具配置变更后调用，下次构图重新加载。"""
    _cache.clear()
