"""
Configuration management for the application.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Resume Parser & ATS Scorer"
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Database
    database_url: str = Field(env="DATABASE_URL")
    database_echo: bool = False
    pool_size: int = 20
    max_overflow: int = 10

    # JWT
    secret_key: str = Field(env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # LLM Providers
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    groq_api_key: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    default_llm_provider: str = "gemini"

    # File Upload
    max_upload_size_mb: int = Field(default=10, env="MAX_UPLOAD_SIZE_MB")
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    allowed_extensions: list = [".pdf", ".docx", ".doc"]

    # ChromaDB
    chroma_persist_dir: str = Field(default="./chroma_data", env="CHROMA_PERSIST_DIR")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # CORS
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:5173", env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("allowed_origins", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def database_url_async(self) -> str:
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.database_url


settings = Settings()
