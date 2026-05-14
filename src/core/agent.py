"""Base agent abstraction."""

from abc import ABC, abstractmethod
from typing import Optional

from .config import Config
from .llm import HelloAgentsLLM
from .message import Message


class Agent(ABC):
    """Base class for all agents."""

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str, **kwargs):
        """Run agent."""
        pass

    def add_message(self, message: Message):
        """Add a message to conversation history."""
        self._history.append(message)

        max_history_length = getattr(
            self.config,
            "max_history_length",
            getattr(self.config, "max_histroy_length", None),
        )
        if max_history_length and len(self._history) > max_history_length:
            self._history = self._history[-max_history_length:]

    def clear_history(self):
        """Clear conversation history."""
        self._history.clear()

    def get_history(self) -> list[Message]:
        """Return a shallow copy of conversation history."""
        return self._history.copy()

    def __str__(self) -> str:
        return f"Agent(name={self.name}, provider={self.llm.provider})"
