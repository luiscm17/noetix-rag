from openai import AzureOpenAI
from src.config.settings import AgentSettings


class EmbeddingService:
    def __init__(self):
        self._client = AzureOpenAI(
            api_key=AgentSettings.LLM_EMBEDDING_APIKEY,
            azure_endpoint=AgentSettings.LLM_EMBEDDING_ENDPOINT,
            api_version=AgentSettings.LLM_EMBEDDING_API_VERSION,
        )
        self._model = AgentSettings.LLM_EMBEDDING_MODEL

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]
