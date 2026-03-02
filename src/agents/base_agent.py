from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    async def build(self, name: str, instructions: str, tools: list = None):
        pass