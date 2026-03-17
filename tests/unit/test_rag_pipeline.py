from unittest.mock import Mock, patch


class TestEmbeddingService:
    """Tests for EmbeddingService."""

    @patch("src.rag.pipeline.embedding.AzureOpenAI")
    @patch("src.rag.pipeline.embedding.AgentSettings")
    def test_embed_single_text(self, mock_settings, mock_azure_openai):
        """Test embedding a single text."""
        mock_settings.LLM_EMBEDDING_APIKEY = "test-key"
        mock_settings.LLM_EMBEDDING_ENDPOINT = "https://test.openai.azure.com"
        mock_settings.LLM_EMBEDDING_API_VERSION = "2024-02-01"
        mock_settings.LLM_EMBEDDING_MODEL = "text-embedding-3-small"

        mock_client = Mock()
        mock_azure_openai.return_value = mock_client

        mock_response = Mock()
        mock_data = Mock()
        mock_data.embedding = [0.1, 0.2, 0.3]
        mock_response.data = [mock_data]
        mock_client.embeddings.create.return_value = mock_response

        from src.rag.pipeline.embedding import EmbeddingService

        service = EmbeddingService()

        result = service.embed(["hello world"])

        assert result == [[0.1, 0.2, 0.3]]
        mock_client.embeddings.create.assert_called_once()

    @patch("src.rag.pipeline.embedding.AzureOpenAI")
    @patch("src.rag.pipeline.embedding.AgentSettings")
    def test_embed_multiple_texts(self, mock_settings, mock_azure_openai):
        """Test embedding multiple texts."""
        mock_settings.LLM_EMBEDDING_APIKEY = "test-key"
        mock_settings.LLM_EMBEDDING_ENDPOINT = "https://test.openai.azure.com"
        mock_settings.LLM_EMBEDDING_API_VERSION = "2024-02-01"
        mock_settings.LLM_EMBEDDING_MODEL = "text-embedding-3-small"

        mock_client = Mock()
        mock_azure_openai.return_value = mock_client

        mock_response = Mock()
        mock_data1 = Mock()
        mock_data1.embedding = [0.1, 0.2, 0.3]
        mock_data2 = Mock()
        mock_data2.embedding = [0.4, 0.5, 0.6]
        mock_response.data = [mock_data1, mock_data2]
        mock_client.embeddings.create.return_value = mock_response

        from src.rag.pipeline.embedding import EmbeddingService

        service = EmbeddingService()

        result = service.embed(["hello", "world"])

        assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]


class TestVectorStore:
    """Tests for VectorStore."""

    @patch("src.rag.pipeline.vector_store.QdrantClient")
    @patch("src.rag.pipeline.vector_store.AgentSettings")
    @patch("src.rag.pipeline.vector_store.QdrantSettings")
    @patch("src.rag.pipeline.vector_store.EmbeddingService")
    def test_init_creates_collection(
        self,
        mock_embedding,
        mock_qdrant_settings,
        mock_agent_settings,
        mock_qdrant_client,
    ):
        """Test initialization creates collection if not exists."""
        mock_agent_settings.validate_llm_embedding_settings = Mock()
        mock_qdrant_settings.COLLECTION_NAME = "test_collection"
        mock_qdrant_settings.VECTOR_SIZE = 1536
        mock_qdrant_settings.get_qdrant_client_config = Mock(
            return_value={"host": "localhost", "port": 6333}
        )

        mock_client_instance = Mock()
        mock_collections = Mock()
        mock_collection = Mock()
        mock_collection.name = "other_collection"
        mock_collections.collections = [mock_collection]
        mock_client_instance.get_collections.return_value = mock_collections
        mock_qdrant_client.return_value = mock_client_instance

        mock_embedding_instance = Mock()
        mock_embedding.return_value = mock_embedding_instance

        from src.rag.pipeline.vector_store import VectorStore

        VectorStore()

        mock_client_instance.create_collection.assert_called()

    @patch("src.rag.pipeline.vector_store.QdrantClient")
    @patch("src.rag.pipeline.vector_store.AgentSettings")
    @patch("src.rag.pipeline.vector_store.QdrantSettings")
    @patch("src.rag.pipeline.vector_store.ChunkingSettings")
    @patch("src.rag.pipeline.vector_store.EmbeddingService")
    def test_search_similar_chunks(
        self,
        mock_embedding,
        mock_chunking_settings,
        mock_qdrant_settings,
        mock_agent_settings,
        mock_qdrant_client,
    ):
        """Test searching similar chunks."""
        mock_agent_settings.validate_llm_embedding_settings = Mock()
        mock_qdrant_settings.COLLECTION_NAME = "test_collection"
        mock_qdrant_settings.VECTOR_SIZE = 1536
        mock_qdrant_settings.SCORE_THRESHOLD = 0.5
        mock_qdrant_settings.get_qdrant_client_config = Mock(
            return_value={"host": "localhost", "port": 6333}
        )
        mock_chunking_settings.CHUNK_LIMIT = 5

        mock_client_instance = Mock()
        mock_collections = Mock()
        mock_collections.collections = []
        mock_client_instance.get_collections.return_value = mock_collections

        mock_search_result = Mock()
        mock_payload = {
            "text": "test chunk",
            "source": "doc.md",
            "filename": "doc",
            "container": "processed",
        }
        mock_search_result.payload = mock_payload
        mock_search_result.score = 0.9
        mock_client_instance.query_points.return_value.points = [mock_search_result]
        mock_qdrant_client.return_value = mock_client_instance

        mock_embedding_instance = Mock()
        mock_embedding_instance.embed.return_value = [[0.1, 0.2, 0.3]]
        mock_embedding.return_value = mock_embedding_instance

        from src.rag.pipeline.vector_store import VectorStore

        store = VectorStore()

        results = store.search_similar_chunks("test query")

        assert len(results) == 1
        assert results[0]["text"] == "test chunk"
        assert results[0]["score"] == 0.9


