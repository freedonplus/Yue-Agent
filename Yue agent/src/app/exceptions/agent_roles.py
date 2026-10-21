from app.core.exceptions import AppException


class AgentError(AppException):
    """agent 模块所有异常的父类。"""
    status_code = 400
    code = "AGENT_ERROR"
    default_message = "员工操作失败"


class AgentNotFoundError(AgentError):
    status_code = 404
    code = "AGENT_NOT_FOUND"
    default_message = "员工不存在"


class AgentSlugExistsError(AgentError):
    status_code = 409
    code = "AGENT_SLUG_EXISTS"
    default_message = "slug 已存在"


class AgentProviderNotFoundError(AgentError):
    status_code = 400
    code = "AGENT_PROVIDER_NOT_FOUND"
    default_message = "指定的厂商不存在"


class AgentSupervisorExistsError(AgentError):
    status_code = 409
    code = "AGENT_SUPERVISOR_EXISTS"
    default_message = "系统中已存在调度员，且只允许一个"


class AgentSupervisorLockedError(AgentError):
    status_code = 409
    code = "AGENT_SUPERVISOR_LOCKED"
    default_message = "唯一调度员不可删除、降级或停用"
