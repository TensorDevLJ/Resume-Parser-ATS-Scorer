
from typing import Optional
from enum import Enum

class LLMProvider(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"

class LLMFactory:
    @staticmethod
    def get_provider(provider: str = "gemini"):
        if provider == "gemini":
            from .gemini import GeminiProvider
            return GeminiProvider()
        elif provider == "groq":
            from .groq import GroqProvider
            return GroqProvider()
        elif provider == "ollama":
            from .ollama import OllamaProvider
            return OllamaProvider()
        else:
            raise ValueError(f"Unknown provider: {provider}")

class BaseLLMProvider:
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError
