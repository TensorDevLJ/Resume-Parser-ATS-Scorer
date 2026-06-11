#!/usr/bin/env python3
"""Generate complete backend infrastructure"""

from pathlib import Path

PROJECT_ROOT = Path("/tmp/resume-parser-project")

def write(path, content):
    p = PROJECT_ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w') as f:
        f.write(content)

# Database connection
write("backend/database/__init__.py", '''
from .connection import get_db, engine, AsyncSessionLocal, init_db
__all__ = ["get_db", "engine", "AsyncSessionLocal", "init_db"]
''')

write("backend/database/connection.py", '''
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.base import Base
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.database_url_async,
    echo=settings.database_echo,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
''')

# LLM Providers
write("backend/llm/__init__.py", '''
from .factory import LLMFactory
__all__ = ["LLMFactory"]
''')

write("backend/llm/factory.py", '''
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
''')

write("backend/llm/gemini.py", '''
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
''')

write("backend/llm/groq.py", '''
from groq import Groq
from core.config import settings
from .factory import BaseLLMProvider
import logging

logger = logging.getLogger(__name__)

class GroqProvider(BaseLLMProvider):
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "llama-3.3-70b-versatile"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
            raise
''')

write("backend/llm/ollama.py", '''
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
''')

# Services
write("backend/services/__init__.py", '')

write("backend/services/user_service.py", '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        hashed_password = hash_password(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User created: {user.email}")
        return db_user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
''')

# Repositories  
write("backend/repositories/__init__.py", '')

write("backend/repositories/base.py", '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import TypeVar, Generic, Type, List

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model
    
    async def get(self, id: int) -> T | None:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()
    
    async def get_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()
    
    async def create(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def delete(self, id: int) -> bool:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False
''')

# API endpoints
write("backend/api/v1/__init__.py", '')

write("backend/api/v1/endpoints/__init__.py", '')

write("backend/api/v1/endpoints/auth.py", '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
from services.user_service import UserService
from core.security import create_access_token
from database import get_db
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await UserService.get_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = await UserService.create_user(db, user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await UserService.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
''')

# Main app
write("backend/main.py", '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from core.logging import get_logger
from database import init_db
from api.v1.endpoints import auth

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(
    title=settings.app_name,
    description="Production-grade Resume Parser & ATS Scorer",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}

@app.get("/")
async def root():
    return {"message": "Resume Parser & ATS Scorer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
''')

print("✅ Complete backend created")
