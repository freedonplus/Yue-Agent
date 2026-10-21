from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import ADMIN_COOKIE_NAME, verify_admin_session
from app.exceptions.auth import NotAuthenticatedError
from app.schemas.chat_sessions import (
    ChatMessageOut,
    SessionCreate,
    SessionOut,
    SessionUpdate,
)
from app.services import message_service, session_service

"""
    ═══════════════════════════════════════════════════
                    会话管理接口
    ═══════════════════════════════════════════════════

    POST    /api/sessions                       创建会话
    GET     /api/sessions                       会话列表
    GET     /api/sessions/{session_id}          会话详情
    GET     /api/sessions/{session_id}/messages 会话消息（用于重新打开会话时回放）
    PATCH   /api/sessions/{session_id}          更新会话
    DELETE  /api/sessions/{session_id}          删除会话

    session_id 是前端生成的会话标识，与 /api/chat/stream 里的 session_id 对应。

    权限：
        创建 / 查询 / 更新 → 无需鉴权
        删除             → 管理员 Cookie 会话
"""

router = APIRouter()


# —————————管理员校验：接口返回 401，而不是跳登录页————————
async def require_admin_api(request: Request) -> dict:
    payload = verify_admin_session(request.cookies.get(ADMIN_COOKIE_NAME))
    if payload is None:
        raise NotAuthenticatedError()
    return payload


@router.post("", response_model=SessionOut, status_code=201)
async def create_session(
    payload: SessionCreate,
    session: AsyncSession = Depends(get_session),
):
    return await session_service.create_session(session, payload)


@router.get("", response_model=list[SessionOut])
async def list_sessions(
    q: str | None = Query(None, max_length=100),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await session_service.list_sessions(
        session, q=q, limit=limit, offset=offset
    )


@router.get("/{session_id}", response_model=SessionOut)
async def get_session_detail(
    session_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await session_service.get_session(session, session_id)


@router.get(
    "/{session_id}/messages",
    response_model=list[ChatMessageOut],
)
async def list_session_messages(
    session_id: str,
    limit: int = Query(200, ge=1, le=1000),
    before_id: int | None = Query(None, ge=1),
    session: AsyncSession = Depends(get_session),
):
    """按时间正序返回消息；用 before_id 向前翻页。"""
    return await message_service.list_messages(
        session, session_id, limit=limit, before_id=before_id
    )


@router.patch("/{session_id}", response_model=SessionOut)
async def update_session(
    session_id: str,
    payload: SessionUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await session_service.update_session(session, session_id, payload)


@router.delete("/{session_id}", status_code=204)
async def delete_session(
    session_id: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(require_admin_api),
):
    await session_service.delete_session(session, session_id)
    return Response(status_code=204)
