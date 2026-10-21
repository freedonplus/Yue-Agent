from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

"""
    ═══════════════════════════════════════════════════
                        对话 Schema
    ═══════════════════════════════════════════════════
"""


class ChatMessage(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1, max_length=20000)


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=20000)
    # 可选的历史消息，用于多轮对话；由前端维护
    history: list[ChatMessage] = Field(default_factory=list, max_length=50)
    # 前端生成的会话标识，用于关联会话表里的工作目录
    session_id: str | None = Field(default=None, max_length=100)
    # 本次会话的工作目录；不传则读取 session_id 对应的会话设置
    workdir: str | None = Field(default=None, max_length=1000)
    # 本次任务指定使用的技能 slug；不传则由员工自行判断是否加载技能
    skill_slug: str | None = Field(default=None, max_length=50)
    # 跨会话记忆归属；没有账号体系时用稳定标识即可，默认 default
    user_id: str = Field(default="default", max_length=100)
    # 本轮可选的模型参数，覆盖厂商默认值；不传则沿用厂商配置
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_tokens: int | None = Field(default=None, ge=1, le=200_000)


class ApprovalDecision(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # 对应 approval_required 事件里的 interrupt_id
    interrupt_id: str = Field(min_length=1, max_length=100)
    type: Literal["approve", "reject"]
    # 拒绝时可以附一句原因，会作为工具结果回给模型
    message: str | None = Field(default=None, max_length=2000)


class ChatApprovalRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # 发起对话时返回的 run_id，也是图的 thread_id
    run_id: str = Field(min_length=1, max_length=100)
    decisions: list[ApprovalDecision] = Field(min_length=1, max_length=20)
    session_id: str | None = Field(default=None, max_length=100)
    # 续跑时也要带上，否则模型不知道本会话的工作目录
    workdir: str | None = Field(default=None, max_length=1000)
    # 续跑时也要带上，否则员工会丢掉本次任务指定的技能
    skill_slug: str | None = Field(default=None, max_length=50)
    # 续跑时保持同一个记忆归属
    user_id: str = Field(default="default", max_length=100)
    # 续跑时也要带上，否则会退回厂商默认参数
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_tokens: int | None = Field(default=None, ge=1, le=200_000)

    @property
    def resume_payload(self) -> dict:
        """转成 per_call 模式要求的 {interrupt_id: Decision}。"""
        payload: dict = {}
        for item in self.decisions:
            decision: dict = {"type": item.type}
            if item.type == "reject" and item.message:
                decision["message"] = item.message
            payload[item.interrupt_id] = decision
        return payload
