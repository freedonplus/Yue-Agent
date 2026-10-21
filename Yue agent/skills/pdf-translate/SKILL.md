---
name: PDF 翻译
description: 将PDF文档翻译成中文，并采用专业排版。提取文本，逐段翻译为结构良好的Markdown格式，然后通过weasyprint生成支持完整CJK的PDF。当用户要求翻译PDF时使用，例如用户说“翻译PDF”、“translate this document”或“pdf translate”。
---

# PDF Translation Skill

翻译 PDF 文档并生成排版精美的中文文档。输出 Markdown + PDF 双格式。

## 版本信息

**当前版本**: v4.0.0
**发布日期**: 2026-02-21

### v4.0.0 变更

- 采用 Markdown-first 工作流：先生成结构化 Markdown，再转 PDF
- PDF 引擎从 reportlab 切换为 weasyprint（支持完整 HTML/CSS 排版）
- 修复代码块中文乱码问题（添加 CJK 字体 fallback）
- 完整支持：标题层级、代码块、表格、列表、引用、粗体斜体
- 新增 `scripts/md2pdf.py` 通用转换脚本

## 核心工作流

### Step 1: 提取 PDF 文本

```python
import pdfplumber

pdf = pdfplumber.open("输入文件.pdf")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text:
        print(f"--- Page {i+1} ---")
        print(text)
```

长文档（>20 页）先提取前几页了解结构，再分批提取。

### Step 2: 分析文档结构

通读全文，识别以下元素并规划 Markdown 映射：

| 原文元素 | Markdown 映射 |
|---------|-------------|
| 文档标题 | `#` |
| 章节（Chapter） | `##` |
| 小节（Section） | `###` |
| 子小节（Subsection） | `####` |
| 目录 | 链接列表 `- [章节名](#锚点)` |
| 正文段落 | 段落（空行分隔） |
| 代码块 | ` ``` ` 围栏（**不翻译**内容） |
| 表格 | `\| 列1 \| 列2 \|` 语法 |
| 有序列表 | `1. ` 开头 |
| 无序列表 | `- ` 开头 |
| 引用/提示框 | `> ` 语法 |
| 页脚/页码 | 丢弃 |

### Step 3: 逐章节翻译为中文 Markdown

**必须逐章节翻译**，不要一次输出全文。每完成一个章节就追加写入文件。

#### 翻译规则

1. **专有名词保留英文**：首次出现时括号附英文，如"渐进式披露（Progressive Disclosure）"
2. **代码块不翻译**：` ``` ` 内代码保持原文，只翻译围栏外说明文字
3. **行内代码不翻译**：反引号内标识符、命令、文件名保持英文
4. **保持层级结构**：`#` → `##` → `###` → `####` 不跳级
5. **段落间必须空行**：每个段落、列表、代码块、表格前后都要有空行
6. **列表格式**：`- ` 或 `1. ` 开头，嵌套用 2 空格缩进
7. **表格格式**：`| 列1 | 列2 |` 语法，必须有 `|---|---|` 分隔行
8. **引用格式**：`> ` 开头

#### 翻译质量标准

参见 [translation-standards.md](references/translation-standards.md)

- 三步翻译工作流：重写初稿 → 问题诊断 → 润色定稿
- 四大语言转换策略：形合→意合、被动→主动、抽象→具体、精简冗余
- 杜绝"欧化表达"和"翻译腔"

#### 必须避免的格式错误

- ❌ 段落之间没有空行 → 文字挤在一起
- ❌ 列表项前没有空行 → 不被识别为列表
- ❌ 表格前后没有空行 → 表格无法渲染
- ❌ 代码块 ` ``` ` 前后没有空行 → 代码块不显示
- ❌ 标题 `##` 前后没有空行 → 标题不识别
- ❌ 翻译代码块内的代码
- ❌ 一次性输出全部内容导致截断

### Step 4: 输出 Markdown 文件

