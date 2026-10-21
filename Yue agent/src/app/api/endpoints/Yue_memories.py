from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response

from app.core.security import ADMIN_COOKIE_NAME, verify_admin_session
from app.exceptions.auth import NotAuthenticatedError
from Yue.memory import store
from Yue.memory.schemas import MemoryCreate, MemoryOut

"""
    ═══════════════════════════════════════════════════
                    跨会话记忆接口
    ═══════════════════════════════════════════════════

    GET    /api/memories                查看记忆（默认 user_id=default）
    POST   /api/memories                手动写入一条记忆
    DELETE /api/memories/{memory_id}    删除记忆（管理员）

    对话时员工通过 save_memory / search_memory 工具使用同一份数据；
    记忆按 user_id 隔离，跨会话保留。
"""

router = APIRouter()


async def require_admin_api(request: Request) -> dict:
    payload = verify_admin_session(request.cookies.get(ADMIN_COOKIE_NAME))
    if payload is None:
        raise NotAuthenticatedError()
    return payload


@router.get("", response_model=list[MemoryOut])
async def list_memories(
    user_id: str = Query("default", max_length=100),
    q: str | None = Query(None, max_length=100),
    limit: int = Query(50, ge=1, le=200),
):
    return await store.list_memories(user_id, query=q, limit=limit)


@router.post("", response_model=MemoryOut, status_code=201)
async def create_memory(payload: MemoryCreate):
    item, _ = await store.save_memory(
        payload.user_id,
        payload.content,
        tags=payload.tags,
        kind=payload.kind,
        source_session_id=payload.source_session_id,
    )
    return item


@router.delete("/{memory_id}", status_code=204)
async def delete_memory(
    memory_id: str,
    user_id: str = Query("default", max_length=100),
    _: dict = Depends(require_admin_api),
):
    if not await store.delete_memory(user_id, memory_id):
        raise HTTPException(status_code=404, detail="记忆不存在")
    return Response(status_code=204)
