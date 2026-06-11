from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        logger.info(f"Embedder initialized with {model_name}")
    
    def embed(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.model.encode(text)
    
    def embed_batch(self, texts: list) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts)
