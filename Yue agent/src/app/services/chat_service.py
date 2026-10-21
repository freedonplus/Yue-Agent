import asyncio
import json
import logging
from uuid import uuid4

from fastapi import Request
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.types import Command

from app.core.database import SessionLocal
from app.exceptions.skills import SkillNotFoundError
from app.schemas.chat import ChatRequest
from app.services import message_service, session_service, skill_service

"""
    ═══════════════════════════════════════════════════
                    对话流式输出（SSE）
    ═══════════════════════════════════════════════════

    /api/chat/stream 与 /admin/playground/stream 共用，
    区别只在鉴权方式（Bearer Token / 管理员 Cookie）。
"""

logger = logging.getLogger(__name__)

_ROLE_MAP = {
    "user": HumanMessage,
    "assistant": AIMessage,
    "system": SystemMessage,
}

# 历史总长度上限：防止前端把几十条长消息一次性塞进上下文
MAX_HISTORY_CHARS = 60_000
# 调试用的 state 事件只保留最近一段，避免工具参数与大段正文撑爆 SSE
MAX_STATE_MESSAGES = 30
MAX_STATE_CONTENT_CHARS = 4_000
MAX_STATE_REASONING_CHARS = 2_000
MAX_STATE_TOOL_ARGS_CHARS = 2_000


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "…（已截断）"


# —————————把请求里的历史 + 本轮输入转成 LangChain 消息————————
def to_messages(payload: ChatRequest) -> list[BaseMessage]:
    history = list(payload.history)
    total_chars = sum(len(item.content) for item in history)
    dropped = 0
    # 从最旧的消息开始丢弃，优先保留最近的上下文
    while history and total_chars > MAX_HISTORY_CHARS:
        total_chars -= len(history.pop(0).content)
        dropped += 1
    if dropped:
        logger.info(
            "history trimmed | dropped=%d kept=%d chars=%d",
            dropped,
            len(history),
            total_chars,
        )

    messages: list[BaseMessage] = []
    for item in history:
        factory = _ROLE_MAP[item.role]
        messages.append(factory(content=item.content))
    messages.append(HumanMessage(content=payload.message))
    return messages