写入 `.md` 文件，路径与原 PDF 同目录，文件名：`原文件名_中文翻译.md`

### Step 5: 生成 PDF

使用 `scripts/md2pdf.py` 将 Markdown 转为排版精美的 PDF：

```bash
python3 ${SKILL_DIR}/scripts/md2pdf.py "输入.md" "输出.pdf"
```

macOS 上如果报 gobject 找不到：

```bash
DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib" python3 ${SKILL_DIR}/scripts/md2pdf.py "输入.md" "输出.pdf"
```

也可以使用项目目录下的副本：

```bash
python3 scripts/md2pdf.py "输入.md" "输出.pdf"
```

PDF 排版特性：
- A4 版面，自动分页，页码
- 中文字体（苹方/黑体/雅黑）+ 英文字体 fallback
- 深色背景代码块（支持中文注释）
- 专业表格样式（交替行色、边框）
- 蓝色左边框引用块
- 标题层级样式（蓝色边线、字号递减）

### Step 6: 确认输出

翻译完成后告知用户：
1. `.md` 文件路径
2. `.pdf` 文件路径
3. 文档概况（页数、字数）

## 依赖安装

```bash
# macOS
brew install pango
pip3 install pdfplumber markdown weasyprint

# 旧方案依赖（仍可用）
pip3 install reportlab pypdf
```

## 脚本目录

| 脚本 | 用途 |
|------|------|
| `scripts/md2pdf.py` | **推荐** Markdown → PDF（weasyprint 引擎） |
| `scripts/translate_pdf.py` | 旧版：基础 PDF 提取和生成（reportlab） |
| `scripts/generate_complete_pdf.py` | 旧版：完整工作流（reportlab） |

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 代码块中文乱码 | 使用 `md2pdf.py`（v4.0，已修复 CJK font fallback） |
| weasyprint 报 gobject 找不到 | `DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib"` |
| 中文字体不显示 | 确认系统有苹方或黑体字体 |
| Markdown 格式错乱 | 检查块级元素前后是否有空行 |

更多问题参见 [troubleshooting.md](references/troubleshooting.md)

---

**参考文档**：
- [翻译标准](references/translation-standards.md)
- [字体配置](references/font-configuration.md)
- [故障排除](references/troubleshooting.md)
- [完整示例](references/complete-example.md)

---

## 参考资料：references/complete-example.md

# 完整PDF生成示例

本文档提供完整的端到端PDF生成示例，包含Markdown解析、目录生成、中英文字体混排等功能。

## 完整工作流示例

以下是一个完整的端到端PDF生成脚本，展示如何从Markdown文本生成包含封面、目录、正文的PDF文档。

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os
import re

# 1. 注册字体
def register_fonts():
    """注册中英文字体"""
    chinese_font_paths = [
        '/System/Library/Fonts/STHeiti Light.ttc',  # macOS 黑体
        '/System/Library/Fonts/PingFang.ttc',       # macOS 苹方
        'C:/Windows/Fonts/msyh.ttc',                # Windows 微软雅黑
        'C:/Windows/Fonts/simhei.ttf',              # Windows 黑体
    ]

    chinese_font = None
    for font_path in chinese_font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
                chinese_font = 'ChineseFont'
                break
            except:
                continue

    if not chinese_font:
        chinese_font = 'Helvetica'

    try:
        pdfmetrics.registerFont(TTFont('EnglishFont', '/System/Library/Fonts/Helvetica.ttc', subfontIndex=0))
        english_font = 'EnglishFont'
    except:
        english_font = 'Helvetica'

    return chinese_font, english_font

# 2. Markdown解析函数
def markdown_to_pdf_content(markdown_text):
    """将Markdown文本转换为PDF内容结构"""
    lines = markdown_text.split('\n')
    content = []

    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        if line.startswith('## '):
            content.append(('heading1', line[3:].strip()))
        elif line.startswith('### '):
            content.append(('heading2', line[4:].strip()))
        elif line.startswith('---'):
            content.append(('pagebreak', ''))
        else:
            if line.strip():
                content.append(('paragraph', line.strip()))

    return content

