import re
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.skills import SkillError, SkillNotFoundError, SkillSlugExistsError
from app.model.skills import Skills
from app.schemas.skills import SLUG_PATTERN, SkillCreate, SkillUpdate, parse_skill_markdown

"""
    ═══════════════════════════════════════════════════
                      技能业务逻辑
    ═══════════════════════════════════════════════════
"""

MAX_IMPORT_BYTES = 500_000


# —————————技能列表：后台展示全部（含停用）————————
async def list_skills(session: AsyncSession) -> list[Skills]:
    stmt = select(Skills).order_by(Skills.name.asc(), Skills.created_at.asc())
    return list((await session.execute(stmt)).scalars().all())


# —————————轻量技能列表：只取元数据，不读大段正文————————
async def list_skill_summaries(session: AsyncSession) -> list[dict]:
    stmt = (
        select(
            Skills.id,
            Skills.slug,
            Skills.name,
            Skills.description,
            Skills.source_path,
            Skills.enabled,
            Skills.updated_at,
        )
        .order_by(Skills.name.asc(), Skills.created_at.asc())
    )
    rows = (await session.execute(stmt)).all()
    return [dict(row._mapping) for row in rows]


# —————————获取单个技能————————
async def get_skill(session: AsyncSession, skill_id: str) -> Skills:
    skill = await session.get(Skills, skill_id)
    if skill is None:
        raise SkillNotFoundError()
    return skill


# —————————按 slug 查找已启用的技能（对话时用户指定用）————————
async def find_enabled_skill(
    session: AsyncSession, slug: str
) -> Skills | None:
    slug = (slug or "").strip().lower()
    if not slug:
        return None
    return await session.scalar(
        select(Skills).where(
            Skills.slug == slug,
            Skills.enabled.is_(True),
        )
    )


# —————————slug 唯一性校验————————
async def _ensure_slug_available(
    session: AsyncSession, slug: str, *, exclude_id: str | None = None
) -> None:
    stmt = select(Skills.id).where(Skills.slug == slug)
    if exclude_id:
        stmt = stmt.where(Skills.id != exclude_id)
    if await session.scalar(stmt):
        raise SkillSlugExistsError()


# —————————创建技能————————
async def create_skill(session: AsyncSession, data: SkillCreate) -> Skills:
    await _ensure_slug_available(session, data.slug)

    skill = Skills(**data.model_dump())
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill


# —————————更新技能：只改传入字段————————
async def update_skill(
    session: AsyncSession, skill_id: str, data: SkillUpdate
) -> Skills:
    skill = await get_skill(session, skill_id)
    changes = data.model_dump(exclude_unset=True)

    if "slug" in changes and changes["slug"] != skill.slug:
        await _ensure_slug_available(
            session, changes["slug"], exclude_id=skill.id
        )

    for field, value in changes.items():
        setattr(skill, field, value)

    await session.commit()
    await session.refresh(skill)
    return skill


# —————————删除技能————————
async def delete_skill(session: AsyncSession, skill_id: str) -> None:
    skill = await get_skill(session, skill_id)
    await session.delete(skill)
    await session.commit()


# —————————从 skills/<slug>/SKILL.md 导入 / 更新技能————————
async def import_skills_from_directory(
    session: AsyncSession, directory: Path
) -> dict:
    """按目录名作为 slug 导入；已存在则覆盖名称、描述和正文。

    返回 {"created": n, "updated": n, "skipped": [原因...]}。
    """
    if not directory.is_dir():
        raise SkillError(f"技能目录不存在：{directory}")

    created = 0
    updated = 0
    skipped: list[str] = []

    for path in sorted(directory.glob("*/SKILL.md")):
        slug = path.parent.name.strip().lower()
        if not re.fullmatch(SLUG_PATTERN, slug):
            skipped.append(f"{path.parent.name}：目录名不是合法 slug")
            continue

        try:
            if path.stat().st_size > MAX_IMPORT_BYTES:
                skipped.append(f"{path.parent.name}：文件超过 {MAX_IMPORT_BYTES} 字节")
                continue
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            skipped.append(f"{path.parent.name}：读取失败（{exc}）")
            continue

        meta, body = parse_skill_markdown(raw)
        if not body:
            skipped.append(f"{path.parent.name}：正文为空")
            continue

        name = (meta.get("name") or slug)[:100]
        description = meta.get("description", "")[:2000]
        source_path = path.relative_to(directory.parent).as_posix()

        existing = await session.scalar(
            select(Skills).where(Skills.slug == slug)
        )
        if existing is None:
            session.add(
                Skills(
                    slug=slug,
                    name=name,
                    description=description,
                    content=body,
                    source_path=source_path,
                    enabled=True,
                )
            )
            created += 1
        else:
            existing.name = name
            existing.description = description
            existing.content = body
            existing.source_path = source_path
            updated += 1

    await session.commit()
    return {"created": created, "updated": updated, "skipped": skipped}
