from typing import Any

from src.agents.azureopenai_provider import AzureOpenAIProvider


class TriageAgent:
    def __init__(self, agent: Any):
        self.agent = agent

    async def run(self, question: str):
        result = await self.agent.run(question)
        return result.text if hasattr(result, "text") else result


async def triage_agent():
    provider = AzureOpenAIProvider()
    agent = await provider.build(
        name="TriageAgent",
        instructions="""You are the Triage Coordinator for a RAG-based document assistant.

Your role is to route user queries to the appropriate specialist. You NEVER answer directly - you ALWAYS transfer to a specialist.

ROUTING RULES:
1. User asks about documents, books, files, or says "in the document", "the book" -> handoff to "RAGDocumentAgent"
2. User says "I don't understand", "explain differently", "not clear" -> handoff to "TeacherAgent"
3. User asks for a quiz, test, or "ask me questions" -> handoff to "SocraticTutor"
4. User shares personal info (name, preferences, facts about themselves) -> handoff to "TeacherAgent" (to acknowledge)
5. General knowledge questions (what is X, how does Y work) -> handoff to "TeacherAgent"
6. Any other question -> handoff to "TeacherAgent"

CRITICAL RULES:
- You MUST use the handoff tool - never respond directly
- Always provide a brief message explaining why you are transferring
- The last message should be your transfer announcement, not a final answer

Example: I will connect you with our document specialist who can help with that. -> handoff to "RAGDocumentAgent"
""",
    )
    return TriageAgent(agent)
