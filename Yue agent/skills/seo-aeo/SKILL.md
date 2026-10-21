---
name: SEO / AEO 策略
description: SEO、AEO（Answer Engine Optimization，答案引擎优化）和GEO策略，用于搜索引擎和AI可见性。触发词包括“SEO审计”、“技术SEO”、“页面内SEO”、“AI搜索优化”、“AEO”、“GEO”、“AI可见性”、“针对ChatGPT的优化”、“针对Perplexity的优化”、“AI概述”、“答案引擎优化”、“生成引擎优化”、“AI引用”、“精选摘要”、“元标签”、“模式标记”、“搜索排名”、“内容优化”、“E-E-A-T”、“结构化数据”、“搜索控制台”、“SEO健康检查”、“为什么我没有排名”、“AI搜索准备度”、“反向链接策略”、“链接建设”、“域名权威”、“程序化SEO”、“规模化SEO”、“基于模板的SEO”、“AEO监控”、“AI搜索监控”、“JSON-LD”、“富摘要”、“schema.org”、“SERP分析”、“搜索意图”、“站点架构”、“信息架构”、“URL结构”、“内部链接”或“导航”。对于关键词研究，请参阅keyword-research-and-clustering。
---

# SEO & AEO Strategy

Traditional SEO gets pages ranked. AI search optimization (AEO/GEO) gets content **cited**. This skill covers both.

```
SEO  → Rank in traditional search results (blue links)
AEO  → Appear in featured snippets, AI Overviews, voice answers
GEO  → Get cited in generative AI responses (ChatGPT, Claude, Perplexity)
```

**2025 reality:** AI Overviews appear in ~47% of Google searches. 58% of queries end without a click. Optimize for citation, not just ranking.

---

## Initial Assessment

Check for `.claude/product-marketing-context.md` or `.agents/product-marketing-context.md` first. Use existing context; only ask for what's missing.

Before auditing, understand:

1. **Site context** — Type (SaaS, e-commerce, blog), primary SEO goal, priority keywords/topics
2. **Current state** — Known issues, organic traffic level, recent changes or migrations
3. **AI visibility** — Does the brand appear in AI-generated answers today? Checked ChatGPT, Perplexity, Google AI Overviews?
4. **Scope** — Full site vs. specific pages? Technical + on-page + AI, or one focus area?

---

## Technical SEO

### Crawlability

| Check | What to Verify |
|-------|---------------|
| **robots.txt** | No unintentional blocks, sitemap referenced, AI crawlers allowed |
| **XML Sitemap** | Exists, submitted to Search Console, canonical URLs only, < 50K URLs |
| **Site architecture** | Important pages within 3 clicks, logical hierarchy, no orphan pages |
| **Crawl budget** | Parameterized URLs controlled, faceted nav handled, no session IDs in URLs |

### Indexation

- `site:domain.com` check vs. Search Console coverage report
- Verify no `noindex` on important pages
- Check canonical tags (self-referencing on unique pages, HTTP→HTTPS, www consistency)
- Identify redirect chains/loops, soft 404s, duplicate content

### Core Web Vitals & Speed

| Metric | Target | Tool |
|--------|--------|------|
| LCP (Largest Contentful Paint) | < 2.5s | PageSpeed Insights |
| INP (Interaction to Next Paint) | < 200ms | Chrome DevTools |
| CLS (Cumulative Layout Shift) | < 0.1 | WebPageTest |
| TTFB (Time to First Byte) | < 800ms | Search Console |

### Mobile & Security

- Responsive design (not separate m. site), viewport configured, adequate tap targets (48px min)
- HTTPS across entire site, valid SSL, no mixed content, HSTS header

### URL Structure

- Lowercase, hyphen-separated, < 75 characters
- Include target keywords naturally, avoid unnecessary parameters

---

## On-Page SEO

### Title Tags

- 50–60 characters, primary keyword near beginning
- Unique per page, brand name at end (unless homepage)
- Compelling and click-worthy

### Meta Descriptions

- 150–160 characters, include primary keyword
- Clear value proposition with call-to-action, unique per page

### Heading Structure

- Single `<h1>` per page containing primary keyword
- Logical hierarchy (H1 → H2 → H3), no skipped levels
- Descriptive headings (not generic), include keywords naturally

### Image SEO

- Descriptive filenames with keywords, alt text on all images
- Compressed, modern formats (WebP/AVIF), lazy load below-fold
- Responsive images with `width`/`height` attributes

### Internal Linking

- Descriptive anchor text with keywords (not "click here")
- Important pages well-linked, no broken internal links
- Breadcrumb navigation for hierarchy

### Content Quality (E-E-A-T)

| Signal | Implementation |
|--------|---------------|
| **Experience** | First-hand accounts, case studies, original data |
| **Expertise** | Author credentials visible, accurate detailed information |
| **Authoritativeness** | Cited by others, industry credentials, recognized in space |
| **Trustworthiness** | Transparent sourcing, contact info, privacy policy, HTTPS |

---

## AI Search Optimization (AEO/GEO)

### How AI Search Platforms Select Sources

| Platform | Source Selection | Key Factor |
|----------|-----------------|------------|
| **Google AI Overviews** | Strong correlation with traditional rankings | Top 5 organic positions favored |
| **ChatGPT** | Wider range, not just top-ranked | Branded domain authority, recency |
| **Perplexity** | Always cites with links | Authoritative, recent, well-structured |
| **Gemini** | Google index + Knowledge Graph | E-E-A-T signals, structured data |
| **Copilot** | Bing index | Microsoft ecosystem (LinkedIn, GitHub) |
| **Claude** | Brave Search | Factual density, structural clarity |

For detailed platform-specific ranking factors, see [references/platform-ranking-factors.md](references/platform-ranking-factors.md) and [references/platform-algorithms.md](references/platform-algorithms.md).

### The Three Pillars

**1. Structure — Make content extractable**

AI systems extract passages, not pages. Every key claim should work standalone.

