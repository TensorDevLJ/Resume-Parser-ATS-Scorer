
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
