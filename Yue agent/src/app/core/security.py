import base64
import hashlib
import hmac
import json
import time
from typing import Any

from app.exceptions.auth import InvalidTokenError, TokenExpiredError
from settings import settings

"""
    ═══════════════════════════════════════════════════
                 Token 签发与校验（HMAC-SHA256）
    ═══════════════════════════════════════════════════

    token 结构：
        base64url(payload) . base64url(HMAC-SHA256(secret, payload))

    payload：
        {"iat": 签发时间, "exp": 过期时间}   （Unix 秒）
"""

# 允许客户端时钟最多超前 60 秒
CLOCK_SKEW = 60


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(payload_part: str, secret: str | None = None) -> str:
    digest = hmac.new(
        (secret or settings.AUTH_TOKEN).encode("utf-8"),
        payload_part.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return _b64url_encode(digest)


def create_token(ttl: int = 300) -> str:
    """后端测试/调试用；正式签发在前端完成。"""
    now = int(time.time())
    payload = json.dumps(
        {"iat": now, "exp": now + ttl},
        separators=(",", ":"),
    )
    payload_part = _b64url_encode(payload.encode("utf-8"))
    return f"{payload_part}.{_sign(payload_part)}"


def verify_signed_token(token: str) -> dict[str, Any]:
    try:
        payload_part, signature = token.split(".", 1)

        if not hmac.compare_digest(signature, _sign(payload_part)):
            raise InvalidTokenError()

        payload = json.loads(_b64url_decode(payload_part))
        exp = int(payload["exp"])
        iat = int(payload.get("iat", 0))
    except InvalidTokenError:
        raise
    except (ValueError, KeyError, TypeError):
        # base64 非法、JSON 损坏、缺字段，统一按无效 token 处理
        raise InvalidTokenError()

    now = int(time.time())

    if exp <= now:
        raise TokenExpiredError()

    if iat > now + CLOCK_SKEW:
        raise InvalidTokenError("Token 时间异常")

    return payload


""" ── 管理后台会话 ─────────────────────────────────────
    独立于 AUTH_TOKEN 的签名密钥，结构复用上面的 payload.signature。
    cookie 里只放 sub/iat/exp，不存密码。
"""

ADMIN_COOKIE_NAME = "yue_admin"


def verify_admin_credentials(username: str, password: str) -> bool:
    """常量时间比较，避免用户名/密码被计时侧信道猜解。"""
    username_ok = hmac.compare_digest(
        username.encode("utf-8"), settings.ADMIN_USERNAME.encode("utf-8")
    )
    password_ok = hmac.compare_digest(
        password.encode("utf-8"), settings.ADMIN_PASSWORD.encode("utf-8")
    )
    return username_ok and password_ok


def create_admin_session(username: str) -> str:
    now = int(time.time())
    payload = json.dumps(
        {
            "sub": username,
            "iat": now,
            "exp": now + settings.ADMIN_SESSION_TTL,
        },
        separators=(",", ":"),
    )
    payload_part = _b64url_encode(payload.encode("utf-8"))
    return f"{payload_part}.{_sign(payload_part, settings.ADMIN_SESSION_SECRET)}"


def verify_admin_session(token: str | None) -> dict[str, Any] | None:
    """校验失败一律返回 None，由调用方决定跳登录还是 401。"""
    if not token:
        return None
    try:
        payload_part, signature = token.split(".", 1)
        expected = _sign(payload_part, settings.ADMIN_SESSION_SECRET)
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(_b64url_decode(payload_part))
        if payload.get("sub") != settings.ADMIN_USERNAME:
            return None
        if int(payload["exp"]) <= int(time.time()):
            return None
        return payload
    except (ValueError, KeyError, TypeError):
        return None


def create_csrf_token(session_token: str) -> str:
    return _sign(session_token, settings.ADMIN_SESSION_SECRET)


def verify_csrf_token(session_token: str, token: str) -> bool:
    return hmac.compare_digest(token, create_csrf_token(session_token))
