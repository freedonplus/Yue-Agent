import logging

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelResponse,
    wrap_model_call,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import ensure_config
from langgraph.prebuilt import ToolNode

from Yue.common import _text
from Yue.memory.store import build_memory_note
from Yue.models import get_model
from Yue.schemas import GetModel, SupervisorOutput
from Yue.state.state import AgentState

"""
    ═══════════════════════════════════════════════════
        节点
    ═══════════════════════════════════════════════════
"""

# 技能正文较短时直接注入系统提示词；超过这个长度就改为提示模型 load_skill
logger = logging.getLogger(__name__)

SKILL_INLINE_LIMIT = 40_000

# 调度员派活时插入的提示消息，不是给用户看的成果；
# 用这个标记和「调度员兜底答复」区分开。
SUPERVISOR_ROUTE_KEY = "supervisor_route"
SUPERVISOR_ROUTE_NAME = "supervisor_route"


def _is_route_message(message) -> bool:
    # name 会稳定地随消息进入 worker 子图；additional_kwargs 只作为冗余标记
    if getattr(message, "name", None) == SUPERVISOR_ROUTE_NAME:
        return True
    kwargs = getattr(message, "additional_kwargs", None) or {}
    return bool(kwargs.get(SUPERVISOR_ROUTE_KEY))


def _model_param_overrides(configurable: dict) -> dict:
    """请求级模型参数：覆盖厂商默认的温度与最大输出。

    只接受合法数值，前端没传或传了非法值就沿用厂商配置。
    """
    overrides: dict = {}
    temperature = configurable.get("temperature")
    if isinstance(temperature, (int, float)) and not isinstance(temperature, bool):
        overrides["temperature"] = float(temperature)
    max_tokens = configurable.get("max_tokens")
    if (
        isinstance(max_tokens, int)
        and not isinstance(max_tokens, bool)
        and max_tokens > 0
    ):
        overrides["max_tokens"] = max_tokens
    return overrides


def _last_message_of_type(messages, type_name: str):
    for message in reversed(messages or []):
        if getattr(message, "type", "") == type_name:
            return message
    return None


def _skill_note(skill, *, for_supervisor: bool = False) -> str:
    """把「本次会话指定技能」转成运行时提示词片段。

    技能由用户在对话请求里选择，通过 configurable.skill 传入，
    不参与图状态，续跑时需要再传一次。
    """
    if not isinstance(skill, dict):
        return ""

    name = str(skill.get("name") or "").strip()
    slug = str(skill.get("slug") or "").strip()
    content = str(skill.get("content") or "")
    if not name or not slug:
        return ""

    if for_supervisor:
        return (
            "\n\n【本次任务指定技能】\n"
            f"用户要求本次任务使用技能「{name}」（{slug}）。"
            "请把任务交给最合适的员工，并在 instructions 里明确要求对方"
            f"本次必须使用技能「{slug}」执行，不要自行省略或改写技能里的要求。"
        )

    if len(content) <= SKILL_INLINE_LIMIT:
        return (
            f"\n\n【本次任务指定技能：{name}】\n"
            "用户要求本次任务必须使用这个技能。请严格按以下技能说明执行；"
            "如果它和用户本轮明确提出的要求冲突，以用户当前要求为准。\n"
            "--- 技能开始 ---\n"
            f"{content}\n"
            "--- 技能结束 ---"
        )

    return (
        f"\n\n【本次任务指定技能：{name}】\n"
        f"这个技能的正文较长，请先调用 load_skill 工具加载「{slug}」，"
        "再严格按它执行。"
    )


