from typing import Any

from agent_framework import AgentSession, BaseContextProvider, SessionContext


class MemoryProvider(BaseContextProvider):
    """Custom context provider for long-term memory using vector store.

    This provider:
    - Searches relevant memories in vector store before each run
    - Injects them into the agent context
    - Stores new facts from the conversation
    """

    def __init__(self) -> None:
        super().__init__("user_memory")

    async def before_run(
        self,
        *,
        agent: Any,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Search for relevant memories and inject into context."""
        from src.rag.pipeline.vector_store import VectorStore
        from src.config.settings import AgentSettings

        AgentSettings.validate_llm_embedding_settings()

        if not hasattr(self, "_vector_store"):
            self._vector_store = VectorStore()

        user_message = None
        for msg in context.input_messages:
            if hasattr(msg, "role") and msg.role == "user":
                user_message = msg.text if hasattr(msg, "text") else str(msg)
                break

        if not user_message:
            return

        extracted = self._extract_facts(user_message)
        if extracted:
            for fact in extracted:
                self._vector_store.store_memory(fact)

        memories = self._vector_store.search_memories(
            query=user_message,
            limit=3,
        )

        if not memories:
            return

        memory_texts = [f"- {m['text']}" for m in memories]
        memory_context = "\n".join(memory_texts)

        context.extend_instructions(
            self.source_id,
            f"\nUser memories (use these when relevant):\n{memory_context}",
        )

    def _extract_facts(self, text: str) -> list[str]:
        """Extract factual statements from text."""
        facts = []

        indicators = [
            "my name is",
            "i am a",
            "i like",
            "i prefer",
            "i love",
            "i hate",
            "my favorite",
            "i work as",
            "i work at",
            "remember that",
            "remember my",
        ]

        text_lower = text.lower()
        for indicator in indicators:
            if indicator in text_lower:
                facts.append(text)

        return facts
