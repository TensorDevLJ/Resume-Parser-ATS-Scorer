
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
