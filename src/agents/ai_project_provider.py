from agents.base_agent import BaseAgent
from config.settings import AgentSettings
from agent_framework.azure import AzureAIProjectAgentProvider
from azure.identity.aio import AzureCliCredential

class AIProjectProvider(BaseAgent):    
    async def build(self, name: str, instructions: str, tools: list = None):
        client = AzureAIProjectAgentProvider(
            project_client=AgentSettings.AI_PROJECT_ENDPOINT,
            model=AgentSettings.AI_MODEL_DEPLOYMENT_NAME,
            credential=AzureCliCredential()
        ).as_agent(
            name=name,
            instructions=instructions,
            tools=tools or []
        )
        return client
