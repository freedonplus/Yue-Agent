from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Yue.agent.graph import reset_graph
from app.core.database import get_session
from app.schemas.common import EnabledUpdate
from app.schemas.providers import ProviderCreate, ProviderOut, ProviderUpdate
from app.services import provider_service

"""
    ═══════════════════════════════════════════════════
                        厂商接口
    ═══════════════════════════════════════════════════

    POST   /api/providers                新增厂商
    GET    /api/providers                厂商列表
    GET    /api/providers/{id}           厂商详情
    PATCH  /api/providers/{id}           修改厂商
    PATCH  /api/providers/{id}/enabled   启用 / 停用

    删除仍仅限管理后台（/admin/providers）。
    响应中的 api_key 始终为掩码。
"""

router = APIRouter()


# —————————新增厂商：slug 唯一，默认厂商全局只保留一个————————
@router.post("", response_model=ProviderOut, status_code=201)
async def create_provider(
    payload: ProviderCreate,
    session: AsyncSession = Depends(get_session),
):
    provider = await provider_service.create_provider(session, payload)
    reset_graph()
    return provider


# —————————获取厂商列表：支持关键字检索，只返回启用的————————
@router.get("", response_model=list[ProviderOut])
async def list_providers(
    q: str | None = Query(None, max_length=100),
    session: AsyncSession = Depends(get_session),
):
    return await provider_service.list_providers(session, q=q)


# —————————获取单个厂商详情：api_key 已掩码————————
@router.get("/{provider_id}", response_model=ProviderOut)
async def get_provider(
    provider_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await provider_service.get_provider(session, provider_id)


# —————————修改厂商：只更新传入字段，密钥留空表示保持原值————————
@router.patch("/{provider_id}", response_model=ProviderOut)
async def update_provider(
    provider_id: str,
    payload: ProviderUpdate,
    session: AsyncSession = Depends(get_session),
):
    provider = await provider_service.update_provider(
        session, provider_id, payload
    )
    reset_graph()
    return provider


# —————————启用 / 停用厂商————————
@router.patch("/{provider_id}/enabled", response_model=ProviderOut)
async def set_provider_enabled(
    provider_id: str,
    payload: EnabledUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await provider_service.set_provider_enabled(
        session, provider_id, payload.enabled
    )
