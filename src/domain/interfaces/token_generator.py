from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User


class ITokenGenerator(ABC):
    """Port: define the contract for JWT token generation."""

    @abstractmethod
    def generate(self, user: User) -> tuple[str, str]:
        """Generate a JWT token for the user. Returns (token, jti)."""
        ...

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Decode a JWT token and return the payload."""
        ...

    @abstractmethod
    def get_jti(self, token: str) -> Optional[str]:
        """Extract JTI from token without validation."""
        ...

    @abstractmethod
    def get_remaining_ttl(self, token: str) -> int:
        """Get remaining TTL in seconds from token exp claim."""
        ...
