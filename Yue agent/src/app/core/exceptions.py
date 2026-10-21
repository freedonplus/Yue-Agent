
"""
    ═══════════════════════════════════════════════════
                     自定义全局异常基类
    ═══════════════════════════════════════════════════
"""

class AppException(Exception):
    """所有业务异常的基类。"""

    status_code = 400
    code = "APP_ERROR"
    default_message = "请求处理失败"

    def __init__(self, message: str | None = None, *, detail=None):
        self.message = message or self.default_message
        self.detail = detail
        super().__init__(self.message)