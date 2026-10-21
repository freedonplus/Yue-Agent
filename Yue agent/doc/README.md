# Yue Agent 文档

| 文档 | 内容 |
|---|---|
| [AGENTS.md](AGENTS.md) | 员工、MCP 工具、技能手册，以及调度与审批机制 |
| [API.md](API.md) | HTTP API 参考：厂商、员工、工具、技能、对话、会话、记忆 |

## 快速启动

```bash
cd "C:/Users/tzy88/Desktop/Yue Agent/Yue agent"
.venv/Scripts/python.exe main.py
```

启动后：

| 入口 | 地址 |
|---|---|
| 管理后台 | `http://127.0.0.1:8000/admin` |
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| 健康检查 | `GET http://127.0.0.1:8000/` |

## 运行依赖

- Python 虚拟环境：`.venv`
- Node.js（`npx`）：Playwright、Excel、PDF Reader、YouTube 字幕等 MCP 服务
- `uv` / `uvx`：Fetch、DuckDuckGo、Time、arXiv 等 MCP 服务

首次对话会启动所有已挂载的本地 MCP 服务，因此比后续请求慢一些。

## 目录

```text
Yue agent/
├─ main.py                 # 启动入口
├─ src/
│  ├─ app/                 # FastAPI：路由、模型、服务、管理后台
│  └─ Yue/                 # LangGraph：调度员、员工、MCP、记忆
├─ skills/                 # SKILL.md 源文件（可导入数据库）
├─ data/
│  ├─ yue.db               # SQLite 数据库
│  └─ arxiv/               # arXiv 论文存储目录
├─ template/               # 管理后台页面模板
└─ doc/                    # 文档
```

## 数据与配置

- 数据库：`data/yue.db`，首次启动自动建表并做轻量迁移。
- 模型厂商、API Key：在管理后台「厂商」中配置，密钥在接口响应中自动掩码。
- MCP 原始配置只保存在数据库，公开接口不返回，避免泄露密钥与本地路径。
- 技能是全局的：不需要挂载给员工，对话时通过 `skill_slug` 指定即可。

### 运行时配置

在 `.env` 中可覆盖的常用项（未设置时使用默认值）：

| 变量 | 默认 | 说明 |
|---|---|---|
| `APP_RELOAD` | `true` | 启动时自动重载。已排除 `.venv`、`data`、`__pycache__` 等目录；生产环境建议设为 `false` |
| `APP_DEBUG` | `false` | 调试模式 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `DB_PATH` | `data/yue.db` | SQLite 文件路径（相对路径按项目根目录解析） |
| `SQLALCHEMY_ECHO` | `false` | 打印 SQL |

SQLite 连接默认启用 WAL、`synchronous=NORMAL`、外键约束和 5 秒忙等待。

### 响应与流式输出

- 普通 JSON 响应（≥ 1 KB）自动 GZip 压缩；SSE 流（`/api/chat/*`、`/admin/playground/*`）不压缩。
- `GET /api/skills/summary` 返回不含 `content` 的轻量技能列表，前端选择技能时用它。
- `state` 事件是截断后的状态摘要，详见 [API.md](API.md#102-sse-事件)。
