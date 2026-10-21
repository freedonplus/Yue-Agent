from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    ═══════════════════════════════════════════════════
                        技能 Schema
    ═══════════════════════════════════════════════════

    技能内容沿用 SKILL.md 约定：可选的 YAML frontmatter
    （name / description）+ Markdown 正文。
"""

SLUG_PATTERN = r"^[a-z0-9][a-z0-9_-]*$"


# —————————拆分 SKILL.md 的 frontmatter 与正文————————
def parse_skill_markdown(raw: str) -> tuple[dict[str, str], str]:
    """返回 (meta, body)。

    只解析最简单的 key: value 形式，不引入 YAML 依赖；
    解析不了时把整段当成正文，不让导入失败。
    """
    text = (raw or "").replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        return {}, text.strip()

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text.strip()

    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip()] = value

    body = text[end + 4 :].lstrip("\n").strip()
    return meta, body


class SkillCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str = Field(min_length=1, max_length=50, pattern=SLUG_PATTERN)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=2000)
    content: str = Field(min_length=1, max_length=500_000)
    source_path: str = Field(default="", max_length=300)
    enabled: bool = True


class SkillUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=SLUG_PATTERN
    )
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    content: str | None = Field(default=None, min_length=1, max_length=500_000)
    enabled: bool | None = None


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    description: str
    content: str
    source_path: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("source_path", mode="before")
    @classmethod
    def _default_source_path(cls, v):
        return v or ""


class SkillSummaryOut(BaseModel):
    """轻量列表：不返回 content，避免一次传输几百 KB 的技能正文。"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    description: str
    source_path: str
    enabled: bool
    updated_at: datetime

    @field_validator("source_path", mode="before")
    @classmethod
    def _default_source_path(cls, v):
        return v or ""