class TestChunkerParsing:
    """Tests for chunker response parsing."""

    def test_parse_response_with_valid_json(self):
        """Test parsing valid JSON response."""
        with patch("src.rag.pipeline.chunker.AgentSettings") as mock_settings:
            mock_settings.openai_settings = Mock()
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.OPENAI_ENDPOINT = "https://test.openai.azure.com"
            mock_settings.OPENAI_MODEL_ID = "gpt-4"

            with patch("src.rag.pipeline.chunker.AzureOpenAIChatClient") as mock_client:
                mock_agent = Mock()
                mock_response = Mock()
                mock_response = '{"chunks": [{"content": "chunk1", "metadata": {"section": "1", "title": "Intro"}}]}'
                mock_agent.run.return_value = mock_response
                mock_client.return_value.as_agent.return_value = mock_agent

                from src.rag.pipeline.chunker import AgenticChunker

                chunker = AgenticChunker()

                result = chunker._parse_response(mock_response)

                assert len(result) == 1
                assert result[0]["content"] == "chunk1"

    def test_parse_response_fallback_paragraphs(self):
        """Test parsing fallback to paragraphs."""
        with patch("src.rag.pipeline.chunker.AgentSettings") as mock_settings:
            mock_settings.openai_settings = Mock()

            with patch("src.rag.pipeline.chunker.AzureOpenAIChatClient"):
                from src.rag.pipeline.chunker import AgenticChunker

                chunker = AgenticChunker()

                result = chunker._parse_response("Just plain text without JSON")

                assert len(result) > 0
                assert "content" in result[0]


class TestDocumentProcessorInit:
    """Tests for DocumentProcessor initialization."""

    @patch("src.rag.pipeline.document_processor.BlobStorageSettings")
    @patch("src.rag.pipeline.document_processor.AgentSettings")
    def test_init_requires_valid_settings(
        self, mock_agent_settings, mock_blob_settings
    ):
        """Test processor requires valid settings."""
        mock_blob_settings.validate = Mock()
        mock_blob_settings.AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net"
        mock_agent_settings.openai_settings = Mock()
        mock_agent_settings.OPENAI_API_KEY = "test-key"
        mock_agent_settings.OPENAI_MODEL_ID = "gpt-4"
        mock_agent_settings.OPENAI_ENDPOINT = "https://test.openai.azure.com"

        with patch("src.rag.pipeline.document_processor.DocumentConverter"):
            from src.rag.pipeline.document_processor import DocumentProcessor

            processor = DocumentProcessor()

            assert processor is not None
