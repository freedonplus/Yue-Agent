# Yue/models.py 请求参数变量
from pydantic import BaseModel, Field


class GetModel(BaseModel):
    MODEL_NAME: str=Field(default="deepseek-flash",description="模型名称:默认:deepseek-flash")
    MODEL_BASE_URL: str=Field(default="https://api.deepseek.com",description="模型请求URL:默认:https://api.deepseek.com")
    MODEL_API_KEY: str=Field(default="sk-asf***********",description="模型:api_key")
    MODEL_TEMPERATURE: float=Field(default=1.0,description="模型温度:默认:1.0")
    MODEL_MAX_TOKENS: int=Field(default=8192,description="模型最大输出TOKEN:默认:8192")
    MODEL_MAX_RETRIES: int=Field(default=3,description="模型最大重试次数:默认:3")


class SupervisorOutput(BaseModel):
    next: str=Field(default="FINISH",description="员工slug 或 FINISH")
    instructions: str=Field(description="给该员工的完整指令；FINISH 时为空字符串")