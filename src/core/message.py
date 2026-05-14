"""消息系统"""

from pydantic import BaseModel
from typing import Literal, Dict, Any, Optional
from datetime import datetime

# 定义消息角色的类型，限制其取值
MessageRole = Literal["user", "system", "assistant", "tool"]


class Message(BaseModel):
    """消息类，用作 Agent 之间的消息协议"""

    content: str
    role: MessageRole
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

    def __init__(self, content: str, role: MessageRole, **kwargs):
        super().__init__(
            content=content,
            role=role,
            timestamp=kwargs.get("timestamp", datetime.now()),
            metadata=kwargs.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, any]:
        """转换为字典格式（OpenAI API格式）"""
        return {"role": self.role, "content": self.content}

    def __str__(self) -> str:
        return "f[{self.role}] {self.content}"
