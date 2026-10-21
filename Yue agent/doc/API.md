# Yue Agent API 文档

员工、MCP 工具、技能的实际配置与调度机制见 [AGENTS.md](AGENTS.md)。

## 1. 基本信息

| 项目 | 说明 |
|---|---|
| 服务地址 | `http://127.0.0.1:8000` |
| 数据格式 | `application/json`（UTF-8） |
| 交互式文档 | `GET /docs`（Swagger UI） |
| 备用文档 | `GET /redoc`（ReDoc） |
| OpenAPI 描述 | `GET /openapi.json` |
| 文档信息 | `GET /docs/info` |

业务接口统一挂在 `/api` 前缀下。根路由、文档页不挂鉴权。

### 当前鉴权状态

`main.py` 中 Token 依赖目前是注释状态：

```python
# app.include_router(api_router,
#                    prefix="/api",
#                    dependencies=[Depends(verify_token)])
```

所以**当前所有 `/api/*` 接口无需 Bearer Token**。若打开注释，除文档页与根路由外，其余接口都需要 Token。

部分写操作另有管理员 Cookie 校验，与 Bearer Token 是两套机制：

| 操作 | 权限 |
|---|---|
| 厂商新增、修改、启停 | 当前公开 |
| 工具新增、修改、启停、刷新 | 当前公开 |
| 员工查询、启停、工具挂载 | 当前公开 |
| 员工创建、修改、删除 | 管理员 Cookie |
| 技能新增、导入、修改、删除 | 管理员 Cookie |
| 厂商、工具、会话、记忆的删除 | 管理员 Cookie |

管理后台登录入口：`GET /admin/login`。

---

## 2. Bearer Token 鉴权

前后端共享 `.env` 中的 `AUTH_TOKEN`（HMAC 签名密钥），前端生成带过期时间的 Token，后端只校验。

### Token 结构

```text
base64url(payload) + "." + base64url(HMAC-SHA256(AUTH_TOKEN, base64url(payload)))
```

payload：

```json
{"iat": 1760000000, "exp": 1760000300}
```

- `iat`：签发时间（Unix 秒）
- `exp`：过期时间（Unix 秒）
- 签名使用 HMAC-SHA256，Base64 URL 编码并去掉 `=` 填充
- 后端允许 60 秒时钟偏差

### 请求头

```http
Authorization: Bearer <token>
```

### Python 生成示例（调试用）

```python
import base64
import hashlib
import hmac
import json
import time

SECRET = "你的 AUTH_TOKEN"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def create_token(ttl: int = 300) -> str:
    now = int(time.time())
    payload = json.dumps({"iat": now, "exp": now + ttl}, separators=(",", ":"))
    payload_part = b64url(payload.encode())
    sig = hmac.new(SECRET.encode(), payload_part.encode(), hashlib.sha256).digest()
    return f"{payload_part}.{b64url(sig)}"
```

### 鉴权错误

| HTTP | code | 说明 |
|---|---|---|
| 401 | `NOT_AUTHENTICATED` | 缺少 Bearer Token，或管理员未登录 |
| 401 | `INVALID_TOKEN` | 签名错误或结构非法 |
| 401 | `TOKEN_EXPIRED` | Token 已过期 |

---

## 3. 统一响应与错误格式

### 错误响应

```json
{
  "code": "PROVIDER_NOT_FOUND",
  "message": "厂商不存在",
  "detail": null,
  "request_id": "5745b8aff7fc4ea2a6b7a4b37bde2896"
}
```

| 字段 | 说明 |
|---|---|
| `code` | 机器可读错误码 |
| `message` | 中文错误信息 |
| `detail` | 附加信息，通常是参数校验明细 |
| `request_id` | 请求 ID，与响应头 `X-Request-ID` 一致 |

### 参数校验失败（422）

```json
{
  "code": "VALIDATION_ERROR",
  "message": "参数校验失败",
  "detail": [
    {
      "loc": ["body", "base_url"],
      "msg": "Value error, base_url 必须以 http:// 或 https:// 开头",
      "type": "value_error",
      "input": "ftp://x"
    }
  ],
  "request_id": "..."
}
```

### 响应头

| 响应头 | 说明 |
|---|---|
| `X-Request-ID` | 请求 ID，便于排查日志 |
| `X-Process-Time-Ms` | 服务端处理耗时（毫秒） |

---

## 4. 列表与分页约定

