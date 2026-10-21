---
name: Excel 业务分析报告
description: 面向运营、销售、产品及业务负责人，将一张结构清晰的 Excel／CSV 自动转化为有结论、有依据、有行动建议的业务分析报告，并按需生成可编辑 PPT。适合经营分析、运营分析、销售分析、周报、月报和阶段复盘；提供 10 万行公开模拟案例与首次使用教程。AI 会围绕汇报目标寻找重要变化和风险，核查关键数字，把零散发现串成汇报主线，并根据实际数据匹配图表，最后给出可验证的行动建议。 【完整案例】：https://majichuan.github.io/sheet-to-report/
---

# 数据分析&汇报小助手

**把一张业务表，变成有依据、讲得清、能行动的经营简报。**

面向运营、销售、产品及业务负责人。提供一张结构清晰的 Excel／CSV 和汇报目标，由 AI 检查口径、寻找重点、补查依据、组织结论和行动建议；先生成可离线阅读的 HTML，按需继续制作可编辑标准 PPT，并可选择使用 SlideViber 美化。

## 30 秒了解

- **适合谁：** 需要做周报、月报、活动复盘或阶段经营汇报的运营、销售、产品及业务负责人。
- **准备什么：** 一张结构清晰的 Excel／CSV、汇报对象，以及希望解决的问题。
- **能得到什么：** 一份可离线阅读的 HTML 分析简报；按需生成可编辑标准 PPT；还可选择单独安装 SlideViber 继续制作美化版。
- **怎样配合：** 你负责提供数据和业务目标、确认必要口径；AI 负责检查、分析、组织结论和生成报告。
- **实际效果：** [在线查看完整合成案例](https://majichuan.github.io/sheet-to-report/)，包括 HTML、标准 PPT 与 SlideViber 美化版的同源对照。

**第一次试用？[跟着示例做一次](https://majichuan.github.io/sheet-to-report/guide.html)**：下载完全合成的10万行练习表，选择“直接分析”或“先确认方案”，照着步骤得到 HTML；需要汇报时再继续制作 PPT。

## 为什么选择 sheet-to-report

**帮你看懂业务变化，串起汇报主线，也把下一步讲清楚。**

- **抓住值得关注的问题——找问题**

  围绕你的汇报目标，从表中寻找重要变化、机会和风险。发现异常后，在数据支持的范围内继续按时间、渠道、人群或商品细分核查，并选择合适的图表说明。
- **结论有依据，判断有边界——核依据**

  先核对指标含义和比较范围，再组织结论。关键数字可以追溯到计算依据；数据不足时说明哪些还无法判断，避免把猜测当成事实。
- **把零散发现串成清楚的汇报主线——串主线**

  将整体表现、关键变化、细分证据和经营含义逐层展开，让读者顺着“发生了什么—哪些因素值得关注—依据是什么—下一步怎么做”理解整份报告。图表与文字前后呼应，汇报时更容易让听众跟上。
- **建议具体到行动和验证——落行动**

  说明针对哪个业务环节、建议怎么做、观察什么指标，以及什么情况下需要调整，帮助你把分析结果转成下一步工作安排。
- **一份分析，衔接阅读与汇报——出报告**

  按需生成离线 HTML、可编辑标准 PPT，并可另行安装 SlideViber 进一步美化。三类产物沿用同一套分析依据，并校验关键数字、口径与结论的一致性。

## 开始前准备

先准备三样东西：

1. 已安装本 Skill，并且能读取文件、运行本地代码的 AI 工具。
2. 一张结构清晰的 Excel 或 CSV；当前一次分析一张表。
3. 汇报对象和希望解决的问题。不确定时可以先说“请帮我判断这张表适合回答什么问题”。

HTML 需要 Python 3.10+ 和本 Skill 所列依赖；标准 PPT 还需要 Node.js 18+、python-pptx 及可用的预览工具；SlideViber 需单独安装。让 AI 先检查环境即可，无需自己编写脚本或 JSON。单纯把 Skill 上传到平台，不代表该平台已经具备运行模型、读取文件和生成产物的完整条件。

若文件含姓名、手机号、邮箱、证件号或详细地址等个人信息，先删除、脱敏或改用合成数据。脚本本身不调用外部 API；承载 AI 的平台仍可能读取你上传的文件，请同时遵循所在平台的隐私政策。

## 从 Excel 到报告

| 阶段 | AI 会做什么 | 你怎样参与 | 可见结果 |
| --- | --- | --- | --- |
| 1. 明确分析范围 | 检查文件和运行条件，识别字段与时间范围；按所选方式展示简短方案或开始分析 | 提供目标；需要时确认口径或调整方案 | 清楚知道要分析什么、是否还需补充 |
| 2. 生成 HTML 简报 | 寻找业务问题、补查证据、串联结论与行动，生成并检查 HTML | 阅读报告，可提出修改；只要 HTML 可在此结束 | 可打开的 HTML 及检查状态 |
| 3. 制作标准 PPT（可选） | 在可预览环境展示主题小样；选择后生成完整稿 | 回复“生成 PPT”，再选主题；已明确风格或授权代选则沿用 | 主题预览、整稿阅读入口、可编辑 PPTX |
| 4. 继续美化（可选） | 检查 SlideViber 依赖和编辑需求，在同源分析基础上优化版式 | 回复“制作美化版”；必要时确认编辑性取舍 | 单独保存的美化稿及其预览，标准稿保留 |

确认次数取决于数据口径、开始方式、已有偏好和运行环境。AI 不应为走流程重复询问已经确认的内容。

## 两种开始方式

### 首次推荐：先确认分析方案

适合第一次使用、希望先确认时间范围、汇报重点和关键口径的情况。明确说“先给方案，等我确认后再生成”，AI 会先用短句给出分析范围、重点问题、必要待确认项和预计交付；你确认或修改后才开始生成正式 HTML。

> 请用 sheet-to-report 分析这份 Excel，面向业务负责人做月度复盘。先检查数据，用简短的方案告诉我：建议分析哪个时间范围、重点回答哪些业务问题、有哪些需要我确认的口径。等我确认后再生成 HTML 分析简报。完成后，请告诉我如何继续制作可编辑 PPT。

周报、活动复盘等场景可替换“月度复盘”和汇报对象。你可以这样回答方案：

> 按这个方案分析。重点看渠道效率；收入使用退款后的净收入。先只生成 HTML。

这只是回答形式示例，不是所有数据的默认口径。

### 已熟悉时：直接分析

适合目标和口径已经清楚、希望尽快得到结果的情况。明确说“直接分析，只确认影响结论的问题”，AI 不再额外等待整份方案批准；日期、指标分母、业务对象粒度等真实歧义仍会询问，不能猜测。

> 请用 sheet-to-report 直接分析这份 Excel，面向业务负责人做月度复盘。先检查字段和时间范围；遇到影响结论的口径不清时再向我确认。先生成 HTML，完成后告诉我如何继续制作可编辑 PPT。

Agent 执行时先运行与目标对应的环境预检；失败时保留已经通过的产物，并按[快速帮助与故障定位](references/quick-help.md)用普通用户能理解的语言说明“卡在哪一步、影响什么、下一步做什么”。

**使用前需要了解的内容到这里结束。** 你可以上传文件，复制上面的指令开始。下面是供 AI 执行的详细规则，无需提前学习；AI 仍须完整遵守。

## 供 AI 执行的详细规则

## 开始前确认

先明确分析意图，避免把工程测试包装成业务结论：

- `business_review`：回答经营变化、结构驱动、风险与行动；正式 HTML 按有证据的业务问题组织章节，不预设页数。
- `exploration`：在已确认语义范围内探索可验证线索；证据不足的内容降级为带限制的假设。
- `engineering_regression`：只输出计算合同、数据质量与回归核验 dossier，不生成经营洞察或行动建议。

仅向用户呈现两种选择。用户未表明方式、也没有本次任务已确认的分析计划时，默认先给简短方案确认；明确要求直接分析或已有已确认方案时，不增加重复审批：

- **直接分析**：自动扫描字段与少量预览；只采用高置信语义，存在歧义时返回结构化待确认问题。
- **确认分析计划**：确认语义合同、分析问题、指标契约、受众、目标、维度、比较方式和主题后再执行。中置信字段只有在确认后才可使用，低置信字段始终需要确认。

确认分析计划时，面向用户只显示“分析范围、重点问题、必要待确认项、预计交付”四项短句；没有待确认项就明确写“无”。不要让用户填写 `analysis_intent`、JSON、脚本参数或其他内部合同。实验性分析画像等既有规则要求先确认时，即使用户说“直接分析”，也要说明原因后确认。

无论哪种模式，不能可靠判断时都要询问用户，不猜口径：

- 汇报目标、受众和 `analysis_intent`
- 周报或月报、日期字段、未完成周期策略
- 1–6 个核心指标及其单位、聚合方式、分子分母
- 0–4 个拆解维度
- 只要数据简报，还是同时需要可编辑 PPTX

先查看字段名和少量预览。可运行 `python scripts/sheet_to_report.py --inspect path/to/data.xlsx` 获取机器可读的候选字段与待确认问题。若发现姓名、手机号、邮箱、证件号、详细地址等个人信息，提示用户先删除、脱敏或改用合成数据。脚本本身不调用外部 API；运行它的 AI 平台仍可能读取用户提供的文件，应遵循所在平台的隐私政策。

## 受控混合分析链路

执行顺序固定为：

`分析意图 → 语义能力与质量决定 → 分析简报 → 候选问题图 → 确定性计算与受控补查 → 决策章节 → 行动合同 → 内容 QA → HTML/PPT`

- `analysis_profile=auto` 是默认入口。`general`、`retail_growth` 与 `transactional_commerce` 为 verified；`content_operations` 与 `project_operations` 为 experimental，必须经“确认分析计划”后在 `general` 执行层运行；unavailable 必须明确失败，不能伪装为通用分析成功。
- 交易表必须声明表粒度与订单、数量、单价等字段映射。销售域与客户域分开：缺客户 ID 的交易仍可保留在销售口径，但不得伪造匿名客户。
- 负数量、取消、退货、零价和异常价格分别记录数量、影响金额、规则与范围；任何排除都必须来自已确认的白名单规则，不能静默清洗。
- 新比率请求明确单行分母为零的处理。全量投入除以全量产出等总量比率使用 `zero_denominator_policy=include_in_totals`，保留零产出行的投入；仅汇总分母为零时不可计算。旧请求未指定时保留 `exclude_row` 兼容口径，不能把其数值当作全量成本效率。
- 分析问题只能从已确认的业务对象、字段、指标和时间覆盖中选择。确定性计算负责数字与公式，叙事层只能选择、排序和压缩证据，不得自创数字、公式、因果或行业基准。
- 高优先问题按“事实—驱动—细分—经营含义”记录 `required_depth / achieved_depth`。深度不足且仍有合法表内路径时必须继续受控补查；没有真实信息增量时降级，不能用非空文本冒充回答。
- 正文选择单位是业务章节，不是孤立指标或单条洞察。核心诊断应说明问题、判断、证据与经营含义；行动可由多个章节共同支持，背景章节无需制造行动。
- `report_model.json` 是一次生成的内容真相源，洞察、行动、图表均引用可解析的 evidence ID。新版 `html-chapters/1` 通过独立 `chapter-presentation/1` 接续标准PPT或SlideViber，不交给旧PPT消费者；旧模型只保留原兼容路径。

## 执行流程

1. 要求 Python 3.10 或更高版本。先运行环境预检：

   ```bash
   python scripts/environment_check.py --target html
   ```

   PPT阶段另运行 `python scripts/environment_check.py --target standard`；美化版改为 `--target slideviber --slideviber-dir <已单独安装的SlideViber目录>`。Node不在PATH时传 `--node <Node可执行文件>`。检查按目标区分：HTML不要求PPT/Node；标准完整稿及主题小样使用公开python-pptx与Node，不需要Codex私有工具。预检通过不代表字体、浏览器或实际视觉已验。

2. 预检提示缺少依赖时，再运行 `python -m pip install -r requirements.txt`；不要把依赖或生成文件打包进 Skill。普通安装不要求Git；版本追溯保留文件指纹，Git信息只在本Skill自身仓库可读取时补充，缺失不冒充已知版本或干净工作区。
3. 读取 [请求与报告模型](references/report-model.md)，确定意图、分析画像与语义合同。选择“直接分析”时可先执行：

   ```bash
   python scripts/sheet_to_report.py --inspect path/to/data.xlsx
   ```

4. **正式 HTML 默认由宿主 AI 驱动**。先读 [宿主 HTML 分析合同](references/html-analysis.md)，显式使用本 Skill 绝对目录。初扫 → 阅读证据并逐问题判断充分性 → 必要时受控补查 → 绑定最终快照提交故事 → compose → finalize。无需用户手写问题或提案；脚本只做确定性计算，不会独立调用模型。不允许手修最终模型或 HTML。`html-chapters/1` 与旧 PPT 页型解耦；背景无需制造行动，数字仍必须绑定证据。以下一键入口保留为旧分析/兼容用途，不代表完成新版宿主 AI 分析：

   ```bash
   python scripts/sheet_to_report.py --request path/to/request.json --output path/to/output
   ```

5. **以下为旧模型兼容入口，不接续上面的新版 HTML 流程。** 经确认的旧分析流程可分两阶段运行。`--analyse-only` 只生成确定性 `analysis_evidence.json`；`--finalize` 只接受与来源哈希、请求指纹和 evidence 严格绑定的 story plan：

   ```bash
   python scripts/sheet_to_report.py --request path/to/request.json --output path/to/output --analyse-only
   python scripts/sheet_to_report.py --output path/to/output --finalize path/to/story_plan.json
   ```

   默认 story plan 只能重排已有内容。若表内已有结构证据却缺经营判断，先由当前 AI 阅读冻结证据，按 [证据后判断提案](references/report-model.md#证据后判断提案) 提交结构化 proposals，再用 `--compose-decisions` 编译故事计划。数字、范围、深度和章节归属仍由脚本生成与校验；不得直接改 seed 或内容锁。来源不匹配、引用越权、缺少必需页面角色或内容证据不足时必须失败，不能静默生成。
6. 新版 HTML 在组织提案前读取 [共享图表规格](references/chart-spec.md)。按判断任务与数据条件选图，用 `chart-spec/1` 记录选择理由、限制、尺度和重点；新运行不能退回旧细横条合同。柱图、分布、构成、关系和贡献图各有数据约束，不按行业名或固定图型配额选择。图中分箱、比例和累计坐标只消费已计算证据；能力不足须说明原因，不能交给渲染器临时计算。检查 `report_model.json`、`report.html`、`html_qa.json` 和数据质量提示。`html-chapters/1` 必须走 `html_analysis.py finalize` 对应的检查，不能再交给只支持旧 `analysis_chapters` 的 `html_qa.py`；结构／证据通过不等于视觉通过。实际审核关键图能否支持判断，优先桌面；手机只查基础可用性。机器 QA 通过不等于实际阅读验收完成。

   HTML 完成后先给可打开的报告入口，再用普通文字报告已经完成和仍未验证的检查；用户未排除 PPT 时，说明可以回复“生成 PPT”继续。用户明确只要 HTML 时不再推荐后续产物。优先补充一条与本次汇报目标相关、已绑定证据的发现，避免只交付文件。
7. 若用户选择 PPTX，新版 HTML 先读取 [章节到演示投影](references/chapter-presentation.md)，使用独立 `chapter-presentation/1` 及对应新消费者，不把模型直接送入旧 `build_pptx.py`。按当前已验证能力执行，显式拒绝尚未支持的布局或图形条件。交付 `report.pptx` 与 `ppt_qa.json`；标准版必须先独立通过字号、边界、重叠、占位符、标题—图表证据一致性、内容锁定与中文排版门禁。
8. 生成任何 PPT 前读取 [主题选择](references/ppt-theme-selection.md)。已明确指定或已确认沿用的风格优先；用户明确说“你决定、直接生成”且无已确认偏好时，使用默认清晰商务。无偏好且未授权代选时，先推荐清晰商务，备选最多两种当前完整稿已验证的方向；每种实际导出同内容的封面＋真实图表两页 PPT 小样，并优先把真实渲染图片直接展示在聊天中。不能渲染时须在让用户选主题前说明，并让用户选择“按文字方向选择”或“明确授权使用推荐主题”；不得用网页示意图冒充真实 PPT、让用户自己寻找本地文件夹，或因超时和沉默自动代选。

   一个待选择节点只发一次清楚问题，然后停止并等待新用户输入。没有新输入时，不重复催选、重做小样或自行生成完整稿；自动续跑不构成用户确认。只列当前完整稿已经验证的主题，`editorial` 两页小样可做不代表完整稿可用。

   标准版通过后，交付完整稿阅读入口和独立可编辑 PPTX；只有入口实际可用时才写“预览完整稿”或“下载可编辑 PPT”。随后若用户尚未表态，简短说明可回复“制作美化版”通过 SlideViber 继续；同时说明它需单独安装、标准稿会保留，图表编辑方式可能不同。用户已拒绝时不重复询问。美化版继承同一已确认选择，保留标准稿、完整内容和来源校验；新版章节模型使用 [章节到演示投影](references/chapter-presentation.md) 的独立构图消费者，旧模型使用 `slideviber_handoff.md`。预览及实际 PPT 核验后另存 `report-polished.pptx`，不重复审批。
9. 美化稿在同一显示尺寸下对照标准稿，检查视觉焦点、图文对应、图表可读性及整稿节奏；只换颜色、分辨率或导出器不算美化完成。精修版导出后运行对应合同的一致性检查；缺少日期、关键数值、判断标题或 evidence 对应关系时不得交付。新版章节投影使用 `chapter_presentation_qa.py` 并传入绑定的 `--scene`；以下命令仅用于旧模型：

   ```bash
   python scripts/slideviber_consistency.py --model report_model.json --pptx report-polished.pptx --output slideviber_qa.json
   ```

## 自适应叙事与内容门禁

本节页数、旧字段与 featured 限制描述旧模型兼容行为。新版 `html-chapters/1` 以宿主 HTML 合同为准，背景可进正文、无需制造行动；主图设计与正文事实选择相互独立。

- 6–10 页只适用于证据充足的 `business_review`；页面由已选择的分析镜头和直接证据决定，不凑固定页数。证据不足返回 `needs_input / insufficient_evidence`，并保留上一版已通过产物。
- `engineering_regression` 使用明确的 QA dossier，允许少于 6 页；不得出现经营复盘、管理摘要、经营杠杆或行动路线等业务包装。
- `analysis_brief` 固化受众、目标、节奏与最小必要确认；`candidate_question_graph` 保留问题来源、初扫信号、选择／拒绝理由和字段支持。
- `analysis_lenses` 记录问题、优先级、所需对象、指标、深度缺口、补查轨迹和停止原因。未选择、不可用或深度不足的问题不得伪装成核心回答。
- `analysis_chapters` 以问题为单位组合事实、驱动、细分、经营含义、图表和行动；管理摘要只引用已入选章节。
- evidence 必须记录公式、过滤范围、样本数、受影响行数／金额、业务对象和限制；事实、诊断、推断、假设分别声明 `claim_type`、`evidence_strength` 和限制。
- 行动必须包含类型、对象、依据、解释、步骤、成功信号、止损护栏、限制、来源章节和 evidence ID；缺任一项不得进入正式输出。行动对象回答“针对谁或哪个业务环节采取措施”，必须与来源证据相连；不可用负责人替代。执行分工仅在有依据时单列“建议协同角色”，未知时省略，不编造组织安排。
- `content_validation` 阻断原始字段泄漏、数字复述、无证据因果、重复结论、套话、空槽、悬空 evidence 和未解析占位符。

## HTML 业务呈现规则

- 图表先按本页要证明的关系和数据语义选择，再核对目标输出能力；保留候选取舍理由，不以图型数量作为质量指标。HTML、标准PPT与SlideViber复用同一来源投影。十类图型的选择依据见[共享图表合同](references/chart-spec.md)，实际容量、原生图表与可编辑形状的区别见[跨格式能力](references/chapter-presentation.md#图表跨格式能力)。换数据后重新选型，不能照搬既有案例图表清单。
- HTML 只生成一套统一的标准商务样式；主题选择只作用于标准 PPT 与可选的 SlideViber 美化版，不作用于 HTML，也不因换 PPT 主题生成多份 HTML。
- 主标题是报告身份与分析主题，不得使用 Skill 产品名。`report_subtitle` 只承载周期或范围，`judgement_headline` 承载最重要判断。
- `period_overview` 展示分析期累计或整体口径；`latest_snapshot` 展示最新完整周期及实际对比周期。禁止把最新一个周期冒充整个分析期。
- HTML 正文按已选业务问题章节递进；KPI、趋势与经营杠杆只作为上下文或证明材料，不能形成孤立单指标堆叠。没有核心章节时不得把浅层模块包装为合格经营简报。
- 章节标题使用业务判断，正文明确对应问题、经营含义、证明图表、行动和边界。原始 `chapter_id / question_id / evidence_id` 只留在模型与 QA，不进入观众可见正文。
- `featured` 继续作为旧接口兼容和章节内部候选记录；最终正文选择以 `value_selection.selection_unit=analysis_chapter` 与 `analysis_chapters[].selection_status` 为准。
- 新版 HTML 可用 supporting 表达必要背景，但不能把浅排名包装为强诊断。旧模型的 supporting 附录规则只用于旧接口兼容。管理摘要不能用普通 KPI 事实挤掉有证据的诊断。
- 采用证据优先规则：现有字段能够回答的问题必须完成趋势、结构或交叉分析；只有确实缺少字段、周期或业务事件证据时，才准确说明无法验证。
- 核心结论逐条采用“简短判断标题＋解释与证据”：标题由宿主根据正文和所引章节概括，HTML加粗，PPT复用为同条判断的标题；不能只写分类标签或机械截取首句，不能遗漏关键范围、比较条件与不确定性。正文保留证据和边界，详见宿主HTML合同。
- PPT按“核心判断→整体概况→判断依据→行动安排→口径附录”组织，保留分析期基本盘；通过独立演示编排把图表标题、结论编号和各页用途连起来。正文眉题说明对应哪项结论或属于全局背景，行动区区分执行、验证与边界，页码提供整体进度。标准版与美化版复用同一映射，不能只按字数机械切页；见[章节到演示投影](references/chapter-presentation.md)。
- 设计表达根据本页已有内容关系选择构图，不能用大小、顺序或颜色制造未经支持的优先级与因果；图表重点须绑定图中类别及本页判断，强调区不能只重复原读数。美化可将正文无损分段或呈现有原文依据的步骤，必须逐字拼回且全段可见，不转移到备注；主指标需声明与汇报目的有关的理由。长内容或密集图回退到可读布局，SVG预览与最终PPT重导入都要核验，不缩字、不溢出、不丢信息。新正式任务由宿主按当前数据提供`presentation-visual/2`，不得复用旧案例编排；主指标、短标注和步骤关系按证据选用，无依据保留同级或并列。字段规则与内部设计评审入口见[有来源的设计表达](references/chapter-presentation.md#有来源的设计表达)；内部小样不改变普通用户的主题选择流程。
- 强制“摘要—章节—行动闭环”：每条摘要判断引用已选章节；正式行动引用来源章节并按最终筛选结果连续编号，再同步回管理摘要。
- 同比同时写明实际最新周期与实际同比周期；子集与整体同页时明确范围，必要时给出同期全渠道基准。
- “贡献最高”等结构判断必须继续调用可用的成本、质量、转化或效率证据完成交叉分析。
- evidence ID、来源哈希、原始字段名与渲染提示不进入观众页面，但完整保留在模型、交接和 QA 中。

## 标准 PPT 规则

- 页面从九类候选构图中按证据选择：封面、管理摘要、KPI、趋势、结构、经营杠杆、机会风险、行动路线、数据与口径。缺证据的可选页必须消失。
- `visual_spec.eyebrow` 使用中文功能眉题；`tone`、`density`、`focus_evidence_ids`、`display_claim`、可选比较口径和图表焦点控制视觉表达。无法可靠确定时留空，不得猜测。
- 主题入口为 clean、corporate、editorial、warm，配置与适用路径见主题选择参考。旧PPT布局只支持前三个旧ID clean/corporate/warm，不将editorial静默降级为换色。正文对比度不低于4.5:1，大字和装饰性元信息不低于3:1。
- 趋势和结构优先使用原生可编辑图表；每页只保留一个视觉焦点，内容超容量时精简、换低密度布局、拆页或失败，不缩小字号硬塞。
- 所有中文运行使用 `lang=zh-CN`，段落启用东亚换行与悬挂标点；PPT QA 必须检查孤立标点、字号、边界、重叠、对比度、布局角色、视觉焦点、密度和重复口径。
- SlideViber 是可选精修层，不是标准版依赖。它只能提升视觉表现，不得改变页 ID、日期、数字、指标口径、结论或行动含义。

## 快速体验与公开样例

公开体验只使用内置脚本自生成模拟数据，不冒充真实企业数据：

```bash
python scripts/generate_sample.py --output-dir generated
```

生成后，把 `generated/synthetic-business.xlsx` 交给当前 Agent，并说：

> 请用 sheet-to-report 直接分析这份模拟业务表，先生成 HTML；如果继续生成 PPT，请按主题选择流程执行。

生成约 10 万行、18 个月、带已知业务信号的正式体验案例：

```bash
python scripts/generate_sample.py --output-dir main-case --main-case --rows 100000 --write-xlsx
```

生成后，把 `main-case/retail-omnichannel-main.xlsx` 交给当前 Agent；分析仍按本 Skill 的宿主 AI 链路执行，不把旧兼容命令当成新版完整分析。

## 边界

- v0.2 只支持一张结构清晰的数据表；可用 `sheet_name` 选择工作表。多 Sheet 联合、多层表头和合并单元格进入后续版本。
- 先完成表内可验证的趋势、结构和交叉分析；只有确实缺字段、周期或业务事件证据时，才请求补充数据或口径。
- 支持 `sum`、`ratio`、`average`、`last`。比率必须声明分子、分母与 `scale`；余额取期末值。
- 默认 `Asia/Shanghai`、周一为周起点、排除未完成周期并提示；只接受 `weekly` 或 `monthly`。
- HTML固定为一套标准商务样式；PPT四方向共享选择记录，主题不改变内容或分析结论；新版完整链路及实际已验主题以章节演示合同为准。公司母版或原生数据编辑要求不可因选主题而降级。
- 示例仅用于体验和说明；每次以用户当前输入与问题重新分析，不绑定任何内置数据或预设结论。
- 未获得单独发布授权时，不打包、上传、推送或更新公开站点。
- 输出是描述性分析、证据受控的诊断与复核建议，不用于医疗、投资、人事评价、授信等高风险决策。
- 任何高层级结论都要保留数据范围、缺失、重复、过滤、字段口径、证据强度与限制。

---

## 参考资料：references/chapter-presentation.md

# 新版章节报告的演示侧投影

源 `html-chapters/1` 的 `ppt_supported:false` 表示不能直接交给旧 PPT 消费者。新入口生成独立 `chapter-presentation/1`，不改源模型封印、不补写旧 slide_plan，也不重新读取原始表。旧标准与旧 SlideViber 入口继续使用旧模型。

## 输入与依赖

使用已完成宿主分析并 finalize 的 `report_model.json`，按照 [主题选择](ppt-theme-selection.md) 取得绑定该模型的 ready 选择。当前完整章节消费者支持 clean/corporate/warm；editorial 整稿未验证，明确拒绝，不能用两页小样通过代替整稿支持。未选择不得生成。

标准消费者使用Node.js 18+编排场景、Python 3.10+和公开python-pptx 1.0+导出。`RUNTIME_PYTHON`可指定Python，否则Windows使用python、其他系统使用python3；不读取RUNTIME_NODE_MODULES或PRESENTATIONS_SKILL_DIR，也不依赖Codex私有包。标准执行前运行 `python scripts/environment_check.py --target standard`，Node不在PATH时传 `--node PATH`。主题两页小样沿用同一公开写入层。

SlideViber场景作者只需Python基础分析依赖与Node；实际PPT导出须单独获取SlideViber和它声明的公开依赖。运行 `python scripts/environment_check.py --target slideviber --slideviber-dir PATH` 检查模块与入口；字体、浏览器启动与视觉效果仍需实际验证。标准稿不要求安装SlideViber。不要复制宿主私有运行库或把本机绝对路径写入Skill。

## 执行

1. 宿主先形成独立 `presentation-story/1` 演示编排，绑定 `source_model_sha256`。`themes` 按摘要原顺序逐条提供 `{summary_index:0,title:"短主线名称"}`；`chart_titles` 为每个已选 chart ID 提供判断标题片段数组。逐图核对标题是否由图内指标、范围和比较条件直接支撑，数字只能引用该图的 evidence cell。不能把章结论中未画出的指标当图表标题，也不能制造因果；证据不足时用准确的中性概括。运行 `python scripts/chapter_presentation.py --model report_model.json --selection selection.json --story presentation-story.json --output presentation.json`。完整保留摘要、整体概况、章节正文／含义／限制、所有选中图表、行动和口径，不改冻结分析。
2. `node scripts/chapter_deck.mjs report_model.json selection.json presentation.json NEW_BUILD_DIR full presentation-story.json`。作者重新验证投影与源模型、主题及独立编排的完整相等关系。只消费冻结图表投影，标准版产生 draft.pptx，SlideViber 产生 theme.json 和 slides/*.svg，两种输出各用独立选择与新目录。`scene-only` 和 `design-sample:1,N` 模式第六参数同样传编排文件。旧调用允许不提供编排作兼容，不代表完成了宿主的演示判断审查。

   正文固定具备轻量眉题（对应结论＋本页用途）、阶段指引和页码/总页数。整体概况位于摘要之后、细分分析之前，读取 overview 全部公开指标及原单位，不以最新月替代整体；超过容量续页，不能静默删除指标。摘要连续编号，章节/图表通过真实 chapter_ids 对应摘要，共享依据标记多项结论，无匹配标记补充背景。行动按执行安排、验证与边界分组，口径按数据范围、指标定义、分母处理分组；各组内部容量拆页保持文字完整。不展示内部证据ID，也不为满足模板强造结论联系。

   最终运行 `chapter_presentation_qa.py` 时同样传 `--story presentation-story.json`，从独立输入重新验证映射、概况及可见眉题；随后实际查看最终PPT，核对图表标题、结论对应关系、阅读顺序与长文本。机器封印和字段检查不能替代语义与视觉验收。
3. 标准作者通过 `chapter_pptx_export.py` 再核对源模型/主题/投影与场景，输出draft.pptx、draft.qa.json和来源回执；包含中文字体脚本及换行声明，不再需要宿主私有最终化工具。核对来源/几何/原生图表数据与嵌入工作簿后，用当前可用的PowerPoint、WPS或其他实际PPT渲染器查看完整稿，再另存正式文件。没有可用的实际渲染能力时保留待验状态，不用SVG示意或出文件成功代替。新原生图表工作簿只作为冻结数值快照，不冒充原表公式。SlideViber 先实际 preview 检查 SVG，再调用其 export；若导出未声明中文字体，使用 `python scripts/chapter_pptx_prepare.py --input draft.pptx --output font-ready.pptx --font SELECTED_FONT` 补全所选字体的文字脚本声明，然后最终化。此步骤只处理候选字体，不改文本、图形坐标或数值。作者使用实际1920×1080坐标，避免转换器对文字与图形的祖先缩放处理不一致。
4. `python scripts/chapter_presentation_qa.py --model report_model.json --selection selection.json --projection presentation.json --pptx FINAL.pptx --output NEW_QA.json`。核对完整文本、系列名称、类别顺序、原生图表数值／数值横坐标。两种目标都应增加 `--scene NEW_BUILD_DIR/scene.json`；SlideViber缺少scene必须失败。核对文字和图形的最终几何及来源值；没有场景不能通过。该脚本通过不等于视觉通过，必须实看最终页。
5. 交付实际文件、编辑能力和残余限制，遵守当前任务的人工作品验收门禁，不把内部通过自动写成用户认可。小样优先交付由受测PPTX真实渲染的图片；完整稿同时提供逐页阅读入口和独立可编辑PPTX。只有链接在当前宿主实际可打开时才标为“预览完整稿”或“下载可编辑PPT”。
6. 标准稿完成后，若用户未拒绝美化，用普通文字说明可回复“制作美化版”继续，并明确SlideViber需单独安装、标准稿会保留、图表编辑方式可能与标准版不同。美化是可选视觉优化，不得暗示标准稿不合格；用户已拒绝时不重复提示。

## 能力边界与失败

真实预览依赖宿主可调用的PPT渲染能力。若受测PPTX无法导入当前渲染器或宿主不能展示图片，保留源PPTX并在主题选择前说明：用户可以按文字方向选择，或明确授权使用推荐的清晰商务。不得静默使用默认主题，也不得把失败渲染器产生的空白页、SVG源文件或重新绘制的网页示意当成PPT预览。该降级不代表预览体验验收通过。

### 有来源的设计表达

新任务的正式标准稿与美化稿均由宿主在独立`presentation-story/1`中提供`visual: {version:"presentation-visual/2", chart_focus:{}}`，按当前数据逐页选择下述设计意图；空的重点映射表示未发现应单独强调的类别，仍启用通用层级与容量适配。历史无visual或`presentation-visual/1`输入只保留兼容，不作为新任务省略设计步骤的理由。用户无需填写这些技术字段，也不增加审批。

每图最多两个不同重点类别，必须出现在真实图表类别及该页判断标题中；无匹配则拒绝，不能用未画出的指标作重点。数字和标签从已冻结图表投影读取，保持系列/颜色/比例和全部其他类别可读；重点只是对应当前标题，不是重要性排名，也不新增因果。

摘要默认同级判断；整体指标无宿主依据时保持同级，不由数值大小或字段排列推断重要性。`presentation-visual/1`继续兼容；新任务使用`presentation-visual/2`，其中以下字段均可选：

- `overview_focus:{metric,rationale}`：引用overview中的公开指标键，说明与汇报目的的关系。宿主审查理由是否合理，代码只验证引用和声明完整，不能把格式检查当作主次已获业务证明。重点区域不编码不同单位之间的面积比例，其余指标与全部单位保持可见。
- `chart_annotations:{chart_id:{类别:短标注}}`：类别必须已在`chart_focus`，短标注逐字来自该页判断标题。当前最多四类别的column/grouped开放就近短标注，其他图型或密集图明确拒绝该声明，可不加标注使用宽幅。只做就近解释，不重复抄一组完整金额占据强调区；图型、系列、其他类别、原始数值及范围不变。
- `action_layouts:{action_owner:{relation,parts,basis}}`：owner是投影的`action-N`，relation为`sequence`或`parallel`；parts包含2至4段`{label,text}`，label逐字来自该段，所有text必须按原顺序逐字拼回action.steps。basis逐字引用原行动标题或步骤，sequence还须有明确先后表达，宿主仍需核验关系；无先后依据使用parallel，不制造时间或因果。原文若已跨容量拆页则保持原完整分页，不漏掉续页。

美化版由独立`chapter_slideviber_design.mjs`按有来源的意图、信息关系和可用容量构图；标准版沿用克制的表达。完整不等于保留大段落形态，但全部事实、正文、数字、单位、限定和停止条件必须可见。场景记录源块与分段；最终QA逐段核对可见内容并验证拼回原文，不将内容放备注或隐藏对象充数。窄栏同时预留实际PPT文本框内边距，SVG预览通过后仍须检查最终PPT重导入的换行和边界。容量不足回退宽幅、并列或原分组，仍放不下明确失败，不缩字或删除。

标准版采用克制的层级与指标台账；图表增强统一取消无信息增量的重复读数侧栏。SlideViber可呈现同级判断、声明的主指标、宽幅图内标注、原文步骤关系与验证对照。强调色依据所选主题派生满足可读对比度的文字色，不改变图表系列语义。没有视觉编排的旧调用保持原布局。是否通过全稿、其他主题或其他宿主的实际验收，以相应证据为准。

更换数据时重新读取其冻结分析与汇报目标，再选择主指标、重点类别和行动关系；不得复用案例名称、固定页码、金额或旧案例的编排JSON。没有主次依据就保留同级指标，未明确先后就保留并列行动；不能为追求丰富而强填字段。逐项检查源正文、图表、限定和行动跨页完整，再检查最终PPT的实际换行与整稿节奏。若未命中特殊布局，应说明容量回退原因并查看回退结果；无法完整呈现或图型未受支持时明确失败，不把旧版式或删减稿宣称为已达到当前设计标准。

内部设计评审使用`design-review:page-002,page-003,...`，页ID来自完整已封印投影、保持源顺序且不重复；QA传`--review-pages`同样的页ID集合并传独立`--story`和`--scene`。scene标记`design-review`，禁止当作完整稿验收。主题选择原来的`design-sample:封面,图表`不变；此内部评审入口不为终端用户增加五页审批流程。正式稿仍用`full`，最终PPT重导入渲染后评估重点、对应关系和全稿节奏。

### 独立美化构图与小样门禁

SlideViber 目标默认由 `chapter_slideviber_layout.mjs` 生成独立构图，标准目标保持标准版式；两者共用冻结内容、图表语义与所选配色。scene 记录 `slideviber-composition/2` 和逐页构图角色。需要两页真实小样时使用显式模式 `design-sample:封面源页码,图表源页码`（页码从1开始），从完整投影取页，采用与整稿相同的构图函数。不能把两页输出当作完整稿验收。

- 封面强化标题层级，将末尾括号说明单独排版，保留全文。少量类别且文字容量允许的图表页采用判断与证据左右并置；侧栏只选取同章节、共享证据且至少提及两个实际绘制数值的已有段落，记录具体源块索引。这是相关段落筛选，不能替代宿主检查指标、范围和结论是否匹配；无合适段落或密集图表保留宽幅。
- 摘要使用编号判断；章节突出主证据并区分经营含义与适用边界；行动区分依据／执行与验证／边界；口径采用平直的条目或单项定义。按页型和实际内容容量选择布局，保留所有源段落。超容量明确报错，不缩字或丢内容；不把所有行业强行塞进一套案例文案。
- 同主题允许不同构图，但不得换图型、改分母、伪造关键数或挤压证据。小样由实际 PPTX 最终重导入图展示，不以 SVG 网页冒充最终结果。网格与分隔线以细矩形输出并核对，避免零尺寸线段在导入时丢失。
- 小样 QA 显式增加 `--sample-pages 封面页码,图表页码 --scene scene.json`；默认 QA 仍要求整稿，侧栏正文也须核对源投影。
- 已覆盖封面、摘要、章节、图表、行动和口径页型；实际验收范围以项目记录为准。美化稿沿用已确认的视觉方向，除用户指定的校准或验收节点外，不为每次导出追加审批。

验收美化价值时，在同一显示尺寸比较：是否更快识别要点、判断与证据是否更容易对应、图表是否仍可读、整稿是否有合适的页面变化。换导出器、分辨率、颜色或图表对象类型不构成美化通过证据。完整导出与视觉核验通过后才按本次授权同步运行代码，旧成品另存保留；技术核验不代替用户最终验收。

- 正文主要数字、范围、对象顺序与图表坐标不可被主题改变。不能修改 presentation.json 后重新算个哈希冒充来源相同；校验器会对源模型重新投影比较。

## 图表跨格式能力

十类仍须先通过chart-spec/1。下面是新版章节作者的能力，旧PPT入口、其他主题及原生PowerPoint/WPS不能自动继承此验收。六种新增图以清晰商务的中性完整稿验证；中性样本只证明工程路径，不能作为业务结论。

| 图型 | 标准PPT | SlideViber | 当前单图对象上限与条件 |
| --- | --- | --- | --- |
| line | 原生折线或按真实时间/数值轴的XY连线 | 可编辑矢量线与点 | 18；缺失须另行支持分段，不填零 |
| bar / column / grouped | 原生条/柱/分组柱 | 可编辑矩形 | 18；保留正负坐标和零轴 |
| paired | 两幅独立标尺的原生条形 | 两面板矢量条形 | 8；同序分类对象；时间双面板尚未开放 |
| stacked | 原生堆叠柱 | 按共享bases/ends绘制 | 12；合法完整分量，总高度按总和确定 |
| donut | 原生环图及独立可编辑标签 | 可编辑扇区形状及标签 | 2–6；完整百分比，零值仍列出 |
| scatter | 原生XY点图 | 可编辑点与对象编号 | 至多8且受标签空间限制；相同坐标不抖动，编号合并指向完整对象表；过密明确失败 |
| waterfall | 可编辑矩形与连接线 | 可编辑矢量 | 12；起终点与正负分量已由计算端对账 |
| histogram | 零间距原生柱形表示既有等宽箱 | 连续等宽矢量矩形 | 20；计算端已分箱，不是自动分箱图表 |

上限是拒绝阈值，不是任意长标签均可读的保证；实际空间不足时受控聚合、拆页或失败，不缩字、截字、删对象。散点对象键列出编号及源x/y，便于识别点；不同单位对读分别注明单位与标尺。标准瀑布与全部美化图是形状编辑，不能宣称能编辑原生数据表；用户要求原生数据编辑时明确区分并按其要求处理。

最终QA从源投影核对原生图型、系列、缓存数值、坐标域、堆叠总高、零箱间隙，以及矢量柱、点、累计连接线和环图扇区顶点；再检查实际PPT重导入图与完整阅读路径。渲染成功或几何通过不代替可读性核验。
- HTML 仍是一套商务样式；PPT 主题只决定演示外观。针对案例的叙事在宿主提案，不进通用作者。

---

## 参考资料：references/chart-spec.md

---
updated: 2026-09-09
version: chart-spec/1
---

# 共享图表合同 chart-spec/1

本合同提供共享图表设计。旧无 version 合同仍由旧模块显式处理；新合同失败不得降级成旧横条。`scripts/chart_contract.py` 的 `validate_chart(chart, record)` 抛出 ValueError 阻断非法组合；`project_chart(chart, record)` 返回与屏幕无关的确定性投影。HTML与新版章节PPT消费同一投影；各消费者的实际容量与编辑能力见[跨格式能力](chapter-presentation.md#图表跨格式能力)。

## 宿主选型

先明确本页要让观众理解的关系：趋势、对象比较、完整构成、分布、两指标关系或变化贡献。结合粒度、单位、分母、完整性、负值、缺失及长尾比较适用候选，再检查输出能力。`task/reason/constraints`保留选择依据；不能因PPT入口尚不支持某图，就把现有柱形说成业务最优。没有需要时保留清楚的原图，不设置图型数量配额，也不将不同分母的占比堆叠成一个总体。

能力不足时：只有仍能表达同一主要关系且不丢对象、数值、范围的替代才可使用，并说明理由；否则明确报告缺口。正式任务不得在渲染器新增占比、分箱或分解。已冻结报告仅调整图表时，可用`scripts/revise_charts.py --model 原模型 --proposal 原提案 --correction 修订.json --output 新目录`；修订为`{source_model_sha256,charts:{章节ID:[完整图表提案]}}`，只复用该章已绑定证据，重组与封印新模型，原模型和正文保持不变。宿主须另行核验候选是否更合适，代码通过不代替业务判断。

## 图表提案

必需字段：`version` 固定 `chart-spec/1`；`id` 稳定标识；`task` 为 trend/comparison/composition/distribution/relationship/contribution；`reason` 非空选择理由；`constraints` 字符串数组；`evidence_id`；`kind`；`x`、`y` 列 key；`title` 非空现有文本片段数组；`limit` 为 1–500 整数。

kind：line/bar/column/grouped/paired/stacked/donut/scatter/waterfall/histogram。可选字段只有：`series`（grouped/stacked 的 2–6 个列 key，首项必须是 y）、`y2`（仅 paired）、`x_scale`（category/time/linear）、`order`（source/descending/absolute）、`emphasis`（primary/supporting）、`highlight`（已有对象标签字符串数组）、`label`（仅 scatter 的对象标识列）。新值或多余字段均拒绝。允许任务与图型的合理重叠；理由不能替代数值与语义校验。

默认 x_scale：scatter 为 linear，其余 category；默认 order：line/waterfall/histogram/scatter 为 source，其余 descending。time 或 linear 必须 source。累计曲线采用 line + linear。柱/条/构成/瀑布图必须保留零起点；投影以 axes.zero_baseline 声明，消费者不得擅自截轴。可读对象上限为 bar/paired 30、column/grouped/stacked/waterfall 24、donut 6、histogram 40、line/scatter 500；超出需明确截取（若允许）或计算合适的聚合证据。

## 计算端证据语义

证据仍包含 `columns`、`rows`、`scope`，由原证据快照和哈希绑定，宿主提案不得提供以下语义。`chart_semantics` 必须由受控计算构造，不能从任意宿主布尔标记推导事实。

- `partition={mutually_exclusive:true,complete:true}`：跨行构成，仅供 donut。y 必须是已计算百分比，列 unit 为 `%`，有非空 denominator 标识；全部行非负、合计 100，2–6 类，全部展示。
- `series_partition={mutually_exclusive:true,complete:true}`：同一行内跨 series 构成，供 stacked；每列 additive=true、单位一致；百分比时列 denominator 一致且每行合计100。普通 grouped 只要求单位一致；百分比指标可以各自使用明确的不同 denominator，但必须在投影保留分母供消费者说明。
- `time={frequency:'day'|'week'|'month',expected_values:[完整有序 ISO 日期或 YYYY-MM]}`：时间域由计算端生成，必须是连续周期。实际行顺序严格递增、不可超域；缺期投影为 null 与 gap_indices，不补零、不无提示连线。
- `cumulative={x_key,y_key,total:100,order:'descending'}`：x 是已计算的实体累计百分比，严格递增、0–100、终点100；y 有限且终点100。负值、下降和超过100保留，并投影 signed_cumulative 与警示；不得强制裁剪为漂亮曲线。
- `histogram={lower_key,upper_key,count_key,sample_count}`：行提供已计算箱边界和人数/对象数，x 是箱标签，y 必须 count_key。连续等宽不重叠边界，计数为非负整数、合计 sample_count；最后一箱闭右侧，其他左闭右开。不等宽需要另行计算密度证据，本版本拒绝直接以计数作高度。分箱与实体聚合只能发生在计算端。
- `waterfall={role_key,base_key,end_key}`：行 role 为 start/delta/end，首尾为 start/end，中间为 delta。y 是已算金额，base/end 是已算图形坐标。start/end 均 base=0、end=y；每个 delta 的 base=前一行 end，end=base+y；终点 y=前一行 end。y 列必须 additive=true。图形不重新计算新业务量。

任何被 limit 隐藏的行仍校验缺失、非有限数、对象重复等。line/donut/stacked/waterfall/histogram 禁止裁尾；排名和散点允许显式截取，并投影 shown/source/omitted 和尾部说明。scatter 仅允许 source 截取，不宣称随机抽样或完整总体。

## 投影接口

统一字段：version/id/task/kind/title/reason/constraints/evidence_id/scope；labels（展示字符串）、x_values（category 字符串、linear 原数值、time Unix UTC 毫秒）；series（key/label/unit/values，如有 denominator 同时保留）；source_count/shown_count/omitted_count/truncated/tail_note；order/emphasis/highlight；axes={x:{key,label,unit,scale},y:{independent:boolean},zero_baseline:boolean}。

可选字段：time 提供 gap_indices；累计曲线提供 signed_cumulative/warnings；waterfall 提供 roles/bases/ends；histogram 提供 bin_lower/bin_upper；scatter label 用于 labels，x_values 始终为数值。highlight_indices 传递重点对象的展示位置；stacked 的 series[].bases/ends 仅是已有分量的几何位置。贡献任务的全部图型要求可加总并禁止截尾。投影不生成 SVG、不读取原表、不计算比例、分箱或新聚合，不改变输入对象。

---

## 参考资料：references/html-analysis.md

# 宿主驱动的 HTML 分析合同

当前章节合同 `html-chapters/1`；新运行图表合同 `chart-spec/1`。本文件负责HTML阶段；已完成模型通过[章节演示投影](chapter-presentation.md)接续PPT，不能直接调用旧PPT消费者。

## 必须按顺序执行

1. 先读本文件、`report-model.md` 和 [共享图表规格](chart-spec.md)。显式使用已确认版本的 Skill 绝对根目录，核对安装版或待验版的真实文件清单；不误用旧版。本地初扫记录根目录和既定 Skill/参考文件/Python脚本清单的文件哈希。Git仅为可选开发元数据：本Skill自身仓库可读取时记录Commit与已跟踪改动，否则二者为null并记录不可用原因，不要求普通用户安装Git。文件读取或指纹失败仍阻断；补查及最终化仍禁止混用不同文件版本。更新Skill后不得续算旧运行或手改旧快照指纹，已完成模型可按既有来源合同继续用于PPT。
2. 使用已确认请求，`output_mode=report`，输出为新目录。运行 `python <绝对根>/scripts/sheet_to_report.py --html-analysis --analyse-only --request <请求> --output <新运行目录>`。此路径仅计算基本盘、周期和主要对象分布，不调用旧自动补查，不写正式故事。
3. 阅读 `snapshot-000.json` 的证据目录、小聚合、口径与能力。针对重点问题记录已有证据是否充分；有可回答的真实缺口时提交批次。不得用既有示例结论或预设答案替代当前输入的证据分析。
4. `--html-analysis --followup <批次.json> --output <同一目录>`。批次含 `run_id/snapshot_version/snapshot_sha256`（从当前快照取得）、`batch_id`、`paths`。每条路径包含 `question_id/decision_use/gap/basis_evidence/operation/metrics/dimension`；可选 `periods` 与 `filters:[{field,values}]`。当前算子 `period_breakdown` 按已确认维度和周期对读指标。基础维度总计没有提供联合期间拆解时，这是一条真实新信息路径。
5. 阅读新快照后修正或停止。新批次占一轮；最多四轮、总十二路径、同计算问题族三路径。问题改名、改期或改筛选不重置问题族预算。拒绝/重复不扣路径但占轮，失败计算扣路径；同批次原样重放不重新计数。源变化需显式新运行及原因，不能借新运行绕过预算。中断预留文件阻止未核实重算。
6. 基于最终快照提交故事；`--html-analysis --compose-decisions <提案.json> --output <运行>`。提案含三个绑定字段以及 `title/summary/chapters/actions/sufficiency`。`title` 和所有文案使用片段数组：普通字符串不能包含游离阿拉伯数字；需要数字/对象/日期时引用 `{evidence_id,row,column}`。引用由程序解析并携带单位，不能修改计算值。
7. 章节含 `id/role/claim_type/title/body/meaning/limitations/evidence_ids/charts`，可选 `nav_title` 使用一至十二字符的业务短名片段数组。role 可为 background/diagnostic/supporting；claim_type 可为 fact/structural/hypothesis。背景无需行动。图表含 `evidence_id/kind/x/y/title/limit`（limit不超过24），kind 支持 line/bar/paired/contribution。可选 `order=source/descending/absolute`、`emphasis=primary/supporting`；paired 额外指定 `y2`，同一对象同序显示两指标，各用独立标尺和单位。contribution 使用全部证据行显示首要拉动对象、其余对象合计与全体净变动，limit 不裁掉尾部抵减；仅用于可加总的金额/数量变化，禁止对去重人数、单均和比例求和。不接受自行提供图数据。summary 项含 `chapter_ids/headline/text`；action 项含 `chapter_ids/title/target/basis/steps/success_signal/boundary`。`sufficiency` 每项含 `question/evidence_ids/decision/reason`，decision 区分 sufficient/followed_up/data_limit/implementation_gap/budget_stop。
8. `--html-analysis --finalize <生成的story文件> --output <运行>`。只读冻结证据和提案，不读原表、不补算；生成新最终目录。不编辑 report_model 或 HTML。修复计算/提案/渲染后重新生成，旧结果保留。

## 完成检查与用户交付

- `html-chapters/1` 的结构和证据检查由本流程的 `finalize` 结果及对应 `html_qa.json` 承担。只支持旧 `analysis_chapters` 的 `html_qa.py` 不得读取新版模型；入口必须明确拒绝，不能输出误导性的失败或空成功。
- 结构、内容、证据和文件封印通过后，仍要区分 `visual=passed` 与 `visual=not_verified`。未实际查看桌面、手机基础可用性和打印结果时，不得写成视觉已通过。
- HTML 完成后先提供真实可打开的报告入口，并用普通语言列明已经完成、尚未完成的检查。用户未排除 PPT 时，说明可回复“生成 PPT”继续；用户明确只要 HTML 时到此结束，不重复推荐。
- 交付说明优先包含一条与汇报目标相关且已绑定证据的发现。不得只扔出文件，也不得向用户展示内部 evidence ID、合同版本或调试堆栈。

第七步中的四类无 version 图只供旧快照兼容。新快照声明 `capabilities.chart_spec_version=chart-spec/1`，每张图必须遵循该版本规格；错误版本或非法图型组合直接失败，不静默回退。章节、摘要、行动、范围和数值插值的合同不变。

## 新版图表的宿主决策

先明确每个关键判断希望读者看到的关系：趋势、比较、构成、分布、两指标关系或变化贡献。核对证据目录中的粒度、单位、分母、负值、长尾、缺失和 `chart_semantics`，再选最适合的图；理由和约束保存于图表提案内部，不铺正文。新图必填 version/id/task/reason/constraints 及既有引用字段，具体白名单和例子以共享规格为准。图型种类和张数不作配额；必要时保留表格或准确说明缺口。

新图数据只引用快照中的计算记录。预声明的 `chart_evidence.enrich` 从已有聚合生成：各已分组对象指标的直方分布、互斥分组占比、购买频次人数占比、客户实际累计比例、客户身份销售覆盖，以及已有分解分量的起终点桥接。动态期间×对象证据在既有补查预算内产生；其已计算结果可派生完整类别系列和贡献桥接，不重新查询原表。派生记录保留公式、源记录指纹与口径；histogram 箱宽可能因长尾而不适合重点展示，宿主应检查分布实际解释力，不能只因为已生成就放进正文。

`bridge_period_components` 表示前期净销售经交易单/单均数学分量到本期净销售；`bridge_components_*` 表示从零到总增量的分量对账；`bridge_change_*` 含首要对象、其余对象合计和净变动。上述是通用计算角色而非默认故事顺序。直方图证据 `hist_dimension_*` 的样本是维度聚合后的对象，不是原表每一行；累计曲线 `customer_curve` 的横轴是实际客户人数比例，不能当等间距类别。

compose 将投影冻结为模型 `chart_views`，保留章节、快照和 scope 绑定；HTML 仅将它们映射到几何和标签。PPT已通过独立chapter-presentation投影消费相同图表语义；HTML渲染不依赖PPT导出器。正式检查以桌面为主，移动端只需基础可读与无页面横溢，不逐章精修。图形及注释不能把结构关联升级为因果。

## 审核与失败处理

每章额外声明 `scope_bindings:{evidence_id: scope的canonical_sha256}` 与 `scope_relation`。同一总体用 `same_population`，独立范围必须用 `separate_scopes` 并在文案披露分母，不能以全期/客户域/单期数值互相冒充。程序按快照核对范围指纹。补查默认复用初扫冻结周期，不能随日历自动扩大范围；补查及最终化核对 Skill/scripts/references 文件哈希，版本变化不得混进旧运行。任一未提交批次预留阻断改名重算；须先核对恢复记录。

交易表预声明基础覆盖还包括多指标月度、最新期规模/单均数学分解、地域/条目总盘、客户累计贡献与正向购买频次、质量与原表对账；这些计算在初扫前声明。期间×对象的联合变化仍为动态补查。两期补查产生对象并集变化；商品字段和数量/金额合同支持时，追加逐条目数量/单位净金额/新增退出分解。单位净金额含交易组合及调整，不宣称挂牌价或因果。费用文字线索只是候选视图，不能冒充已批准分类或清洗；费用候选继续进入全体总额。

快照指纹、运行/版本、数值引用、章节/行动来源、图表列、内容锁失败均阻止输出。背景允许无行动，诊断不能靠加动作冒充强证据。逐项审阅数值、比较范围、完整覆盖、故事与行动、桌面手机和打印；机器通过不替代宿主阅读或用户校准。需要新增算子时标记实现能力缺口，不写成数据不足。正式生成必须由宿主读证据并组织提案；单独确定性脚本不代表完成 AI 分析。

## 阅读与图表校准

- 先用一句简短判断说明每章问题，数字优先放在主图和必要依据中；不删掉改变结论的范围或限制。数字引用已带单位，不再接“位”等重复量词。
- 页面用暖白底、深灰正文、深蓝主色；青绿突出正向贡献，橙红表示负向贡献，琥珀色标示待确认事项。颜色与符号、标签并用，不靠整页浅色底或彩虹排名区分内容。
- 每章按问题选择主图，必要时以 `emphasis=primary` 突出一图；辅助图保留必要比较，避免连续同类排名充数。频次/分层对读用 source 顺序；累计贡献组相互重叠，使用有明确标签的顺序曲线，不能相加或冒充互斥分层。
- 导航使用短业务名，与正文完整判断标题分开；只保留一个锚点偏移来源。被动滚动高亮只更新选中状态，不触发页面纵向滚动。
- 收到用户对完整候选的体验校准后，可以在已审核的自有提案基础上聚合修订；必须在新证据上重新核对引用、重绑快照并记录来源。这属于同一候选修订，不得声称隔离生成。隔离验收依然只提供 Skill、原表和已确认请求。

## 行动对象与协同角色

新快照声明 action_target_version=action-target/1。每条行动的 target 必须具体描述干预的人群、渠道、商品、任务记录或流程环节；target_refs 为非空证据单元格引用数组（evidence_id/row/column），来自行动所属章节，且引用的业务对象必须出现在 target 文本。不能仅用数字、日期或负责人作为对象。

suggested_role 是可选文本片段数组，含义固定为“建议协同角色”；没有真实分工依据时省略。不能将角色建议写成已确定的责任分配。宿主还须阅读对象、证据、步骤三者是否一致：字符串匹配与黑名单不能替代语义判断。旧快照没有绑定标记时保留具体对象的兼容路径，但新 compose 也拒绝明显的负责人占位。

仅修订既有行动对象时，可使用 scripts/revise_action_targets.py --model 源模型 --proposal 原始提案 --correction 修訂提案 --output 新目录。修订提案只含 source_model_sha256 与完整 actions，且只允许变动 target/target_refs/suggested_role。程序复用原冻结快照、预算和计算版本，单列本次生成版本及来源指纹；不回读数据、不补查、不改变其他文案或图表。输出由正常 compose 与渲染器生成，不手修最终模型或文件。
## 核心结论的简短判断标题

新快照以 `capabilities.summary_headline_version=summary-headline/1` 要求每条摘要提供 `headline` 片段数组。与 `text` 使用相同的章节证据引用范围及数字解析规则，不能生成游离数值。通常用约8–22个中文字符；结构上限40字符，保留准确性所需的范围及不确定性，不为凑字数改变含义。

宿主先阅读完整正文和所引章节，再概括“哪个对象有什么变化／差异／值得注意的判断”。不要机械截取第一句、照搬某个案例、仅写“增长分析”等分类名、把结构关联加强成因果，或将试验方向写成已证明的结果。标题和正文合读应保持原结论含义；限定词需要出现在标题时不得移到正文后声称标题仍准确。结构校验无法证明语义蕴含，宿主须逐条核对。

HTML以加粗短标题开头，正文和证据链接继续保留。标准PPT与SlideViber复用同一个标题，分别调整展示层级，完整正文超容量时拆页，不隐藏或缩小硬塞。旧快照未声明能力时可兼容无标题报告，不自动猜标题。

既有冻结报告仅补充或修订摘要标题时，使用：
`python scripts/revise_summary_headlines.py --model OLD_MODEL --proposal ORIGINAL_PROPOSAL --correction CORRECTION --output NEW_DIR`。
CORRECTION仅含 `source_model_sha256` 与按原摘要顺序排列的 `headlines`（每项为片段数组）。入口验证原提案和源模型封印，只更新headline并重新compose/render；摘要正文、章节引用、行动、图表、快照及计算预算不变，保留既有行动修订记录。本次修订版本与原计算版本分别记录，不声称重新分析。

---

## 参考资料：references/ppt-theme-selection.md

# PPT 主题选择

此入口管理演示稿视觉偏好，不重新计算分析结果。旧模型PPT仍走旧校验；新版HTML模型通过独立章节演示投影生成PPT，完整主题支持范围见chapter-presentation.md。冻结模型不可为换主题而修改。

## 交互决策

- 首屏最多四方向：清晰商务 clean、沉稳管理 corporate、编辑叙事 editorial、温暖亲和 warm。目录见 `ppt-theme-directions.json`，颜色见 `themes.json`。
- 本轮明确要求优先，其次当前项目已确认偏好、标准版已确认方向。此前AI自动选择不能标成用户已确认。
- 用户明确说“你决定、直接生成”且无已确认偏好时，使用默认清晰商务；明确指定/确认沿用时，说明方向和理由后继续。
- 正常情况下若没有指定风格、也没有授权代选，第一推荐固定为清晰商务，备选最多两种当前完整稿已验证的方向；每种实际导出同内容的封面和复杂图表两页，再把真实渲染图片直接展示给用户选择。普通汇报也适用，无需用户先提出挑选。不能渲染时在选择前说明，并让用户按文字方向选择或明确授权使用推荐主题；不得用网页示意图冒充真实PPT小样，也不得把寻找本地文件夹作为默认预览流程。
- 每个选择节点只发一次清楚问题，然后等待新用户输入。等待期间可核对内容，但不能重复催选、重做小样，或用超时、沉默和自动续跑代替选择。
- 用户一旦选定，记录为 explicit 再生成完整稿。美化版继承同一方向；需重新排版。输出目标和图表编辑需求分别记录：原生数据图表要求与矢量形状输出冲突时需取舍，不静默降级。
- 公司母版要求优先检查；仅提取颜色不能声称套用母版。本入口不支持任意模板复刻。额外SlideViber风格按需读取其当前CLI目录，不硬编码数量；额外预设需另行可读性核验，不绕过四方向注册表静默使用。
- 偏好仅写当前演示稿旁清单，不写全局记忆。

## 最小选择合同

宿主将已理解的意图写成JSON，调用 `python scripts/ppt_theme_selection.py --request intent.json --output selection.json`。无需用户填写JSON。已有output不会覆盖。

输入：`target` 为 standard/slideviber；`explicit: {id}`、`project_preference: {id, confirmed}`、`inherited: {id, confirmed}` 按上述优先级；`recommendation: {id}` 和未经确认的继承仅用于小样推荐，不构成选定。布尔 `direct / choose / template_required / template_supported / require_native_chart_data`；`direct` 仅在用户明确授权代选/直接生成时设置，没有明确偏好且 `direct` 为假默认 awaiting_choice。`choose` 与旧 `first_important` 保留兼容，不是触发正常选择的必要条件。`reason` 为简短实际依据，`source_model_sha256` 绑定源。

宿主需能够读取Skill、执行本地Python/Node依赖、生成PPT并展示其真实渲染预览。主题小样优先作为聊天内图片交付，允许用户点开看大图；右侧预览面板是有能力宿主的增强项。可视选择不保证所有Agent产品均支持；若缺少执行或展示能力，明确说明缺口，不把色卡、网页示意或源SVG当作最终PPT效果。只有链接实际可打开时才称为“预览”。

输出：`ppt-theme/1`、状态 ready/awaiting_choice/needs_decision、原因、选择来源、确认标志、主题参数及指纹、源模型指纹、编辑边界。`validate_selection` 在正式生成前再次核验状态与配置指纹，拒绝未知或漂移配置。小样须明确 `preview=True`，只能放行 awaiting_choice，不能绕过能力冲突。

`slideviber_theme` 从同一选择输出工作区theme.json。颜色按角色映射，不能机械把SlideViber第3强调色当成业务正向；正负方向与业务好坏分开。生成者保留标签、符号和图表尺度。配置可控制封面/标题构图，编辑叙事必须实际改变留白与构图，而不只是换色。

## 已有消费者与验证

- 原标准消费者 `build_pptx.py` 接受可选 `theme_selection`，先校验原报告合同，再覆盖仅用于渲染的主题；不改model。旧三个主题调用保持原状；旧布局未实现editorial时必须拒绝而不是冒充。
- `slideviber_handoff.py` 可接收相同可选清单并携带确认来源；未指定且未授权代选时等待两页小样选择，已确认偏好不重复审批。
- `ppt_theme_samples.mjs` 从绑定来源的两页内容规格生成标准PPT或SlideViber SVG，主题来自已验证selection；不接收原始Excel或绕过报告合同。它是主题展示消费者，非通用分析/PPT故事生成器。标准小样用公开python-pptx导出，SlideViber分支只输出SVG，不提前加载标准私有工具；运行前按所选目标进行环境预检。小样不得当作整稿，editorial两页可预览仍不代表其完整章节稿已验。
- 验证冻结图表数据、显示标签、顺序/尺度、负值、中文长标签、多系列、导出编辑性。全部方向两种路径的两页小样通过只说明受测主题可用，正式长稿仍须逐页检查。

---

## 参考资料：references/quick-help.md

# 快速帮助与故障定位

这份入口用于首次使用、常见失败和文件定位。它不替代分析、HTML 或 PPT 合同，也不能降低任何内容与质量门禁。

## 先判断卡在哪一步

| 阶段 | 常见现象 | Agent 应做什么 | 对用户怎么说 |
| --- | --- | --- | --- |
| 读取源表 | 找不到文件、工作表或表头 | 核对实际路径、文件格式、工作表和表头结构 | 说明未开始分析；指出需要用户选择的工作表或整理的表头 |
| 理解口径 | 多个日期字段、比率含义不清、对象粒度不明 | 只询问会改变结论的字段或口径，不让用户填写技术配置 | 用业务语言列出候选项及各自影响 |
| 生成 HTML | Python 或基础依赖缺失 | 运行 `environment_check.py --target html`，按返回的下一步修复 | 说明 HTML 尚未生成；列出缺少的软件或包及安装命令 |
| 生成标准 PPT | HTML 已完成，但 Node 或 PPT 依赖缺失 | 保留 HTML，运行 `--target standard`，只修 PPT 环境 | 说明 HTML 不受影响；PPT 卡在什么依赖及如何补齐 |
| 生成美化 PPT | 标准稿已完成，但 SlideViber 未安装或导出失败 | 保留 HTML 和标准稿，运行 `--target slideviber`；不得删减内容绕过失败 | 说明美化版是可选项；已有产物仍可使用 |
| 宿主平台调用失败 | 平台提示模型、账号、API、权限或额度问题 | 先区分宿主模型鉴权与 Skill 运行错误 | 明确这是平台模型未启动还是 Skill 自身失败，避免让用户重装 Skill |

## 新手错误说明格式

遇到失败时，Agent 必须用四句话内给出：

1. **发生在哪一步：** 读取数据、确认口径、HTML、标准 PPT 或美化 PPT。
2. **影响什么：** 哪个产物尚未生成，哪些已完成产物仍然可用。
3. **需要做什么：** 给出一个最小动作或一条可复制命令；不堆内部字段名。
4. **仍不确定什么：** 只有确实需要用户判断时，才列出一个简短选择题。

不要只转发 `analysis_profile`、`semantic_contract`、`evidence_id`、`zero_denominator_policy` 等内部术语。必须先翻译成对应业务含义：分析场景、字段与指标口径、证据来源、零分母处理方式。

## 常见问题

### 第一次使用应该选哪种开始方式？

第一次使用推荐“先确认分析方案”：AI先用短句说明分析范围、重点问题、必要待确认项和预计交付，用户确认后再生成HTML。目标和口径已经清楚时可以明确说“直接分析，只确认影响结论的问题”。两种方式都不会绕过真正影响结论的口径确认。

### 为什么 Agent 还要问我问题？

“直接分析”会自动识别高置信字段；日期、指标分母、客户／订单粒度或未完成周期会改变结论时，必须由用户确认。只问影响结论的问题，不要求用户编写 JSON。

### 一个文件有多个工作表怎么办？

当前一次只分析一张结构清晰的表。Agent 应先列出候选工作表，让用户选择；多工作表联合、多层表头和合并单元格不属于当前版本。

### HTML 已经生成，为什么 PPT 还会失败？

HTML、标准 PPT 和美化 PPT 的依赖按层增加。HTML 成功不代表 Node、PPT 导出或 SlideViber 环境已经就绪。后续失败不得覆盖已经通过的 HTML 或标准稿。

HTML交付后，Agent应明确告诉用户可以回复“生成PPT”继续；用户明确只要HTML时不再推荐。标准PPT完成后，应说明可回复“制作美化版”，并同时说明SlideViber的独立安装和编辑性边界。

### 为什么主题小样不能直接预览？

小样必须来自实际PPTX的渲染页。宿主没有可用渲染器或当前PPTX导入失败时，Agent应在要求选主题前说明，并让用户按文字方向选择或明确授权使用推荐主题。不能把色卡、网页示意或源SVG说成真实PPT效果，也不应让用户反复寻找本地文件夹。

### 一定要安装 SlideViber 吗？

不需要。HTML 与标准 PPT 可以独立交付。SlideViber 是可选的精修环节，用户选择继续时才单独安装，并保留原标准稿。

### 为什么不能直接套用演示案例的结论？

公开案例只展示能力。每次都要根据当前数据重新确认字段、指标、周期、证据和图表，不绑定案例行业或预设答案。

### 平台提示模型账号、API 或额度错误，是 Skill 坏了吗？

不一定。这类错误通常发生在宿主模型调用之前或期间。先确认平台模型能正常运行，再判断 Skill 是否真正开始读取文件；不要把宿主鉴权失败误判为分析失败。

## 文件导航

| 想解决的问题 | 看哪里 |
| --- | --- |
| 第一次怎么用、总体流程和边界 | `SKILL.md` |
| 常见错误和新手解释 | 本文件 |
| 字段、指标、证据与报告模型 | `report-model.md` |
| HTML 分析与生成合同 | `html-analysis.md` |
| 图表为什么这样选 | `chart-spec.md` |
| 标准 PPT 与美化版如何衔接 | `chapter-presentation.md` |
| PPT 主题怎样选择 | `ppt-theme-selection.md` |

环境检查命令：

```bash
python scripts/environment_check.py --target html
python scripts/environment_check.py --target standard
python scripts/environment_check.py --target slideviber --slideviber-dir "SlideViber目录"
```

---

## 参考资料：references/report-model.md

# 请求与 report_model v2

> 本文是已实现接口参考，用于调用和核验当前行为；不替代已批准的技术规格或验收计划。

## 请求 JSON

```json
{
  "source_path": "business-detail.xlsx",
  "mode": "professional",
  "sheet_name": "经营明细",
  "period_type": "monthly",
  "audience": "经营管理层",
  "objective": "判断经营变化、定位结构驱动并形成下一周期动作",
  "analysis_intent": "business_review",
  "analysis_profile": "transactional_commerce",
  "semantic_contract": {
    "domain": "transactional_commerce",
    "table_grain": "order_line",
    "confirmation_status": "confirmed",
    "field_mappings": {
      "order": {"source_field": "订单号", "confidence": "high"},
      "product": {"source_field": "商品编码", "confidence": "high"},
      "customer": {"source_field": "客户编码", "confidence": "high"},
      "time": {"source_field": "下单时间", "confidence": "high"},
      "geography": {"source_field": "区域", "confidence": "high"},
      "quantity": {"source_field": "数量", "confidence": "high"},
      "unit_price": {"source_field": "单价", "confidence": "high"},
      "status": {"source_field": "订单状态", "confidence": "high"}
    },
    "cancellation_rule": {"values": ["已取消"]},
    "return_rule": {"values": ["已退货"]}
  },
  "date_column": "下单时间",
  "primary_metrics": ["销售额", "订单数"],
  "dimensions": ["区域", "商品编码"],
  "metric_contracts": [
    {"name": "销售额", "aggregation": "sum", "unit": "元", "role": "outcome", "direction": "higher_is_better"}
  ],
  "comparisons": ["period_over_period", "year_over_year"],
  "week_start": "monday",
  "timezone": "Asia/Shanghai",
  "incomplete_period_policy": "exclude",
  "theme": "corporate",
  "ppt_refinement": "offer_slideviber",
  "output_mode": "report+pptx"
}
```

相对 `source_path` 以请求 JSON 所在目录为基准。

| 字段 | 必填 | 允许值或约束 |
| --- | ---: | --- |
| `source_path` | 是 | `.csv` 或 `.xlsx` |
| `mode` | 否 | `quick / professional`，默认 `quick` |
| `sheet_name` | 否 | Excel 工作表名；CSV 忽略 |
| `period_type` | 是 | `weekly / monthly` |
| `audience` | 是 | 汇报受众 |
| `objective` | 是 | 本次要回答的问题 |
| `analysis_intent` | 否 | `business_review / exploration / engineering_regression`，默认 `business_review` |
| `analysis_profile` | 否 | `auto / general / retail_growth / transactional_commerce / content_operations / project_operations`，默认 `auto` |
| `semantic_contract` | 视场景 | 交易画像必须提供表粒度、字段映射和显式业务规则；`content_operations` 与 `project_operations` 为 experimental，必须显式 `confirmation_status=confirmed`，且固定使用 general 执行层 |
| `analysis_questions` | 否 | 专业模式可指定镜头、问题、优先级和所需字段；仍需通过证据门禁 |
| `date_column` | 是 | 可解析为日期的字段 |
| `primary_metrics` | 是 | 数值指标 1–6 个 |
| `dimensions` | 否 | 分类字段，建议不超过 4 个 |
| `metric_contracts` | 视指标 | `sum / ratio / average / last`；非加总指标必须提供 |
| `comparisons` | 否 | `period_over_period / year_over_year` |
| `week_start` | 否 | `monday / sunday` |
| `timezone` | 否 | 默认 `Asia/Shanghai` |
| `incomplete_period_policy` | 否 | `exclude / keep`，默认 `exclude` |
| `theme` | 否 | `corporate / clean / warm` |
| `ppt_refinement` | 否 | `standard / offer_slideviber` |
| `output_mode` | 否 | `report / report+pptx` |

## 一键与两阶段接口

默认一键生成：

```bash
python scripts/sheet_to_report.py --request request.json --output output
```

专业或内部流程可把确定性分析与叙事排序拆开：

```bash
python scripts/sheet_to_report.py --request request.json --output output --analyse-only
python scripts/sheet_to_report.py --output output --finalize story_plan.json
```

- `analysis_evidence.json` 保存来源 SHA、请求指纹、分析合同、质量决定、分析镜头、evidence catalog 和确定性 report seed。
- 默认 story plan 只保存已有 `slide_id / layout_id / evidence_ids / chart_ids / content_refs` 的选择与顺序；不能修改页面文案、数字、公式或 evidence。证据后的新判断走下方显式提案入口，不能解锁旧页面进行任意编辑。
- `--finalize` 会重新核对来源 SHA、请求指纹、页面身份、内容引用和证据范围。计划无效、越权或证据不足时返回结构化失败，不覆盖上一版已通过产物。
- 本地请求指纹与内容锁可检测任一未同步篡改；若攻击者能同步替换所有本地请求、seed、锁和哈希，则必须依赖外部不可变摘要或签名证明原始来源。

### 证据后判断提案

当已有结构比较但缺少经营判断时，由当前运行环境中的 AI 阅读 `analysis_evidence.json`，提交 `decisions.json` 数组；不连接新模型 API，不在代码里按行业或案例生成固定结论。

```bash
python scripts/sheet_to_report.py --output output --compose-decisions decisions.json
python scripts/sheet_to_report.py --output output --finalize output/story_plan.json
```

第一条只编译并创建 `story_plan.json`，已有文件拒绝覆盖，校验失败不创建计划；第二条重放原证据和提案后再执行原内容／模型／HTML门禁。`output` 中须已有分析阶段产出的 `analysis_evidence.json`。Python 调用为 `build_story_plan(evidence, decision_proposals=proposals)`。

每条提案严格使用以下字段，额外字段与自报 `achieved_depth / evidence 数值 / 章节归属` 拒绝：

- `proposal_id / question_id`：唯一提案 ID、受支持且已选择的真实问题 ID。
- `headline / operating_implication`：AI 形成的判断标题与资源、风险或验证意义；不是数字复述。
- `claim_type=diagnostic|inference`、`signal_type=risk|opportunity`、非空 `limitations[]`：只在表内证据范围作诊断／受限推断；没有因果证据不写因果保证。
- `proofs[]`：目前白名单为 `{"evidence_id": "已有证据ID", "view": "period_change"}`。单个期间细分证据自行固定其实际两期；完整趋势还需 `current_period / baseline_period`，必须在已计算序列与声明问题范围内。值、单位、对象和比较期由编译器读取；风险／机会必须至少有一个与指标方向相符的实际变化。其他证明形态不会被强转为期间证明。
- `action`：严格包含 `action_type / target / headline / rationale / steps[] / success_signal / guardrails[] / limitations[]`。`target` 必须精确等于一个已证明对象，不能拼接未观测对象；风险／机会方向也须由该对象的证明支持。步骤、成功信号与止损条件由 AI 明确填写，不得只写“继续关注”。数值事实由 proof 投影，提案业务语言不接受游离数值常量，包括中文百分数、倍数等数量表达；已观测对象名称里的数字不当作事实常量。该校验不替代实际经营判断的人工语义审查。

分析阶段用实际行成员登记 `decision_context[]` 的每问题完整证据组合及范围；编译阶段只引用该已计算组合，不能凭哈希猜测并集行数、重读源表或新增补查。证明本身必须具备真实驱动／细分，提案不能通过给普通趋势增加 risk/opportunity 标签升级深度。所附上下文证据也不替代提案实际引用的结构证明。

原 evidence、源／请求指纹、静态问题要求、指标与 scope 不改。派生故事保存 proposals 和 `base_content_hash`，重新计算真实深度、组合选择、摘要、章节、行动及内容锁；finalize 从原 evidence＋提案确定性重建，再校验计划，不接受自行重签的派生页面。最终选择仍可能删除提案或撤销其行动深度；阶段6的五案例与视觉验收尚未因此完成。

## report_model v2 顶层契约

```text
schema_version
source
request
data_profile
metric_contracts
analysis_profile
analysis_contract
quality_decisions
analysis_brief
candidate_question_graph
analysis_lenses
analysis_chapters
periods
period_overview
latest_snapshot
kpis
insights
actions
levers
charts
slide_plan
evidence_index
value_selection
content_validation
validation
```

### `analysis_contract`

- `analysis_intent`：业务复盘、探索或工程回归。
- `semantic_contract`：已确认的业务对象、表粒度、字段映射、置信度、过滤和状态规则。
- `adapter_id`、`adapter_maturity`、`execution_profile`：最终选定的适配器及其执行层。verified 可按已确认边界运行；experimental 只在确认分析计划后运行且使用 general 执行层；unavailable 明确失败。
- `available_objects`：本次可支持的问题对象；未确认对象不得进入正式叙事。

Quick 只能自动采用 high 置信度字段映射。Professional 使用 medium 前必须有 `confirmation_status=confirmed`；low 始终返回 `needs_input`。

### `quality_decisions`

通用层记录问题选择与缺失条件。`transactional_commerce` 另保存：

- 销售、客户、商品、地域等分域口径；缺客户 ID 不影响销售域，但不进入客户域。
- 负数量、取消、退货、零价、异常价格分别记录规则、数量与影响金额。
- 已确认过滤器的输入、保留、排除行数与影响金额；未确认候选规则不执行。
- 工程回归是否关闭业务镜头。

### `analysis_lenses`

每个镜头保存业务问题、优先级、所需对象／指标、图表要求、选择理由、状态与缺失条件；还记录 `required_depth`、`achieved_depth`、`answer_status`、`evidence_ids`、`followup_trace` 与 `stop_reason`。高优先问题未达到规定深度时只能继续补查或降级；`followup_trace` 仅记录白名单聚合路径、真实信息增量与停止信息，不含行级原始数据。

深度由 `analysis_depth.assess_depth` 根据实际证据形状复算：排名不自动成为驱动，计划用途／证据 ID／工具名／自报深度不构成证明；结构证据和同问题的实际经营判断须同时存在才可达到 4。`depth_gaps` 是运行结果，进入根请求重放白名单。联合指标必须具有相同实际样本指纹和时间／过滤上下文；旧证据复用不计新增信息。阶段 6 联调尚未完成，不能据局部探针通过声明全部深度门禁通过。

自定义问题和系统候选使用同一规划字段与真实前置条件检查；缺失字段、对象或指标时不能借已有事实宣称已回答。没有显式深度时，结果问题默认为 1、高优先问题为 4、其余为 3；显式值保留并接受严格类型校验。执行后停止原因来自受控执行器，不接受请求自行伪报终态。

`comparison_scope` 可省略，或声明严格的 `{period_field, baseline, current}`（两侧均为非空、不重复且互不重叠的周期字符串列表）；未知键、任意字符串和非法类型在入口失败。兼容两个明确名称：`latest_complete_period_vs_prior_period` 与 `latest_complete_vs_previous_and_year_over_year`。受控执行器从主分析已计算的完整周期窗口解析名称，使用已确认日期字段和相同周历；“前期”指上一实际保留周期，双比较生成独立环比／同比路径，绝不拼接基准分母。没有完整周期证明（例如keep策略）、缺日期授权或缺对应基期时明确停止；已成功比较保留。根请求的符号合同不改写，实际范围保存在各证据scope及执行轨迹中，finalize不重新解析日期或读取源表。

聚合信息身份比较实际样本指纹、指标合同、分组轴和比较角色；不因无效筛选的写法变化计作新信息。完整分组可证明集中度，集中度摘要不能反向证明完整分组；截断排名也不能冒充完整分组。主趋势按每个实际周期登记 `scope_bindings.periods`，可复用为同一样本的两期比较证明，但不能覆盖新子集。跨问题重复路径仍按批准的重复哈希停止策略处理。

已有期间证据可绑定到具体受支持的自定义 `question_id`，须匹配指标合同、声明维度、实际窗口与比较角色；指标 ID 别名可用，证据 ID 的文本没有业务含义。非期间问题与原始日期字段的显式比较继续交由既有补查执行器核对实际计算身份，不能仅凭指标或月份标签相同借证据。绑定不生成新证据、不增加深度，经营判断仍须独立成立。

洞察和行动的 `question_id` 进入正式共享字段与内容锁；行动从真实来源洞察／章节解析归属。内容 QA 按具体问题检查状态、页面归属及覆盖，不能用同镜头或同显示问题文本覆盖兄弟问题；缺少 ID 的旧记录仅在镜头唯一对应一个问题时回退。单问题业务页不得重标其他问题的判断；总览基线可引用支持性趋势事实，但这不算趋势问题已覆盖。

### `analysis_brief`、`candidate_question_graph` 与 `analysis_chapters`

- `analysis_brief` 固化受众、目标、决策节奏、交互模式和最小必要确认状态。
- `candidate_question_graph` 保存字段能力生成的候选问题、初扫信号、可回答性、价值评分、选择／拒绝理由和稳定问题 ID。
- `analysis_chapters[]` 是正式正文选择单位。每章至少包含 `chapter_id / question_id / decision_question / judgement / answer_status / required_depth / achieved_depth / fact_evidence_ids / driver_evidence_ids / segment_evidence_ids / operating_implication / report_language / chart_ids / action_ids / limitations / selection_status / claim_chart_alignment`。
- 核心章节必须 `answer_status=answered` 且达到深度门槛；否则只能降级。管理摘要通过 `key_conclusion_chapter_ids` 引用已选章节，正式行动通过 `source_chapter_ids` 回链来源章节。
- 核心章节下限独立为 4，不因问题把 required_depth 写低而降低。`judgement_insight_id` 绑定实际合格判断，`judgement` 和 `operating_implication` 从同一洞察投影，不得拿兄弟洞察最大深度授予浅标题。

### `value_selection` 与 `narrative_validation`

- `value_selection.selection_unit=analysis_chapter`；`analysis_chapters` 决定整章进入正文、附录或删除。旧的 `featured / appendix / dropped` 洞察分组保留兼容和章内追溯，但不再单独决定正文故事。
- `presentation_role=supporting` 的普通 KPI 事实最高只能进入 `appendix`；高优先问题覆盖不得把它提升为 `featured`。单一问题下自然达到正文门槛、证据独立且风险／机会信号互补的洞察可以同时保留；管理摘要按“lens＋signal_type”选择最多 3 条结论。
- 正式行动若声明 `source_insight_ids`，这些来源必须全部属于 `featured_insight_ids`；附录或删除项不得绕过中央选择直接升级为关键决策建议。
- `content_validation.narrative_validation` 记录页面故事顺序是否有效及相关阻断；未通过时不得输出正式叙事。

## 证据与内容审计

### 计算范围合同

- 新内核模型及分析证据产物必须包含 `scope_contract_version=analysis-scope-v1` 和顶层 `scope_catalog`；删除目录不能退出范围校验。
- 计算点用源表内部唯一行索引登记实际参与行集。持久化仅包含规则、父范围、时间／筛选／指标契约和行数，不包含原始行或行号。原子 `scope_id` 由规则及父范围生成，完整目录另外受内容锁保护。
- source／atomic／comparison 范围包含不透明 `population_sha256`，只用于同一源表内实际参与样本的等同性证明；不导出成员位图。不同指标恰好行数相同不等于同样本。非零售投影可复用完整主分析分组，真实 rows 进入摘要锁；含“其他”的截断排名不能证明全部对象排序。
- `source.loaded_row_count` 保留原始加载行数，独立于显式过滤后的 `data_profile.row_count`。主分析窗口统一日期、去重、完整周期及数值策略。交易排名进一步要求订单、金额及对应对象有效；客户覆盖不冒用销售总盘。质量影响分别绑定基准／受影响行与金额范围，绝对金额分母保存为 `baseline_absolute_amount`。
- `evidence_index[*].scope_id` 与 `sample_count` 必须对应；周期、质量和多指标比较用 `scope_bindings`／`metric_scope_bindings` 标明各自分母。补查路径身份包含有效分析窗口范围，不能跨窗口复用同一证据身份。
- 洞察、章节、图表和行动通过证据引用绑定 `scope_id / scope_disclosure`。章节合并校验 `fact_evidence_ids / driver_evidence_ids / segment_evidence_ids`；引用不同范围时生成显式 `comparison`，精确列出成员并按真实行集并集计数，声明分母分别计算。无证据且未入选的章节只能声明未作业务判断，不能冒领数字范围。
- 交易预处理原有 whole-source 质量目录保持原义，与新计算窗口范围并列，不用全源计数替换窗口计数。分析证据顶层与两个 seed 的范围／质量决定镜像必须一致；范围目录、各对象绑定及真实图表 payload 一并进入内容锁。所有补查的结果内层范围／行数必须与 evidence 顶层一致，完整结果及其 `result_hash` 受通用锁保护，不仅由某个适配器验证。

每个 `evidence_index` 记录至少包含：

- 唯一 evidence ID、证据类型和指标／维度对象；
- `formula / calculation`；
- `filter_scope`；
- `sample_count`、`affected_rows`、可用时的 `affected_amount`；
- `business_objects` 与 `limitations`；
- `quality_managed=true`。

洞察额外声明 `claim_type=fact|diagnostic|inference|hypothesis`、`evidence_strength=high|medium|low`、`value_score` 和限制。诊断／推断缺少交叉证据时必须降级为假设。

行动必须包含 `action_type / target / basis / rationale / steps / success_signal / guardrails / limitations / source_chapter_ids / evidence_ids / verification_signal / formal`。缺少来源章节、对象、依据、步骤、证据、成功信号或止损护栏时不得进入正式输出。

深度 5 由“真实 4 级判断 + 合格且最终保留的行动”证明，不以请求深度或空 action_ids 授予。生产顺序先准备缺省行动字段，再评估候选，最后在只保留／不新增行动的有界收敛中重算问题与章节；过滤掉行动必须撤回其深度贡献，不重新补查或改低 required_depth。finalize 只使用锁定模型，不读源或补查。

`formal` 必须严格为布尔 true；action_id 唯一且非空，步骤／护栏为非空字符串列表，限制为字符串列表，成功信号为非空字符串，不能把当前观测直接重复为试验成功条件。标准化只补真正缺省字段，显式空值或错误类型不得字符串化洗白。这些内容合同对深度 4 的正式行动同样有效。每个 source_insight_id 必须有同问题的所属章节；source_chapter_ids 与章节 action_ids 双向一致。最终问题仅评估归属本问题章节的行动，章节仅评估自己的行动和代表判断。

`content_validation` 阻断：

- 原始字段泄漏、纯数字复述、无证据因果或目标值；
- 不受支持镜头、重复结论、套话、空槽和未解析占位符；
- 悬空 evidence、非封面内容页无证据、标题与证据没有信息锚点。

## 分析意图与页面规则

- `business_review`：只有证据充足时生成 6–10 页自适应叙事；缺失镜头的可选页直接消失，不凑页数。
- `exploration`：允许输出带限制的可验证假设，不把相关性写成因果。
- `engineering_regression`：输出明确 QA dossier；允许少于 6 页，不生成经营洞察、经营杠杆或行动路线。
- `needs_input / insufficient_evidence` 是正常结构化结果，不是空报告。业务复盘不足 6 个有证据页面时停止渲染并列出补充问题。

`slide_plan[]` 将页面角色分别绑定到管理摘要、KPI、洞察、行动、图表或质量数据的确定路径，并记录 `slide_id`、`layout_id`、`story_role`、`evidence_ids`、`chart_ids`、`content_refs` 和 `visual_spec`。渲染器只能读取这些引用，不得从页面标题猜内容。

### `slide_plan[].visual_spec`

```json
{
  "eyebrow": "关键趋势",
  "tone": "data",
  "density": "standard",
  "display_claim": "收入变化与主要结构线索",
  "comparison_contexts": [
    {"kind": "yoy", "label": "同比", "current_label": "2025年6月", "baseline_label": "2024年6月"}
  ],
  "focus_evidence_ids": ["metric:收入:trend"],
  "chart_focus": {"series_name": "收入", "category_name": null}
}
```

- `eyebrow` 使用中文功能眉题。
- `focus_evidence_ids` 必须属于本页 evidence。
- `comparison_contexts` 只显示模型中实际存在的比较周期。
- 无法可靠确定视觉焦点或图表强调时留空，不得猜测。

## 时间、指标与业务阅读层

- `period_overview` 是分析期累计／整体 KPI；`latest_snapshot` 是最新完整周期 KPI 及实际比较周期，两者不得混用。
- 比率使用分子合计 ÷ 分母合计；均值遵守确认的权重；余额按日期取期末值。
- 同比结论同时显示实际最新周期与实际同比周期；子集与整体同页时明确范围，必要时保存同期全渠道基准。
- 证据优先：表内可回答的问题直接完成趋势、结构和交叉分析；只有确实缺字段、周期或业务事件证据时才说明无法验证。
- 常规趋势与结构优先使用 PowerPoint 原生可编辑图表；复杂图像必须标记不可编辑。

## 输出与一致性

- `report_model.json`：跨格式唯一语义真相源。
- `report.html` 与 `html_qa.json`：按问题章节组织的自包含业务简报，以及结构、资源、章节数量、单指标堆叠、编码型对象和内容检查。
- `report.pptx` 与 `ppt_qa.json`：标准可编辑汇报及字号、边界、重叠、正文对比度、角色、焦点、东亚换行和孤立标点检查。
- `slideviber_handoff.md`：可选精修交接；SlideViber 是可选精修层，不能改变结论。
- `run_result.json`：运行状态、产物清单和失败阶段。

HTML、PPTX 与 SlideViber 必须读取同一 `report_model.json`，且使用同一 `slide_id`、日期、数字、结论、行动与 evidence ID。美化只能改变视觉表达。

主题边界：HTML 使用唯一的标准商务样式，便于稳定阅读、复核与证据追溯；请求中的 `clean / corporate / warm` 只改变标准 PPT 与 SlideViber 的视觉主题，不改变 HTML。HTML 正文按已选 `analysis_chapters` 递进，普通 KPI 与 supporting 事实不得由渲染器自行升级；摘要与正式行动必须分别通过章节 ID 完成双向闭环，技术 ID 不显示给业务读者。

章节的 fact／driver／segment 证据必须有实际可读证明。`chart.evidence_ids` 仅是引用，不等于该图实际展示了证据；只有对象、指标和数值匹配的直接趋势／简单排名可以免表。期间或季节比较、交易驱动、质量诊断、带额外订单数／单均金额／占比的排名保留类型化数值证明表；共享表只渲染一次，并链接到前文唯一锚点。不能可靠投影的证据在写 HTML 前失败，不回读源表或重新计算。

摘要、章节、图表及行动的范围披露读取 `scope_catalog` 的结构化规则及分项绑定，不直接输出带工具／字段 ID 的原始定义。保留实际不连续期间、筛选含义、上级排除量、指标聚合与质量规则；输入行数不是订单／客户数或比率分母，组合范围不共用分母，质量绝对金额与净金额分开，季节性月均不得称为期间合计。确认的英文指标展示名保留，禁止多个不同指标统一改称“指标”。

HTML QA 按逐行单元格矩阵核对证明表对象、期间、单位和数值，并检查范围披露、唯一锚点及静态隐藏属性／行内样式。该静态检查不声称覆盖任意 CSS 级联、布局或阅读体验；浏览器逐章验收仍是独立门禁。

有合格核心章节但仍有未完成问题时，`narrative_selection.status=partial_coverage`，`unresolved_questions[]` 从真实问题与页面重新派生，记录问题 ID、业务问题、证据、回答状态、所需／实际深度、缺口、停止原因、说明及后续处理。HTML 必须明确展示问题、实际缺口与后续处理，不能把这类报告显示为全部问题已回答。附录保留事实不等于问题达到所需深度；这类处置也不计作已回答覆盖。处置元数据进入内容锁；删除、改写或伪装为 complete 均须被 QA 阻断。

## 失败与人工确认

- 缺日期字段、指标契约分子分母或交易必需字段：停止并列出缺项。
- 交易表粒度不清、字段映射低置信或 medium 未确认：返回 `needs_input`。
- 负向、取消、零价或异常交易没有已确认处理规则：保留并显式登记质量决定，不静默剔除。
- 未知聚合、布局、缺图、悬空 evidence、未解析占位符或标题—图表证据不一致：明确失败。
- 业务复盘证据不足：返回 `needs_input / insufficient_evidence`；工程回归改用 QA dossier，不伪装成经营分析。
- 多工作表联合、多层表头、合并单元格：先整理为单张单层表。
- 机器 QA 通过不等于人工视觉验收；正式发布前仍需逐页检查。

## 公开样例边界

快速体验和公开示例只使用 `scripts/generate_sample.py` 生成的固定种子模拟数据，并在产物中声明 synthetic provenance。真实或内部压力数据不进入 Skill 文案、示例和发布包。
