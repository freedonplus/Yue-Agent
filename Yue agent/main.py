import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402
from app.api.router import api_router  # noqa: E402
from app.core.database import close_db, init_db  # noqa: E402
from app.core.exception_handlers import register_exception_handlers  # noqa: E402
from app.core.deps import verify_token  # noqa: E402
from app.core.middleware import (  # noqa: E402
    RequestContextMiddleware,
    SelectiveGZipMiddleware,
)
from settings import BASE_DIR, settings  # noqa: E402
from app.api.endpoints import (Yue_admin,
                               Yue_docs,
                               Yue_root)

"""
    ═══════════════════════════════════════════════════
                项目启动入口（右键运行）
    ═══════════════════════════════════════════════════
"""

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("database initialized ------")
    yield
    await close_db()
    logger.info("database closed ------")


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.APP_DEBUG,
    openapi_url=settings.APP_OPENAPI_URL,
    docs_url=None,    # 关掉默认 /docs，避免挡住自定义路由
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SelectiveGZipMiddleware, minimum_size=1024)
app.add_middleware(RequestContextMiddleware)
register_exception_handlers(app)

app.include_router(Yue_root.router)
app.include_router(Yue_docs.router)
app.include_router(Yue_admin.router)
app.include_router(api_router,
                   prefix="/api")
# app.include_router(api_router,
#                    prefix="/api",
#                    dependencies=[Depends(verify_token)])


if __name__ == "__main__":
    # 必须以 "模块:属性" 字符串传入，reload=True 才生效。
    # 只监听项目目录，排除 .venv / data / 缓存，避免安装依赖时误触发重启。
    run_kwargs: dict = {"host": "127.0.0.1", "port": 8000}
    if settings.APP_RELOAD:
        run_kwargs.update(
            reload=True,
            reload_dirs=[str(BASE_DIR)],
            reload_excludes=[
                ".venv",
                ".idea",
                "data",
                "__pycache__",
                "*.pyc",
                "*.pyo",
                "*.log",
            ],
        )
    uvicorn.run("main:app", **run_kwargs)
