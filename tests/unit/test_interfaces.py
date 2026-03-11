import pytest
from unittest.mock import Mock
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.token_generator import ITokenGenerator
from src.domain.entities.user import User, UserRole


class TestIUserRepository:
    """Tests to IUserRepository interface."""

    def test_interface_has_required_methods(self):
        """Test that the interface has the required methods."""
        assert hasattr(IUserRepository, "create")
        assert hasattr(IUserRepository, "get_by_id")
        assert hasattr(IUserRepository, "get_by_email")

    def test_implementation_with_mock(self):
        """Test implementation with mock."""
        mock_repo = Mock(spec=IUserRepository)

        user = User(user_id=1, username="test", email="test@example.com")
        mock_repo.create.return_value = user
        mock_repo.get_by_id.return_value = user
        mock_repo.get_by_email.return_value = None

        result = mock_repo.create(user)
        assert result.username == "test"

        result = mock_repo.get_by_id(1)
        assert result is not None

        result = mock_repo.get_by_email("test@example.com")
        assert result is None


class TestIPasswordHasher:
    """Tests to IPasswordHasher interface."""

    def test_interface_has_required_methods(self):
        """Test that the interface has the required methods."""
        assert hasattr(IPasswordHasher, "hash")
        assert hasattr(IPasswordHasher, "verify")

    def test_implementation_with_mock(self):
        """Test implementation with mock."""
        mock_hasher = Mock(spec=IPasswordHasher)

        mock_hasher.hash.return_value = "hashed"
        mock_hasher.verify.return_value = True

        assert mock_hasher.hash("password") == "hashed"
        assert mock_hasher.verify("password", "hashed") is True


class TestITokenGenerator:
    """Tests to ITokenGenerator interface."""

    def test_interface_has_required_methods(self):
        """Test that the interface has the required methods."""
        assert hasattr(ITokenGenerator, "generate")
        assert hasattr(ITokenGenerator, "decode")

    def test_implementation_with_mock(self):
        """Test implementation with mock."""
        mock_gen = Mock(spec=ITokenGenerator)

        user = User(user_id=1, username="test", email="test@example.com")
        mock_gen.generate.return_value = "jwt_token"
        mock_gen.decode.return_value = {"sub": "1"}

        assert mock_gen.generate(user) == "jwt_token"
        assert mock_gen.decode("jwt_token") == {"sub": "1"}
