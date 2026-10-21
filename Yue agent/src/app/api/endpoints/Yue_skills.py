from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.skills import SkillOut, SkillSummaryOut
from app.services import skill_service

"""
    ═══════════════════════════════════════════════════
                        技能接口（只读）
    ═══════════════════════════════════════════════════

    GET /api/skills          技能列表（前端用来渲染技能选择框）
    GET /api/skills/{id}     技能详情

    创建 / 修改 / 删除仅限管理后台 /admin/skills。
    技能是全局的：前端列出所有技能，由用户在对话请求里通过
    skill_slug 指定本次任务使用哪一个，不需要挂载给员工。
"""

router = APIRouter()


@router.get("", response_model=list[SkillOut])
async def list_skills(session: AsyncSession = Depends(get_session)):
    return await skill_service.list_skills(session)


# —————————轻量列表：前端选择技能时只需要名称和描述————————
@router.get("/summary", response_model=list[SkillSummaryOut])
async def list_skill_summaries(session: AsyncSession = Depends(get_session)):
    return await skill_service.list_skill_summaries(session)


@router.get("/{skill_id}", response_model=SkillOut)
async def get_skill(
    skill_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await skill_service.get_skill(session, skill_id)
