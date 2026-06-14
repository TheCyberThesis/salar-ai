from app.ai.base import AIMessage, AIProvider, MockAIProvider
from app.config import get_settings


class GrokProvider(AIProvider):
    def __init__(self) -> None:
        self.settings = get_settings()
        self.mock = MockAIProvider()

    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        if not self.settings.grok_api_key:
            return await self.mock.generate(messages, complex_case=complex_case)
        # Wire the xAI/Grok API here once the deployment has approved outbound access.
        return await self.mock.generate(messages, complex_case=complex_case)
