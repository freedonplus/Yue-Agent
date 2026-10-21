from pydantic import BaseModel

"""
    ═══════════════════════════════════════════════════
                        通用 Schema
    ═══════════════════════════════════════════════════
"""


class EnabledUpdate(BaseModel):
    """公开接口只允许切换启用/停用。"""

    enabled: bool
