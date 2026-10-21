# 员工、工具与技能手册

本文档对应当前数据库中的实际配置，服务器启动后即可在管理后台或 API 中看到同样的内容。

## 1. 调度机制

```text
用户消息
   │
   ▼
supervisor（唯一调度员）
   │  选择一个员工，写自包含指令
   ▼
worker（员工节点，按需加载自己的 MCP 工具）
   │
   ├─ 完成 → 回到 supervisor
   └─ handoff → 直接转给另一个员工
   │
   ▼
supervisor 决定 FINISH
   │
   ▼
worker_yue_chat（输出管卡，用 Yue 的口吻整理最终答复）
   │
   ▼
返回用户
```

要点：

- `supervisor` 只做调度，不直接替员工编造结果。
- 员工只看到调度指令和自己的工具，不直接暴露内部分工。
- 最终答复统一经过输出管卡 `worker_yue_chat`；管卡本轮已经发言时直接结束，避免重复润色。
- 技能是全局的，不挂载给员工；每轮对话可以用 `skill_slug` 指定本次任务使用的技能。
- 会话工作目录由 `workdir` 注入员工提示词；不传时读取会话表里的设置。
- 跨会话记忆按 `user_id` 隔离，在对话前注入相关记忆，员工也可以通过 `save_memory` / `search_memory` 读写。

## 2. 员工名单

当前共 13 个角色：1 个调度员、1 个输出管卡、11 个员工。

| 顺序 | slug | 名称 | 职责 | 挂载工具 | 人工审批 |
|---|---|---|---|---|---|
| 0 | `worker_yue_chat` | Yue | 输出管卡：用 Yue 的口吻收束并整理最终答复 | 无 | 无 |
| 1 | `supervisor` | supervisor | 理解诉求、拆解任务、派工与收尾 | 无 | 无 |
| 20 | `worker_files` | 文件员工 | 项目内文件查找、读取、修改与目录整理 | `filesystem` | 文件写、改、建目录、移动 |
| 30 | `worker_research` | 研究员 | 查资料、检索论文、核对事实与来源 | `fetch`、`duckduckgo`、`arxiv`、`time` | arXiv 下载论文 |
| 40 | `worker_writer` | 写手 | 文案、文章、邮件、改写与语气打磨 | `fetch`、`duckduckgo`、`time` | 无 |
| 50 | `worker_coder` | 代码工程师 | 读代码、定位问题、落地修改与验证说明 | `filesystem`、`sequential-thinking`、`fetch` | 文件写、改、建目录、移动 |
| 60 | `worker_browser` | 浏览器操作员 | 真实浏览器打开、点击、填表、截图与排查 | `playwright`、`fetch` | 文件上传 |
| 70 | `worker_data` | 数据分析师 | 读表、计算、对比并给出结论 | `excel`、`filesystem`、`sequential-thinking` | 文件写操作、Excel 写操作 |
| 80 | `worker_docs` | 文档专员 | 读取 PDF、整理文档、产出 Markdown/Word 素材 | `pdf-reader`、`excel`、`filesystem` | 文件写操作、Excel 写操作 |
| 90 | `worker_news` | 资讯员 | 跟踪新闻、趋势与视频字幕，给出来源和时间 | `duckduckgo`、`fetch`、`youtube-transcript`、`time` | 无 |
| 100 | `worker_planner` | 规划师 | 把目标拆成可执行计划、排优先级与风险 | `sequential-thinking`、`time`、`fetch` | 无 |
| 110 | `worker_frontend` | 前端工程师 | 界面实现、设计还原、样式与浏览器验收 | `filesystem`、`playwright`、`fetch` | 文件写操作、文件上传 |
| 120 | `worker_life` | 生活助手 | 天气、时间、日常查询与轻量建议 | `weather`、`time`、`duckduckgo`、`fetch` | 无 |

调用员工时使用的是 `slug`，不是显示名称。

### 审批工具名

审批按 MCP 返回的工具全名配置，例如：

```json
[
  "filesystem_write_file",
  "filesystem_edit_file",
  "filesystem_create_directory",
  "filesystem_move_file",
  "excel_excel_write_to_sheet",
  "excel_excel_create_table",
  "excel_excel_copy_sheet",
  "excel_excel_format_range",
  "arxiv-mcp-server_download_paper",
  "playwright_browser_file_upload"
]
```

