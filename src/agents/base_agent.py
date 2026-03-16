from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


T = TypeVar("T")


class BaseAgent(ABC, Generic[T]):
    @abstractmethod
    async def build(
        self, name: str, instructions: str, tools: list[Any] | None = None
    ) -> T:
        pass
