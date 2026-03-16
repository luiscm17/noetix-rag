import asyncio
from typing import Annotated, Any

from agent_framework import tool
from src.agents.azureopenai_provider import AzureOpenAIProvider
from src.rag.pipeline.vector_store import VectorStore


class RAGAgent:
    def __init__(self, agent):
        self.agent = agent

    async def run(self, question: str):
        result = await self.agent.run(question)
        return result.text if hasattr(result, "text") else result


def _create_search_tool(vector_store: VectorStore):
    @tool(approval_mode="never_require")
    def search_documents(
        query: Annotated[str, "The search query to find relevant documents"],
    ) -> str:
        try:
            results = vector_store.search_similar_chunks(query)

            if not results:
                return "No se encontraron documentos relevantes para tu consulta."

            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(
                    f"Documento {i} (Score: {result['score']:.3f}):\n"
                    f"Fuente: {result['filename']}\n"
                    f"Contenido: {result['text'][:500]}...\n"
                )

            context = "\n---\n".join(context_parts)
            return context

        except Exception as e:
            return f"Error al buscar documentos: {str(e)}"

    return search_documents


async def rag_agent():
    vector_store = VectorStore()
    search_tool = _create_search_tool(vector_store)

    provider = AzureOpenAIProvider()
    agent = await provider.build(
        name="RAGDocumentAgent",
        instructions="""You are a document specialist that answers questions using ONLY the provided documents.

IMPORTANT RESTRICTIONS:
- You do NOT have internet access
- You can ONLY answer using information from the loaded documents
- If no documents are loaded, clearly state that no documents are available

When a user asks a question:
1. ALWAYS use the search_documents tool first to find relevant information
2. Analyze the documents found - check the content and sources
3. If results are found: Answer based ONLY on the document content, citing sources
4. If NO results found: Clearly state "No relevant information found in the loaded documents" and suggest the user upload documents

RESPONSE RULES:
- Never make up information - only use what's in the documents
- Always cite sources: "According to [filename], ..."
- If the question is general knowledge unrelated to documents, tell the user to ask the triage agent""",
        tools=[search_tool],
    )
    return RAGAgent(agent)
