from agents.base_agent import BaseAgent
from agent_framework.openai import OpenAIChatClient
from config.settings import AgentSettings

class OpenAIProvider(BaseAgent):
    async def build(self, name: str, instructions: str, tools: list = None):
        client = OpenAIChatClient(
            model_id=AgentSettings.OPENAI_MODEL_ID,
            base_url=AgentSettings.OPENAI_ENDPOINT,
            api_key=AgentSettings.OPENAI_API_KEY,
        ).as_agent(
            name=name,
            instructions=instructions,
            tools=tools or []
        )
        return client
