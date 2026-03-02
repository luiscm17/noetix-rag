import asyncio
from agents.openai_provider import OpenAIProvider

class TeacherAgent:
    def __init__(self, agent):
        self.agent = agent

    async def run(self, question: str):
        result = await self.agent.run(question)
        return result.text if hasattr(result, "text") else result

async def teacher_agent():
    provider = OpenAIProvider()
    agent = await provider.build(
        name="Teacher Agent",
        instructions="You are a helpful teacher agent.",
    )
    return TeacherAgent(agent)
