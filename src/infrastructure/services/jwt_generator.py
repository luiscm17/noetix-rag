import jwt
from datetime import datetime, timedelta, timezone
from src.domain.entities.user import User
from src.domain.interfaces.token_generator import ITokenGenerator
from src.config.settings import AuthSettings


class JWTGenerator(ITokenGenerator):
    """Adapter: implement the contract of ITokenGenerator using JWT."""

    def generate(self, user: User) -> str:
        """Generate a JWT token for the user."""
        payload = {
            "sub": str(user.user_id) if user.user_id is not None else "",
            "email": user.email,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=AuthSettings.JWT_EXPIRE_DELTA),
        }
        return jwt.encode(
            payload, AuthSettings.JWT_SECRET_KEY, algorithm=AuthSettings.JWT_ALGORITHM
        )

    def decode(self, token: str) -> dict:
        """Decode a token JWT and return the payload."""
        try:
            return jwt.decode(
                token,
                AuthSettings.JWT_SECRET_KEY,
                algorithms=[AuthSettings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
