from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from src.main import app
from src.config.dependencies import (
    get_user_repository,
    get_password_hasher,
    get_token_generator,
)
from src.api.dependencies import get_current_user
from src.domain.entities.user import User, UserRole
from src.api.routes.documents import get_repo


class TestHealthEndpoint:
    """Tests to health check endpoint."""

    def setup_method(self):
        """Setup."""
        self.client = TestClient(app)

    def test_health_check(self):
        """Test health check retorna status healthy."""
        response = self.client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self):
        """Test endpoint root."""
        response = self.client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data


class TestAuthEndpoints:
    """Tests to authentication endpoints."""

    def setup_method(self):
        """Setup."""
        self.client = TestClient(app)
        self.mock_user_repo = Mock()
        self.mock_hasher = Mock()
        self.mock_token = Mock()

    def teardown_method(self):
        """Cleanup."""
        app.dependency_overrides.clear()

    def test_register_success(self):
        """Test register successful."""
        self.mock_user_repo.get_by_email.return_value = None

        user = Mock()
        user.user_id = 1
        user.username = "testuser"
        user.email = "newuser@example.com"
        user.role = "user"

        self.mock_user_repo.create.return_value = user

        self.mock_hasher.hash.return_value = "hashed"
        self.mock_token.generate.return_value = ("jwt_token", "jti-123")

        app.dependency_overrides[get_user_repository] = lambda: self.mock_user_repo
        app.dependency_overrides[get_password_hasher] = lambda: self.mock_hasher
        app.dependency_overrides[get_token_generator] = lambda: self.mock_token

        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "testuser",
                "password": "password123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data

    def test_register_duplicate_email(self):
        """Test register with existing email."""
        existing_user = Mock()
        existing_user.user_id = 1
        existing_user.username = "existing"
        existing_user.email = "test@example.com"

        self.mock_user_repo.get_by_email.return_value = existing_user

        app.dependency_overrides[get_user_repository] = lambda: self.mock_user_repo
        app.dependency_overrides[get_password_hasher] = lambda: self.mock_hasher
        app.dependency_overrides[get_token_generator] = lambda: self.mock_token

        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
            },
        )

        assert response.status_code == 400

    def test_register_invalid_email(self):
        """Test register with invalid email."""
        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "username": "testuser",
                "password": "password123",
            },
        )

        assert response.status_code == 422

    def test_register_missing_fields(self):
        """Test register with missing fields."""
        response = self.client.post(
            "/api/auth/register", json={"email": "test@example.com"}
        )

        assert response.status_code == 422


class TestDocumentsEndpoints:
    """Tests to documents endpoints."""

    def setup_method(self):
        """Setup."""
        self.client = TestClient(app)
        self.mock_user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role=UserRole.USER,
        )
        self.mock_repo = Mock()
        self.mock_repo.list_documents.return_value = []
        self.mock_repo.get_document = AsyncMock(return_value=None)

    def teardown_method(self):
        """Cleanup."""
        app.dependency_overrides.clear()

    def test_list_documents_empty(self):
        """Test list documents when there are none."""
        app.dependency_overrides[get_current_user] = lambda: self.mock_user
        app.dependency_overrides[get_repo] = lambda: self.mock_repo

        response = self.client.get("/api/documents/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "documents" in data
        assert isinstance(data["documents"], list)

    def test_get_document_not_found(self):
        """Test get document when it does not exist."""
        app.dependency_overrides[get_current_user] = lambda: self.mock_user
        app.dependency_overrides[get_repo] = lambda: self.mock_repo

        response = self.client.get("/api/documents/99999")

        assert response.status_code == 404