# ———员工工厂————————————
def make_worker_graph(getModel: GetModel,
                      tools: list,
                      system_prompt: str,
                      slug: str,
                      approval_tools: list[str] | None = None,
                      is_output_gate: bool = False,
    ):
    """返回 create_agent 编译出的子图本体，直接作为父图节点。

    只有子图身份才能让 handoff 工具里的 Command.PARENT 冒泡到父图；
    外面千万不要再包一层 call_model。
    """

    # 子图产出的消息默认没有 name，调度员靠 name 判断"谁发过言"，
    # 所以每条模型回复都要盖章。
    @wrap_model_call
    async def stamp_name(request, handler):
        response = await handler(request)
        stamped = [
            m.model_copy(update={"name": slug})
            if m.type == "ai" and not getattr(m, "name", None)
            else m
            for m in response.result
        ]
        return ModelResponse(
            result=stamped,
            structured_response=response.structured_response,
        )

    # 会话工作目录：由请求的 configurable.workdir 传入，
    # 不写进角色提示词，同一个员工在不同会话里可以用不同的目录。
    @wrap_model_call
    async def apply_workdir(request, handler):
        config = ensure_config()
        workdir = (config.get("configurable") or {}).get("workdir")
        if not isinstance(workdir, str):
            return await handler(request)
        # 只取单行路径，防止通过换行往系统提示词里追加指令
        workdir = " ".join(workdir.split())[:1000]
        if not workdir:
            return await handler(request)

        note = (
            "\n\n【本次会话的工作目录】\n"
            f"{workdir}\n"
            "涉及文件的操作都以这个目录为根目录：相对路径按它解析，"
            "读写、创建、移动文件时优先放在它里面。"
            "除非用户明确要求，不要访问这个目录之外的路径。"
            "如果它和工具自身允许的根目录不一致，以工具允许的范围为准。"
        )
        base = request.system_message
        content = ((base.text if base else "") + note).strip()
        return await handler(
            request.override(system_message=SystemMessage(content=content))
        )

    # 本次会话指定的技能：用户在前端选了哪个，就强制这个员工按它执行。
    @wrap_model_call
    async def apply_skill(request, handler):
        config = ensure_config()
        note = _skill_note((config.get("configurable") or {}).get("skill"))
        if not note:
            return await handler(request)
        base = request.system_message
        content = ((base.text if base else "") + note).strip()
        return await handler(
            request.override(system_message=SystemMessage(content=content))
        )

    # 跨会话记忆：按 user_id 读取长期记忆，作为背景注入系统提示词。
    # 只是参考信息，和本轮要求冲突时以本轮为准。
    @wrap_model_call
    async def apply_memory(request, handler):
        messages = getattr(request, "messages", None) or []

        # 输出管卡也读同一份记忆：用户直接找管卡、或调度员兜底时，
        # 管卡仍能保持跨会话一致；整理上游成果时以对话里的成果为准。
        config = ensure_config()
        user_id = (config.get("configurable") or {}).get("user_id")

        human = _last_message_of_type(messages, "human")
        query = _text(human) if human is not None else ""

        try:
            note = await build_memory_note(user_id or "default", query)
        except Exception:
            # 记忆读取失败不能影响本轮对话
            logger.warning("memory recall failed", exc_info=True)
            return await handler(request)

        logger.debug(
            "memory middleware | slug=%s user=%s note_chars=%s",
            slug,
            user_id,
            len(note),
        )

        if not note:
            return await handler(request)
        base = request.system_message
        content = ((base.text if base else "") + note).strip()
        return await handler(
            request.override(system_message=SystemMessage(content=content))
        )

    # 请求级模型参数：前端可以在每轮对话里覆盖温度和最大输出，
    # 不传时保持厂商配置里的默认值。
    @wrap_model_call
    async def apply_model_params(request, handler):
        config = ensure_config()
        overrides = _model_param_overrides(config.get("configurable") or {})
        if not overrides:
            return await handler(request)
        current = dict(getattr(request, "model_settings", None) or {})
        return await handler(
            request.override(model_settings={**current, **overrides})
        )

    # 最终输出管卡：上游已有其他员工/调度员的答复时，
    # 这里只做整理、润色和收尾，用管卡员工自己的风格输出。
    @wrap_model_call
    async def apply_output_gate(request, handler):
        messages = getattr(request, "messages", None) or []
        last_ai = _last_message_of_type(messages, "ai")

        # 没有上游成果、或只是调度员的派活提示时，按普通员工处理
        if (
            last_ai is None
            or _is_route_message(last_ai)
            or getattr(last_ai, "name", None) in (None, slug)
        ):
            return await handler(request)

        note = (
            "\n\n【最终输出管卡】\n"
            "本轮任务已经由上游员工处理完毕。现在由你担任最后一道输出关口：\n"
            "- 基于对话里已有的成果，直接给用户最终答复，不要重新执行任务。\n"
            "- 保留事实、结论、数据和链接；上游没有提供的内容不要编造。\n"
            "- 用你自己的身份、语气和排版来写，不要提及其他员工、内部派发、"
            "工具调用或系统结构。\n"
            "- 不要调用工具，只输出最终答复。"
        )
        base = request.system_message
        content = ((base.text if base else "") + note).strip()
        return await handler(
            request.override(system_message=SystemMessage(content=content))
        )

    middleware = [apply_workdir, apply_skill, apply_memory, apply_model_params]
    if is_output_gate:
        middleware.append(apply_output_gate)
    middleware.append(stamp_name)

    # 只给真正挂载了的工具加审批，避免配置里残留的名字导致误判
    tool_names = {tool.name for tool in tools}
    gated = [
        name for name in dict.fromkeys(approval_tools or [])
        if name in tool_names
    ]
    if gated:
        middleware.append(
            HumanInTheLoopMiddleware(
                interrupt_on={
                    name: {"allowed_decisions": ["approve", "reject"]}
                    for name in gated
                },
                interrupt_mode="per_call",
                description_prefix="这个操作会改动文件或环境，需要你确认后才会执行",
            )
        )

    return create_agent(
        model=get_model(getModel),
        tools=tools,
        system_prompt=system_prompt,
        name=slug,
        middleware=middleware,
    )

