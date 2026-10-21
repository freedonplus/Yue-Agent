from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.providers import ProviderNotFoundError, ProviderSlugExistsError
from app.model.agent_roles import AgentRoles
from app.model.providers import Providers
from app.schemas.providers import ProviderCreate, ProviderUpdate

"""
    ═══════════════════════════════════════════════════
                        厂商业务逻辑
    ═══════════════════════════════════════════════════
"""


# —————————获取厂商列表：关键字检索，只含启用项————————
async def list_providers(
    session: AsyncSession,
    *,
    q: str | None = None,
) -> list[Providers]:
    # 对外只暴露启用的厂商
    conditions = [Providers.enabled.is_(True)]
    if q:
        like = f"%{q.strip()}%"
        conditions.append(
            or_(Providers.name.ilike(like), Providers.slug.ilike(like))
        )

    stmt = (
        select(Providers)
        .where(*conditions)
        .order_by(Providers.created_at.desc())
    )
    items = (await session.execute(stmt)).scalars().all()
    return list(items)


# —————————获取单个厂商：不存在抛 ProviderNotFoundError————————
async def get_provider(session: AsyncSession, provider_id: str) -> Providers:
    provider = await session.get(Providers, provider_id)
    if provider is None:
        raise ProviderNotFoundError()
    return provider


# —————————创建厂商：slug 唯一，默认厂商全局只保留一个————————
async def create_provider(
    session: AsyncSession, data: ProviderCreate
) -> Providers:
    exists = await session.scalar(
        select(Providers.id).where(Providers.slug == data.slug)
    )
    if exists:
        raise ProviderSlugExistsError()

    payload = data.model_dump()

    # 全局只能有一个默认厂商
    if payload.get("is_default"):
        await session.execute(update(Providers).values(is_default=False))

    provider = Providers(**payload)
    session.add(provider)
    await session.commit()
    await session.refresh(provider)
    return provider


# —————————更新厂商：只改传入字段，设为默认时清掉其他默认————————
async def update_provider(
    session: AsyncSession, provider_id: str, data: ProviderUpdate
) -> Providers:
    provider = await get_provider(session, provider_id)
    changes = data.model_dump(exclude_unset=True)

    if "slug" in changes and changes["slug"] != provider.slug:
        exists = await session.scalar(
            select(Providers.id).where(Providers.slug == changes["slug"])
        )
        if exists:
            raise ProviderSlugExistsError()

    if changes.get("is_default") is True:
        await session.execute(
            update(Providers)
            .where(Providers.id != provider_id)
            .values(is_default=False)
        )

    for field, value in changes.items():
        setattr(provider, field, value)

    await session.commit()
    await session.refresh(provider)
    return provider


# —————————启用 / 停用厂商：公开接口使用————————
async def set_provider_enabled(
    session: AsyncSession, provider_id: str, enabled: bool
) -> Providers:
    """公开接口的启用/停用。"""
    provider = await get_provider(session, provider_id)

    provider.enabled = enabled
    await session.commit()
    await session.refresh(provider)
    return provider


# —————————删除厂商：先解绑引用它的员工，再删除————————
async def delete_provider(session: AsyncSession, provider_id: str) -> None:
    provider = await get_provider(session, provider_id)

    # 显式解绑引用该厂商的员工，避免异步懒加载关系
    await session.execute(
        update(AgentRoles)
        .where(AgentRoles.provider_id == provider_id)
        .values(provider_id=None)
    )

    await session.delete(provider)
    await session.commit()
