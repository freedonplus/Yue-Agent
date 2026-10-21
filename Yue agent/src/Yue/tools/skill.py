from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

"""
    ═══════════════════════════════════════════════════
                        技能加载工具
    ═══════════════════════════════════════════════════

    技能正文可能很长（例如整份写作规范），不适合全部塞进系统提示词。
    这里按「渐进披露」处理：工具描述里只放技能名和简介，
    模型真正需要时再调用 load_skill 读取全文。
    技能是全局的，所有启用技能对所有员工可用，无需挂载。
"""


class LoadSkillArgs(BaseModel):
    skill: str = Field(description="要加载的技能 slug 或名称，从可用技能列表里选")


def make_skill_tool(skills: list):
    """生成 load_skill 工具；skills 传全局已启用的技能。"""
    usable = [skill for skill in skills if getattr(skill, "enabled", True)]
    if not usable:
        return None

    by_slug = {skill.slug.lower(): skill for skill in usable}
    by_name = {skill.name: skill for skill in usable}
    catalog = "\n".join(
        f"- {skill.slug}：{skill.name}"
        + (f" —— {skill.description}" if skill.description else "")
        for skill in usable
    )

    def load_skill(skill: str) -> str:
        key = (skill or "").strip()
        found = by_slug.get(key.lower()) or by_name.get(key)
        if found is None:
            return (
                f"没有找到技能「{key}」。可用技能：\n{catalog}"
            )
        return (
            f"【技能：{found.name}】\n"
            f"技能 slug：{found.slug}\n\n"
            f"{found.content}"
        )

    return StructuredTool.from_function(
        func=load_skill,
        name="load_skill",
        description=(
            "加载一项技能的完整工作说明。\n"
            "用户指定了技能时，本次任务必须按该技能执行；"
            "没有指定时，在开始相关任务前先调用它，一次只加载当前任务需要的技能。\n"
            f"可用技能：\n{catalog}"
        ),
        args_schema=LoadSkillArgs,
    )
