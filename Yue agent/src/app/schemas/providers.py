from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

"""
    ═══════════════════════════════════════════════════
                        厂商 Schema
    ═══════════════════════════════════════════════════
"""

SLUG_PATTERN = r"^[a-z0-9][a-z0-9_-]*$"


class ProviderCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str = Field(min_length=1, max_length=50, pattern=SLUG_PATTERN)
    name: str = Field(min_length=1, max_length=100)
    base_url: str = Field(min_length=1, max_length=255)
    api_key: str | None = Field(default=None, max_length=255)
    default_model: str | None = Field(default=None, max_length=100)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=4096, gt=0)
    max_retries: int = Field(default=3, ge=0, le=10)
    request_timeout: int = Field(default=60, gt=0)
    enabled: bool = True
    is_default: bool = False

    @field_validator("base_url")
    @classmethod
    def _check_base_url(cls, v: str) -> str:
        v = v.rstrip("/")
        if not v.startswith(("http://", "https://")):
            raise ValueError("base_url 必须以 http:// 或 https:// 开头")
        return v

    @field_validator("api_key", "default_model", mode="before")
    @classmethod
    def _blank_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v


class ProviderUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    slug: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=SLUG_PATTERN
    )
    name: str | None = Field(default=None, min_length=1, max_length=100)
    base_url: str | None = Field(default=None, min_length=1, max_length=255)
    api_key: str | None = Field(default=None, max_length=255)
    default_model: str | None = Field(default=None, max_length=100)
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_tokens: int | None = Field(default=None, gt=0)
    max_retries: int | None = Field(default=None, ge=0, le=10)
    request_timeout: int | None = Field(default=None, gt=0)
    enabled: bool | None = None
    is_default: bool | None = None

    @field_validator("base_url")
    @classmethod
    def _check_base_url(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.rstrip("/")
        if not v.startswith(("http://", "https://")):
            raise ValueError("base_url 必须以 http:// 或 https:// 开头")
        return v

    @field_validator("api_key", "default_model", mode="before")
    @classmethod
    def _blank_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v


class ProviderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    name: str
    base_url: str
    api_key: str | None = None
    default_model: str | None = None
    temperature: float
    max_tokens: int
    max_retries: int
    request_timeout: int
    enabled: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("api_key")
    def _mask_api_key(self, value: str | None) -> str | None:
        """响应中只返回掩码，不暴露完整密钥。"""
        if not value:
            return None
        if len(value) <= 8:
            return "*" * len(value)
        return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"