# 3. 中英文字体混排
def apply_mixed_font(text, english_font):
    """应用中英文字体混排"""
    english_pattern = r'([a-zA-Z0-9_\-\.]+(?:\s+[a-zA-Z0-9_\-\.]+)*)'

    def replace_english(match):
        english_text = match.group(1)
        common_terms = ['API', 'JSON', 'PDF', 'AI', 'Claude', 'REST']
        if any(term in english_text for term in common_terms):
            return f'<font name="{english_font}">{english_text}</font>'
        if len(english_text.split()) > 2 or len(english_text) > 10:
            return f'<font name="{english_font}">{english_text}</font>'
        return english_text

    return re.sub(english_pattern, replace_english, text)

# 4. 完整PDF生成
def create_complete_pdf(markdown_content, output_path):
    """生成包含封面、目录、正文的完整PDF"""

    # 注册字体
    chinese_font, english_font = register_fonts()

    # 创建文档
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)

    # 定义样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
        fontName=chinese_font, fontSize=24,
        textColor=HexColor('#1a1a1a'), spaceAfter=30,
        alignment=TA_CENTER, leading=32)

    heading1_style = ParagraphStyle('CustomHeading1', parent=styles['Heading1'],
        fontName=chinese_font, fontSize=18,
        textColor=HexColor('#2563eb'), spaceAfter=12,
        spaceBefore=20, leading=24)

    body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'],
        fontName=chinese_font, fontSize=11,
        textColor=HexColor('#374151'), spaceAfter=8,
        leading=16, alignment=TA_JUSTIFY)

    story = []

    # 封面页
    story.append(Paragraph("文档标题", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("副标题", ParagraphStyle('CustomSubtitle', parent=styles['Normal'],
        fontName=chinese_font, fontSize=14, textColor=HexColor('#666666'),
        alignment=TA_CENTER, leading=20)))
    story.append(PageBreak())

    # 目录页（使用显式数据结构）
    story.append(Paragraph("目录", heading1_style))
    story.append(Spacer(1, 20))

    toc_items = [
        ("", "第一章", "3"),
        ("", "第二章", "5"),
        ("", "第三章", "7"),
    ]

    for category, title, page in toc_items:
        if category:
            story.append(Paragraph(f"<b>{category}</b>：{title} ………………………… {page}", body_style))
        else:
            story.append(Paragraph(f"{title} ………………………… {page}", body_style))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # 解析Markdown内容
    content = markdown_to_pdf_content(markdown_content)

    for item_type, item_content in content:
        if item_type == 'heading1':
            story.append(Paragraph(apply_mixed_font(item_content, english_font), heading1_style))
        elif item_type == 'heading2':
            story.append(Paragraph(apply_mixed_font(item_content, english_font),
                ParagraphStyle('CustomHeading2', parent=styles['Heading2'],
                fontName=chinese_font, fontSize=16, textColor=HexColor('#1e40af'),
                spaceAfter=10, spaceBefore=15, leading=22)))
        elif item_type == 'paragraph':
            # 正确处理粗体标签（使用正则表达式避免嵌套错误）
            processed = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', item_content)
            story.append(Paragraph(apply_mixed_font(processed, english_font), body_style))
        elif item_type == 'pagebreak':
            story.append(PageBreak())

    # 生成PDF
    doc.build(story)
    print(f"✅ PDF生成成功：{output_path}")

# 使用示例
FULL_TRANSLATION = '''# 文档标题

## 第一章

这是**粗体文本**和普通文本的混合。

### 1.1 小节

更多内容...

---

## 第二章

继续内容...
'''

create_complete_pdf(FULL_TRANSLATION, "output.pdf")
```

## 关键要点总结

### 1. Markdown解析
使用`markdown_to_pdf_content()`函数按行解析，返回结构化内容：
```python
content = [('heading1', '标题'), ('paragraph', '内容'), ...]
```

### 2. 粗体处理
使用正则表达式`\*\*([^*]+)\*\*`避免HTML标签嵌套错误：
```python
processed = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
```

### 3. 字体混排
使用`apply_mixed_font()`自动识别英文关键词：
```python
mixed_text = apply_mixed_font("Claude Code 支持 RESTful API", english_font)
```

### 4. 目录结构
使用显式数据结构确保目录不会丢失：
```python
toc_items = [("分类", "标题", "页码"), ...]
```

### 5. 完整流程
封面 → 目录 → 正文

## 使用场景

此完整工作流适用于：
- 需要生成包含目录的专业文档
- 需要中英文字体混排的技术文档
- 需要从Markdown生成格式化PDF

## 更多示例

参见主脚本：`scripts/generate_complete_pdf.py`

---

## 返回主文档：[SKILL.md](../SKILL.md)

---

## 参考资料：references/font-configuration.md

# 字体配置指南

本文档详细说明pdf-translate skill的字体配置和中英文字体混排规则。

## 字体优先级

**默认中文字体**：黑体（STHeiti）- 优先用于中文文本
**默认英文字体**：Helvetica - 用于英文关键词和专有名词

## 系统字体配置

### macOS系统字体（优先级从高到低）

1. **STHeiti Light**（黑体）- 默认选择，适合正式文档
2. **PingFang**（苹方）- 备选方案
3. **Helvetica** - 后备字体（也用于英文）

### Windows系统字体

1. **Microsoft YaHei**（微软雅黑）
2. **SimHei**（黑体）
3. **Helvetica** - 英文字体

### Linux系统字体

1. **Droid Sans Fallback**
2. **WenQuanYi Micro Hei**
3. **Helvetica** - 英文字体

## 中英文字体混排规则

在翻译后的PDF中，遵循以下字体使用规则：

| 文本类型 | 使用字体 | 说明 |
|---------|---------|------|
| 中文正文、标题 | 黑体（ChineseFont） | 默认中文字体 |
| 英文关键词 | Helvetica（EnglishFont） | 专业术语、技术名词 |
| 英文专有名词 | Helvetica（EnglishFont） | 人名、地名、公司名 |
| 英文缩写 | Helvetica（EnglishFont） | API、JSON、PDF等 |
| 混合文本 | 按字符自动切换 | 中文用黑体，英文用Helvetica |

### 混排示例

```
Claude Code 是一个强大的 AI 编程助手，支持 RESTful API 和 JSON 格式。
↑ 黑体        ↑ 黑体      ↑ 黑体            ↑ Helvetica  ↑ 黑体   ↑ Helvetica  ↑ 黑体
```

## 代码实现

### 字体注册

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('ChineseFont', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=0))

# 注册英文字体
pdfmetrics.registerFont(TTFont('EnglishFont', '/System/Library/Fonts/Helvetica.ttc', subfontIndex=0))
```

### 字体混排函数

```python
import re

def apply_mixed_font(text, english_font):
    """应用中英文字体混排"""
    # 匹配英文文本的模式（包括常见缩写）
    english_pattern = r'([a-zA-Z0-9_\-\.]+(?:\s+[a-zA-Z0-9_\-\.]+)*)'

    def replace_english(match):
        english_text = match.group(1)
        # 常见技术术语列表
        common_terms = ['API', 'JSON', 'PDF', 'AI', 'URL', 'HTTP', 'REST', 'SQL', 'HTML', 'CSS', 'Claude', 'GitHub', 'SDK']
        if any(term in english_text for term in common_terms):
            return f'<font name="{english_font}">{english_text}</font>'
        # 较长的英文短语（可能是专有名词）
        if len(english_text.split()) > 2 or len(english_text) > 10:
            return f'<font name="{english_font}">{english_text}</font>'
        return english_text

    # 应用字体到英文文本
    result = re.sub(english_pattern, replace_english, text)
    return result
```

### 使用示例

```python
# 在段落中使用混合字体
text = '<font name="ChineseFont">中文文本</font><font name="EnglishFont">English Keywords</font>'
story.append(Paragraph(text, body_style))
```

## 混排规则详细说明

### 自动识别规则

1. **英文缩写**：自动应用英文字体
   - 包括：API、JSON、PDF、AI、URL、HTTP、REST、SQL、HTML、CSS等

2. **专业术语**：保留英文并应用英文字体
   - 包括：Claude、GitHub、SDK等技术名词

3. **长英文短语**：应用英文字体
   - 字符数>10 或 单词数>2 的英文短语

4. **混合文本**：按字符自动切换字体
   - 中文用ChineseFont（黑体）
   - 英文用EnglishFont（Helvetica）

## PDF样式配置

### 颜色方案

| 元素 | 颜色代码 | 用途 |
|------|----------|------|
| 标题 | `#1a1a1a` | 主标题颜色 |
| 一级标题 | `#2563eb` | 蓝色强调 |
| 二级标题 | `#1e40af` | 深蓝色 |
| 三级标题 | `#374151` | 灰色 |
| 正文 | `#374151` | 深灰色 |
| 副标题/页脚 | `#666666` | 浅灰色 |

### 字体大小

| 元素 | 字号 | 行距 |
|------|------|------|
| 主标题 | 24pt | 32pt |
| 副标题 | 14pt | 20pt |
| 一级标题 | 18pt | 24pt |
| 二级标题 | 16pt | 22pt |
| 三级标题 | 14pt | 20pt |
| 正文 | 11pt | 16pt |

### 间距配置

- 页边距：0.75英寸（上下左右）
- 标题后间距：30pt
- 段落后间距：8pt
- 段落前间距：12-20pt（根据标题级别）

---

## 返回主文档：[SKILL.md](../SKILL.md)

---

## 参考资料：references/translation-standards.md

# 翻译质量标准

本文档定义了pdf-translate skill的翻译质量标准和核心翻译工作流。

## 翻译角色定位

你将扮演一位顶尖的英汉学术翻译专家，同时也是一位卓越的中文写作者。你深谙思果和余光中"翻译即重写"(Translation as Rewriting)的精髓。

## 核心任务与目标

你的任务是将专业的英文学术文本转化为高质量的中文译文。你必须彻底摒弃"逐字翻译"，而是深层理解原文的意义、逻辑和语境，以地道、流畅、精准的现代中文进行重新创作。

**最终目标**：产出一篇读起来宛如中文原创的、可供直接发表的高水准文章。

## 目标与风格

- **目标受众**：有一定知识背景，但非该特定领域专家的中文读者
- **语言风格**：现代、清晰、流畅、优雅。确保专业严谨，同时表达清晰易懂，逻辑连贯
- **核心要求**：坚决杜绝"翻译腔"和任何"欧化表达"(Europeanized language)

## 中西语言转换核心策略（必须严格执行）

【重要】英文重"形合"(Hypotaxis，依赖形式连接)，中文重"意合"(Parataxis，依赖意义连贯)。

在"重写"过程中，必须严格执行以下策略：

### 1. 化"形合"为"意合"（结构重组）

- 大胆拆分英文长句（尤其是包含复杂从句、关系词的结构）
- 重新组织语序，使其符合中文的叙述逻辑（如因果、先后、轻重）
- 多用短句，避免冗长复杂的句式

### 2. 化被动为主动（语态转换）

- 尽量将原文的被动句转换为中文的主动句、"把"字句或无主句
- 坚决避免滥用"被"字

### 3. 化抽象为具体（词性转换）

- 英文多抽象名词，中文多动词
- 将抽象的名词化表达转换为更自然的动词短语
- 例如：将"进行分析"优化为"分析"

### 4. 精简冗余（消除欧化表达）

- 避免直译连接词（如减少"当...的时候"、"关于"）
- 避免过度使用"的"字结构和不必要的代词（如"他的"、"它们的"）

## 核心翻译原则

1. **忠实性与地道性**：100%忠实于原文信息，同时表达必须完全符合中文学术语境和语言习惯。地道性优先于形式对应。

2. **术语处理**：
   - 专业术语：优先采用学界公认译名。若无，保留英文原文，并在首次出现时于括号内注明中文释义
   - 专有名词：人名、地名等，若有公认权威译名则使用；否则，一律保留英文原文，不作音译

3. **文体对等**：精准匹配原文的文体和语气。保持学术严谨性，同时确保行文清晰流畅，逻辑连贯。

4. **格式保留**：完全保留原文格式结构（段落、标题、列表、公式等），并将标点符号转换为中文规范用法。

## 三步翻译工作流（必须严格遵循）

你必须严格按照以下三个步骤执行翻译任务：

### 步骤一：应用策略，重写初稿

- 深入理解当前文本块的完整意思和逻辑
- 强制执行「中西语言转换核心策略」
- 彻底摆脱原文句子结构的束缚，用自然流畅的中文进行重写

### 步骤二：自我批判与问题诊断

以批判性的眼光和中文母语读者的视角审阅初稿，检查：

- **欧化病症诊断**（是否存在滥用"被"字、"的"字；句子结构是否依然遵循英文逻辑）
- **策略执行检查**（是否彻底执行了长句拆分、语态转换等）
- **表达与逻辑**（用词是否精准？句式是否冗长别扭？逻辑衔接是否顺畅？）
- **术语与完整性**（术语处理是否规范？信息点是否遗漏？）

### 步骤三：润色与定稿

针对第二步诊断出的所有问题进行全面优化，产出最终版本。核心是实现"言辞整句化"：确保每个句子结构完整、意思清晰、表达专业。

## 分块处理规则

- 每次处理的原文篇幅建议在1000至2000个英文单词左右
- 确保每个文本块都经过完整的三步工作流处理
- 处理完一块后再进行下一块，确保质量一致性

## 实际执行要点

**翻译时必须注意**：
- 保持原有文档结构（标题、段落、列表等）
- 保留专业术语的准确性，首次出现时注明中文
- 适当调整中文表达习惯，消除翻译腔
- 保持原文档的格式和排版逻辑
- 标点符号使用中文规范（中文使用全角标点）

---

## 返回主文档：[SKILL.md](../SKILL.md)

---

## 参考资料：references/troubleshooting.md

# 故障排除指南

本文档提供pdf-translate skill常见问题的解决方案。

## 目录或特殊格式内容丢失

### 问题现象
生成的PDF缺少原文档的目录（TOC）或其他特殊格式内容。

### 问题原因
1. PDF中的目录包含特殊格式字符（如省略号……、页码对齐）
2. 通用Markdown解析器无法正确处理这些特殊格式
3. 特殊格式内容在解析过程中被忽略或跳过

### 解决方案

#### 方案A：显式目录处理（推荐）

```python
# 1. 识别目录内容（通常在文档开头，有规律格式）
# 2. 创建显式的目录数据结构
toc_items = [
    ("分类", "标题", "页码"),
    ("前言", "从辅助到协作", "3"),
    ("基础趋势", "构造性变革", "4"),
]

# 3. 手动构建目录内容
for category, title, page in toc_items:
    if category:  # 有分类的目录项
        story.append(Paragraph(f"<b>{category}</b>：{title} ……………… {page}", body_style))
    else:  # 无分类的目录项
        story.append(Paragraph(f"{title} ……………… {page}", body_style))
```

#### 方案B：保留原始格式

```python
# 1. 直接从提取的文本中识别目录部分
# 2. 使用原始文本构建Paragraph，不进行格式转换
story.append(Paragraph(raw_toc_text, body_style))
```

### 预防措施
- 翻译前先查看PDF提取的文本内容，确认是否有特殊格式
- 对于包含目录的文档，优先使用显式处理方式
- 保留原文档的结构层次（使用标题样式区分不同级别）

## 中文字体不显示

### 问题现象
生成的PDF中文显示为方块或乱码。

### 解决方案

1. **检查系统字体**
   ```bash
   # macOS
   ls /System/Library/Fonts/STHeiti*.ttc

   # Windows
   ls C:/Windows/Fonts/msyh.ttc

   # Linux
   ls /usr/share/fonts/truetype/droid/
   ```

2. **使用自定义字体路径**
   ```bash
   python3 translate_pdf.py input.pdf -o output.pdf --font /path/to/font.ttf
   ```

3. **确保字体文件包含中文字符集**
   - 字体文件必须是TTF或TTC格式
   - 必须包含中文字符集（UTF-8编码支持）

## PDF内容提取不完整

### 问题现象
某些PDF内容无法提取或提取不完整。

### 可能原因
- PDF包含图片或扫描内容
- PDF使用了特殊编码
- PDF有密码保护

### 解决方案

#### 扫描PDF处理

```bash
# 安装OCR依赖
pip3 install pytesseract pdf2image

# 使用OCR提取文本
```

#### 密码保护PDF

```python
import pypdf

reader = PdfReader("encrypted.pdf")
writer = PdfWriter()

# 解密PDF
if reader.is_encrypted:
    reader.decrypt("password")

for page in reader.pages:
    writer.add_page(page)

with open("decrypted.pdf", "wb") as output:
    writer.write(output)
```

## 内存不足

### 问题现象
处理大型PDF时出现内存不足错误。

### 解决方案

```python
# 分页处理，每处理N页保存一次
def process_large_pdf(pdf_path, output_path, chunk_size=10):
    """分块处理大型PDF"""
    # 处理逻辑
    pass
```

## HTML标签嵌套错误

### 问题现象
PDF生成时出现 `Parse error: saw </para> instead of expected </b>` 错误。

### 问题原因
粗体标签使用简单字符串替换导致HTML标签嵌套错误：
```python
# 错误方式
text.replace('**', '<b>').replace('**', '</b>')  # 可能产生 <b><b>text</b></b>
```

### 解决方案

使用正则表达式精确匹配：

```python
import re

# 正确方式
processed_content = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
```

## 粗体文本不显示

### 问题现象
翻译内容中的 `**粗体文本**` 在PDF中没有显示为粗体。

### 解决方案

确保在将Markdown转换为PDF内容时正确处理粗体标签：

```python
def markdown_to_pdf_content(markdown_text):
    """将Markdown文本转换为PDF内容"""
    lines = markdown_text.split('\n')
    content = []

    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        # 识别标题
        if line.startswith('## '):
            content.append(('heading1', line[3:].strip()))
        elif line.startswith('### '):
            content.append(('heading2', line[4:].strip()))
        elif line.startswith('---'):
            content.append(('pagebreak', ''))
        else:
            if line.strip():
                content.append(('paragraph', line.strip()))

    return content

# 处理粗体标签
for item_type, item_content in content:
    if item_type == 'paragraph':
        # 使用正则表达式处理粗体
        processed = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', item_content)
        story.append(Paragraph(processed, body_style))
```

## 其他常见问题

### 依赖包未安装

```bash
# 安装所有必需的依赖
pip3 install pdfplumber reportlab pypdf

# 或使用conda
conda install -c conda-forge pdfplumber reportlab
```

### 文件路径错误

确保使用绝对路径或相对于当前工作目录的正确路径：

```python
import os
from pathlib import Path

# 使用pathlib处理路径
input_path = Path("input.pdf").resolve()
if not input_path.exists():
    raise FileNotFoundError(f"Input file not found: {input_path}")
```

---

## 返回主文档：[SKILL.md](../SKILL.md)
