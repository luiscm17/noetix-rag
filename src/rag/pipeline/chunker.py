import json
import os
from typing import List, Dict, Any

from azure.storage.blob import BlobServiceClient
from chunking_evaluation.chunking import ClusterSemanticChunker
from chunking_evaluation.utils import openai_token_count
from chromadb.utils import embedding_functions

from src.config.settings import (
    AgentSettings,
    BlobStorageSettings,
    BlobStorageContainerSettings,
    ChunkingSettings,
)


class DocumentChunker:
    def __init__(self):
        BlobStorageSettings.validate()
        AgentSettings.validate_llm_embedding_settings()

        conn_str = BlobStorageSettings.AZURE_STORAGE_CONNECTION_STRING
        assert conn_str is not None
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)

        embedding_endpoint = AgentSettings.LLM_EMBEDDING_ENDPOINT
        embedding_model = AgentSettings.LLM_EMBEDDING_MODEL
        embedding_apikey = AgentSettings.LLM_EMBEDDING_APIKEY
        assert embedding_endpoint is not None
        assert embedding_model is not None
        assert embedding_apikey is not None

        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=embedding_apikey,
            model_name=embedding_model,
            api_base=embedding_endpoint,
        )

        self.semantic_chunker = ClusterSemanticChunker(
            embedding_function=self.embedding_function,
            max_chunk_size=ChunkingSettings.MAX_CHUNK_SIZE,
            min_chunk_size=ChunkingSettings.MIN_CHUNK_SIZE,
            length_function=openai_token_count,
        )

    def chunk_document_from_azure(self, document_name: str) -> List[Dict[str, Any]]:
        container_client = self.blob_service_client.get_container_client(
            BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER
        )

        blob_client = container_client.get_blob_client(document_name)
        blob_content = blob_client.download_blob().readall()
        document_content = blob_content.decode("utf-8")

        chunks = self._semantic_chunking(document_content, document_name)

        self._save_chunks_to_azure(chunks, document_name)

        return chunks

    def _semantic_chunking(
        self, document_content: str, document_name: str
    ) -> List[Dict[str, Any]]:
        doc_chunks = self.semantic_chunker.split_text(document_content)

        doc_name = os.path.splitext(os.path.basename(document_name))[0]

        chunks = [
            {
                "text": chunk,
                "metadata": {
                    "source": document_name,
                    "filename": doc_name,
                    "container": BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER,
                },
            }
            for chunk in doc_chunks
        ]

        return chunks

    def _save_chunks_to_azure(self, chunks: List[Dict[str, Any]], document_name: str):
        try:
            self.blob_service_client.create_container(
                BlobStorageContainerSettings.DOCUMENT_CHUNKS_CONTAINER
            )
        except Exception:
            pass

        chunks_json = json.dumps(chunks, ensure_ascii=False, indent=2)
        chunks_blob_client = self.blob_service_client.get_blob_client(
            container=BlobStorageContainerSettings.DOCUMENT_CHUNKS_CONTAINER,
            blob=f"chunks_{len(chunks)}_items.json",
        )
        chunks_blob_client.upload_blob(chunks_json, overwrite=True)
