from fastapi import APIRouter

from settings import settings

"""
    ═══════════════════════════════════════════════════
                           根路由
    ═══════════════════════════════════════════════════
"""


router = APIRouter(tags=['根路由'])

@router.get("/")
async def root():
    return {"message": f"{settings.APP_NAME}"}