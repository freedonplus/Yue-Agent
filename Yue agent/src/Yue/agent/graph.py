import asyncio
import json

from langgraph.graph import StateGraph,START,END
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Yue.checkpoint import get_checkpointer
from Yue.mcp import get_mcp_tools, reset_mcp_tools
from Yue.memory.tools import make_memory_tools
from Yue.tools.handoff import make_handoff_tool
from Yue.tools.skill import make_skill_tool
from Yue.tools.supervisor import Supervisor_tools
from app.core.database import SessionLocal
from app.model.agent_roles import AgentRoles
from app.model.providers import Providers
from app.model.skills import Skills
from app.model.tools import AgentRoleTools, Tools
from app.schemas.agent_roles import parse_approval_tools
from Yue.nodes import nodes
from Yue.schemas import GetModel
from Yue.state.state import AgentState

"""
    ═══════════════════════════════════════════════════
                            图的编排
    ═══════════════════════════════════════════════════
"""

workers={}
worker_slugs={}
# 最终输出管卡的 slug；为空表示不启用
output_gate_slug=None

# —————————读取全局默认厂商，组装模型参数————————
async def get_provider(session) -> GetModel:
    provider = await session.scalar(
        select(Providers).where(
            Providers.is_default.is_(True),
            Providers.enabled.is_(True),
        )
    )
    if provider is None:
        raise RuntimeError("没有可用的全局默认厂商，请先设置")

    return GetModel(
        MODEL_NAME=provider.default_model or "",
        MODEL_BASE_URL=provider.base_url,
        MODEL_API_KEY=provider.api_key or "",
        MODEL_TEMPERATURE=provider.temperature,
        MODEL_MAX_TOKENS=provider.max_tokens,
        MODEL_MAX_RETRIES=provider.max_retries,
    )


# —————————按角色读取启用的角色并注册为节点————————
async def build_role_node(
    builder: StateGraph,
    gm: GetModel,
    role: str,
    session,
) -> list[AgentRoles]:
    global workers
    agents = (
        await session.execute(
            select(AgentRoles)
            .options(selectinload(AgentRoles.tools))
            .where(
                AgentRoles.enabled.is_(True),
                AgentRoles.role == role,
            )
            .order_by(AgentRoles.sort_order.asc())
        )
    ).scalars().all()

    if role == "supervisor":
        for agent in agents:
            builder.add_node(
                agent.slug,
                nodes.make_supervisor_node(
                    gm,
                    [*Supervisor_tools],
                    system_prompt=agent.system_prompt,
                    slug=agent.slug,
                    workers=workers,
                ),
            )
    else:
        global output_gate_slug
        slugs = [agent.slug for agent in agents]
        gate = next((a for a in agents if a.is_output_gate), None)
        output_gate_slug = gate.slug if gate is not None else None

        # 读取每个员工挂载的配置，以及配置下选中的具体工具
        mount_rows = (
            await session.execute(
                select(AgentRoleTools, Tools)
                .join(Tools, Tools.id == AgentRoleTools.tool_id)
                .where(
                    AgentRoleTools.agent_role_id.in_([a.id for a in agents]),
                    Tools.enabled.is_(True),
                )
                .order_by(Tools.name.asc())
            )
        ).all()

        # tool_names 为 None：挂载该配置下全部工具；
        # 为 JSON 数组（允许空）：只挂选中的工具
        mounts: dict[str, list[tuple[Tools, list[str] | None]]] = {}
        for link, tool in mount_rows:
            names = (
                None
                if link.tool_names is None
                else json.loads(link.tool_names)
            )
            mounts.setdefault(link.agent_role_id, []).append((tool, names))

        # 相同配置只启动一次 MCP 服务
        unique_configs = list(
            {tool.config for pairs in mounts.values() for tool, _ in pairs}
        )
        loaded_lists = await asyncio.gather(
            *(get_mcp_tools([config]) for config in unique_configs)
        )
        loaded_by_config = dict(zip(unique_configs, loaded_lists))

        def tools_for_agent(agent: AgentRoles) -> list:
            result = []
            for tool, names in mounts.get(agent.id, []):
                loaded = loaded_by_config.get(tool.config, [])
                if names is not None:
                    wanted = set(names)
                    loaded = [t for t in loaded if t.name in wanted]
                result.extend(loaded)
            return result

        tool_lists = [tools_for_agent(agent) for agent in agents]

        # 技能是全局的：所有启用的技能都对员工开放，不需要按员工挂载。
        # 用户在对话里指定技能后，运行时会强制注入；未指定时由员工按需加载。
        available_skills = list(
            (
                await session.execute(
                    select(Skills)
                    .where(Skills.enabled.is_(True))
                    .order_by(Skills.name.asc())
                )
            ).scalars().all()
        )

        for agent, mcp_tools in zip(agents, tool_lists):
            tools = [*mcp_tools]
            is_gate = agent.slug == output_gate_slug
            # 输出管卡只负责收尾，不再转交给其他员工
            if len(slugs) > 1 and not is_gate:
                tools.append(make_handoff_tool(slugs, agent.slug))
            # 技能按需加载，避免把大段说明一次性塞进系统提示词
            skill_tool = make_skill_tool(available_skills)
            if skill_tool is not None:
                tools.append(skill_tool)
            # 跨会话记忆：按运行时 user_id 读写，所有员工共享同一份
            tools.extend(make_memory_tools())
            builder.add_node(
                agent.slug,
                nodes.make_worker_graph(
                    gm,
                    tools,
                    system_prompt=agent.system_prompt,
                    slug=agent.slug,
                    approval_tools=parse_approval_tools(agent.approval_tools),
                    is_output_gate=is_gate,
                ),
            )
        workers=list(agents)


    return list(agents)


