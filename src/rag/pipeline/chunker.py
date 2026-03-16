import json
import os
from typing import List, Dict, Any

from azure.storage.blob import BlobServiceClient
from agent_framework.azure import AzureOpenAIChatClient

from src.config.settings import (
    AgentSettings,
    BlobStorageSettings,
    BlobStorageContainerSettings,
)

SYSTEM_PROMPT = """You are a document chunking specialist for scientific and technical documents.

Your task: Divide any document into semantically coherent chunks.

RULES:
- Each chunk = one complete semantic unit (one section OR one subsection OR one paragraph that stands alone)
- NEVER combine different sections or topics in one chunk
- If a section is too large (>800 tokens), split it at logical points (subsections, paragraphs)
- If a section is too small (<200 tokens), merge with previous or next chunk if semantically related

CONTENT TO PRESERVE EXACTLY:
- Equations (LaTeX, MathML)
- Tables
- Image references
- Code blocks
- Markdown formatting
- Bullet points and lists

DO NOT: summarize, paraphrase, modify, or add any content.

OUTPUT - JSON only:
{"chunks": [{"content": "...", "metadata": {"section": "heading number from document", "title": "heading text from document"}}]}"""


class AgenticChunker:
    def __init__(self):
        AgentSettings.openai_settings()

        self._client = AzureOpenAIChatClient(
            api_key=AgentSettings.OPENAI_API_KEY,
            endpoint=AgentSettings.OPENAI_ENDPOINT,
            deployment_name=AgentSettings.OPENAI_MODEL_ID,
        )
        self._agent = self._client.as_agent(name="Chunker", instructions=SYSTEM_PROMPT)

    async def chunk(self, text: str) -> List[Dict[str, Any]]:
        response = await self._agent.run(f"Chunk this document:\n\n{text}")
        return self._parse_response(response)

    def chunk_sync(self, text: str) -> List[Dict[str, Any]]:
        import asyncio

        return asyncio.run(self.chunk(text))

    def _parse_response(self, response) -> List[Dict[str, Any]]:
        import json
        import re

        content = str(response)
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            data = json.loads(match.group())
            chunks = data.get("chunks", [])
            if chunks:
                for chunk in chunks:
                    if "metadata" not in chunk:
                        chunk["metadata"] = {}
                return chunks

        content_clean = content.strip()
        paragraphs = re.split(r"\n\n+", content_clean)
        return [
            {"content": p.strip(), "metadata": {"section": "", "title": ""}}
            for p in paragraphs
            if p.strip()
        ]


class DocumentChunker:
    def __init__(self):
        BlobStorageSettings.validate()
        AgentSettings.openai_settings()

        conn_str = BlobStorageSettings.AZURE_STORAGE_CONNECTION_STRING
        assert conn_str is not None
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)

        self._chunker = AgenticChunker()

    def chunk_document(self, document_name: str) -> List[Dict[str, Any]]:
        container_client = self.blob_service_client.get_container_client(
            BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER
        )

        blob_client = container_client.get_blob_client(document_name)
        blob_content = blob_client.download_blob().readall()
        document_content = blob_content.decode("utf-8")

        chunks = self._semantic_chunking(document_content, document_name)

        self._save_chunks(chunks, document_name)

        return chunks

    def _semantic_chunking(
        self, document_content: str, document_name: str
    ) -> List[Dict[str, Any]]:
        raw_chunks = self._chunker.chunk_sync(document_content)

        doc_name = os.path.splitext(os.path.basename(document_name))[0]

        chunks = [
            {
                "text": chunk.get("content", ""),
                "metadata": {
                    "source": document_name,
                    "filename": doc_name,
                    "container": BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER,
                    "section": chunk.get("metadata", {}).get("section", ""),
                    "title": chunk.get("metadata", {}).get("title", ""),
                },
            }
            for chunk in raw_chunks
        ]

        return chunks

    def _save_chunks(self, chunks: List[Dict[str, Any]], document_name: str):
        try:
            self.blob_service_client.create_container(
                BlobStorageContainerSettings.DOCUMENT_CHUNKS_CONTAINER
            )
        except Exception:
            pass

        chunks_json = json.dumps(chunks, ensure_ascii=False, indent=2)
        doc_name = os.path.splitext(os.path.basename(document_name))[0]
        chunks_blob_client = self.blob_service_client.get_blob_client(
            container=BlobStorageContainerSettings.DOCUMENT_CHUNKS_CONTAINER,
            blob=f"chunk_{doc_name}.json",
        )
        chunks_blob_client.upload_blob(chunks_json, overwrite=True)