- 厂商、员工、工具、技能列表不分页，直接返回 JSON 数组。
- 会话列表支持 `limit` / `offset`。
- 会话消息支持 `limit` / `before_id` 向前翻页。
- 记忆列表支持 `limit`。
- 厂商列表只返回 `enabled = true` 的记录；员工列表默认也只返回启用项，管理端可传 `include_disabled=true` 查看停用员工；工具与技能列表返回全部记录，由前端按 `enabled` 展示。

---

## 5. 数据模型

### 5.1 Provider（厂商）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 响应 | UUID |
| `slug` | string | 是 | 唯一标识，`^[a-z0-9][a-z0-9_-]*$`，最长 50 |
| `name` | string | 是 | 显示名称，最长 100 |
| `base_url` | string | 是 | 必须以 `http://` 或 `https://` 开头，最长 255；末尾 `/` 会去掉 |
| `api_key` | string \| null | 否 | 密钥，最长 255；响应自动掩码 |
| `default_model` | string \| null | 否 | 默认模型名，最长 100 |
| `temperature` | float | 否 | 采样温度，0-2，默认 0.7 |
| `max_tokens` | int | 否 | 最大输出 token，默认 4096 |
| `max_retries` | int | 否 | 最大重试次数，0-10，默认 3 |
| `request_timeout` | int | 否 | 请求超时秒数，默认 60 |
| `enabled` | bool | 否 | 是否启用，默认 `true` |
| `is_default` | bool | 否 | 是否默认厂商，全局只能有一个 |
| `created_at` | string | 响应 | ISO 8601 |
| `updated_at` | string | 响应 | ISO 8601 |

### 5.2 AgentRole（员工 / 调度员）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 响应 | UUID |
| `slug` | string | 是 | 唯一标识，规则同 Provider |
| `name` | string | 是 | 显示名称，最长 100 |
| `role` | string | 是 | `supervisor` 或 `worker` |
| `description` | string | 否 | 描述 |
| `system_prompt` | string | 是 | 系统提示词，不能为空 |
| `approval_tools` | string[] | 否 | 需要人工审批的 MCP 工具全名 |
| `enabled` | bool | 否 | 是否启用，默认 `true` |
| `is_output_gate` | bool | 否 | 是否最终输出管卡，默认 `false` |
| `sort_order` | int | 否 | 升序排列，默认 `0` |
| `provider_id` | string \| null | 否 | 绑定的厂商 |
| `created_at` | string | 响应 | ISO 8601 |
| `updated_at` | string | 响应 | ISO 8601 |

### 5.3 Tool（MCP 工具配置）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | UUID |
| `slug` | string | 唯一标识 |
| `name` | string | 显示名称 |
| `description` | string | 描述 |
| `enabled` | bool | 是否启用 |
| `servers` | string[] | 配置中的 MCP 服务名 |
| `available_tools` | object[] | 已拉取的工具清单，元素为 `{"name", "description"}` |
| `tools_checked_at` | string \| null | 最近一次成功拉取的时间 |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

> 公开响应**不返回原始 `config`**，避免泄露密钥、令牌和本地路径。原始配置只在管理后台查看和编辑。

### 5.4 Skill（技能）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | UUID |
| `slug` | string | 唯一标识 |
| `name` | string | 显示名称 |
| `description` | string | 描述 |
| `content` | string | SKILL.md 正文（不含 frontmatter） |
| `source_path` | string | 来源文件相对路径，可为空 |
| `enabled` | bool | 是否启用 |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

### 5.5 Session（会话）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 数据库主键 |
| `session_id` | string | 前端会话标识，与对话请求里的 `session_id` 对应 |
| `title` | string | 标题 |
| `last_message` | string | 最近一条消息摘要 |
| `message_count` | int | 消息数 |
| `workdir` | string | 会话工作目录，空串表示使用员工默认目录 |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

### 5.6 ChatMessage（会话消息）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 自增主键 |
| `session_id` | string | 会话标识 |
| `role` | string | `user` 或 `assistant` |
| `content` | string | 消息正文 |
| `name` | string \| null | 最终发言的员工 slug |
| `created_at` | string | ISO 8601 |

只持久化用户消息与每轮最终答复；中间的调度指令、工具调用不写入会话消息。

