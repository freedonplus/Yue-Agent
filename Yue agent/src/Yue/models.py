from functools import lru_cache
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, convert_to_messages
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

from settings import settings
from Yue.schemas import GetModel
"""
    ═══════════════════════════════════════════════════
                        进行配置并获取模型
    ═══════════════════════════════════════════════════
"""


class ChatDeepSeekThinking(ChatDeepSeek):
    """DeepSeek 思考模式要求把上一轮的 reasoning_content 原样回传。

    langchain-deepseek 只负责把返回值放进 additional_kwargs，
    再次请求时不会写回 payload，历史里只要有 assistant 消息就会 400。
    这里在序列化之后统一补上该字段；我们自己合成的消息（调度员指令、
    前端传来的历史）没有思考内容，补空字符串占位即可。
    """

    def _get_request_payload(
        self,
        input_: Any,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)

        try:
            messages = convert_to_messages(input_)
        except Exception:
            return payload

        payload_messages = payload.get("messages") or []
        if len(messages) != len(payload_messages):
            return payload

        for message, item in zip(messages, payload_messages):
            if not isinstance(message, AIMessage):
                continue
            if item.get("role") != "assistant":
                continue
            reasoning = message.additional_kwargs.get("reasoning_content")
            item["reasoning_content"] = (
                reasoning if isinstance(reasoning, str) else ""
            )

        return payload


@lru_cache(maxsize=100)
def _create_model(
        model_name: str,
        base_url: str,
        api_key: str,
        temperature: float,
        max_tokens: int,
        max_retries: int,
) -> BaseChatModel:
    # 流式调用默认不返回用量；开启后 OpenAI 兼容端点会在最后一块带 usage
    stream_usage = settings.MODEL_STREAM_USAGE

    # ChatOpenAI 会丢弃非标准返回字段（如 DeepSeek 的 reasoning_content）；
    # DeepSeek 端点改用专用子类，思考内容才能进入 additional_kwargs。
    if "deepseek" in f"{model_name} {base_url}".lower():
        return ChatDeepSeekThinking(
            model=model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            stream_usage=stream_usage,
        )

    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        max_retries=max_retries,
        stream_usage=stream_usage,
    )


def get_model(setting: GetModel) -> BaseChatModel:
    return _create_model(
        setting.MODEL_NAME,
        setting.MODEL_BASE_URL,
        setting.MODEL_API_KEY,
        setting.MODEL_TEMPERATURE,
        setting.MODEL_MAX_TOKENS,
        setting.MODEL_MAX_RETRIES,
    )
