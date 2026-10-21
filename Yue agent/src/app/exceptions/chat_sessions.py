from app.core.exceptions import AppException

"""
    ═══════════════════════════════════════════════════
                    会话模块异常
    ═══════════════════════════════════════════════════
"""


class SessionError(AppException):
    """会话模块所有异常的父类。"""

    status_code = 400
    code = "SESSION_ERROR"
    default_message = "会话操作失败"


class SessionNotFoundError(SessionError):
    status_code = 404
    code = "SESSION_NOT_FOUND"
    default_message = "会话不存在"


class SessionExistsError(SessionError):
    status_code = 409
    code = "SESSION_EXISTS"
    default_message = "session_id 已存在"
