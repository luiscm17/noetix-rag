import pytest
from src.domain.entities.user import User, UserRole
from src.domain.entities.document import Document, DocumentStatus


class TestUserEntity:
    """Tests to useer entity."""

    def test_create_user(self):
        """Test create user."""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )

        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.role == UserRole.USER
        assert user.is_active is True

    def test_is_admin(self):
        """Test verification of admin role."""
        regular_user = User(username="user", email="user@test.com", role=UserRole.USER)
        admin_user = User(username="admin", email="admin@test.com", role=UserRole.ADMIN)

        assert regular_user.is_admin() is False
        assert admin_user.is_admin() is True

    def test_set_password(self):
        """Test setting the password."""
        user = User(username="test", email="test@test.com")
        user.set_password("test_password")

        assert user.password_hash is not None
        assert user.password_hash != "test_password"

    def test_check_password(self):
        """Test verification of password."""
        user = User(username="test", email="test@test.com")
        user.set_password("test_password")

        assert user.check_password("test_password") is True
        assert user.check_password("wrong_password") is False

    def test_default_values(self):
        """Test default values."""
        user = User(username="test", email="test@example.com")

        assert user.user_id is None
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert user.password_hash is None


class TestDocumentEntity:
    """Tests to the Document entity."""

    def test_create_document(self):
        """Test create document."""
        doc = Document(
            document_id=1,
            title="Test Document",
            file_path="/path/to/file.pdf",
            page_count=10,
        )

        assert doc.document_id == 1
        assert doc.title == "Test Document"
        assert doc.file_path == "/path/to/file.pdf"
        assert doc.page_count == 10
        assert doc.status == DocumentStatus.PENDING

    def test_document_status_enum(self):
        """Test document statuses."""
        assert DocumentStatus.PENDING.value == "pending"
        assert DocumentStatus.PROCESSING.value == "processing"
        assert DocumentStatus.PROCESSED.value == "processed"
        assert DocumentStatus.ERROR.value == "error"

    def test_validate_title(self):
        """Test validation of title."""
        with pytest.raises(ValueError):
            Document(title="", file_path="/test.pdf", page_count=1)

    def test_default_values(self):
        """Test default values."""
        doc = Document(title="Test", file_path="/test.pdf", page_count=0)

        assert doc.document_id is None
        assert doc.page_count == 0
        assert doc.status == DocumentStatus.PENDING
        assert doc.tags is None