### 5.7 Memory（跨会话记忆）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | UUID |
| `user_id` | string | 记忆归属，默认 `default` |
| `kind` | string | `profile` / `preference` / `decision` / `fact` |
| `content` | string | 记忆内容，最长 2000 |
| `tags` | string | 标签，逗号分隔 |
| `source_session_id` | string | 来源会话，可为空 |
| `created_at` | string | ISO 8601 |
| `updated_at` | string | ISO 8601 |

---

## 6. 厂商接口

### 6.1 创建厂商

```http
POST /api/providers
```

```json
{
  "slug": "deepseek",
  "name": "DeepSeek",
  "base_url": "https://api.deepseek.com",
  "api_key": "sk-1234567890abcdef",
  "default_model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 4096,
  "enabled": true,
  "is_default": true
}
```

成功响应 `201`：厂商对象，`api_key` 为掩码。

错误：`409 PROVIDER_SLUG_EXISTS`、`422 VALIDATION_ERROR`。

### 6.2 厂商列表

```http
GET /api/providers?q=deep
```

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `q` | string | 否 | 按 `name` / `slug` 模糊搜索，最长 100 |

只返回 `enabled = true` 的厂商。

### 6.3 厂商详情

```http
GET /api/providers/{provider_id}
```

错误：`404 PROVIDER_NOT_FOUND`。

### 6.4 更新厂商

```http
PATCH /api/providers/{provider_id}
```

只传需要修改的字段：

```json
{
  "name": "DeepSeek 官方",
  "enabled": false
}
```

说明：

- 不传的字段保持不变。
- `api_key` 传 `""` 或 `null` 表示清空；不传表示保持原值。
- 每次传入 `is_default: true` 会自动把其他厂商的 `is_default` 置为 `false`。
- 错误：`404 PROVIDER_NOT_FOUND`、`409 PROVIDER_SLUG_EXISTS`、`422 VALIDATION_ERROR`。

### 6.5 启用 / 停用厂商

```http
PATCH /api/providers/{provider_id}/enabled
```

```json
{"enabled": false}
```

### 6.6 删除厂商

公开 API 不提供删除。请在管理后台 `/admin/providers` 删除；删除后关联员工的 `provider_id` 会被置为 `null`。

---

## 7. 员工 / 调度员接口

公开接口只提供查询、启停和工具挂载；创建、修改、删除在管理后台 `/admin/roles`。

### 7.1 员工列表

```http
GET /api/agent_roles?role=worker&provider_id=xxx&q=写
```

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `role` | string | 否 | `supervisor` 或 `worker` |
| `provider_id` | string | 否 | 按厂商过滤 |
| `q` | string | 否 | 按 `name` / `slug` 模糊搜索，最长 100 |
| `include_disabled` | bool | 否 | `true` 时连同停用员工一起返回，供管理端启停使用 |

默认只返回 `enabled = true` 的员工，按 `sort_order` 升序、`created_at` 升序排列。管理端需要看到停用员工时传 `include_disabled=true`，否则员工停用后会从列表里消失、无法再启用。

### 7.2 员工详情

```http
GET /api/agent_roles/{agent_id}
```

错误：`404 AGENT_NOT_FOUND`。

### 7.3 启用 / 停用员工

```http
PATCH /api/agent_roles/{agent_id}/enabled
```

```json
{"enabled": false}
```

唯一启用的调度员不能被停用，否则返回 `409 AGENT_SUPERVISOR_LOCKED`。

### 7.4 查看员工挂载的工具

```http
GET /api/agent_roles/{agent_id}/tools
```

响应：

```json
[
  {
    "tool_id": "工具 ID",
    "slug": "excel",
    "name": "Excel 表格",
    "enabled": true,
    "tool_names": null
  }
]
```

`tool_names` 为 `null` 表示该配置下全部工具；数组表示只挂载选中的工具。

### 7.5 覆盖式挂载工具

```http
PUT /api/agent_roles/{agent_id}/tools
```

```json
{
  "tools": [
    {"tool_id": "工具 ID", "tool_names": null},
    {"tool_id": "另一个工具 ID", "tool_names": ["excel_excel_read_sheet"]}
  ]
}
```

说明：

- 这是覆盖式更新，未出现在列表中的旧挂载会被清除。
- `tool_names` 不传或为 `null`：该配置下全部工具。
- `tool_names` 为 `[]`：一个工具都不给。
- 成功响应为更新后的挂载列表。
- 错误：`404 AGENT_NOT_FOUND`、`404 TOOL_NOT_FOUND`。

