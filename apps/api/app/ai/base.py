from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AIMessage:
    role: str
    content: str


class AIProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        raise NotImplementedError


class AIProviderUnavailable(RuntimeError):
    """Raised when a configured provider cannot be used for this request."""


class MockAIProvider(AIProvider):
    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        return (
            "I can help with general civic guidance. I will classify the issue, ask for missing details, "
            "and generate a guidance report with source notes once enough information is available."
        )
