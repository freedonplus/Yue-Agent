from app.core.exceptions import AppException


class AuthError(AppException):
    status_code = 401
    code = "AUTH_ERROR"
    default_message = "认证失败"


class NotAuthenticatedError(AuthError):
    status_code = 401
    code = "NOT_AUTHENTICATED"
    default_message = "缺少 Token"


class InvalidTokenError(AuthError):
    status_code = 401
    code = "INVALID_TOKEN"
    default_message = "Token 无效"


class TokenExpiredError(AuthError):
    status_code = 401
    code = "TOKEN_EXPIRED"
    default_message = "Token 已过期"
