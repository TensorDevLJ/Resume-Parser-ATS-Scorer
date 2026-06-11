from .base import BaseParser
from docx import Document
import logging

logger = logging.getLogger(__name__)

class DocxParser(BaseParser):
    async def parse(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"DOCX parsing error: {e}")
            raise
