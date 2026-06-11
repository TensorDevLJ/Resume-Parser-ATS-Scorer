
import google.generativeai as genai
from core.config import settings
from .factory import BaseLLMProvider
import logging

logger = logging.getLogger(__name__)

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
