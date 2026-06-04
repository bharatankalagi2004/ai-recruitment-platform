from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    resume_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer)
    jd_id = Column(Integer)
    fit_score = Column(Float)
    gap_analysis = Column(Text)
    interview_questions = Column(Text)
    cover_letter = Column(Text)
    rewritten_resume = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
