#!/usr/bin/env python3
"""
Project structure generator for Resume Parser & ATS Scorer
Generates all necessary backend and frontend files
"""

import os
import json
from pathlib import Path

PROJECT_ROOT = Path("/tmp/resume-parser-project")

# Create all directories
DIRS = [
    "backend/core",
    "backend/database",
    "backend/models",
    "backend/schemas",
    "backend/repositories",
    "backend/services",
    "backend/parsers",
    "backend/extractors",
    "backend/nlp",
    "backend/embeddings",
    "backend/vector_db",
    "backend/rag",
    "backend/llm",
    "backend/prompts",
    "backend/api/v1/endpoints",
    "backend/api/dependencies",
    "backend/tasks",
    "backend/analytics",
    "backend/cache",
    "backend/middleware",
    "backend/tests/unit",
    "backend/tests/integration",
    "frontend/public",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/hooks",
    "frontend/src/types",
    "frontend/src/utils",
    "frontend/src/store",
    ".github/workflows",
]

for dir_path in DIRS:
    (PROJECT_ROOT / dir_path).mkdir(parents=True, exist_ok=True)

print("✅ Directories created")

# Helper function to create files
def create_file(path, content):
    file_path = PROJECT_ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return file_path

# Backend Files
FILES = {
    # Core
    "backend/__init__.py": "",
    "backend/core/__init__.py": "",
    "backend/core/logging.py": '''
import logging
import sys
from pythonjsonlogger import jsonlogger

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # JSON formatter
    formatter = jsonlogger.JsonFormatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
''',
    "backend/core/security.py": '''
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    sub: str
    exp: datetime
    iat: datetime

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
''',
    "backend/core/exceptions.py": '''
from fastapi import HTTPException, status

class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

class ResumeParsError(HTTPException):
    def __init__(self, detail: str = "Error parsing resume"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class FileUploadError(HTTPException):
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
''',
}

for file_path, content in FILES.items():
    create_file(file_path, content)

print("✅ Core files created")

