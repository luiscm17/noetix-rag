import pytest
from src.domain.entities.user import User, UserRole
from src.domain.entities.document import Document, DocumentStatus
from src.domain.entities.conversation import Conversation, Message


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


class TestConversationEntity:
    """Tests for the Conversation entity."""

    def test_create_conversation(self):
        """Test create conversation."""
        conversation = Conversation(
            user_id=1,
            document_id=10,
            conversation_id="conv-123",
            title="My Research",
        )

        assert conversation.user_id == 1
        assert conversation.document_id == 10
        assert conversation.conversation_id == "conv-123"
        assert conversation.title == "My Research"
        assert conversation.created_at is None
        assert conversation.updated_at is None

    def test_conversation_default_title(self):
        """Test default title for conversation."""
        conversation = Conversation(
            user_id=1,
            document_id=10,
            conversation_id="conv-456",
        )

        assert conversation.title == "Untitled Conversation"

    def test_conversation_with_timestamps(self):
        """Test conversation with timestamps."""
        from datetime import datetime

        now = datetime.now()
        conversation = Conversation(
            user_id=1,
            document_id=10,
            conversation_id="conv-789",
            title="Test",
            created_at=now,
            updated_at=now,
        )

        assert conversation.created_at == now
        assert conversation.updated_at == now


class TestMessageEntity:
    """Tests for the Message entity."""

    def test_create_message(self):
        """Test create message."""
        message = Message(
            message_id=1,
            conversation_id="conv-123",
            role="user",
            content="Hello, how are you?",
        )

        assert message.message_id == 1
        assert message.conversation_id == "conv-123"
        assert message.role == "user"
        assert message.content == "Hello, how are you?"
        assert message.created_at is None

    def test_message_with_timestamp(self):
        """Test message with timestamp."""
        from datetime import datetime

        now = datetime.now()
        message = Message(
            message_id=1,
            conversation_id="conv-123",
            role="assistant",
            content="I'm doing well!",
            created_at=now,
        )

        assert message.created_at == now

    def test_message_roles(self):
        """Test different message roles."""
        user_msg = Message(
            message_id=1, conversation_id="c1", role="user", content="Question?"
        )
        assistant_msg = Message(
            message_id=2, conversation_id="c1", role="assistant", content="Answer."
        )
        system_msg = Message(
            message_id=3, conversation_id="c1", role="system", content="System prompt"
        )

        assert user_msg.role == "user"
        assert assistant_msg.role == "assistant"
        assert system_msg.role == "system"
