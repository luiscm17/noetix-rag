from typing import Any

from agent_framework import AgentSession, BaseContextProvider, SessionContext


class QdrantMemoryProvider(BaseContextProvider):
    """Custom context provider for long-term memory using Qdrant.

    This provider:
    - Searches relevant memories in Qdrant before each run
    - Injects them into the agent context
    - Stores new facts from the conversation
    """

    def __init__(self) -> None:
        super().__init__("qdrant_memory")

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

        memories = self._vector_store.search_similar_chunks(
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

    async def after_run(
        self,
        *,
        agent: Any,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Store new user facts from the conversation."""
        from src.rag.pipeline.vector_store import VectorStore
        from src.config.settings import AgentSettings

        if not hasattr(self, "_vector_store"):
            AgentSettings.validate_llm_embedding_settings()
            self._vector_store = VectorStore()

        facts_to_store = []

        if context.response and hasattr(context.response, "text"):
            text = context.response.text
            if text:
                extracted = self._extract_facts(text)
                facts_to_store.extend(extracted)

        if facts_to_store:
            chunks = [
                {
                    "text": fact,
                    "metadata": {
                        "source": "memory",
                        "filename": "user_memory",
                        "container": "long_term_memory",
                    },
                }
                for fact in facts_to_store
            ]
            self._vector_store.vectorize_and_store_chunks(chunks)

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