### 7.6 创建 / 修改 / 删除员工

通过管理后台 `/admin/roles` 操作。允许的字段与 5.2 一致；约束：

- 全局只能有一个 `role = supervisor`，重复创建返回 `409 AGENT_SUPERVISOR_EXISTS`。
- 不能删除或停用最后一个启用的调度员，返回 `409 AGENT_SUPERVISOR_LOCKED`。
- `provider_id` 指向的厂商必须存在，否则返回 `400 AGENT_PROVIDER_NOT_FOUND`。
- slug 重复返回 `409 AGENT_SLUG_EXISTS`。

---

## 8. 工具接口

### 8.1 新建工具

```http
POST /api/tools
```

```json
{
  "slug": "excel",
  "name": "Excel 表格",
  "description": "读写 xlsx 工作表",
  "config": "{\"mcpServers\":{\"excel\":{\"command\":\"npx\",\"args\":[\"--yes\",\"@negokaz/excel-mcp-server\"]}}}",
  "enabled": true
}
```

`config` 接受三种写法，统一规范化为 `{"mcpServers": {...}}`：

1. Claude Desktop 完整配置：`{"mcpServers": {...}}`
2. `servers` 别名：`{"servers": {...}}`
3. 顶层直接是服务名到配置的映射：`{"excel": {...}}`

每个服务必须包含 `command` 或 `url`。

成功响应 `201`：工具对象（不含 `config`）。

错误：`409 TOOL_SLUG_EXISTS`、`422 VALIDATION_ERROR`。

### 8.2 工具列表 / 详情

```http
GET /api/tools
GET /api/tools/{tool_id}
```

返回全部工具（包括停用的）；详情不存在返回 `404 TOOL_NOT_FOUND`。

### 8.3 修改工具

```http
PATCH /api/tools/{tool_id}
```

```json
{
  "name": "Excel 表格服务",
  "config": "{\"mcpServers\":{...}}"
}
```

说明：

- 只更新传入字段。
- 修改 `config` 会清空 `available_tools` 和 `tools_checked_at`，需要重新调用刷新接口。
- 错误：`404 TOOL_NOT_FOUND`、`409 TOOL_SLUG_EXISTS`、`422 VALIDATION_ERROR`。

### 8.4 启用 / 停用工具

```http
PATCH /api/tools/{tool_id}/enabled
```

```json
{"enabled": false}
```

### 8.5 刷新工具清单

```http
POST /api/tools/{tool_id}/refresh
```

连接 MCP 服务并拉取实际工具清单，保存到 `available_tools`。首次拉取可能需要下载依赖，耗时较长。

错误：

| HTTP | code | 场景 |
|---|---|---|
| 400 | `TOOL_CONFIG_INVALID` | 启动命令错误、依赖缺失、网络失败或超时 |
| 404 | `TOOL_NOT_FOUND` | 工具不存在 |

### 8.6 删除工具

公开 API 不提供删除。请在管理后台 `/admin/tools` 删除；挂载关系会级联清理。

---

## 9. 技能接口

技能是全局的，不需要挂载给员工。前端列出所有启用的技能，对话时通过 `skill_slug` 指定。

### 9.1 技能列表

```http
GET /api/skills
```

返回全部技能（包括停用的），包含完整 `content`。技能较多时响应体可能较大。

### 9.2 技能摘要列表（轻量）

```http
GET /api/skills/summary
```

只返回 `id`、`slug`、`name`、`description`、`source_path`、`enabled`、`updated_at`，不含 `content`。
前端技能选择框用它即可，避免一次下载几百 KB 的技能正文。

### 9.3 技能详情

```http
GET /api/skills/{skill_id}
```

错误：`404 SKILL_NOT_FOUND`。

### 9.4 创建 / 导入 / 修改 / 删除技能

仅限管理后台：

| 操作 | 地址 |
|---|---|
| 查看列表 | `/admin/skills` |
| 新建 | `/admin/skills/new` |
| 从 `skills/` 导入 | `POST /admin/skills/import` |
| 编辑 | `/admin/skills/{skill_id}/edit` |
| 删除 | `POST /admin/skills/{skill_id}/delete` |

错误码：`404 SKILL_NOT_FOUND`、`409 SKILL_SLUG_EXISTS`。

---

## 10. 对话接口（SSE）

### 10.1 发起对话