# ———工具工厂：主图暂时用不到，保留给以后需要独立工具节点的场景————————————
def make_tool_node(tools: list):
    return ToolNode(tools)


def make_supervisor_node(gm: GetModel,
                         tools: list,
                         system_prompt,
                         slug: str,
                         workers: dict,
    ):

    # 把员工名单渲染进 {{WORKERS}}
    roster = "\n".join(f"{w.slug} | {w.name} | {w.description or ''}" for w in workers)

    prompt = system_prompt.replace("{{WORKERS}}", roster)
    model = get_model(gm).bind_tools(tools)
    slugs = {w.slug for w in workers}

    async def call_supervisor(state):
        msgs = state["messages"]
        config = ensure_config()
        configurable = config.get("configurable") or {}
        skill_note = _skill_note(
            configurable.get("skill"),
            for_supervisor=True,
        )

        human = _last_message_of_type(msgs, "human")
        query = _text(human) if human is not None else ""
        try:
            memory_note = await build_memory_note(
                configurable.get("user_id") or "default", query
            )
        except Exception:
            memory_note = ""

        # 本轮已经发过言的员工（员工消息带 name=slug）
        spoken = {
            m.name for m in msgs
            if m.type == "ai" and getattr(m, "name", None) in slugs
        }

        # 带来源标记的纯文本历史：不传 assistant 消息，避免
        # thinking 模式要求回传 reasoning_content 的 400。
        # 工人现在是子图，内部会产生 tool_call / ToolMessage，
        # 这些不进 transcript，否则调度员的上下文会被工具噪音塞满。
        def label(m):
            if m.type == "human":
                return "用户"
            if m.type == "ai":
                name = getattr(m, "name", None)
                return f"员工:{name}" if name in slugs else "调度员"
            return None

        lines = []
        for m in msgs:
            who = label(m)
            text = _text(m).strip()
            if who and text:
                lines.append(f"【{who}】{text}")
        transcript = "\n".join(lines)

        # 调度员不经过中间件，请求级模型参数在这里单独绑定
        overrides = _model_param_overrides(configurable)
        active_model = model.bind(**overrides) if overrides else model

        reply = await active_model.ainvoke(
            [
                SystemMessage(content=prompt + skill_note + memory_note),
                HumanMessage(content=transcript),
            ]
        )

        calls = getattr(reply, "tool_calls", None) or []
        args = calls[0].get("args") if calls else {}
        if not isinstance(args, dict):
            args = {}

        route = SupervisorOutput(
            next=str(args.get("next") or "FINISH").strip(),
            instructions=str(args.get("instructions") or "").strip(),
        )

        # 非法 slug，或想重复派遣本轮已发言的员工：收尾
        if route.next not in slugs or route.next in spoken:
            route.next = "FINISH"

        if route.next == "FINISH":
            # 员工已经答过：保留员工那条消息，不再追加空消息
            if spoken:
                return {"next": "FINISH"}
            # 没人答过：用调度员自己的正文兜底
            return {
                "messages": [
                    AIMessage(
                        content=_text(reply) or route.instructions,
                        name="supervisor",
                    )
                ],
                "next": "FINISH",
            }

        return {
            "messages": [
                AIMessage(
                    content=route.instructions,
                    name=SUPERVISOR_ROUTE_NAME,
                    additional_kwargs={SUPERVISOR_ROUTE_KEY: True},
                )
            ],
            "next": route.next,
        }

    return call_supervisor
