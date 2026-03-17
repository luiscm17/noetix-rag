from typing import Any

from agent_framework.orchestrations import GroupChatBuilder
from agent_framework.redis import RedisHistoryProvider

from src.agents.memory_provider import MemoryProvider
from src.agents.rag_agent import rag_agent
from src.agents.socratic_agent import socratic_agent
from src.agents.teacher_agent import teacher_agent
from src.agents.triage_agent import triage_agent
from src.config.settings import RedisSettings


class AgentOrchestrator:
    def __init__(self, triage: Any, rag: Any, teacher: Any, socratic: Any):
        workflow = GroupChatBuilder(
            participants=[
                rag.agent,
                teacher.agent,
                socratic.agent,
            ],
            termination_condition=lambda msgs: sum(
                1 for m in msgs if hasattr(m, "role") and m.role == "assistant"
            )
            >= 5,
            orchestrator_agent=triage.agent,
        ).build()

        self._history_provider = RedisHistoryProvider(
            redis_url=RedisSettings.get_redis_url(),
            load_messages=True,
            key_prefix=RedisSettings.REDIS_KEY_PREFIX,
        )

        self._memory_provider = MemoryProvider()

        self.agent = workflow.as_agent(
            name="AgentOrchestrator",
        )

        self.agent.context_providers = [self._history_provider, self._memory_provider]

    async def run(self, message: str, session_id: str | None = None) -> str:
        """Run the group chat workflow and return the response."""
        if session_id:
            session = self.agent.create_session(session_id=session_id)
            result = await self.agent.run(message, session=session)
        else:
            result = await self.agent.run(message)

        messages = result.messages if hasattr(result, "messages") else []

        assistant_texts = []
        for msg in messages:
            if hasattr(msg, "role") and msg.role == "assistant":
                if hasattr(msg, "text") and msg.text:
                    if "termination" in msg.text.lower():
                        continue
                    assistant_texts.append(msg.text)

        if assistant_texts:
            return assistant_texts[-1]

        return str(result)[:500] if len(str(result)) > 500 else str(result)


_orchestrator: AgentOrchestrator | None = None


async def create_orchestrator() -> AgentOrchestrator:
    """Create and configure the group chat workflow."""
    global _orchestrator
    if _orchestrator is None:
        triage = await triage_agent()
        rag = await rag_agent()
        teacher = await teacher_agent()
        socratic = await socratic_agent()
        _orchestrator = AgentOrchestrator(triage, rag, teacher, socratic)
    return _orchestrator


async def get_response(
    message: str, session_id: str | None = None, user_id: int | None = None
) -> str:
    """Helper function to get a complete response from the orchestrator."""
    orchestrator = await create_orchestrator()
    return await orchestrator.run(message, session_id=session_id)
