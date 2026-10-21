import sys
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
    ═══════════════════════════════════════════════════
                        全局系统配置
    ═══════════════════════════════════════════════════
"""

# 打包成单文件 exe（PyInstaller）后，__file__ 位于临时解压目录 _MEIPASS，
# 不能用来定位 .env / data。此时改用 exe 自身所在目录，保证配置和数据库
# 落在安装目录旁，重启后持久保留。
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        validate_default=True,
        case_sensitive=True,     # 环境变量名大小写敏感，字段名必须和 .env 一模一样
        extra="allow",          # .env 里有本类没声明的变量时，忽略而不是报错
    )

    # ── 应用配置 ──────────────────────────────────────
    APP_NAME: str = "Yue Agent"
    APP_VERSION: str = "0.1.0"
    APP_DEBUG: bool = False
    # 本地开发自动重载；生产环境设为 False，避免文件监听开销
    APP_RELOAD: bool = True
    APP_OPENAPI_URL: str = "/openapi.json"   # 置空（APP_OPENAPI_URL=）即关闭
    LOG_LEVEL: str = "INFO"
    # 流式调用时向厂商请求 token 用量（stream_options.include_usage）；
    # 个别 OpenAI 兼容端点不认这个字段时置 False，代价是拿不到 token 统计
    MODEL_STREAM_USAGE: bool = True
    # 可选的工作区列表（JSON 数组）：
    # [{"id": "yue", "name": "Yue Agent", "root_path": "C:/Users/tzy88/Desktop/Yue Agent"}]
    # 留空时自动使用项目目录、上级目录和用户主目录
    WORKSPACES: list[dict] = Field(default_factory=list)

    # ── CORS 跨域配置 ─────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    CORS_ALLOW_CREDENTIALS: bool = False

    # ── 认证 ──────────────────────────────────────────
    # 前后端共享的 HMAC 签名密钥；前端用它签发带 exp 的 token
    AUTH_TOKEN: str = Field(min_length=16)

    # ── 管理后台 ──────────────────────────────────────
    # 管理员账号密码（明文放在 .env，切勿提交到仓库）
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = Field(min_length=8)
    # 后台登录 cookie 的签名密钥，必须和 AUTH_TOKEN 不同：
    # AUTH_TOKEN 会下发到前端，不能拿来签管理员会话
    ADMIN_SESSION_SECRET: str = Field(min_length=32)
    ADMIN_SESSION_TTL: int = Field(default=3600, ge=60, le=86400)
    # 走 HTTPS 时置 True
    ADMIN_COOKIE_SECURE: bool = False

    # ── 数据库连接配置 ────────────────────────────────
    DB_PATH: Path = DATA_DIR / "yue.db"
    POOL_SIZE: int = Field(default=5, ge=1, le=20)
    MAX_OVERFLOW: int = Field(default=5, ge=0, le=20)
    POOL_TIMEOUT: int = Field(default=30, ge=1)
    SQLALCHEMY_ECHO: bool = False

    # ── 校验 ──────────────────────────────────────────
    @field_validator("DB_PATH", mode="before")
    @classmethod
    def _db_path(cls, v: object) -> Path:
        raw = str(v).strip() if v is not None else ""
        p = Path(raw).expanduser() if raw else DATA_DIR / "yue.db"
        if not p.is_absolute():
            p = BASE_DIR / p
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def _upper_log_level(cls, v: object) -> str:
        return str(v).strip().upper() or "INFO"

    @model_validator(mode="after")
    def _cors_credential_check(self):
        if self.CORS_ALLOW_CREDENTIALS and "*" in self.cors_origin_list:
            raise ValueError("CORS_ALLOW_CREDENTIALS=True 时 CORS_ORIGINS 不能为 '*'")
        return self

    # ── 派生属性 ──────────────────────────────────────
    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
