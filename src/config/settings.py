import os

from dotenv import load_dotenv
load_dotenv()

class AgentSettings:
    """Configuration for Agent"""
    
    # AI Foundry Settings
    AI_PROJECT_ENDPOINT = os.getenv("AI_PROJECT_ENDPOINT")
    AI_MODEL_DEPLOYMENT_NAME = os.getenv("AI_MODEL_DEPLOYMENT_NAME")

    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID")
    OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
    
    # Ollama Settings
    OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL_ID")
    OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT")
    
    @classmethod
    def ai_project_settings(cls):
        """Validate that Azure AI Foundry configurations are present"""
        if not cls.AI_PROJECT_ENDPOINT:
            raise ValueError("AI_PROJECT_ENDPOINT is not configured")
        if not cls.AI_MODEL_DEPLOYMENT_NAME:
            raise ValueError("AI_MODEL_DEPLOYMENT_NAME is not configured")
    
    @classmethod
    def openai_settings(cls):
        """Validate that OpenAI configurations are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        if not cls.OPENAI_MODEL_ID:
            raise ValueError("OPENAI_MODEL_ID is not configured")
        if not cls.OPENAI_ENDPOINT:
            raise ValueError("OPENAI_ENDPOINT is not configured")
            
    @classmethod
    def ollama_settings(cls):
        """Validate that Ollama configurations are present"""
        if not cls.OLLAMA_MODEL_ID:
            raise ValueError("OLLAMA_MODEL_ID is not configured")
        if not cls.OLLAMA_ENDPOINT:
            raise ValueError("OLLAMA_ENDPOINT is not configured")