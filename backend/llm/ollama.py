
import requests
from core.config import settings
from .factory import BaseLLMProvider
import logging

logger = logging.getLogger(__name__)

class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = "llama2"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt}
            )
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            raise
