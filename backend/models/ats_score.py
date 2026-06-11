
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
