from app.core.exceptions import AppException


class SkillError(AppException):
    """skill 模块所有异常的父类。"""
    status_code = 400
    code = "SKILL_ERROR"
    default_message = "技能操作失败"


class SkillNotFoundError(SkillError):
    status_code = 404
    code = "SKILL_NOT_FOUND"
    default_message = "技能不存在"


class SkillSlugExistsError(SkillError):
    status_code = 409
    code = "SKILL_SLUG_EXISTS"
    default_message = "技能 slug 已存在"
