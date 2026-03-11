import bcrypt
from typing import Optional

from src.domain.interfaces.password_hasher import IPasswordHasher


class BcryptHasher(IPasswordHasher):
    """Adapter: implement the contract of IPasswordHasher using bcrypt."""

    def hash(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, plain_password: str, hashed_password: Optional[str]) -> bool:
        """Verify that the password matches the hash."""
        if not hashed_password:
            return False
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
