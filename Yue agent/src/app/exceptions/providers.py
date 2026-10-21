from app.core.exceptions import AppException


"""
    ═══════════════════════════════════════════════════
                        进行配置并获取模型
    ═══════════════════════════════════════════════════
"""

class ProviderError(AppException):
    status_code = 400
    code = "PROVIDER_ERROR"
    default_message = "厂商操作失败"


class ProviderNotFoundError(ProviderError):
    status_code = 404
    code = "PROVIDER_NOT_FOUND"
    default_message = "厂商不存在"


class ProviderSlugExistsError(ProviderError):
    status_code = 409
    code = "PROVIDER_SLUG_EXISTS"
    default_message = "厂商 slug 已存在"