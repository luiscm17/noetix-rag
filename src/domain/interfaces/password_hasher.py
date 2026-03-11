from abc import ABC, abstractmethod
from typing import Optional


class IPasswordHasher(ABC):
    """Port: define the contract for password hashing."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a password."""
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: Optional[str]) -> bool:
        """Verify that the password matches the hash."""
        ...