def _last_ai_name(state: AgentState) -> str | None:
    for message in reversed(state.get("messages") or []):
        if getattr(message, "type", "") == "ai":
            return getattr(message, "name", None)
    return None


def route_next(state: AgentState) -> str:
    nxt = state.get("next")

    # 调度员要派员工，正常进入员工节点
    if nxt in worker_slugs:
        return nxt

    # 调度员决定收尾：如果配置了输出管卡，且管卡本轮还没发过言，
    # 先把当前结果交给它整理成最终答复。管卡发言后直接结束。
    if output_gate_slug and _last_ai_name(state) != output_gate_slug:
        return output_gate_slug

    return "FINISH"


# —————————构建图————————
async def build_graph():
    # 全局导入
    global worker_slugs

    # 构件图
    builder = StateGraph(AgentState)

    # 开启会话读取role并添加节点（员工各自的 MCP 工具在节点里加载）
    async with SessionLocal() as session:
        gm = await get_provider(session)
        await build_role_node(builder, gm, "worker", session)
        supervisors = await build_role_node(builder, gm, "supervisor", session)

    supervisor =supervisors[0]

    # 执行编排之前解决worker_slug赋值
    worker_slugs = {worker.slug for worker in workers}


    # 编排
    builder.add_edge(START,supervisor.slug)
    builder.add_conditional_edges(supervisor.slug,
                                  route_next,
                                  {slug: slug for slug in worker_slugs} | {"FINISH": END},
                                  )

    # 工人 → handoff 目标 或 回调度员。
    # 不能用作静态边：handoff 的 Command 跳转与静态边会在同一超步
    # 同时触发目标工人和调度员，导致调度员看不到工人的回答就做决定。
    # 改成条件边后，Command 的 next 与路由判断一致，只执行一次。
    def route_after_worker(self_slug: str):
        def route(state: AgentState) -> str:
            # 输出管卡产出就是最终答复，直接结束
            if self_slug == output_gate_slug:
                return "END"
            nxt = state.get("next")
            # next 仍指向自己 = 没有转交，收尾回调度员
            return nxt if nxt in worker_slugs and nxt != self_slug else "supervisor"

        return route

    for slug in worker_slugs:
        builder.add_conditional_edges(
            slug,
            route_after_worker(slug),
            # 排除自己，避免图里出现无意义的自环边
            {
                **{s: s for s in worker_slugs if s != slug},
                "supervisor": supervisor.slug,
                "END": END,
            },
        )


    # 人工审批用 interrupt 暂停，必须挂 checkpointer 才能保存现场
    checkpointer = await get_checkpointer()
    return builder.compile(checkpointer=checkpointer)


# —————————编译后的图缓存：进程内只构建一次————————
_graph = None
_graph_lock = asyncio.Lock()


async def get_graph():
    """首次调用时构图并缓存；并发请求只构建一次。"""
    global _graph
    if _graph is None:
        async with _graph_lock:
            if _graph is None:
                _graph = await build_graph()
    return _graph


def reset_graph() -> None:
    """厂商 / 角色 / MCP 配置发生变更后调用，让下一次请求重新构图。"""
    global _graph
    _graph = None
    reset_mcp_tools()
