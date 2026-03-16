import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class AgentSettings:
    AI_PROJECT_ENDPOINT: Optional[str] = os.getenv("AI_PROJECT_ENDPOINT")
    AI_MODEL_DEPLOYMENT_NAME: Optional[str] = os.getenv("AI_MODEL_DEPLOYMENT_NAME")

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_ID: Optional[str] = os.getenv("OPENAI_MODEL_ID")
    OPENAI_ENDPOINT: Optional[str] = os.getenv("OPENAI_ENDPOINT")

    OLLAMA_MODEL_ID: Optional[str] = os.getenv("OLLAMA_MODEL_ID")
    OLLAMA_ENDPOINT: Optional[str] = os.getenv("OLLAMA_ENDPOINT")

    LLM_EMBEDDING_ENDPOINT: str = os.getenv("LLM_EMBEDDING_ENDPOINT", "")
    LLM_EMBEDDING_MODEL: str = os.getenv(
        "LLM_EMBEDDING_MODEL", "text-embedding-3-large"
    )
    LLM_EMBEDDING_APIKEY: Optional[str] = os.getenv("LLM_EMBEDDING_APIKEY")
    LLM_EMBEDDING_API_VERSION: str = os.getenv(
        "LLM_EMBEDDING_API_VERSION", "2024-02-01"
    )

    @classmethod
    def ai_project_settings(cls) -> None:
        if not cls.AI_PROJECT_ENDPOINT:
            raise ValueError("AI_PROJECT_ENDPOINT is not configured")
        if not cls.AI_MODEL_DEPLOYMENT_NAME:
            raise ValueError("AI_MODEL_DEPLOYMENT_NAME is not configured")

    @classmethod
    def openai_settings(cls) -> None:
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        if not cls.OPENAI_MODEL_ID:
            raise ValueError("OPENAI_MODEL_ID is not configured")
        if not cls.OPENAI_ENDPOINT:
            raise ValueError("OPENAI_ENDPOINT is not configured")

    @classmethod
    def ollama_settings(cls) -> None:
        if not cls.OLLAMA_MODEL_ID:
            raise ValueError("OLLAMA_MODEL_ID is not configured")
        if not cls.OLLAMA_ENDPOINT:
            raise ValueError("OLLAMA_ENDPOINT is not configured")

    @classmethod
    def validate_llm_embedding_settings(cls) -> None:
        if not cls.LLM_EMBEDDING_ENDPOINT:
            raise ValueError("LLM_EMBEDDING_ENDPOINT is not configured")
        if not cls.LLM_EMBEDDING_MODEL:
            raise ValueError("LLM_EMBEDDING_MODEL is not configured")


class BlobStorageSettings:
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING"
    )
    AZURE_STORAGE_CONTAINER: Optional[str] = os.getenv("AZURE_STORAGE_CONTAINER")

    @classmethod
    def validate(cls) -> None:
        if not cls.AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not configured")
        if not cls.AZURE_STORAGE_CONTAINER:
            raise ValueError("AZURE_STORAGE_CONTAINER is not configured")


class DBSettings:
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    @classmethod
    def get_database_url(cls) -> Optional[str]:
        return cls.DATABASE_URL

    @classmethod
    def validate_database_settings(cls) -> None:
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is not configured")


class AuthSettings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key_for_dev_only")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_DELTA: int = int(os.getenv("JWT_EXPIRE_DELTA", "1800"))

    @classmethod
    def validate_auth_settings(cls) -> None:
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is not configured")


class QdrantSettings:
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME: str = "document_chunks"
    VECTOR_SIZE: int = 3072
    BATCH_SIZE: int = 100
    SCORE_THRESHOLD: float = 0.3

    @classmethod
    def get_qdrant_client_config(cls) -> dict:
        return {"url": cls.QDRANT_URL, "api_key": cls.QDRANT_API_KEY, "timeout": 60}


class ChunkingSettings:
    MAX_CHUNK_SIZE: int = 800
    MIN_CHUNK_SIZE: int = 200
    CHUNK_LIMIT: int = 5


class BlobStorageContainerSettings:
    DOCUMENTS_PDF_CONTAINER: str = os.getenv("DOCUMENTS_PDF_CONTAINER", "documentspdf")
    DOCUMENT_PROCESSED_CONTAINER: str = os.getenv(
        "DOCUMENT_PROCESSED_CONTAINER", "documentprocessed"
    )
    DOCUMENT_CHUNKS_CONTAINER: str = os.getenv(
        "DOCUMENT_CHUNKS_CONTAINER", "documentchunks"
    )
