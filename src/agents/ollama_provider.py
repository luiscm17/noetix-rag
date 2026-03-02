from agents.base_agent import BaseAgent
from agent_framework.ollama import OllamaChatClient
from config.settings import AgentSettings

class OllamaProvider(BaseAgent):
    async def build(self, name: str, instructions: str, tools: list = None):
        client = OllamaChatClient(
            model=AgentSettings().OLLAMA_MODEL_ID,
            base_url=AgentSettings().OLLAMA_ENDPOINT,
        ).as_agent(
            name=name,
            instructions=instructions,
            tools=tools or []
        )
        return client

