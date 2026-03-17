import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.document_repository_blob import (
    DocumentRepositoryBlob,
)
from src.domain.entities.user import User, UserRole
from src.domain.entities.document import Document


class TestUserRepository:
    """Tests for UserRepository."""

    def setup_method(self):
        """Setup mock session."""
        self.mock_db = Mock()
        self.repository = UserRepository(self.mock_db)

    def _create_mock_user_model(
        self, user_id=1, email="test@example.com", username="testuser"
    ):
        """Helper to create a properly mocked user model."""
        mock_model = Mock()
        mock_model.user_id = user_id
        mock_model.email = email
        mock_model.username = username
        mock_model.password_hash = "hashed_password"
        mock_model.role = "user"
        mock_model.is_active = True
        mock_model.registration_date = datetime.now()
        return mock_model

    def test_create_user(self):
        """Test creating a user adds and commits."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )

        self.mock_db.add = Mock()
        self.mock_db.commit = Mock()

        with patch(
            "src.infrastructure.repositories.user_repository.UserModel"
        ) as MockUserModel:
            mock_instance = Mock()
            mock_instance.user_id = 1
            mock_instance.email = "test@example.com"
            mock_instance.username = "testuser"
            mock_instance.password_hash = "hashed_password"
            mock_instance.role = "user"
            mock_instance.is_active = True
            mock_instance.registration_date = datetime.now()
            MockUserModel.return_value = mock_instance

            self.repository.create(user)

        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()

    def test_get_by_email_found(self):
        """Test get user by email when found."""
        mock_model = self._create_mock_user_model()

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_model
        self.mock_db.query.return_value = mock_query

        result = self.repository.get_by_email("test@example.com")

        assert result is not None
        assert result.email == "test@example.com"

    def test_get_by_email_not_found(self):
        """Test get user by email when not found."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query

        result = self.repository.get_by_email("nonexistent@example.com")

        assert result is None

    def test_get_by_id_found(self):
        """Test get user by ID when found."""
        mock_model = self._create_mock_user_model()

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_model
        self.mock_db.query.return_value = mock_query

        result = self.repository.get_by_id(1)

        assert result is not None
        assert result.user_id == 1

    def test_get_by_id_not_found(self):
        """Test get user by ID when not found."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query

        result = self.repository.get_by_id(999)

        assert result is None


class TestDocumentRepositoryBlob:
    """Tests for DocumentRepositoryBlob."""

    @patch("src.infrastructure.repositories.document_repository_blob.BlobServiceClient")
    @patch(
        "src.infrastructure.repositories.document_repository_blob.BlobStorageSettings"
    )
    def test_init_success(self, mock_settings, mock_blob_service):
        """Test initialization with valid settings."""
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net"
        mock_settings.AZURE_STORAGE_CONTAINER = "test-container"

        mock_container = Mock()
        mock_blob_service.from_connection_string.return_value.get_container_client.return_value = mock_container

        repo = DocumentRepositoryBlob(
            connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net",
            container_name="test-container",
        )

        assert repo is not None

    @patch("src.infrastructure.repositories.document_repository_blob.BlobServiceClient")
    @patch(
        "src.infrastructure.repositories.document_repository_blob.BlobStorageSettings"
    )
    def test_init_missing_connection_string(self, mock_settings, mock_blob_service):
        """Test initialization fails without connection string."""
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = None
        mock_settings.AZURE_STORAGE_CONTAINER = "test-container"

        with pytest.raises(ValueError, match="not configured"):
            DocumentRepositoryBlob(
                connection_string=None, container_name="test-container"
            )

    @patch("src.infrastructure.repositories.document_repository_blob.BlobServiceClient")
    @patch(
        "src.infrastructure.repositories.document_repository_blob.BlobStorageSettings"
    )
    def test_init_missing_container(self, mock_settings, mock_blob_service):
        """Test initialization fails without container name."""
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net"
        mock_settings.AZURE_STORAGE_CONTAINER = None

        with pytest.raises(ValueError, match="not configured"):
            DocumentRepositoryBlob(
                connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net",
                container_name=None,
            )

    @patch("src.infrastructure.repositories.document_repository_blob.BlobServiceClient")
    @patch(
        "src.infrastructure.repositories.document_repository_blob.BlobStorageSettings"
    )
    def test_get_blob_name(self, mock_settings, mock_blob_service):
        """Test blob name generation."""
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net"
        mock_settings.AZURE_STORAGE_CONTAINER = "test-container"

        mock_container = Mock()
        mock_blob_service.from_connection_string.return_value.get_container_client.return_value = mock_container

        repo = DocumentRepositoryBlob(
            connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net",
            container_name="test-container",
        )

        doc = Document(
            document_id=1, user_id=5, title="test.pdf", file_path="/test.pdf"
        )
        blob_name = repo._get_blob_name(doc)

        assert blob_name == "5_1_test.pdf"

    @patch("src.infrastructure.repositories.document_repository_blob.BlobServiceClient")
    @patch(
        "src.infrastructure.repositories.document_repository_blob.BlobStorageSettings"
    )
    def test_get_blob_name_without_user_id(self, mock_settings, mock_blob_service):
        """Test blob name generation without user_id."""
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net"
        mock_settings.AZURE_STORAGE_CONTAINER = "test-container"

        mock_container = Mock()
        mock_blob_service.from_connection_string.return_value.get_container_client.return_value = mock_container

        repo = DocumentRepositoryBlob(
            connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key==;EndpointSuffix=core.windows.net",
            container_name="test-container",
        )

        doc = Document(
            document_id=1, user_id=None, title="test.pdf", file_path="/test.pdf"
        )
        blob_name = repo._get_blob_name(doc)

        assert blob_name == "0_1_test.pdf"
