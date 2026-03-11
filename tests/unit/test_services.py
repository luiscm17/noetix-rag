import pytest
from src.infrastructure.services.bcrypt_hasher import BcryptHasher
from src.infrastructure.services.jwt_generator import JWTGenerator
from src.domain.entities.user import User, UserRole


class TestBcryptHasher:
    """Tests to BcryptHasher."""

    def setup_method(self):
        """Setup."""
        self.hasher = BcryptHasher()

    def test_hash_password(self):
        """Test hashing of password."""
        password = "test_password_123"
        hashed = self.hasher.hash(password)

        assert hashed is not None
        assert hashed != password
        assert hashed.startswith("$2")  # bcrypt prefix

    def test_verify_correct_password(self):
        """Test verification with correct password."""
        password = "test_password_123"
        hashed = self.hasher.hash(password)

        assert self.hasher.verify(password, hashed) is True

    def test_verify_wrong_password(self):
        """Test verification with incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = self.hasher.hash(password)

        assert self.hasher.verify(wrong_password, hashed) is False

    def test_verify_empty_hash(self):
        """Test verification with empty hash."""
        assert self.hasher.verify("password", "") is False
        assert self.hasher.verify("password", None) is False


class TestJWTGenerator:
    """Tests to JWTGenerator."""

    def setup_method(self):
        """Setup."""
        self.token_gen = JWTGenerator()

    def test_generate_token(self):
        """Test generation of token."""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            role=UserRole.USER,
        )

        token = self.token_gen.generate(user)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token(self):
        """Test decoding of token."""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            role=UserRole.USER,
        )

        token = self.token_gen.generate(user)
        payload = self.token_gen.decode(token)

        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "user"

    def test_decode_invalid_token(self):
        """Test decoding of invalid token."""
        with pytest.raises(ValueError, match="Invalid token"):
            self.token_gen.decode("invalid_token")
