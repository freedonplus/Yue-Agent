import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import AppException


"""
    ═══════════════════════════════════════════════════
                        全局异常捕获
    ═══════════════════════════════════════════════════
"""



logger = logging.getLogger(__name__)

def error_body(code: str, message: str, detail=None, request_id: str | None = None):
    return {
        "code": code,
        "message": message,
        "detail": detail,
        "request_id": request_id,
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(
                exc.code, exc.message, exc.detail,
                getattr(request.state, "request_id", None),
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        # errors() 的 ctx 里可能带 ValueError 等异常对象，不能直接 JSON 序列化
        details = [
            {
                "loc": list(err.get("loc", ())),
                "msg": err.get("msg", ""),
                "type": err.get("type", ""),
                "input": err.get("input"),
            }
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=error_body(
                "VALIDATION_ERROR", "参数校验失败", details,
                getattr(request.state, "request_id", None),
            ),
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError):
        logger.warning("database integrity error: %s", exc)
        return JSONResponse(
            status_code=409,
            content=error_body(
                "DB_CONFLICT", "数据冲突",
                getattr(request.state, "request_id", None),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(
                "HTTP_ERROR", str(exc.detail),
                getattr(request.state, "request_id", None),
            ),
            # 保留 Location / WWW-Authenticate 等响应头，
            # 后台守卫的 303 跳转依赖这里
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        logger.exception("unhandled error: %s", exc)
        return JSONResponse(
            status_code=500,
            content=error_body(
                "INTERNAL_ERROR", "服务器内部错误",
                getattr(request.state, "request_id", None),
            ),
        )
