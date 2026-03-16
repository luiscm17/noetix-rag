from typing import Any

from agent_framework import InMemoryHistoryProvider
from agent_framework.redis import RedisHistoryProvider


class SessionManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._history_provider = RedisHistoryProvider(
            redis_url=redis_url,
            load_messages=True,
        )

    @property
    def history_provider(self) -> RedisHistoryProvider:
        return self._history_provider


_session_manager: SessionManager | None = None


def get_session_manager() -> SessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
