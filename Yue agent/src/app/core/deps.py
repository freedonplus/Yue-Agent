from urllib.parse import quote

from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import (
    ADMIN_COOKIE_NAME,
    verify_admin_session,
    verify_signed_token,
)
from app.exceptions.auth import NotAuthenticatedError

"""
    ═══════════════════════════════════════════════════
                    全局依赖：权限认证
    ═══════════════════════════════════════════════════
"""

# auto_error=False：缺少请求头时返回 None，交给统一异常处理
bearer_scheme = HTTPBearer(auto_error=False)


async def verify_token(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
) -> dict:
    if credentials is None:
        raise NotAuthenticatedError()

    return verify_signed_token(credentials.credentials)


async def require_admin(request: Request) -> dict:
    """管理后台的 HTML 路由守卫：未登录直接 303 跳登录页。"""
    payload = verify_admin_session(request.cookies.get(ADMIN_COOKIE_NAME))
    if payload is None:
        next_path = quote(request.url.path, safe="")
        raise HTTPException(
            status_code=303,
            headers={"Location": f"/admin/login?next={next_path}"},
        )
    return payload
