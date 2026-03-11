from abc import ABC, abstractmethod
from src.domain.entities.user import User


class ITokenGenerator(ABC):
    """Port: define the contract for JWT token generation."""

    @abstractmethod
    def generate(self, user: User) -> str:
        """Generate a JWT token for the user."""
        ...

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Decode a JWT token and return the payload."""
        ...