只读工具（搜索、抓取、读取、截图、查询天气等）不触发审批。

## 3. MCP 工具清单

当前共 13 个工具配置，其中 10 个为本次新增，原有 `filesystem`、`chrome-devtools-mcp`、`figma` 保留。

| slug | 名称 | 来源 | 启动方式 | 工具数 |
|---|---|---|---|---|
| `fetch` | 网页抓取 | 魔塔 `@modelcontextprotocol/fetch` | `uvx mcp-server-fetch` | 1 |
| `duckduckgo` | DuckDuckGo 搜索 | 魔塔 `@nickclyde/duckduckgo-mcp-server` | `uvx duckduckgo-mcp-server` | 3 |
| `playwright` | Playwright 浏览器 | 魔塔 `@microsoft/playwright-mcp` | `npx @playwright/mcp@latest` | 25 |
| `sequential-thinking` | 结构化思考 | 魔塔 `@modelcontextprotocol/sequentialthinking` | `npx -y @modelcontextprotocol/server-sequential-thinking` | 1 |
| `time` | 时间与时区 | 魔塔 `@modelcontextprotocol/time` | `uvx mcp-server-time` | 2 |
| `excel` | Excel 表格 | 魔塔 `@negokaz/excel-mcp-server` | `npx --yes @negokaz/excel-mcp-server` | 7 |
| `pdf-reader` | PDF 阅读器 | 魔塔 `@sylphxltd/pdf-reader-mcp` | `npx @sylphxltd/pdf-reader-mcp` | 1 |
| `arxiv` | arXiv 论文 | 魔塔 `@blazickjp/arxiv-mcp-server` | `uv tool run arxiv-mcp-server` | 19 |
| `youtube-transcript` | YouTube 字幕 | 魔塔 `@kimtaeyoon83/mcp-server-youtube-transcript` | `npx -y @kimtaeyoon83/mcp-server-youtube-transcript` | 1 |
| `weather` | 天气查询 | Open-Meteo | `npx -y open-meteo-mcp-weather-server` | 1 |
| `filesystem` | 文件系统 | 原有 | `npx -y @modelcontextprotocol/server-filesystem` | 14 |
| `chrome-devtools-mcp` | Chrome 开发者工具 | 原有 | `npx chrome-devtools-mcp@latest` | 32 |
| `figma` | Figma | 原有，远程 SSE | 远程服务 | 0 |

### 常用工具名

调度和审批都要使用带服务器前缀的全名：

| 用途 | 工具名 |
|---|---|
| 抓网页 | `fetch_fetch` |
| 网页搜索 | `ddg-search_search` |
| 抽取网页正文 | `ddg-search_fetch_content` |
| 浏览器导航 | `playwright_browser_navigate` |
| 浏览器快照 | `playwright_browser_snapshot` |
| 浏览器截图 | `playwright_browser_take_screenshot` |
| 浏览器点击 | `playwright_browser_click` |
| Excel 看结构 | `excel_excel_describe_sheets` |
| Excel 读表 | `excel_excel_read_sheet` |
| Excel 写表 | `excel_excel_write_to_sheet` |
| PDF 读取 | `pdf-reader-mcp_read_pdf` |
| arXiv 检索 | `arxiv-mcp-server_search_papers` |
| arXiv 下载 | `arxiv-mcp-server_download_paper` |
| YouTube 字幕 | `youtube-transcript_get_transcript` |
| 天气 | `open-meteo_get_weather` |
| 当前时间 | `time_get_current_time` |

### 配置说明

- `chrome-devtools-mcp` 与 `figma` 目前没有挂载给员工，需要时在管理后台按需挂载。
- 工具的原始 `config` 保存在数据库，公开 API 只返回服务器名称和已拉取的工具清单，不返回配置原文。
- `arxiv` 的论文存放目录为 `data/arxiv`，首次使用会自动创建。
- `excel` 设置了 `EXCEL_MCP_PAGING_CELLS_LIMIT=4000`，大表按页读取。
- 修改工具配置后，旧的工具清单会清空；需要调用 `POST /api/tools/{id}/refresh` 重新拉取。
- 新增工具后不会自动挂载到员工，需要在 `/api/agent_roles/{id}/tools` 或管理后台中挂载。

