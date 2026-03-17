import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from typing import cast
import uuid
from src.domain.entities.user import User
from src.domain.interfaces.token_generator import ITokenGenerator
from src.config.settings import AuthSettings


class JWTGenerator(ITokenGenerator):
    """Adapter: implement the contract of ITokenGenerator using JWT."""

    def generate(self, user: User) -> tuple[str, str]:
        """Generate a JWT token for the user. Returns (token, jti)."""
        secret_key = cast(str, AuthSettings.JWT_SECRET_KEY)
        jti = str(uuid.uuid4())

        payload = {
            "jti": jti,
            "sub": str(user.user_id) if user.user_id is not None else "",
            "email": user.email,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=AuthSettings.JWT_EXPIRE_DELTA),
        }
        token = jwt.encode(payload, secret_key, algorithm=AuthSettings.JWT_ALGORITHM)
        return token, jti

    def decode(self, token: str) -> dict:
        """Decode a token JWT and return the payload."""
        secret_key = cast(str, AuthSettings.JWT_SECRET_KEY)

        try:
            return jwt.decode(
                token,
                secret_key,
                algorithms=[AuthSettings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def get_jti(self, token: str) -> Optional[str]:
        """Extract JTI from token without validation."""
        try:
            payload = jwt.decode(
                token,
                cast(str, AuthSettings.JWT_SECRET_KEY),
                algorithms=[AuthSettings.JWT_ALGORITHM],
                options={"verify_signature": False},
            )
            return payload.get("jti")
        except jwt.InvalidTokenError:
            return None

    def get_remaining_ttl(self, token: str) -> int:
        """Get remaining TTL in seconds from token exp claim."""
        try:
            payload = jwt.decode(
                token,
                cast(str, AuthSettings.JWT_SECRET_KEY),
                algorithms=[AuthSettings.JWT_ALGORITHM],
                options={"verify_signature": False},
            )
            exp = payload.get("exp")
            if exp:
                remaining = exp - datetime.now(timezone.utc).timestamp()
                return int(remaining) if remaining > 0 else 0
            return 0
        except jwt.InvalidTokenError:
            return 0
