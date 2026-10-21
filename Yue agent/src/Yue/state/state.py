from typing import Annotated

from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

"""
    ═══════════════════════════════════════════════════
                            状态
    ═══════════════════════════════════════════════════
"""


class AgentState(MessagesState):
    next: str
