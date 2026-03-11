import pytest
from unittest.mock import Mock, MagicMock
from src.application.use_cases.auth.register_user import (
    RegisterUserUseCase,
    RegisterUserRequest,
)
from src.application.use_cases.auth.login_user import LoginUserUseCase, LoginRequest
from src.domain.entities.user import User, UserRole


class TestRegisterUserUseCase:
    """Tests to RegisterUserUseCase."""

    def setup_method(self):
        """Setup mocks."""
        self.mock_user_repo = Mock()
        self.mock_hasher = Mock()
        self.mock_token_gen = Mock()

        self.use_case = RegisterUserUseCase(
            user_repository=self.mock_user_repo,
            password_hasher=self.mock_hasher,
            token_generator=self.mock_token_gen,
        )

    def test_register_success(self):
        """Test register successful."""
        # Arrange
        self.mock_user_repo.get_by_email.return_value = None
        self.mock_hasher.hash.return_value = "hashed_password"

        saved_user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        self.mock_user_repo.create.return_value = saved_user
        self.mock_token_gen.generate.return_value = "jwt_token"

        request = RegisterUserRequest(
            email="test@example.com", username="testuser", password="password123"
        )

        # Act
        result = self.use_case.execute(request)

        # Assert
        assert result.success is True
        assert result.user is not None
        assert result.user.username == "testuser"
        assert result.access_token == "jwt_token"
        self.mock_hasher.hash.assert_called_once_with("password123")
        self.mock_user_repo.create.assert_called_once()

    def test_register_email_already_exists(self):
        """Test register with existing email."""
        # Arrange
        existing_user = User(
            user_id=1,
            username="existing",
            email="test@example.com",
            password_hash="hash",
            role=UserRole.USER,
        )
        self.mock_user_repo.get_by_email.return_value = existing_user

        request = RegisterUserRequest(
            email="test@example.com", username="testuser", password="password123"
        )

        # Act
        result = self.use_case.execute(request)

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "already registered" in result.error
        self.mock_user_repo.create.assert_not_called()


class TestLoginUserUseCase:
    """Tests to LoginUserUseCase."""

    def setup_method(self):
        """Setup mocks."""
        self.mock_user_repo = Mock()
        self.mock_hasher = Mock()
        self.mock_token_gen = Mock()

        self.use_case = LoginUserUseCase(
            user_repository=self.mock_user_repo,
            password_hasher=self.mock_hasher,
            token_generator=self.mock_token_gen,
        )

    def test_login_success(self):
        """Test login successful."""
        # Arrange
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        self.mock_user_repo.get_by_email.return_value = user
        self.mock_hasher.verify.return_value = True
        self.mock_token_gen.generate.return_value = "jwt_token"

        request = LoginRequest(email="test@example.com", password="password123")

        # Act
        result = self.use_case.execute(request)

        # Assert
        assert result.success is True
        assert result.user is not None
        assert result.access_token == "jwt_token"
        self.mock_hasher.verify.assert_called_once_with(
            "password123", "hashed_password"
        )

    def test_login_invalid_email(self):
        """Test login with non-existent email."""
        # Arrange
        self.mock_user_repo.get_by_email.return_value = None

        request = LoginRequest(email="nonexistent@example.com", password="password123")

        # Act
        result = self.use_case.execute(request)

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "Invalid credentials" in result.error
        self.mock_token_gen.generate.assert_not_called()

    def test_login_invalid_password(self):
        """Test login with incorrect password."""
        # Arrange
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        self.mock_user_repo.get_by_email.return_value = user
        self.mock_hasher.verify.return_value = False

        request = LoginRequest(email="test@example.com", password="wrong_password")

        # Act
        result = self.use_case.execute(request)

        # Assert
        assert result.success is False
        assert result.error is not None
        assert "Invalid credentials" in result.error
        self.mock_token_gen.generate.assert_not_called()
