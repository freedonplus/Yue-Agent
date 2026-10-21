from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.chat import ChatApprovalRequest, ChatRequest
from app.services import chat_service
from Yue.agent.graph import get_graph

"""
    ═══════════════════════════════════════════════════
                        对话接口（SSE）
    ═══════════════════════════════════════════════════

    POST /api/chat/stream

    请求体：
        {
            "message": "用户输入",
            "history": [{"role": "user|assistant|system", "content": "..."}],
            "session_id": "可选，前端会话标识",
            "workdir": "可选，本次会话的工作目录；不传则读取会话表设置",
            "skill_slug": "可选，本次任务强制使用的技能 slug",
            "user_id": "可选，跨会话记忆归属，默认 default",
            "temperature": 0.7,       # 可选，覆盖厂商默认温度
            "max_tokens": 4096        # 可选，覆盖厂商默认最大输出
        }

    工作目录、指定技能和模型参数会注入运行时配置，不参与图状态。
    审批通过后调用 /api/chat/approve 时建议再传一次相同的 workdir、
    skill_slug、temperature 和 max_tokens，否则续跑时会丢失。

    响应：text/event-stream，每条事件是一行 JSON：

        {"type": "node",  "node": "员工slug", "session_id": "..."}
        {"type": "token", "content": "增量文本", "session_id": "..."}
        {"type": "tool_call", "node": "...", "tool_calls": [...]}
        {"type": "approval_required", "run_id": "...", "approvals": [...]}
        {"type": "usage", "usage": {"input_tokens": 123, "output_tokens": 456,
                                    "total_tokens": 579}, "session_id": "..."}
        {"type": "done",  "content": "最终答复", "paused": false, "run_id": "..."}
        {"type": "error", "message": "错误信息", "session_id": "..."}

    需要人工审批时，流会以 paused=true 结束；把 run_id 和审批结果
    POST 到 /api/chat/approve 继续执行。

    流式转换逻辑在 app/services/chat_service.py，
    管理后台的测试页复用同一套实现。
"""

# 对话接口无需鉴权，前端可直接调用
router = APIRouter()


def _stream_response(
    *, request, graph, session_id, thread_id, messages=None, resume=None,
    workdir="", skill=None, user_id="default",
    temperature=None, max_tokens=None,
):
    return StreamingResponse(
        chat_service.event_stream(
            request,
            graph,
            messages,
            session_id,
            thread_id=thread_id,
            resume=resume,
            workdir=workdir,
            skill=skill,
            user_id=user_id,
            temperature=temperature,
            max_tokens=max_tokens,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # 关闭 Nginx 等反向代理的缓冲，避免一次性吐出
            "X-Accel-Buffering": "no",
        },
    )


# —————————流式对话：SSE 推送节点与 token————————
@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    try:
        graph = await get_graph()
    except RuntimeError as exc:
        # 例如没有默认厂商、没有唯一调度员
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    workdir = await chat_service.resolve_workdir(
        session, payload.session_id, payload.workdir
    )
    skill = await chat_service.resolve_skill(session, payload.skill_slug)

    return _stream_response(
        request=request,
        graph=graph,
        session_id=payload.session_id,
        thread_id=uuid4().hex,
        messages=chat_service.to_messages(payload),
        workdir=workdir,
        skill=skill,
        user_id=payload.user_id,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
    )


# —————————人工审批：批准 / 拒绝后继续同一次运行————————
@router.post("/approve")
async def chat_approve(
    payload: ChatApprovalRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    try:
        graph = await get_graph()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    if not await chat_service.has_pending_approval(graph, payload.run_id):
        raise HTTPException(
            status_code=409,
            detail="没有待审批的操作，可能已经处理或已过期",
        )

    workdir = await chat_service.resolve_workdir(
        session, payload.session_id, payload.workdir
    )
    skill = await chat_service.resolve_skill(session, payload.skill_slug)

    return _stream_response(
        request=request,
        graph=graph,
        session_id=payload.session_id,
        thread_id=payload.run_id,
        resume=payload.resume_payload,
        workdir=workdir,
        skill=skill,
        user_id=payload.user_id,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
    )
