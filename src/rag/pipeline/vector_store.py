import uuid
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.config.settings import AgentSettings, QdrantSettings, ChunkingSettings
from src.rag.pipeline.embedding import EmbeddingService


class VectorStore:
    def __init__(self):
        AgentSettings.validate_llm_embedding_settings()

        self._embedding = EmbeddingService()
        self.client = QdrantClient(**QdrantSettings.get_qdrant_client_config())

        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            collections = self.client.get_collections()
            collection_exists = any(
                c.name == QdrantSettings.COLLECTION_NAME
                for c in collections.collections
            )

            if not collection_exists:
                self.client.create_collection(
                    collection_name=QdrantSettings.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=QdrantSettings.VECTOR_SIZE, distance=Distance.COSINE
                    ),
                )
        except Exception:
            self.client.create_collection(
                collection_name=QdrantSettings.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=QdrantSettings.VECTOR_SIZE, distance=Distance.COSINE
                ),
            )

    def _ensure_memory_collection_exists(self):
        try:
            collections = self.client.get_collections()
            collection_exists = any(
                c.name == QdrantSettings.MEMORY_COLLECTION
                for c in collections.collections
            )

            if not collection_exists:
                self.client.create_collection(
                    collection_name=QdrantSettings.MEMORY_COLLECTION,
                    vectors_config=VectorParams(
                        size=QdrantSettings.VECTOR_SIZE, distance=Distance.COSINE
                    ),
                )
        except Exception:
            self.client.create_collection(
                collection_name=QdrantSettings.MEMORY_COLLECTION,
                vectors_config=VectorParams(
                    size=QdrantSettings.VECTOR_SIZE, distance=Distance.COSINE
                ),
            )

    def vectorize_and_store_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        points = []

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self._embedding.embed(texts)

        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "source": chunk["metadata"]["source"],
                    "filename": chunk["metadata"]["filename"],
                    "container": chunk["metadata"]["container"],
                },
            )
            points.append(point)

        stored_count = 0
        for i in range(0, len(points), QdrantSettings.BATCH_SIZE):
            batch = points[i : i + QdrantSettings.BATCH_SIZE]
            self.client.upsert(
                collection_name=QdrantSettings.COLLECTION_NAME, points=batch
            )
            stored_count += len(batch)

        return stored_count

    def search_similar_chunks(
        self, query: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        if limit is None:
            limit = ChunkingSettings.CHUNK_LIMIT

        query_embeddings = self._embedding.embed([query])
        query_vector = query_embeddings[0]

        search_results = self.client.query_points(
            collection_name=QdrantSettings.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            score_threshold=QdrantSettings.SCORE_THRESHOLD,
            with_payload=True,
        ).points

        results = []
        for hit in search_results:
            payload = hit.payload
            if payload:
                results.append(
                    {
                        "text": payload.get("text", ""),
                        "source": payload.get("source", ""),
                        "filename": payload.get("filename", ""),
                        "container": payload.get("container", ""),
                        "score": hit.score,
                    }
                )

        return results

    def store_memory(self, text: str) -> int:
        """Store a memory in the memory collection."""
        self._ensure_memory_collection_exists()

        embeddings = self._embedding.embed([text])
        embedding = embeddings[0]

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": text,
                "source": "memory",
                "filename": "user_memory",
                "container": "long_term_memory",
            },
        )

        self.client.upsert(
            collection_name=QdrantSettings.MEMORY_COLLECTION,
            points=[point],
        )

        return 1

    def search_memories(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Search memories in the memory collection."""
        self._ensure_memory_collection_exists()

        query_embeddings = self._embedding.embed([query])
        query_vector = query_embeddings[0]

        search_results = self.client.query_points(
            collection_name=QdrantSettings.MEMORY_COLLECTION,
            query=query_vector,
            limit=limit,
            score_threshold=0.3,
            with_payload=True,
        ).points

        results = []
        for hit in search_results:
            payload = hit.payload
            if payload:
                results.append(
                    {
                        "text": payload.get("text", ""),
                        "score": hit.score,
                    }
                )

        return results