```http
POST /api/chat/stream
Content-Type: application/json
```

```json
{
  "message": "帮我查一下北京现在的天气",
  "history": [
    {"role": "user", "content": "早"},
    {"role": "assistant", "content": "主上早。"}
  ],
  "session_id": "session-001",
  "workdir": "C:/Users/tzy88/Desktop/Yue Agent",
  "skill_slug": "copywriting",
  "user_id": "default",
  "temperature": 0.7,
  "max_tokens": 4096
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message` | string | 是 | 用户输入，最长 20000 |
| `history` | object[] | 否 | 前端维护的历史消息，最多 50 条；服务端从最旧的消息开始裁剪，总字符数上限 60,000 |
| `session_id` | string | 否 | 关联会话表里的工作目录，最长 100 |
| `workdir` | string | 否 | 本次会话工作目录；优先于会话表设置 |
| `skill_slug` | string | 否 | 本次任务强制使用的技能 |
| `user_id` | string | 否 | 跨会话记忆归属，默认 `default` |
| `temperature` | number | 否 | 0–2，覆盖厂商默认温度；不传沿用厂商配置 |
| `max_tokens` | integer | 否 | 覆盖厂商默认最大输出；不传沿用厂商配置 |

响应为 `text/event-stream`，每行一条 JSON：

```text
data: {"type": "node", "node": "supervisor", "session_id": "session-001"}

data: {"type": "token", "content": "北京", "node": "worker_yue_chat", "session_id": "session-001"}

data: {"type": "done", "content": "最终答复", "run_id": "...", "session_id": "session-001"}
```

### 10.2 SSE 事件

| type | 说明 |
|---|---|
| `node` | 进入某个节点，`node` 为节点 slug |
| `reasoning` | 模型思考增量，`content` 为增量文本 |
| `token` | 正文增量，`content` 为增量文本 |
| `tool_call` | 模型发起工具调用，`tool_calls` 为完整调用列表 |
| `state` | 状态摘要，见下方说明 |
| `approval_required` | 需要人工审批，`run_id`、`approvals` 用于续跑 |
| `usage` | 本轮 token 用量，`usage` 含 `input_tokens` / `output_tokens` / `total_tokens`；在 `done` 之前推送 |
| `done` | 本轮结束，`content` 为最终答复，`paused` 为 `true` 时表示停在审批 |
| `error` | 运行失败，`message` 为错误信息 |

`usage` 事件示例：

```text
data: {"type": "usage", "usage": {"input_tokens": 123, "output_tokens": 456, "total_tokens": 579}, "session_id": "session-001"}
```

用量汇总本轮所有模型调用（调度员、员工以及工具循环中的每次调用）。
厂商不返回用量时三个字段均为 `0`。服务端通过 `MODEL_STREAM_USAGE`
（默认 `true`）向厂商开启 `stream_options.include_usage`；个别兼容端点
不支持该字段时可在 `.env` 里置 `MODEL_STREAM_USAGE=false` 关闭。

`state` 事件是**有上限的调试摘要**，不保证是完整图状态：

| 字段 | 说明 |
|---|---|
| `state.messages` | 最近 30 条消息；正文截断到 4,000 字符，`reasoning` 截断到 2,000 字符，工具参数序列化后截断到 2,000 字符 |
| `state.messages_total` | 图状态里消息总数 |
| `state.messages_truncated` | 被省略的消息条数，仅在确实省略时出现 |
| `state.nodes` | 本轮访问过的节点顺序 |
| 其他键 | 图状态中的其他值，按原样（不可 JSON 化时转字符串）输出 |

被截断的文本末尾会带 `…（已截断）`。如果需要完整状态，请直接查询检查点或服务端日志。

`approval_required.approvals` 元素：

```json
{
  "interrupt_id": "审批 ID",
  "tool_call_id": "工具调用 ID",
  "tool": "filesystem_write_file",
  "args": {"path": "..."},
  "description": "需要人工确认"
}
```

### 10.3 提交审批

```http
POST /api/chat/approve
```

```json
{
  "run_id": "发起对话时返回的 run_id",
  "decisions": [
    {"interrupt_id": "审批 ID", "type": "approve"},
    {
      "interrupt_id": "另一个审批 ID",
      "type": "reject",
      "message": "不要覆盖原文件"
    }
  ],
  "session_id": "session-001",
  "workdir": "C:/Users/tzy88/Desktop/Yue Agent",
  "skill_slug": "copywriting",
  "user_id": "default",
  "temperature": 0.7,
  "max_tokens": 4096
}
```