## 4. 技能清单

技能是全局的，所有启用的技能都会出现在前端技能选择框里，不需要挂载给员工。

对话请求带上 `skill_slug` 即可强制本次任务使用该技能：

```json
{
  "message": "把这份报告改成更像发布会稿件的语气",
  "skill_slug": "copywriting",
  "session_id": "session-001",
  "user_id": "default"
}
```

员工节点通过 `load_skill` 工具按需加载技能正文；没有指定时会结合任务自行判断是否加载。

当前共 17 个技能：

| slug | 名称 | 魔塔来源 | 用途 |
|---|---|---|---|
| `script-writing` | script-writing | 原有 | 剧本写作 |
| `anthropics-docx` | Word 文档处理 | `@anthropics/docx` | 生成、编辑、分析 `.docx` |
| `anthropics-pdf` | PDF 文档处理 | `@anthropics/pdf` | PDF 读取、合并、拆分、表单、OCR |
| `anthropics-frontend-design` | 前端界面设计 | `@anthropics/frontend-design` | 前端视觉方向与界面实现 |
| `code-review` | 代码审查 | `@1mangesh1/code-review` | 审查清单、反馈模板、PR 检查 |
| `copywriting` | 营销文案 | `@coreyhaines31/copywriting` | 落地页、定价页、营销邮件 |
| `excel` | Excel 表格处理 | `@duclm1x1/excel` | 读写、格式、图表、导出 |
| `markdown-mermaid` | Markdown 与 Mermaid | `@k-dense-ai/markdown-mermaid-writing` | Markdown 排版与图表 |
| `pdf-translate` | PDF 翻译 | `@chrislee121/pdf-translate-skill` | PDF 文档翻译 |
| `ppt-generation` | PPT 生成 | `@cyangzhou/ppt` | Markdown 大纲转 `.pptx` |
| `pptx` | PPT 演示文稿 | `lichaoyang1998/pptx` | 演示文稿结构与制作 |
| `python-backend` | Python 后端开发 | `@aaaaqwq/python` | FastAPI、Django、SQLAlchemy |
| `react-best-practices` | React 最佳实践 | `@vercel-labs/react-best-practices` | React/Next.js 性能优化 |
| `research-paper-writing` | 论文写作 | `@master-cai/research-paper-writing` | 论文改写、结构与表达 |
| `seo-aeo` | SEO / AEO 策略 | `@manojbajaj95/seo-and-aeo-strategy` | 搜索与 AI 引擎优化 |
| `sheet-to-report` | Excel 业务分析报告 | `majichuan/sheet-to-report` | 表格转经营分析报告 |
| `writing` | 通用写作 | `@agentscope-ai/writing-skill` | 通用写作与校对 |

说明：

- 本次没有覆盖原有的 `script-writing`。
- 源文件位于 `skills/<slug>/SKILL.md`，可在管理后台「技能」中导入或编辑。
- 大技能合并参考资料后最长截断到 60,000 字符，避免单次注入过长。
- 技能正文保存在数据库，修改 `skills/` 下的文件不会自动同步；需要在后台重新导入。

## 5. 使用示例

### 5.1 生活查询

```text
用户：帮我查一下北京现在的天气，适不适合出门。
路由：supervisor → worker_life → open-meteo_get_weather → supervisor → worker_yue_chat
```

### 5.2 资料与论文

```text
用户：找几篇 2025 年关于多智能体协作的论文，总结主要方法。
路由：supervisor → worker_research → ddg-search / arxiv → worker_yue_chat
```

### 5.3 Excel 分析（带审批）

```text
用户：分析 data/sales.xlsx 的月度趋势，并生成一份新表。
路由：supervisor → worker_data → excel_excel_describe_sheets / read_sheet
      → 写表前暂停，返回 approval_required
      → 用户批准后继续 → worker_yue_chat
```

审批请求示例：