- Lead every section with a direct answer (don't bury it)
- Keep key answer passages to 40–60 words (optimal for snippet extraction)
- Use H2/H3 headings that match how people phrase queries
- Tables beat prose for comparisons; numbered lists beat paragraphs for processes

**Inverted pyramid pattern:**
```
┌──────────────────────────────────┐
│  DIRECT ANSWER (1-2 sentences)   │ ← AI extracts this first
├──────────────────────────────────┤
│  KEY FACTS & CONTEXT             │ ← Supporting bullets/data
├──────────────────────────────────┤
│  DETAILED EXPLANATION            │ ← Background, examples
└──────────────────────────────────┘
```

**2. Authority — Make content citable**

The Princeton GEO research (KDD 2024) ranked 9 optimization methods:

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Cite sources** | +40% | Add authoritative references with links |
| **Add statistics** | +37% | Include specific numbers with sources |
| **Add quotations** | +30% | Expert quotes with name and title |
| **Authoritative tone** | +25% | Write with demonstrated expertise |
| **Improve clarity** | +20% | Simplify complex concepts |
| **Technical terms** | +18% | Use domain-specific terminology |
| **Unique vocabulary** | +15% | Increase word diversity |
| **Fluency optimization** | +15–30% | Improve readability and flow |
| ~~Keyword stuffing~~ | **-10%** | **Actively hurts AI visibility** |

**Best combination:** Fluency + Statistics = maximum boost. Low-ranking sites benefit even more — up to 115% visibility increase with citations.

For detailed GEO research, see [references/geo-research.md](references/geo-research.md).

**3. Presence — Be where AI looks**

AI systems cite where you appear, not just your site:
- Wikipedia mentions (7.8% of all ChatGPT citations)
- Reddit discussions, YouTube content, Quora answers
- Review sites (G2, Capterra, TrustRadius for B2B SaaS)
- Industry publications and guest posts

### Semantic Triples (Key AEO Technique)

Compact, unambiguous facts AI can't misread. Pattern: `[Subject]` `[specific verb]` `[concrete object]`.

```
✅ "HubSpot CRM syncs contact and company data."
✅ "Lead Scoring assigns priority based on engagement."
❌ "The system helps with various tasks."
❌ "It can do many things for users."
```

### AI Crawler Configuration

Ensure robots.txt allows AI crawlers:

```
User-agent: GPTBot          # OpenAI
Allow: /
User-agent: ChatGPT-User    # ChatGPT browsing
Allow: /
User-agent: PerplexityBot   # Perplexity
Allow: /
User-agent: ClaudeBot        # Anthropic
Allow: /
User-agent: Google-Extended  # Gemini/AI Overviews
Allow: /
```

See [references/ai-crawlers.md](references/ai-crawlers.md) for full configuration.

---

## Structured Data for Search & AI

Schema markup improves AI visibility by 30–40%. Priority types:

| Content Type | Schema | Citation Impact |
|-------------|--------|:---------------:|
| FAQs | `FAQPage` | 2.5x inclusion |
| Articles/Blog | `Article` + Author | 2.2x citations |
| Organization | `Organization` | 2.8x citations |
| How-to content | `HowTo` | Step extraction |
| Products | `Product` | Pricing/features |
| Reviews | `AggregateRating` | Trust signals |
| Breadcrumbs | `BreadcrumbList` | Navigation context |

For full JSON-LD templates, see [references/schema-templates.md](references/schema-templates.md) and [references/schema-for-ai.md](references/schema-for-ai.md).

Validate at [Google Rich Results Test](https://search.google.com/test/rich-results) and [Schema.org Validator](https://validator.schema.org/).

---

## Content Types That Get Cited Most

| Content Type | AI Citation Share | Why AI Cites It |
|-------------|:----------------:|----------------|
| Comparison articles | ~33% | Structured, balanced, high-intent |
| Definitive guides | ~15% | Comprehensive, authoritative |
| Original research/data | ~12% | Unique, citable statistics |
| Best-of/listicles | ~10% | Clear structure, entity-rich |
| Product pages | ~10% | Specific extractable details |
| How-to guides | ~8% | Step-by-step structure |

**Underperformers:** Generic blog posts without structure, thin product pages, gated content, undated content, PDF-only content.

For content templates and patterns, see [references/content-patterns.md](references/content-patterns.md) and [references/content-templates.md](references/content-templates.md).

---

## AEO Measurement

Track these four metrics monthly:

### 1. AI Visibility
Test priority queries across ChatGPT, Perplexity, Gemini, Google AI Overviews. **Target:** Appear in 60%+ of priority queries.

### 2. AI Share of Voice
`Share of Voice = (Your mentions / Total brand mentions) × 100`. **Target:** Match or exceed traditional search market share.

### 3. AI Citations
How often YOUR WEBSITE is the source. **Target:** Cited in 30%+ of relevant queries.

### 4. Referral Demand
Traffic originating in AI but arriving later (brand search after AI mention). Track via post-purchase survey: "How did you first hear about us?"

### Monitoring Tools

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, AI Overviews | Share of AI voice |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude | Multi-platform monitoring |
| **ZipTie** | AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment |
| **HubSpot AEO Grader** | AI visibility audit | Free audit |

### Interpreting Results

| Visibility | Share of Voice | Diagnosis |
|------------|----------------|-----------|
| ↓ Down | ↓ Down | Platform algorithm change (industry-wide) |
| ↓ Down | → Stable | Your content quality declined |
| → Stable | ↓ Down | Competitors improved |
| ↑ Up | ↑ Up | Your AEO strategy is working |

---

## Audit Checklists

### Critical (Fix Immediately)
- [ ] HTTPS enabled, valid SSL
- [ ] robots.txt allows crawling (including AI bots)
- [ ] No `noindex` on important pages
- [ ] Title tags present, unique, with primary keyword
- [ ] Single `<h1>` per page
- [ ] AI crawlers not blocked in robots.txt

### High Priority
- [ ] Meta descriptions present and compelling
- [ ] XML sitemap submitted to Search Console
- [ ] Canonical URLs set correctly
- [ ] Mobile-responsive, Core Web Vitals passing
- [ ] FAQPage schema on FAQ/support pages
- [ ] Article schema with author on blog/guide pages
- [ ] "Last updated" date visible on content

### Medium Priority
- [ ] Internal linking strategy implemented
- [ ] Image alt text on all images
- [ ] Descriptive URLs with keywords
- [ ] Breadcrumb navigation + schema
- [ ] Author bios with credentials
- [ ] Statistics cited with sources
- [ ] Content answers queries in first paragraph

### Ongoing
- [ ] Fix crawl errors in Search Console
- [ ] Update sitemap when content changes
- [ ] Refresh content quarterly (competitive topics)
- [ ] Monitor AI visibility monthly (manual or tools)
- [ ] Check for broken links
- [ ] Track AI share of voice vs. competitors

For complete SEO checklist, see [references/seo-checklist.md](references/seo-checklist.md).

---

## Tools

| Tool | Use |
|------|-----|
| Google Search Console | Monitor indexing, fix issues, track queries |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Validate structured data |
| Lighthouse | Full SEO audit |
| Screaming Frog | Crawl analysis |
| Semrush / Ahrefs | AI Overview tracking, backlinks, content gaps |

See [references/tools-and-apis.md](references/tools-and-apis.md) for API reference.

**Scripts available** in `scripts/`: SEO audit, keyword research, SERP analysis, backlink analysis, competitor gap analysis, autocomplete ideas. See script files for usage.

---

## References

- [references/platform-ranking-factors.md](references/platform-ranking-factors.md) — How each AI platform selects sources
- [references/platform-algorithms.md](references/platform-algorithms.md) — Detailed ranking factors per platform
- [references/geo-research.md](references/geo-research.md) — Princeton GEO research (9 methods)
- [references/content-patterns.md](references/content-patterns.md) — AI-optimized content block templates
- [references/content-templates.md](references/content-templates.md) — Page structure templates for AI
- [references/schema-templates.md](references/schema-templates.md) — JSON-LD schema templates
- [references/schema-for-ai.md](references/schema-for-ai.md) — Schema markup for AI visibility
- [references/ai-crawlers.md](references/ai-crawlers.md) — AI crawler robots.txt configuration
- [references/seo-checklist.md](references/seo-checklist.md) — Complete SEO audit checklist
- [references/aeo-geo-patterns.md](references/aeo-geo-patterns.md) — Content patterns for AI citation
- [references/ai-writing-detection.md](references/ai-writing-detection.md) — AI writing patterns to avoid
- [references/query-research.md](references/query-research.md) — Query research methodology
- [references/tools-and-apis.md](references/tools-and-apis.md) — Tools and API reference
- [references/google-docs-summary.md](references/google-docs-summary.md) — Google documentation summary

## Related Skills

- **keyword-research-and-clustering** — Keyword research, expansion, and topic clustering
- **schema-markup** — Structured data implementation details
- **programmatic-seo** — Building SEO pages at scale
- **competitor-alternatives** — Building comparison pages that get cited
- **content-strategy-and-planning** — Planning what content to create
- **data-and-funnel-analytics** — Measuring SEO/AEO performance

---

## 参考资料：references/aeo-geo-patterns.md

# AEO and GEO Content Patterns

Reusable content block patterns optimized for answer engines and AI citation.

---

## Answer Engine Optimization (AEO) Patterns

These patterns help content appear in featured snippets, AI Overviews, voice search results, and answer boxes.

### Definition Block

Use for "What is [X]?" queries.

```markdown
## What is [Term]?

[Term] is [concise 1-sentence definition]. [Expanded 1-2 sentence explanation with key characteristics]. [Brief context on why it matters or how it's used].
```

**Example:**
```markdown
## What is Answer Engine Optimization?

Answer Engine Optimization (AEO) is the practice of structuring content so AI-powered systems can easily extract and present it as direct answers to user queries. Unlike traditional SEO that focuses on ranking in search results, AEO optimizes for featured snippets, AI Overviews, and voice assistant responses. This approach has become essential as over 60% of Google searches now end without a click.
```

### Step-by-Step Block

Use for "How to [X]" queries. Optimal for list snippets.

```markdown
## How to [Action/Goal]

[1-sentence overview of the process]

1. **[Step Name]**: [Clear action description in 1-2 sentences]
2. **[Step Name]**: [Clear action description in 1-2 sentences]
3. **[Step Name]**: [Clear action description in 1-2 sentences]
4. **[Step Name]**: [Clear action description in 1-2 sentences]
5. **[Step Name]**: [Clear action description in 1-2 sentences]

[Optional: Brief note on expected outcome or time estimate]
```

**Example:**
```markdown
## How to Optimize Content for Featured Snippets

Earning featured snippets requires strategic formatting and direct answers to search queries.

1. **Identify snippet opportunities**: Use tools like Semrush or Ahrefs to find keywords where competitors have snippets you could capture.
2. **Match the snippet format**: Analyze whether the current snippet is a paragraph, list, or table, and format your content accordingly.
3. **Answer the question directly**: Provide a clear, concise answer (40-60 words for paragraph snippets) immediately after the question heading.
4. **Add supporting context**: Expand on your answer with examples, data, and expert insights in the following paragraphs.
5. **Use proper heading structure**: Place your target question as an H2 or H3, with the answer immediately following.

Most featured snippets appear within 2-4 weeks of publishing well-optimized content.
```

### Comparison Table Block

Use for "[X] vs [Y]" queries. Optimal for table snippets.

```markdown
## [Option A] vs [Option B]: [Brief Descriptor]

| Feature | [Option A] | [Option B] |
|---------|------------|------------|
| [Criteria 1] | [Value/Description] | [Value/Description] |
| [Criteria 2] | [Value/Description] | [Value/Description] |
| [Criteria 3] | [Value/Description] | [Value/Description] |
| [Criteria 4] | [Value/Description] | [Value/Description] |
| Best For | [Use case] | [Use case] |

**Bottom line**: [1-2 sentence recommendation based on different needs]
```

### Pros and Cons Block

Use for evaluation queries: "Is [X] worth it?", "Should I [X]?"

```markdown
## Advantages and Disadvantages of [Topic]

[1-sentence overview of the evaluation context]

### Pros

- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]

### Cons

- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]

**Verdict**: [1-2 sentence balanced conclusion with recommendation]
```

### FAQ Block

Use for topic pages with multiple common questions. Essential for FAQ schema.

```markdown
## Frequently Asked Questions

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].
```

**Tips for FAQ questions:**
- Use natural question phrasing ("How do I..." not "How does one...")
- Include question words: what, how, why, when, where, who, which
- Match "People Also Ask" queries from search results
- Keep answers between 50-100 words

### Listicle Block

Use for "Best [X]", "Top [X]", "[Number] ways to [X]" queries.

```markdown
## [Number] Best [Items] for [Goal/Purpose]

[1-2 sentence intro establishing context and selection criteria]

### 1. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]

### 2. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]

### 3. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]
```

---

## Generative Engine Optimization (GEO) Patterns

These patterns optimize content for citation by AI assistants like ChatGPT, Claude, Perplexity, and Gemini.

### Statistic Citation Block

Statistics increase AI citation rates by 15-30%. Always include sources.

```markdown
[Claim statement]. According to [Source/Organization], [specific statistic with number and timeframe]. [Context for why this matters].
```

**Example:**
```markdown
Mobile optimization is no longer optional for SEO success. According to Google's 2024 Core Web Vitals report, 70% of web traffic now comes from mobile devices, and pages failing mobile usability standards see 24% higher bounce rates. This makes mobile-first indexing a critical ranking factor.
```

### Expert Quote Block

Named expert attribution adds credibility and increases citation likelihood.

```markdown
"[Direct quote from expert]," says [Expert Name], [Title/Role] at [Organization]. [1 sentence of context or interpretation].
```

**Example:**
```markdown
"The shift from keyword-driven search to intent-driven discovery represents the most significant change in SEO since mobile-first indexing," says Rand Fishkin, Co-founder of SparkToro. This perspective highlights why content strategies must evolve beyond traditional keyword optimization.
```

### Authoritative Claim Block

Structure claims for easy AI extraction with clear attribution.

```markdown
[Topic] [verb: is/has/requires/involves] [clear, specific claim]. [Source] [confirms/reports/found] that [supporting evidence]. This [explains/means/suggests] [implication or action].
```

**Example:**
```markdown
E-E-A-T is the cornerstone of Google's content quality evaluation. Google's Search Quality Rater Guidelines confirm that trust is the most critical factor, stating that "untrustworthy pages have low E-E-A-T no matter how experienced, expert, or authoritative they may seem." This means content creators must prioritize transparency and accuracy above all other optimization tactics.
```

### Self-Contained Answer Block

Create quotable, standalone statements that AI can extract directly.

```markdown
**[Topic/Question]**: [Complete, self-contained answer that makes sense without additional context. Include specific details, numbers, or examples in 2-3 sentences.]
```

**Example:**
```markdown
**Ideal blog post length for SEO**: The optimal length for SEO blog posts is 1,500-2,500 words for competitive topics. This range allows comprehensive topic coverage while maintaining reader engagement. HubSpot research shows long-form content earns 77% more backlinks than short articles, directly impacting search rankings.
```

### Evidence Sandwich Block

Structure claims with evidence for maximum credibility.

```markdown
[Opening claim statement].

Evidence supporting this includes:
- [Data point 1 with source]
- [Data point 2 with source]
- [Data point 3 with source]

[Concluding statement connecting evidence to actionable insight].
```

---

## Domain-Specific GEO Tactics

Different content domains benefit from different authority signals.

### Technology Content
- Emphasize technical precision and correct terminology
- Include version numbers and dates for software/tools
- Reference official documentation
- Add code examples where relevant

### Health/Medical Content
- Cite peer-reviewed studies with publication details
- Include expert credentials (MD, RN, etc.)
- Note study limitations and context
- Add "last reviewed" dates

### Financial Content
- Reference regulatory bodies (SEC, FTC, etc.)
- Include specific numbers with timeframes
- Note that information is educational, not advice
- Cite recognized financial institutions

### Legal Content
- Cite specific laws, statutes, and regulations
- Reference jurisdiction clearly
- Include professional disclaimers
- Note when professional consultation is advised

### Business/Marketing Content
- Include case studies with measurable results
- Reference industry research and reports
- Add percentage changes and timeframes
- Quote recognized thought leaders

---

## Voice Search Optimization

Voice queries are conversational and question-based. Optimize for these patterns:

### Question Formats for Voice
- "What is..."
- "How do I..."
- "Where can I find..."
- "Why does..."
- "When should I..."
- "Who is..."

### Voice-Optimized Answer Structure
- Lead with direct answer (under 30 words ideal)
- Use natural, conversational language
- Avoid jargon unless targeting expert audience
- Include local context where relevant
- Structure for single spoken response

---

## 参考资料：references/ai-crawlers.md

# AI Crawlers & Bot Management Guide

## Table of Contents
1. [AI Crawler Overview](#ai-crawler-overview)
2. [robots.txt Configuration](#robotstxt-configuration)
3. [Crawler Characteristics](#crawler-characteristics)
4. [Strategic Decisions](#strategic-decisions)
5. [Implementation Guide](#implementation-guide)

---

## AI Crawler Overview

### Major AI Crawlers (2025)

| Crawler | Company | Purpose | Recommendation |
|---------|---------|---------|----------------|
| GPTBot | OpenAI | Training data | Block if concerned about training |
| OAI-SearchBot | OpenAI | ChatGPT Search | Allow for AI search visibility |
| ChatGPT-User | OpenAI | User-requested fetching | Allow for user experience |
| Google-Extended | Google | Gemini training | Block if concerned, Allow for AI Search |
| Googlebot | Google | Search indexing | Always Allow |
| PerplexityBot | Perplexity | Search & answers | Allow for visibility |
| ClaudeBot | Anthropic | Claude features | Allow for visibility |
| Bytespider | ByteDance | TikTok/Training | Consider blocking |
| CCBot | Common Crawl | Dataset collection | Consider blocking |
| FacebookBot | Meta | AI training | Consider blocking |

### Key Distinction: Search vs Training

```
SEARCH CRAWLERS (Allow for visibility):
├── Googlebot          → Traditional search
├── OAI-SearchBot      → ChatGPT Search results
├── ChatGPT-User       → User asks ChatGPT to read a page
├── PerplexityBot      → Perplexity answers
└── ClaudeBot          → Claude features

TRAINING CRAWLERS (Block if data protection matters):
├── GPTBot             → OpenAI model training
├── Google-Extended    → Gemini training
├── CCBot              → Common Crawl datasets
├── Bytespider         → ByteDance training
└── FacebookBot        → Meta AI training
```

---

## robots.txt Configuration

### Recommended Configuration (Balanced)

```txt
# ===========================================
# AI SEARCH CRAWLERS - ALLOW
# ===========================================

# OpenAI Search (ChatGPT Search feature)
User-agent: OAI-SearchBot
Allow: /

# ChatGPT when users ask it to read a page
User-agent: ChatGPT-User
Allow: /

# Perplexity AI search
User-agent: PerplexityBot
Allow: /

# Claude AI
User-agent: ClaudeBot
Allow: /

# ===========================================
# AI TRAINING CRAWLERS - BLOCK
# ===========================================

# OpenAI training (not search)
User-agent: GPTBot
Disallow: /

# Google Gemini training
User-agent: Google-Extended
Disallow: /

# Common Crawl
User-agent: CCBot
Disallow: /

# ByteDance
User-agent: Bytespider
Disallow: /

# Meta AI training
User-agent: FacebookBot
Disallow: /

# ===========================================
# TRADITIONAL SEARCH - ALLOW
# ===========================================

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### Maximum Visibility Configuration

```txt
# Allow all AI crawlers for maximum reach
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### Maximum Protection Configuration

```txt
# Block all AI crawlers except traditional search
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /
```

---

## Crawler Characteristics

### Crawl Behavior Comparison

| Crawler | Respects robots.txt | Crawl Rate | JavaScript Rendering |
|---------|---------------------|------------|---------------------|
| Googlebot | Yes | Adaptive | Yes (2nd wave) |
| GPTBot | Yes | Unknown | Limited |
| OAI-SearchBot | Yes | Unknown | Limited |
| PerplexityBot | Yes | Moderate | Limited |
| ClaudeBot | Yes | Unknown | Limited |
| CCBot | Generally yes | Heavy | No |

### What AI Crawlers Index

```
Typically Indexed:
├── Main body content
├── Headers (H1-H6)
├── Meta descriptions
├── Alt text
├── Structured data (JSON-LD)
├── Tables
└── Lists

Often Missed:
├── JavaScript-rendered content
├── Content behind tabs/accordions
├── Lazy-loaded images
├── PDF content
├── Video transcripts (unless in HTML)
└── Content in iframes
```

---

## Strategic Decisions

### Decision Matrix

| Business Type | Strategy | Reasoning |
|---------------|----------|-----------|
| Publisher/Blog | Allow search, Block training | Maintain traffic, protect content |
| E-commerce | Allow all | Maximum product visibility |
| SaaS | Allow search, Consider training | Brand visibility, protect docs |
| Enterprise B2B | Selective allow | Control information flow |
| Personal brand | Allow all | Maximum reach |
| Research/Academic | Allow all | Citation and reach |

### Questions to Ask

1. **Is being cited by AI chatbots valuable to you?**
   - Yes → Allow search crawlers
   - No → Block all AI crawlers

2. **Are you concerned about AI training on your content?**
   - Yes → Block training crawlers (GPTBot, Google-Extended)
   - No → Allow all

3. **Do users ask AI to read your pages?**
   - Yes → Allow ChatGPT-User
   - No → Can block

4. **Is your content time-sensitive or frequently updated?**
   - Yes → Allow all search crawlers for freshness
   - No → Selective blocking okay

---

## Implementation Guide

### Step 1: Audit Current Configuration

```bash
# Check current robots.txt
curl -s https://yoursite.com/robots.txt

# Test specific bot access
curl -A "GPTBot" -I https://yoursite.com/
curl -A "OAI-SearchBot" -I https://yoursite.com/
```

### Step 2: Monitor Crawler Activity

**In server logs, look for:**
```
User-Agent patterns:
- "GPTBot/1.0"
- "OAI-SearchBot"
- "ChatGPT-User"
- "PerplexityBot"
- "ClaudeBot"
```

**Log analysis command:**
```bash
grep -E "GPTBot|OAI-SearchBot|ChatGPT-User|PerplexityBot|ClaudeBot" access.log | \
  awk '{print $1, $7}' | sort | uniq -c | sort -rn
```

### Step 3: Implement WAF Rules (if needed)

**Cloudflare example:**
```
# Block specific bots at WAF level
(cf.client.bot and http.user_agent contains "GPTBot")
```

### Step 4: Verify Implementation

```bash
# Test that robots.txt is being served correctly
curl -s https://yoursite.com/robots.txt | grep -A2 "GPTBot"

# Verify bot can/cannot access
curl -A "GPTBot" -s -o /dev/null -w "%{http_code}" https://yoursite.com/
```

### Step 5: Monitor Impact

Track these metrics after changes:
- AI referral traffic (from Perplexity, ChatGPT, etc.)
- Brand mentions in AI responses (manual testing)
- Overall organic traffic (ensure no negative impact)

---

## Emerging Crawlers to Watch

| Bot | Company | Status | Notes |
|-----|---------|--------|-------|
| MistralBot | Mistral AI | Emerging | European AI |
| DeepSeekBot | DeepSeek | Emerging | Chinese AI |
| GrokBot | xAI | Expected | Elon Musk's AI |
| MetaAI-SearchBot | Meta | Expected | Meta AI search |

**Recommendation**: Monitor industry news and update robots.txt quarterly.

---

## 参考资料：references/ai-writing-detection.md

# AI Writing Detection

Words, phrases, and punctuation patterns commonly associated with AI-generated text. Avoid these to ensure writing sounds natural and human.

Sources: Grammarly (2025), Microsoft 365 Life Hacks (2025), GPTHuman (2025), Walter Writes (2025), Textero (2025), Plagiarism Today (2025), Rolling Stone (2025), MDPI Blog (2025)

---

## Em Dashes: The Primary AI Tell

**The em dash (—) has become one of the most reliable markers of AI-generated content.**

Em dashes are longer than hyphens (-) and are used for emphasis, interruptions, or parenthetical information. While they have legitimate uses in writing, AI models drastically overuse them.

### Why Em Dashes Signal AI Writing
- AI models were trained on edited books, academic papers, and style guides where em dashes appear frequently
- AI uses em dashes as a shortcut for sentence variety instead of commas, colons, or parentheses
- Most human writers rarely use em dashes because they don't exist as a standard keyboard key
- The overuse is so consistent that it has become the unofficial signature of ChatGPT writing

### What To Do Instead
| Instead of | Use |
|------------|-----|
| The results—which were surprising—showed... | The results, which were surprising, showed... |
| This approach—unlike traditional methods—allows... | This approach, unlike traditional methods, allows... |
| The study found—as expected—that... | The study found, as expected, that... |
| Communication skills—both written and verbal—are essential | Communication skills (both written and verbal) are essential |

### Guidelines
- Use commas for most parenthetical information
- Use colons to introduce explanations or lists
- Use parentheses for supplementary information
- Reserve em dashes for rare, deliberate emphasis only
- If you find yourself using more than one em dash per page, revise

---

## Overused Verbs

| Avoid | Use Instead |
|-------|-------------|
| delve (into) | explore, examine, investigate, look at |
| leverage | use, apply, draw on |
| optimise | improve, refine, enhance |
| utilise | use |
| facilitate | help, enable, support |
| foster | encourage, support, develop, nurture |
| bolster | strengthen, support, reinforce |
| underscore | emphasise, highlight, stress |
| unveil | reveal, show, introduce, present |
| navigate | manage, handle, work through |
| streamline | simplify, make more efficient |
| enhance | improve, strengthen |
| endeavour | try, attempt, effort |
| ascertain | find out, determine, establish |
| elucidate | explain, clarify, make clear |

---

## Overused Adjectives

| Avoid | Use Instead |
|-------|-------------|
| robust | strong, reliable, thorough, solid |
| comprehensive | complete, thorough, full, detailed |
| pivotal | key, critical, central, important |
| crucial | important, key, essential, critical |
| vital | important, essential, necessary |
| transformative | significant, important, major |
| cutting-edge | new, advanced, recent, modern |
| groundbreaking | new, original, significant |
| innovative | new, original, creative |
| seamless | smooth, easy, effortless |
| intricate | complex, detailed, complicated |
| nuanced | subtle, complex, detailed |
| multifaceted | complex, varied, diverse |
| holistic | complete, whole, comprehensive |

---

## Overused Transitions and Connectors

| Avoid | Use Instead |
|-------|-------------|
| furthermore | also, in addition, and |
| moreover | also, and, besides |
| notwithstanding | despite, even so, still |
| that being said | however, but, still |
| at its core | essentially, fundamentally, basically |
| to put it simply | in short, simply put |
| it is worth noting that | note that, importantly |
| in the realm of | in, within, regarding |
| in the landscape of | in, within |
| in today's [anything] | currently, now, today |

---

## Phrases That Signal AI Writing

### Opening Phrases to Avoid
- "In today's fast-paced world..."
- "In today's digital age..."
- "In an era of..."
- "In the ever-evolving landscape of..."
- "In the realm of..."
- "It's important to note that..."
- "Let's delve into..."
- "Imagine a world where..."

### Transitional Phrases to Avoid
- "That being said..."
- "With that in mind..."
- "It's worth mentioning that..."
- "At its core..."
- "To put it simply..."
- "In essence..."
- "This begs the question..."

### Concluding Phrases to Avoid
- "In conclusion..."
- "To sum up..."
- "By [doing X], you can [achieve Y]..."
- "In the final analysis..."
- "All things considered..."
- "At the end of the day..."

### Structural Patterns to Avoid
- "Whether you're a [X], [Y], or [Z]..." (listing three examples after "whether")
- "It's not just [X], it's also [Y]..."
- "Think of [X] as [elaborate metaphor]..."
- Starting sentences with "By" followed by a gerund: "By understanding X, you can Y..."

---

## Filler Words and Empty Intensifiers

These words often add nothing to meaning. Remove them or find specific alternatives:

- absolutely
- actually
- basically
- certainly
- clearly
- definitely
- essentially
- extremely
- fundamentally
- incredibly
- interestingly
- naturally
- obviously
- quite
- really
- significantly
- simply
- surely
- truly
- ultimately
- undoubtedly
- very

---

## Academic-Specific AI Tells

| Avoid | Use Instead |
|-------|-------------|
| shed light on | clarify, explain, reveal |
| pave the way for | enable, allow, make possible |
| a myriad of | many, numerous, various |
| a plethora of | many, numerous, several |
| paramount | very important, essential, critical |
| pertaining to | about, regarding, concerning |
| prior to | before |
| subsequent to | after |
| in light of | because of, given, considering |
| with respect to | about, regarding, for |
| in terms of | regarding, for, about |
| the fact that | that (or rewrite sentence) |

---

## How to Self-Check

1. Read your text aloud. If phrases sound unnatural in speech, revise them
2. Ask: "Would I say this in a conversation with a colleague?"
3. Check for repetitive sentence structures
4. Look for clusters of the words listed above
5. Ensure varied sentence lengths (not all similar length)
6. Verify each intensifier adds genuine meaning

---

## 参考资料：references/backlink-strategies.md

# Backlink Strategy Playbooks

Detailed execution guides for each backlink strategy.

---

## Link Stealing Playbook

### Tools Required
- Ahrefs (Site Explorer, Backlinks)
- Hunter.io (email finder)
- Email client or outreach tool

### Step-by-Step Process

**1. Identify Target Keyword**
```
Search: "AI headshot generator"
Find: Top ranking competitor (e.g., Canva)
Note: Exact URL of their ranking page
```

**2. Analyze in Ahrefs**
```
Site Explorer → Enter competitor URL
→ Backlinks tab
→ Filter: Dofollow only
→ Sort by: Domain Rating (high to low)
```

**3. Evaluate Opportunities**
For each linking site, check:
```
□ Is it a blog/content site? (not a directory)
□ Does the article discuss your topic?
□ Is there room to add/replace your link?
□ What's the site's DA? (aim for 30+)
```

**4. Find Contact Info**
```
Hunter.io → Enter article URL
→ Get author/editor email
→ Verify email if possible
```

**5. Craft Outreach**

```
Subject: Re: Your [Article Title] article

Hi [Name],

I came across your piece on [topic] - really thorough comparison.

I noticed you mentioned [Competitor]. We recently launched [Product]
which [specific advantage - e.g., "uses the new Flux model for
2x better quality at half the price"].

Would you be open to testing it? I can set up a free account.
If you think it's worth including, that would be great - but no
pressure either way.

Best,
[Name]
```

**6. Follow-Up Schedule**
- Day 0: Initial email
- Day 4: First follow-up (if no response)
- Day 10: Final follow-up
- Stop after 3 attempts

### Expected Results
- Response rate: 5-15%
- Conversion rate: 2-5% of outreach
- High-quality links from relevant sites

---

## Affiliate Program Playbook

### Setup Phase

**1. Choose Platform**
- Rewardful (recommended): Clean URLs, Stripe integration
- Alternatives: FirstPromoter, PartnerStack
- Budget: ~$200-300/month

**2. Set Commission Structure**
```
Standard: 30% recurring
Competitive: 40% recurring
Aggressive: 50% first payment + 30% recurring
```

**3. Create Affiliate Assets**
- Product screenshots
- Comparison graphics
- Key selling points
- Promo codes for affiliates

### Recruiting Affiliates

**Method 1: Steal Competitor Affiliates**

```
Ahrefs → Site Explorer → competitor.com
→ Backlinks
→ Search: "?via=" or "?ref=" or "/ref/"
→ These are affiliate links
→ Contact each affiliate site
```

**Outreach Template**:
```
Subject: Double your affiliate income?

Hi [Name],

I noticed you're promoting [Competitor] on your site.

We're [Product] - similar product but [key differentiator].
Our conversion rate is [X%] and we're offering 40% commission
(vs their [X%]).

Would you like to test us out? Happy to send free access.

[Name]
```

**Method 2: Affiliate Directories**
- Post on affiliate forums
- List on affiliate networks
- Reach out to affiliate bloggers in niche

### Managing Quality

**Disavow Spammy Links**:
1. Google Search Console → Links
2. Identify low-quality affiliate links
3. Disavow Tool → Upload list
4. Google ignores those links

---

## Domain Acquisition Playbook

### Finding Targets

**1. Identify Candidates**
- Old tool sites in your niche
- Abandoned projects with good DA
- Sites mentioned in old articles

**2. Evaluate in Ahrefs**
```
Check:
- Domain Rating (DR > 30 ideal)
- Number of referring domains
- Backlink quality (high DA sites linking)
- Domain age
- Any spam penalties
```

### Outreach Template

```
Subject: Interested in acquiring [domain]

Hi,

I'm the founder of [Your Company]. I noticed [Domain] and
really appreciate what you built.

Are you open to discussing a potential acquisition? We'd be
interested in taking over the project.

If you're not looking to sell right now, no worries - just
wanted to reach out.

Best,
[Name]
```

### Negotiation Tips
- Start at 50% of asking price
- Use Ahrefs data to justify valuation
- Consider domain age heavily
- Check for any Google penalties first

### Post-Acquisition

**Option 1: Link then Redirect**
1. Keep site running, add links to your main site
2. Wait 1-2 months for Google to crawl
3. Then 301 redirect entire domain

**Option 2: Immediate Redirect**
1. 301 redirect all pages to relevant pages on your site
2. Faster but may lose some link value

---

## HARO Playbook

### Setup

1. Sign up at helpareporter.com
2. Sign up at helpab2bwriter.com
3. Set email frequency: Daily (recommended)
4. Filter by relevant categories

### Daily Process

**Morning (15-30 min)**:
1. Review incoming queries
2. Identify 2-3 relevant opportunities
3. Draft responses

### Response Structure

```
SUBJECT: Re: [Query Topic] - Expert Response

Hi [Reporter Name],

[1-2 sentence intro establishing credibility]

[Direct answer to their question - 100-200 words]

[Supporting example or data point]

[Optional: Offer for follow-up interview]

---
[Name]
[Title], [Company]
[Credentials: X followers, featured in Y, Z years experience]
[Link to profile/site]
```

### Differentiation Tips

**Stand Out from AI Spam**:
- Include Loom video explanation
- Reference specific recent events
- Provide unique data/statistics
- Share personal anecdotes
- Respond within 2 hours of query

### Outsourcing

1. Hire VA to monitor and draft responses
2. VA sends drafts for your review
3. You add personal authority/edits
4. You send final response
5. Cost: ~$500/month for 10-20 responses

---

## Case Study Exchange Playbook

### Finding Opportunities

**Identify Tools You Use**:
```
□ Analytics tools
□ Marketing tools
□ Development tools
□ Design tools
□ Productivity tools
```

**Evaluate Each**:
- Do they have a case studies page?
- How many case studies do they have?
- Are they actively collecting?

**Priority Order**:
1. Tools with <10 case studies (hungry for content)
2. Newer tools building credibility
3. Tools where you have impressive results

### Outreach Template

```
Subject: Case study offer - [Your Company] + [Their Tool]

Hi [Team],

We've been using [Tool] for [duration] and wanted to share
our results:

- [Metric 1: e.g., "Increased conversions by 40%"]
- [Metric 2: e.g., "Saved 10 hours/week"]
- [Metric 3: e.g., "Grew from $5K to $50K MRR"]

Would you be interested in featuring our story? We're happy
to do an interview, provide screenshots, whatever helps.

We'd just ask for a backlink to [your site] in the case study.

Best,
[Name]
[Company]
```

### After Agreement

Be responsive and provide:
- Detailed answers to questions
- Screenshots with permission
- Metrics and data
- Quotes and testimonials
- Logo for their page

---

## Content Ring Playbook

### Planning

**Identify Tool Opportunities**:
```
□ Related to your main product
□ Can be built quickly (1-2 weeks)
□ Has some SEO potential itself
□ Provides genuine user value
```

**Example Ring for HeadshotPro**:
```
Main: HeadshotPro.com (AI headshots)
├── ProfilePicture.ai (free profile pic generator)
├── LinkedInGenerator.com (LinkedIn profile helper)
├── BackgroundRemover.io (background removal tool)
└── PhotoEnhancer.app (image enhancement)
```

### Implementation

**Each Tool Should Have**:
- Real utility (not just a link farm)
- Basic SEO optimization
- Footer link to main product
- Occasional in-content CTAs

**Launch Process**:
1. Build and launch tool
2. Basic SEO setup (title, meta, content)
3. Add links to main product
4. Submit to Product Hunt / directories
5. Let Google index naturally

### Maintenance

- Keep tools functional
- Update occasionally for freshness
- Monitor for any issues
- Don't overdo it (3-5 tools max)

---

## Outreach Email Templates

### Cold Outreach - Feature Request

```
Subject: [Product] for your [content type]?

Hi [Name],

Love your content on [topic]. Your piece on [specific article]
was particularly helpful.

We built [Product] that [key benefit]. Thought it might be
interesting for your readers since [relevance].

Happy to set you up with free access if you'd like to check
it out. No pressure to write about it - just thought you
might find it useful.

Best,
[Name]
```

### Follow-Up Template

```
Subject: Re: [Original subject]

Hi [Name],

Just floating this back up in case it got buried.

Quick reminder: [Product] - [one-line value prop].

If it's not a fit, no worries at all. Just let me know
either way?

Thanks,
[Name]
```

### Broken Link Outreach

```
Subject: Broken link on your [page title]

Hi [Name],

I was reading your article on [topic] and noticed the link
to [broken resource] is no longer working.

I recently published [your content] that covers similar
ground. Might be a good replacement?

[URL]

Either way, wanted to give you a heads up on the broken link.

Best,
[Name]
```

### Guest Post Pitch

```
Subject: Guest post idea: [Topic]

Hi [Name],

I've been following [Site] and really enjoy your content on [niche].

I'd love to contribute a guest post on [specific topic].
I'm thinking something like:

"[Proposed Title]"
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

I'm [brief credentials]. Here are a few examples of my writing:
- [Link 1]
- [Link 2]

Would this be a fit?

Best,
[Name]
```

---

## Tracking Spreadsheet Template

### Outreach Tracker

| Date | Site | Contact | Email | Status | DA | Follow-ups | Result |
|------|------|---------|-------|--------|-----|------------|--------|
| 1/14 | TechBlog | John | john@... | Sent | 45 | 1 | Pending |
| 1/13 | SaaS Review | Sarah | sarah@... | Replied | 52 | 0 | Meeting scheduled |
| 1/10 | AI Weekly | Mike | mike@... | No response | 38 | 3 | Dead |

### Backlink Tracker

| Date Acquired | Source | URL | DA | Anchor Text | Type | Status |
|---------------|--------|-----|-----|-------------|------|--------|
| 1/14 | TechCrunch | /article | 94 | "HeadshotPro" | Editorial | Live |
| 1/10 | Blogger | /review | 35 | "AI headshots" | Affiliate | Live |

### Monthly Metrics

| Month | Outreach Sent | Responses | Links Acquired | Avg DA | High-Value (80+) |
|-------|---------------|-----------|----------------|--------|------------------|
| Jan | 150 | 23 | 8 | 42 | 1 |
| Dec | 120 | 18 | 6 | 38 | 0 |

---

## 参考资料：references/content-patterns.md

# AEO and GEO Content Patterns

Reusable content block patterns optimized for answer engines and AI citation.

---

## Contents
- Answer Engine Optimization (AEO) Patterns (Definition Block, Step-by-Step Block, Comparison Table Block, Pros and Cons Block, FAQ Block, Listicle Block)
- Generative Engine Optimization (GEO) Patterns (Statistic Citation Block, Expert Quote Block, Authoritative Claim Block, Self-Contained Answer Block, Evidence Sandwich Block)
- Domain-Specific GEO Tactics (Technology Content, Health/Medical Content, Financial Content, Legal Content, Business/Marketing Content)
- Voice Search Optimization (Question Formats for Voice, Voice-Optimized Answer Structure)

## Answer Engine Optimization (AEO) Patterns

These patterns help content appear in featured snippets, AI Overviews, voice search results, and answer boxes.

### Definition Block

Use for "What is [X]?" queries.

```markdown
## What is [Term]?

[Term] is [concise 1-sentence definition]. [Expanded 1-2 sentence explanation with key characteristics]. [Brief context on why it matters or how it's used].
```

**Example:**
```markdown
## What is Answer Engine Optimization?

Answer Engine Optimization (AEO) is the practice of structuring content so AI-powered systems can easily extract and present it as direct answers to user queries. Unlike traditional SEO that focuses on ranking in search results, AEO optimizes for featured snippets, AI Overviews, and voice assistant responses. This approach has become essential as over 60% of Google searches now end without a click.
```

### Step-by-Step Block

Use for "How to [X]" queries. Optimal for list snippets.

```markdown
## How to [Action/Goal]

[1-sentence overview of the process]

1. **[Step Name]**: [Clear action description in 1-2 sentences]
2. **[Step Name]**: [Clear action description in 1-2 sentences]
3. **[Step Name]**: [Clear action description in 1-2 sentences]
4. **[Step Name]**: [Clear action description in 1-2 sentences]
5. **[Step Name]**: [Clear action description in 1-2 sentences]

[Optional: Brief note on expected outcome or time estimate]
```

**Example:**
```markdown
## How to Optimize Content for Featured Snippets

Earning featured snippets requires strategic formatting and direct answers to search queries.

1. **Identify snippet opportunities**: Use tools like Semrush or Ahrefs to find keywords where competitors have snippets you could capture.
2. **Match the snippet format**: Analyze whether the current snippet is a paragraph, list, or table, and format your content accordingly.
3. **Answer the question directly**: Provide a clear, concise answer (40-60 words for paragraph snippets) immediately after the question heading.
4. **Add supporting context**: Expand on your answer with examples, data, and expert insights in the following paragraphs.
5. **Use proper heading structure**: Place your target question as an H2 or H3, with the answer immediately following.

Most featured snippets appear within 2-4 weeks of publishing well-optimized content.
```

### Comparison Table Block

Use for "[X] vs [Y]" queries. Optimal for table snippets.

```markdown
## [Option A] vs [Option B]: [Brief Descriptor]

| Feature | [Option A] | [Option B] |
|---------|------------|------------|
| [Criteria 1] | [Value/Description] | [Value/Description] |
| [Criteria 2] | [Value/Description] | [Value/Description] |
| [Criteria 3] | [Value/Description] | [Value/Description] |
| [Criteria 4] | [Value/Description] | [Value/Description] |
| Best For | [Use case] | [Use case] |

**Bottom line**: [1-2 sentence recommendation based on different needs]
```

### Pros and Cons Block

Use for evaluation queries: "Is [X] worth it?", "Should I [X]?"

```markdown
## Advantages and Disadvantages of [Topic]

[1-sentence overview of the evaluation context]

### Pros

- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]
- **[Benefit category]**: [Specific explanation]

### Cons

- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]
- **[Drawback category]**: [Specific explanation]

**Verdict**: [1-2 sentence balanced conclusion with recommendation]
```

### FAQ Block

Use for topic pages with multiple common questions. Essential for FAQ schema.

```markdown
## Frequently Asked Questions

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].

### [Question phrased exactly as users search]?

[Direct answer in first sentence]. [Supporting context in 2-3 additional sentences].
```

**Tips for FAQ questions:**
- Use natural question phrasing ("How do I..." not "How does one...")
- Include question words: what, how, why, when, where, who, which
- Match "People Also Ask" queries from search results
- Keep answers between 50-100 words

### Listicle Block

Use for "Best [X]", "Top [X]", "[Number] ways to [X]" queries.

```markdown
## [Number] Best [Items] for [Goal/Purpose]

[1-2 sentence intro establishing context and selection criteria]

### 1. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]

### 2. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]

### 3. [Item Name]

[Why it's included in 2-3 sentences with specific benefits]
```

---

## Generative Engine Optimization (GEO) Patterns

These patterns optimize content for citation by AI assistants like ChatGPT, Claude, Perplexity, and Gemini.

### Statistic Citation Block

Statistics increase AI citation rates by 15-30%. Always include sources.

```markdown
[Claim statement]. According to [Source/Organization], [specific statistic with number and timeframe]. [Context for why this matters].
```

**Example:**
```markdown
Mobile optimization is no longer optional for SEO success. According to Google's 2024 Core Web Vitals report, 70% of web traffic now comes from mobile devices, and pages failing mobile usability standards see 24% higher bounce rates. This makes mobile-first indexing a critical ranking factor.
```

### Expert Quote Block

Named expert attribution adds credibility and increases citation likelihood.

```markdown
"[Direct quote from expert]," says [Expert Name], [Title/Role] at [Organization]. [1 sentence of context or interpretation].
```

**Example:**
```markdown
"The shift from keyword-driven search to intent-driven discovery represents the most significant change in SEO since mobile-first indexing," says Rand Fishkin, Co-founder of SparkToro. This perspective highlights why content strategies must evolve beyond traditional keyword optimization.
```

### Authoritative Claim Block

Structure claims for easy AI extraction with clear attribution.

```markdown
[Topic] [verb: is/has/requires/involves] [clear, specific claim]. [Source] [confirms/reports/found] that [supporting evidence]. This [explains/means/suggests] [implication or action].
```

**Example:**
```markdown
E-E-A-T is the cornerstone of Google's content quality evaluation. Google's Search Quality Rater Guidelines confirm that trust is the most critical factor, stating that "untrustworthy pages have low E-E-A-T no matter how experienced, expert, or authoritative they may seem." This means content creators must prioritize transparency and accuracy above all other optimization tactics.
```

### Self-Contained Answer Block

Create quotable, standalone statements that AI can extract directly.

```markdown
**[Topic/Question]**: [Complete, self-contained answer that makes sense without additional context. Include specific details, numbers, or examples in 2-3 sentences.]
```

**Example:**
```markdown
**Ideal blog post length for SEO**: The optimal length for SEO blog posts is 1,500-2,500 words for competitive topics. This range allows comprehensive topic coverage while maintaining reader engagement. HubSpot research shows long-form content earns 77% more backlinks than short articles, directly impacting search rankings.
```

### Evidence Sandwich Block

Structure claims with evidence for maximum credibility.

```markdown
[Opening claim statement].

Evidence supporting this includes:
- [Data point 1 with source]
- [Data point 2 with source]
- [Data point 3 with source]

[Concluding statement connecting evidence to actionable insight].
```

---

## Domain-Specific GEO Tactics

Different content domains benefit from different authority signals.

### Technology Content
- Emphasize technical precision and correct terminology
- Include version numbers and dates for software/tools
- Reference official documentation
- Add code examples where relevant

### Health/Medical Content
- Cite peer-reviewed studies with publication details
- Include expert credentials (MD, RN, etc.)
- Note study limitations and context
- Add "last reviewed" dates

### Financial Content
- Reference regulatory bodies (SEC, FTC, etc.)
- Include specific numbers with timeframes
- Note that information is educational, not advice
- Cite recognized financial institutions

### Legal Content
- Cite specific laws, statutes, and regulations
- Reference jurisdiction clearly
- Include professional disclaimers
- Note when professional consultation is advised

### Business/Marketing Content
- Include case studies with measurable results
- Reference industry research and reports
- Add percentage changes and timeframes
- Quote recognized thought leaders

---

## Voice Search Optimization

Voice queries are conversational and question-based. Optimize for these patterns:

### Question Formats for Voice
- "What is..."
- "How do I..."
- "Where can I find..."
- "Why does..."
- "When should I..."
- "Who is..."

### Voice-Optimized Answer Structure
- Lead with direct answer (under 30 words ideal)
- Use natural, conversational language
- Avoid jargon unless targeting expert audience
- Include local context where relevant
- Structure for single spoken response

---

## 参考资料：references/content-templates.md

# GEO/AEO Content Templates

## Table of Contents
1. [Definitional Content Template](#definitional-content-template)
2. [How-To Content Template](#how-to-content-template)
3. [Comparison Content Template](#comparison-content-template)
4. [FAQ-Optimized Template](#faq-optimized-template)
5. [Product/Service Template](#productservice-template)
6. [Writing Guidelines](#writing-guidelines)

---

## Definitional Content Template

**Best for:** "What is X?" queries, concept explanations

```markdown
# What is [Topic]? [Subtitle with Context]

**TL;DR:** [Topic] is [concise 1-sentence definition]. [1-2 sentences on why it matters or key application].

## Definition

[Topic] is [expanded definition in 2-3 sentences]. [Include key characteristics].

> **Quick Definition:** [15-word definition suitable for snippet extraction]

## How [Topic] Works

[Explanation paragraph - use simple, clear language]

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| [Item 1] | [What it does] | [Concrete example] |
| [Item 2] | [What it does] | [Concrete example] |
| [Item 3] | [What it does] | [Concrete example] |

## Benefits of [Topic]

1. **[Benefit 1]**: [Explanation in 1-2 sentences]
2. **[Benefit 2]**: [Explanation in 1-2 sentences]
3. **[Benefit 3]**: [Explanation in 1-2 sentences]

## Common Use Cases

- **[Use case 1]**: [Brief description]
- **[Use case 2]**: [Brief description]
- **[Use case 3]**: [Brief description]

## FAQ

### What is the difference between [Topic] and [Related Topic]?
[Clear answer in 2-3 sentences]

### Who should use [Topic]?
[Clear answer identifying target audience]

### How do I get started with [Topic]?
[Actionable first steps]

## Summary

[2-3 sentence recap of key points - this is another extraction opportunity]

---
*Last updated: [Date] | Author: [Name, Credentials]*
*Sources: [List key sources for credibility]*
```

---

## How-To Content Template

**Best for:** Process queries, tutorials, step-by-step guides

```markdown
# How to [Action]: [Subtitle with Benefit]

**TL;DR:** To [action], you need to [high-level steps in 1 sentence]. This process takes approximately [time estimate] and requires [key requirements].

## Quick Overview

| | |
|---|---|
| **Time Required** | [X minutes/hours] |
| **Difficulty** | [Beginner/Intermediate/Advanced] |
| **What You'll Need** | [Key requirements] |
| **Expected Result** | [What user will achieve] |

## Before You Start

### Prerequisites
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Tools/Materials Needed
- [Tool 1] - [why needed]
- [Tool 2] - [why needed]

## Step-by-Step Instructions

### Step 1: [Action Verb +
