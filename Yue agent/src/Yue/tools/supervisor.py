from langchain_core.tools import tool

from Yue.schemas import SupervisorOutput


@tool("route", args_schema=SupervisorOutput)
def route_tool(next: str, instructions: str) -> str:
    """决定这一步该谁上。"""
    return next


Supervisor_tools = [route_tool]