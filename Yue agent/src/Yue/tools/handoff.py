from typing import Literal

from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.types import Command

"""
    ═══════════════════════════════════════════════════
                        工人间转交
    ═══════════════════════════════════════════════════

    这里用工厂而不是全局唯一的工具，原因有两个：
    1. 白名单要按「当前工人」生成，且不能包含自己；
    2. 模块导入时 workers 还没从数据库读出来，不能在模块级写死 Literal。

    Command.PARENT 能生效的前提：工人节点必须是 create_agent 编译出的
    子图本体（见 nodes.make_worker_graph），外面不能再包一层函数。
"""


def make_handoff_tool(targets: list[str], self_slug: str):
    """给某个工人生成 handoff 工具：白名单 = 其余工人。"""
    allowed = sorted({t for t in targets if t and t != self_slug})
    Target = Literal[tuple(allowed)] if allowed else str

    @tool("handoff")
    def handoff(target: Target, reason: str) -> Command:
        """把这个任务转交给另一位工人，由它来接着回答用户。

        当用户的要求不属于你的职责、而属于另一位工人的职责时调用。
        调用后不要自己继续作答，把任务留给对方。

        Args:
            target: 转交给谁 —— 从白名单里挑一个工人。
            reason: 一句话说明为什么转交，会写进对话里给对方看。
        """
        return Command(
            graph=Command.PARENT,
            goto=target,
            update={
                # 父图的条件边靠 next 判断去向，必须和 goto 写同一个目标；
                # 否则会自动回边到调度员，和目标工人并行执行。
                "next": target,
                "messages": [
                    # 带上 name，调度员才知道这条是谁说的
                    AIMessage(content=f"【转交】{reason}", name=self_slug)
                ],
            },
        )

    return handoff
