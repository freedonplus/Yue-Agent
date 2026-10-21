from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import JSONResponse

from settings import settings

"""
    ═══════════════════════════════════════════════════
                         Api 文档
    ═══════════════════════════════════════════════════

    main.py 里 docs_url=None、redoc_url=None，
    所以这里手动注册 /docs 和 /redoc。

    文档页是浏览器直接打开的，不能挂鉴权依赖，
    否则页面本身会先返回 401。
"""

router = APIRouter(tags=["docs"])


def _openapi_url(request: Request) -> str | None:
    return request.app.openapi_url


@router.get("/docs", include_in_schema=False)
async def swagger_ui(request: Request):
    openapi_url = _openapi_url(request)
    if not openapi_url:
        return JSONResponse({"message": "OpenAPI 已关闭"}, status_code=404)

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=f"{settings.APP_NAME} - Swagger UI",
        # 刷新页面后保留已输入的 Bearer token
        swagger_ui_parameters={"persistAuthorization": True},
    )


@router.get("/redoc", include_in_schema=False)
async def redoc(request: Request):
    openapi_url = _openapi_url(request)
    if not openapi_url:
        return JSONResponse({"message": "OpenAPI 已关闭"}, status_code=404)

    return get_redoc_html(
        openapi_url=openapi_url,
        title=f"{settings.APP_NAME} - ReDoc",
    )


@router.get("/docs/info", include_in_schema=False)
async def docs_info(request: Request):
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "swagger_ui": str(request.url_for("swagger_ui")),
        "redoc": str(request.url_for("redoc")),
        "openapi": _openapi_url(request),
    }