```http
POST /api/chat/approve
Content-Type: application/json

{
  "run_id": "上一步返回的 run_id",
  "decisions": [
    {"interrupt_id": "approval_required 里的 interrupt_id", "type": "approve"}
  ],
  "session_id": "session-001",
  "user_id": "default"
}
```

### 5.4 指定技能写作

```json
POST /api/chat/stream
{
  "message": "写一版新产品发布会的开场文案",
  "skill_slug": "copywriting",
  "session_id": "session-002",
  "user_id": "default"
}
```

### 5.5 代码与前端

```text
用户：这个页面的按钮点不动，帮我看看。
路由：supervisor → worker_coder 或 worker_frontend
      → filesystem 读代码 / playwright 打开页面核对
      → 写文件前审批 → worker_yue_chat
```

## 6. 管理与运维

### 6.1 管理入口

| 功能 | 地址 |
|---|---|
| 员工管理 | `/admin/roles` |
| 工具管理 | `/admin/tools` |
| 技能管理 | `/admin/skills` |
| 厂商管理 | `/admin/providers` |
| 会话管理 | `/admin/sessions`、`/admin/sessions/{session_id}` |
| 调试对话 | `/admin/playground` |

管理后台使用管理员 Cookie 登录；删除类操作只在这里提供。

### 6.2 工具接口

| 操作 | 接口 |
|---|---|
| 新建工具 | `POST /api/tools` |
| 工具列表 / 详情 | `GET /api/tools`、`GET /api/tools/{id}` |
| 修改 / 启停 | `PATCH /api/tools/{id}`、`PATCH /api/tools/{id}/enabled` |
| 重新拉取工具清单 | `POST /api/tools/{id}/refresh` |
| 查看员工挂载 | `GET /api/agent_roles/{id}/tools` |
| 覆盖式挂载 | `PUT /api/agent_roles/{id}/tools` |

`PUT /api/agent_roles/{id}/tools` 请求体：

```json
{
  "tools": [
    {"tool_id": "工具 ID", "tool_names": null},
    {"tool_id": "另一个工具 ID", "tool_names": ["excel_excel_read_sheet"]}
  ]
}
```

- `tool_names` 为 `null` 或不传：该配置下全部工具。
- `tool_names` 为 `[]`：一个工具都不给。
- 列表里没有的旧挂载会被清除（覆盖式更新）。

### 6.3 变更后的生效方式

- 通过 API 修改工具、挂载、厂商、员工启用状态时，后端会调用 `reset_graph()`，下一次对话重新构图。
- 直接改数据库不会触发重载，需要重启服务或调用一次相关管理操作。
- 重启会终止正在运行的 MCP 子进程；下一轮对话会按需重新拉起。

### 6.4 首次请求较慢

图构建时会并行启动所有被员工挂载的本地 MCP 服务（当前 11 个配置）。首次对话通常需要十几秒，之后使用进程内缓存。

### 6.5 常见问题

| 现象 | 处理 |
|---|---|
| 工具清单为空 | 检查 `npx` / `uvx` / `uv` 是否在 PATH，然后调用 `POST /api/tools/{id}/refresh` |
| 工具拉取超时 | MCP 服务首次下载依赖会较慢；确认网络后重试 |
| 首次对话卡住 | 等待 MCP 启动；查看服务端日志中的 `MCP 已加载` 行 |
| 审批后没有继续 | 确认 `run_id`、`interrupt_id` 正确，且 `workdir`、`skill_slug`、`user_id` 与发起时一致 |
| 8000 端口被占用 | 结束监听 8000 的进程后重新启动 `main.py` |
| 技能内容没更新 | 修改 `skills/` 文件后需要在后台重新导入，技能正文以数据库为准 |

## 7. 安全边界

- `filesystem` 工具只允许访问 `C:/Users/tzy88/Desktop/Yue Agent`。
- 写文件、改文件、建目录、移动文件、写 Excel、下载论文、上传文件默认需要人工审批。
- 公开接口不返回 MCP 原始配置，避免暴露密钥、令牌和本地路径。
- 工具、员工、技能、厂商的删除仅限管理后台。
- 员工提示词要求不读取 `.env`、密钥、令牌，不把这些内容写进回复。
- 记忆保存时不要写入密码、密钥、令牌或他人的私人数据。