说明：

- `run_id` 也是图的 `thread_id`。
- 续跑时应再次传入 `workdir`、`skill_slug`、`user_id`、`temperature`、`max_tokens`，否则会丢失上下文或退回厂商默认参数。
- 没有待审批操作时返回 `409`。
- 响应与 `/api/chat/stream` 相同，继续推送 SSE 事件。

### 10.4 会话消息持久化

- 用户消息在每轮开始时保存。
- 每轮最终答复在流结束后保存，`name` 为最后发言的员工 slug。
- 审批暂停的一轮不会提前保存最终答复，续跑完成后才保存。
- 历史由前端通过 `history` 传入；会话消息接口用于重新打开会话时回放。

### 10.5 工作区列表

```http
GET /api/workspaces
```

```json
[
  {"id": "yue-agent", "name": "Yue agent", "root_path": "C:/Users/tzy88/Desktop/Yue Agent/Yue agent"},
  {"id": "yue-agent-2", "name": "Yue Agent", "root_path": "C:/Users/tzy88/Desktop/Yue Agent"},
  {"id": "tzy88", "name": "tzy88", "root_path": "C:/Users/tzy88"}
]
```

- `root_path` 可直接作为 `/api/chat/stream` 的 `workdir` 回传，统一使用正斜杠。
- 默认返回项目目录、项目上级目录和用户主目录（只包含真实存在的目录，重复目录去重）。
- 如需自定义，在 `.env` 里配置 JSON 数组（配置后完全替换默认列表）：

```dotenv
WORKSPACES=[{"id":"yue","name":"Yue Agent","root_path":"C:/Users/tzy88/Desktop/Yue Agent"}]
```

---

## 11. 会话接口

### 11.1 创建会话

```http
POST /api/sessions
```

```json
{
  "session_id": "session-001",
  "title": "北京天气",
  "last_message": "",
  "message_count": 0,
  "workdir": "C:/Users/tzy88/Desktop/Yue Agent"
}
```

`session_id` 不传时由服务端生成 UUID。重复返回 `409 SESSION_EXISTS`。

### 11.2 会话列表

```http
GET /api/sessions?q=天气&limit=50&offset=0
```

| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `q` | string | 无 | 按标题 / 最近消息模糊搜索 |
| `limit` | int | 50 | 1-200 |
| `offset` | int | 0 | 偏移量 |

### 11.3 会话详情

```http
GET /api/sessions/{session_id}
```

错误：`404 SESSION_NOT_FOUND`。

### 11.4 会话消息

```http
GET /api/sessions/{session_id}/messages?limit=200&before_id=100
```

| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `limit` | int | 200 | 1-1000 |
| `before_id` | int | 无 | 向前翻页，只返回 id 小于该值的消息 |

返回按时间正序排列的消息数组。重新打开会话时用它回放。

### 11.5 更新会话

```http
PATCH /api/sessions/{session_id}
```

```json
{
  "title": "新标题",
  "last_message": "最近一条消息",
  "message_count": 4,
  "workdir": "C:/Users/tzy88/Desktop/Yue Agent"
}
```

### 11.6 删除会话

仅限管理员 Cookie：

```http
DELETE /api/sessions/{session_id}
```

成功返回 `204`，同时删除该会话的消息记录。未登录返回 `401 NOT_AUTHENTICATED`。

---

## 12. 跨会话记忆接口

记忆按 `user_id` 隔离，跨会话保留。对话时相关记忆会自动注入提示词，员工也可以通过 `save_memory` / `search_memory` 工具读写同一份数据。

### 12.1 记忆列表

```http
GET /api/memories?user_id=default&q=项目&limit=50
```

| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `user_id` | string | `default` | 记忆归属 |
| `q` | string | 无 | 内容模糊搜索 |
| `limit` | int | 50 | 1-200 |

### 12.2 写入记忆

```http
POST /api/memories
```

```json
{
  "user_id": "default",
  "content": "用户的项目叫 Yue Agent",
  "tags": "项目,名称",
  "kind": "fact",
  "source_session_id": "session-001"
}
```

`kind` 只能是 `profile`、`preference`、`decision`、`fact`。重复内容会做去重处理。成功返回 `201`。

> 不要写入密码、密钥、令牌或他人的私人数据。

