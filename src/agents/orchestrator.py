from typing import Any

from agent_framework.orchestrations import GroupChatBuilder

from src.agents.rag_agent import rag_agent
from src.agents.socratic_agent import socratic_agent
from src.agents.teacher_agent import teacher_agent
from src.agents.triage_agent import triage_agent


class AgentOrchestrator:
    def __init__(self, triage: Any, rag: Any, teacher: Any, socratic: Any):
        self.workflow = GroupChatBuilder(
            participants=[
                rag.agent,
                teacher.agent,
                socratic.agent,
            ],
            termination_condition=lambda msgs: sum(
                1 for m in msgs if hasattr(m, "role") and m.role == "assistant"
            )
            >= 2,  # End after triage responds + specialist responds
            orchestrator_agent=triage.agent,
        ).build()

    async def run(self, message: str) -> str:
        """Run the group chat workflow and return the response."""
        result = await self.workflow.run(message)

        # Result is a list of WorkflowEvent
        if isinstance(result, list):
            for event in result:
                if event.type == "output":
                    data = event.data
                    if isinstance(data, list):
                        texts = []
                        for msg in data:
                            if (
                                hasattr(msg, "text")
                                and msg.text
                                and msg.text != message
                            ):
                                # Skip termination messages
                                if "termination" in msg.text.lower():
                                    continue
                                texts.append(msg.text)
                        # Get last unique message (final response)
                        if texts:
                            return texts[-1]

        return str(result)[:500] if len(str(result)) > 500 else str(result)


async def create_orchestrator() -> AgentOrchestrator:
    """Create and configure the group chat workflow."""
    triage = await triage_agent()
    rag = await rag_agent()
    teacher = await teacher_agent()
    socratic = await socratic_agent()

    return AgentOrchestrator(triage, rag, teacher, socratic)


async def get_response(message: str) -> str:
    """Helper function to get a complete response from the orchestrator."""
    orchestrator = await create_orchestrator()
    return await orchestrator.run(message)
