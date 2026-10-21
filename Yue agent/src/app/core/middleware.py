import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request


"""
    ═══════════════════════════════════════════════════
                     Middleware：全局环绕
      适合：TraceID、访问日志、耗时统计、CORS、请求体大小限制。
        客户端请求
     │
     ▼
  RequestContextMiddleware.dispatch
     │ ① 取/生成 request_id
     │ ② 存到 request.state
     │ ③ 开始计时
     │ ④ await call_next(request)
     │        │
     │        ▼
     │   其他中间件 → 依赖 → 路由函数 → 返回 Response
     │        │
     │ ⑤ 出错了 → logger.exception → raise
     │ ⑥ 算耗时
     │ ⑦ 加响应头
     │ ⑧ 打日志
     │ ⑨ return response
     ▼
  客户端收到响应（带 X-Request-ID / X-Process-Time-Ms）
    ═══════════════════════════════════════════════════
"""

logger = logging.getLogger("app.request")


class SelectiveGZipMiddleware:
    """压缩普通响应，跳过 SSE。

    SSE 需要逐条实时推送，压缩后部分代理会缓冲，反而破坏流式效果。
    """

    # 对话与管理后台调试流都走 SSE
    _SKIP_PREFIXES = ("/api/chat", "/admin/playground")

    def __init__(self, app, minimum_size: int = 1024) -> None:
        self.app = app
        self._gzip = GZipMiddleware(app, minimum_size=minimum_size)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            if not path.startswith(self._SKIP_PREFIXES):
                await self._gzip(scope, receive, send)
                return
        await self.app(scope, receive, send)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.state.request_id = request_id

        start = time.perf_counter()
        try:
            logger.info("="*100)
            logger.info("-" *70)
            response = await call_next(request)
            cost_ms = (time.perf_counter() - start) * 1000
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time-Ms"] = f"{cost_ms:.2f}"
            logger.info("%s %s -> %s | %.2fms | id=%s",
                        request.method, request.url.path,
                        response.status_code, cost_ms, request_id)
        except Exception:
            logger.exception("unhandled | id=%s %s %s",
                             request_id, request.method, request.url.path)
            raise
        finally:
            logger.info("-" * 70)
            logger.info("=" * 100)




        return response