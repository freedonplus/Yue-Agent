from app.core.exceptions import AppException


class ToolError(AppException):
    """tool 模块所有异常的父类。"""
    status_code = 400
    code = "TOOL_ERROR"
    default_message = "工具操作失败"


class ToolNotFoundError(ToolError):
    status_code = 404
    code = "TOOL_NOT_FOUND"
    default_message = "工具不存在"


class ToolSlugExistsError(ToolError):
    status_code = 409
    code = "TOOL_SLUG_EXISTS"
    default_message = "工具 slug 已存在"


class ToolConfigError(ToolError):
    status_code = 400
    code = "TOOL_CONFIG_INVALID"
    default_message = "MCP 配置不合法"