### 12.3 删除记忆

仅限管理员 Cookie：

```http
DELETE /api/memories/{memory_id}?user_id=default
```

成功返回 `204`；不存在返回 `404`。

---

## 13. 管理后台

管理后台返回 HTML 页面，不是 JSON API。使用管理员 Cookie 登录。

| 功能 | 地址 |
|---|---|
| 登录 / 退出 | `/admin/login`、`POST /admin/logout` |
| 员工管理 | `/admin/roles`、`/admin/roles/new`、`/admin/roles/{id}/edit` |
| 工具管理 | `/admin/tools`、`/admin/tools/new`、`/admin/tools/{id}/edit` |
| 工具拉取 / 删除 | `POST /admin/tools/{id}/refresh`、`POST /admin/tools/{id}/delete` |
| 技能管理 | `/admin/skills`、`/admin/skills/new`、`/admin/skills/import` |
| 厂商管理 | `/admin/providers`、`/admin/providers/new` |
| 会话管理 | `/admin/sessions`、`/admin/sessions/{session_id}` |
| 会话删除 | `POST /admin/sessions/{session_id}/delete`、`POST /admin/sessions/delete`（批量） |
| 调试对话 | `/admin/playground` |

管理后台的修改会调用 `reset_graph()`，下一次对话自动重新构图。

---

## 14. 其他接口

| 方法 | 路径 | 说明 | 响应 |
|---|---|---|---|
| GET | `/` | 根路由 | `{"message": "Yue Agent"}` |
| GET | `/docs` | Swagger UI | HTML |
| GET | `/redoc` | ReDoc | HTML |
| GET | `/docs/info` | 文档地址信息 | JSON |
| GET | `/openapi.json` | OpenAPI 描述 | JSON |

`/docs/info` 响应示例：

```json
{
  "name": "Yue Agent",
  "version": "0.1.0",
  "swagger_ui": "http://127.0.0.1:8000/docs",
  "redoc": "http://127.0.0.1:8000/redoc",
  "openapi": "/openapi.json"
}
```

---

## 15. 错误码汇总

| HTTP | code | 说明 |
|---|---|---|
| 400 | `PROVIDER_ERROR` | 厂商操作失败（父类） |
| 400 | `AGENT_ERROR` | 员工操作失败（父类） |
| 400 | `AGENT_PROVIDER_NOT_FOUND` | 指定的厂商不存在 |
| 400 | `TOOL_ERROR` | 工具操作失败（父类） |
| 400 | `TOOL_CONFIG_INVALID` | MCP 配置启动失败、拉取超时 |
| 400 | `SKILL_ERROR` | 技能操作失败（父类） |
| 400 | `SESSION_ERROR` | 会话操作失败（父类） |
| 401 | `AUTH_ERROR` | 鉴权失败（父类） |
| 401 | `NOT_AUTHENTICATED` | 缺少 Token 或管理员未登录 |
| 401 | `INVALID_TOKEN` | Token 无效 |
| 401 | `TOKEN_EXPIRED` | Token 已过期 |
| 404 | `PROVIDER_NOT_FOUND` | 厂商不存在 |
| 404 | `AGENT_NOT_FOUND` | 员工不存在 |
| 404 | `TOOL_NOT_FOUND` | 工具不存在 |
| 404 | `SKILL_NOT_FOUND` | 技能不存在 |
| 404 | `SESSION_NOT_FOUND` | 会话不存在 |
| 409 | `PROVIDER_SLUG_EXISTS` | 厂商 slug 已存在 |
| 409 | `AGENT_SLUG_EXISTS` | 员工 slug 已存在 |
| 409 | `AGENT_SUPERVISOR_EXISTS` | 已存在调度员 |
| 409 | `AGENT_SUPERVISOR_LOCKED` | 不能删除或停用最后一个调度员 |
| 409 | `TOOL_SLUG_EXISTS` | 工具 slug 已存在 |
| 409 | `SKILL_SLUG_EXISTS` | 技能 slug 已存在 |
| 409 | `SESSION_EXISTS` | 会话已存在 |
| 409 | `DB_CONFLICT` | 数据库唯一约束等冲突 |
| 404 | `HTTP_ERROR` | 路由或资源不存在 |
| 422 | `VALIDATION_ERROR` | 参数校验失败 |
| 500 | `INTERNAL_ERROR` | 服务器内部错误 |
