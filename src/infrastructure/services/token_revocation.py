import redis
from typing import Optional
from src.config.settings import RedisSettings


class TokenRevocationService:
    """Service to manage JWT token revocation using Redis."""

    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    @property
    def redis_client(self) -> redis.Redis:
        if self._redis is None:
            self._redis = redis.from_url(RedisSettings.REDIS_URL)
        return self._redis

    def _get_key(self, jti: str) -> str:
        return f"JWT_BLACKLIST:{jti}"

    def revoke(self, jti: str, ttl_seconds: int) -> None:
        """Revoke a token by adding it to the blacklist."""
        key = self._get_key(jti)
        self.redis_client.setex(key, ttl_seconds, "1")

    def is_revoked(self, jti: str) -> bool:
        """Check if a token has been revoked."""
        key = self._get_key(jti)
        return self.redis_client.exists(key) > 0


_token_revocation_service: Optional[TokenRevocationService] = None


def get_token_revocation_service() -> TokenRevocationService:
    global _token_revocation_service
    if _token_revocation_service is None:
        _token_revocation_service = TokenRevocationService()
    return _token_revocation_service
