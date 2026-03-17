from typing import Any

from src.agents.base_agent import BaseAgent
from agent_framework.azure import AzureOpenAIChatClient
from src.config.settings import AgentSettings


class AzureOpenAIProvider(BaseAgent):
    async def build(self, name: str, instructions: str, tools: list[Any] | None = None):
        client = AzureOpenAIChatClient(
            api_key=AgentSettings.OPENAI_API_KEY,
            endpoint=AgentSettings.OPENAI_ENDPOINT,
            deployment_name=AgentSettings.OPENAI_MODEL_ID,
        ).as_agent(name=name, instructions=instructions, tools=tools or [])
        return client