# —————————从模型输出块里取出纯文本————————
def _text_of(chunk) -> str:
    content = getattr(chunk, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and part.get("type") == "text":
                parts.append(str(part.get("text", "")))
        return "".join(parts)
    return ""


# —————————取出思考内容（DeepSeek reasoning_content）————————
def _reasoning_of(chunk) -> str:
    kwargs = getattr(chunk, "additional_kwargs", None) or {}
    reasoning = kwargs.get("reasoning_content")
    return reasoning if isinstance(reasoning, str) else ""


# —————————提取工具调用（名称 / 参数）————————
def _tool_calls_of(message) -> list[dict]:
    calls = getattr(message, "tool_calls", None) or []
    result: list[dict] = []
    for call in calls:
        if not isinstance(call, dict):
            continue
        result.append(
            {
                "name": call.get("name"),
                "args": call.get("args"),
                "id": call.get("id"),
            }
        )
    return result


# —————————token 用量：兼容 usage_metadata 与厂商原始 token_usage————————
def _int_token(value) -> int:
    try:
        return max(int(value or 0), 0)
    except (TypeError, ValueError):
        return 0


def _usage_of(message) -> tuple[int, int, int] | None:
    """从一次模型调用的结果里取 (输入, 输出, 总计)，取不到返回 None。"""
    if message is None:
        return None

    usage = getattr(message, "usage_metadata", None)
    if not isinstance(usage, dict) or not usage:
        meta = getattr(message, "response_metadata", None) or {}
        usage = meta.get("token_usage") or meta.get("usage")
    if not isinstance(usage, dict) or not usage:
        return None

    input_tokens = _int_token(
        usage.get("input_tokens") or usage.get("prompt_tokens")
    )
    output_tokens = _int_token(
        usage.get("output_tokens") or usage.get("completion_tokens")
    )
    total_tokens = _int_token(usage.get("total_tokens"))
    if not total_tokens:
        total_tokens = input_tokens + output_tokens

    if not (input_tokens or output_tokens or total_tokens):
        return None
    return input_tokens, output_tokens, total_tokens


# —————————单条消息 → 可 JSON 序列化的结构————————
def _message_payload(message) -> dict:
    reasoning = _reasoning_of(message)
    tool_calls = _tool_calls_of(message)
    for call in tool_calls:
        args = call.get("args")
        if args is None:
            continue
        try:
            serialized = json.dumps(args, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            serialized = str(args)
        if len(serialized) > MAX_STATE_TOOL_ARGS_CHARS:
            call["args"] = _clip(serialized, MAX_STATE_TOOL_ARGS_CHARS)

    return {
        "type": getattr(message, "type", type(message).__name__),
        "name": getattr(message, "name", None),
        "content": _clip(_text_of(message), MAX_STATE_CONTENT_CHARS),
        "tool_calls": tool_calls,
        "reasoning": (
            _clip(reasoning, MAX_STATE_REASONING_CHARS) if reasoning else None
        ),
    }


# —————————图状态 → 可 JSON 序列化的结构（有上限的调试摘要）————————
def _state_payload(output) -> dict | None:
    if not isinstance(output, dict):
        return None

    all_messages = output.get("messages") or []
    recent = list(all_messages)[-MAX_STATE_MESSAGES:]
    payload: dict = {
        "messages": [_message_payload(m) for m in recent],
        "messages_total": len(all_messages),
    }
    if len(all_messages) > len(recent):
        payload["messages_truncated"] = len(all_messages) - len(recent)

    for key, value in output.items():
        if key == "messages":
            continue
        try:
            json.dumps(value)
            payload[key] = value
        except (TypeError, ValueError):
            payload[key] = str(value)
    return payload


# —————————拼一条 SSE 事件————————
def sse_event(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False, default=str)}\n\n"


# —————————一个待审批的 interrupt → 前端可读结构————————
def _approval_payload(interrupt) -> dict:
    value = getattr(interrupt, "value", None)
    if not isinstance(value, dict):
        value = {}
    return {
        "interrupt_id": getattr(interrupt, "id", ""),
        "tool_call_id": value.get("tool_call_id"),
        "tool": value.get("name") or "",
        "args": value.get("args") or {},
        "description": value.get("description") or "",
    }


# —————————读取暂停中的 interrupt；没有 checkpointer 时返回空————————
async def _pending_interrupts(graph, config) -> tuple[list, object | None]:
    try:
        snapshot = await graph.aget_state(config)
    except Exception:
        logger.debug("aget_state unavailable", exc_info=True)
        return [], None
    return list(getattr(snapshot, "interrupts", ()) or ()), snapshot


# —————————续跑前确认：这个 run 确实停在审批上————————
async def has_pending_approval(graph, run_id: str) -> bool:
    config = {"configurable": {"thread_id": run_id}}
    try:
        snapshot = await graph.aget_state(config)
    except Exception:
        return False
    return bool(getattr(snapshot, "interrupts", ()))


# —————————对话结束：清理该轮检查点，避免数据库无限增长————————
async def _drop_thread(graph, thread_id: str) -> None:
    checkpointer = getattr(graph, "checkpointer", None)
    delete = getattr(checkpointer, "adelete_thread", None)
    if delete is None:
        return
    try:
        await delete(thread_id)
    except Exception:
        logger.warning("failed to delete checkpoint | thread=%s", thread_id, exc_info=True)


# —————————把 LangGraph 事件流转换成 SSE————————
def normalize_workdir(value: str | None) -> str:
    """目录会被拼进系统提示词：压成一行，避免被塞入额外指令。"""
    return " ".join((value or "").split())[:1000]


async def resolve_workdir(
    session,
    session_id: str | None,
    workdir: str | None,
) -> str:
    """请求里显式带了工作目录就用它，否则读会话表里保存的设置。"""
    value = normalize_workdir(workdir)
    if value:
        return value
    return normalize_workdir(
        await session_service.find_workdir(session, session_id)
    )


def normalize_user_id(value: str | None) -> str:
    """记忆归属只保留单行可见字符，避免拼进提示词时被加料。"""
    user_id = " ".join((value or "").split())[:100]
    return user_id or "default"


# —————————会话消息落库：失败不影响本轮对话————————
async def _persist_message(
    session_id: str | None,
    role: str,
    content: str,
    name: str | None = None,
) -> None:
    if not session_id or not content:
        return
    try:
        async with SessionLocal() as session:
            await message_service.add_message(
                session, session_id, role, content, name=name
            )
    except Exception:
        logger.warning(
            "failed to persist chat message | session=%s role=%s",
            session_id,
            role,
            exc_info=True,
        )


def _last_ai_name(final_state: dict | None) -> str | None:
    """最终答复由哪个员工产出，取自图状态里最后一条 AI 消息。"""
    if not isinstance(final_state, dict):
        return None
    for message in reversed(final_state.get("messages") or []):
        if not isinstance(message, dict):
            continue
        if message.get("type") == "ai":
            return message.get("name")
    return None


async def resolve_skill(session, skill_slug: str | None) -> dict | None:
    """把前端选择的技能 slug 解析成运行时需要的技能快照。

    技能由用户按次选择，不要求事先挂载给员工；停用或不存在的技能
    直接返回 404，避免用户以为用了技能、实际却没生效。
    """
    slug = (skill_slug or "").strip().lower()
    if not slug:
        return None

    skill = await skill_service.find_enabled_skill(session, slug)
    if skill is None:
        raise SkillNotFoundError("技能不存在或已停用")
    return {"slug": skill.slug, "name": skill.name, "content": skill.content}


async def event_stream(
    request: Request,
    graph,
    messages: list[BaseMessage] | None = None,
    session_id: str | None = None,
    *,
    thread_id: str | None = None,
    resume: dict | None = None,
    workdir: str = "",
    skill: dict | None = None,
    user_id: str = "default",
    temperature: float | None = None,
    max_tokens: int | None = None,
):
    """run 一次图。

    - 新对话：传 messages，每个 run 用独立 thread_id 存检查点；
    - 审批后继续：传 resume，沿用同一个 thread_id。

    workdir / skill / user_id / temperature / max_tokens 通过 configurable
    传给员工子图，不参与图状态，因此续跑时需要再传一次。
    模型参数不传时沿用厂商配置。
    """
    thread_id = thread_id or uuid4().hex
    config = {
        "configurable": {
            "thread_id": thread_id,
            "workdir": normalize_workdir(workdir),
            "skill": skill,
            "user_id": normalize_user_id(user_id),
            "session_id": session_id or "",
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    }

    # 只在新对话时记录用户输入；审批续跑不重复写入
    if resume is None and messages:
        await _persist_message(session_id, "user", _text_of(messages[-1]))
    graph_input = (
        Command(resume=resume) if resume is not None else {"messages": messages}
    )

    final_text = ""
    current_node: str | None = None
    visited_nodes: list[str] = []
    final_state: dict | None = None
    # 本轮所有模型调用（调度员 + 员工 + 工具循环）的 token 用量累加
    usage_totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    try:
        async for event in graph.astream_events(
            graph_input, config, version="v2"
        ):
            # 客户端已断开：停止消费模型输出，避免继续消耗 token
            if await request.is_disconnected():
                logger.info(
                    "chat stream disconnected by client | session=%s", session_id
                )
                return

            kind = event.get("event")
            metadata = event.get("metadata") or {}
            node = metadata.get("langgraph_node")

            # 进入节点（调度员 / 员工）时通知前端
            if kind == "on_chain_start" and node and node != current_node:
                current_node = node
                visited_nodes.append(node)
                yield sse_event(
                    {"type": "node", "node": node, "session_id": session_id}
                )

            # 模型增量：思考内容与正文分开推送
            elif kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")

                reasoning = _reasoning_of(chunk)
                if reasoning:
                    yield sse_event(
                        {
                            "type": "reasoning",
                            "content": reasoning,
                            "node": node,
                            "session_id": session_id,
                        }
                    )

                text = _text_of(chunk)
                if text:
                    yield sse_event(
                        {
                            "type": "token",
                            "content": text,
                            "node": node,
                            "session_id": session_id,
                        }
                    )

            # 模型一次调用结束：把工具调用（route）完整推给前端，并累计 token
            elif kind == "on_chat_model_end":
                output = event.get("data", {}).get("output")
                calls = _tool_calls_of(output)
                if calls:
                    yield sse_event(
                        {
                            "type": "tool_call",
                            "node": node,
                            "tool_calls": calls,
                            "session_id": session_id,
                        }
                    )

                usage = _usage_of(output)
                if usage is not None:
                    for key, value in zip(
                        ("input_tokens", "output_tokens", "total_tokens"), usage
                    ):
                        usage_totals[key] += value

            # 根链路结束：取最终状态与最后一条回复
            elif kind == "on_chain_end" and not event.get("parent_ids"):
                output = event.get("data", {}).get("output") or {}
                result_messages = (
                    output.get("messages") if isinstance(output, dict) else None
                )
                if result_messages:
                    final_text = _text_of(result_messages[-1])

                final_state = _state_payload(output)
                if final_state is not None:
                    final_state["nodes"] = list(visited_nodes)

        # 流结束不代表跑完：可能停在工具审批上
        interrupts, snapshot = await _pending_interrupts(graph, config)

        if interrupts:
            if final_state is None and snapshot is not None:
                final_state = _state_payload(getattr(snapshot, "values", None))
                if final_state is not None:
                    final_state["nodes"] = list(visited_nodes)

            if final_state is not None:
                yield sse_event(
                    {"type": "state", "state": final_state, "session_id": session_id}
                )

            yield sse_event(
                {
                    "type": "approval_required",
                    "run_id": thread_id,
                    "approvals": [_approval_payload(i) for i in interrupts],
                    "session_id": session_id,
                }
            )
            yield sse_event(
                {
                    "type": "usage",
                    "usage": dict(usage_totals),
                    "session_id": session_id,
                }
            )
            yield sse_event(
                {
                    "type": "done",
                    "content": final_text,
                    "paused": True,
                    "run_id": thread_id,
                    "session_id": session_id,
                }
            )
            return

        if final_state is not None:
            yield sse_event(
                {"type": "state", "state": final_state, "session_id": session_id}
            )

        # 跑完了，检查点不再需要：下一轮会带完整历史重新开始
        await _drop_thread(graph, thread_id)

        # 只保存最终答复，检查点清理后仍能回放会话
        await _persist_message(
            session_id,
            "assistant",
            final_text,
            name=_last_ai_name(final_state),
        )

        yield sse_event(
            {
                "type": "usage",
                "usage": dict(usage_totals),
                "session_id": session_id,
            }
        )
        yield sse_event(
            {
                "type": "done",
                "content": final_text,
                "run_id": thread_id,
                "session_id": session_id,
            }
        )

    except asyncio.CancelledError:
        # 客户端关闭连接时 Starlette 会取消这个生成器
        raise
    except Exception as exc:
        logger.exception("chat stream failed | session=%s", session_id)
        yield sse_event(
            {"type": "error", "message": str(exc), "session_id": session_id}
        )
