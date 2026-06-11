#!/usr/bin/env python3
"""Generate all backend files"""

import os
from pathlib import Path

PROJECT_ROOT = Path("/tmp/resume-parser-project/backend")

def write_file(path, content):
    file_path = PROJECT_ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

# Database models
write_file("models/user.py", '''
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")
''')

write_file("models/base.py", '''
from sqlalchemy.orm import declarative_base

Base = declarative_base()
''')

write_file("models/resume.py", '''
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String)  # pdf, docx
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="resumes")
    parsed = relationship("ParsedResume", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    versions = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")
    ats_scores = relationship("ATSScore", back_populates="resume", cascade="all, delete-orphan")

class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    version_number = Column(Integer, default=1)
    raw_text = Column(Text)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="versions")
''')

write_file("models/parsed_resume.py", '''
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class ParsedResume(Base):
    __tablename__ = "parsed_resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), unique=True, nullable=False)
    
    # Personal Info
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)
    location = Column(String)
    
    # Extracted Data (JSON)
    education = Column(JSON, default={})
    experience = Column(JSON, default={})
    skills = Column(JSON, default={})
    projects = Column(JSON, default={})
    certifications = Column(JSON, default={})
    achievements = Column(JSON, default={})
    
    # Quality Metrics
    quality_score = Column(Integer, default=0)  # 0-100
    parsed_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="parsed")
''')

write_file("models/job_description.py", '''
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_title = Column(String, nullable=False)
    company_name = Column(String)
    job_url = Column(String)
    raw_text = Column(Text)
    
    required_skills = Column(String)  # JSON stringified
    preferred_skills = Column(String)
    experience_required = Column(String)
    education_required = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    ats_scores = relationship("ATSScore", back_populates="job_description")
''')

write_file("models/ats_score.py", '''
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class ATSScore(Base):
    __tablename__ = "ats_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    
    overall_score = Column(Float, default=0.0)  # 0-100
    skill_match = Column(Float, default=0.0)
    experience_match = Column(Float, default=0.0)
    projects_match = Column(Float, default=0.0)
    education_match = Column(Float, default=0.0)
    keyword_match = Column(Float, default=0.0)
    formatting_score = Column(Float, default=0.0)
    
    matched_skills = Column(JSON, default={})
    missing_skills = Column(JSON, default={})
    extra_skills = Column(JSON, default={})
    
    recommendations = Column(JSON, default={})
    
    scored_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="ats_scores")
    job_description = relationship("JobDescription", back_populates="ats_scores")
''')

print("✅ Models created")

# Schemas
write_file("../schemas/__init__.py", '')

write_file("../schemas/user.py", '''
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
''')

print("✅ Schemas created")
