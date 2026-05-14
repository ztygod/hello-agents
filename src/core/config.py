"""配置管理"""

import os
from typing import Any, Dict, Optional
from pydantic import BaseModel


class Config(BaseModel):
    """HelloAgents 配置类"""

    # LLM 配置
    default_model: str = "deepseek-v4-pro"
    default_provider: str = "DeepSeek"
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    # 系统配置
    debug_tool: bool = False
    log_level: str = "INFO"

    # 其他配置
    max_histroy_length: int = 100

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量创建配置"""
        return cls(
            debug_tool=os.getenv("DEBUG_TOOL", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS"))
            if os.getenv("MAX_TOKENS")
            else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.model_dump()
