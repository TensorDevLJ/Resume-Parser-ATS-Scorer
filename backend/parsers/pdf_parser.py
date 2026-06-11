from .base import BaseParser
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

class PDFParser(BaseParser):
    async def parse(self, file_path: str) -> str:
        try:
            pdf = fitz.open(file_path)
            text = ""
            for page in pdf:
                text += page.get_text()
            pdf.close()
            return text
        except Exception as e:
            logger.error(f"PDF parsing error: {e}")
            raise
