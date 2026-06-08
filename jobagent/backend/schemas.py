from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CandidateCreate(BaseModel):
    name: str
    email: str
    resume_text: str

class CandidateResponse(CandidateCreate):
    id: int
    uploaded_at: datetime
    class Config:
        from_attributes = True

class JDCreate(BaseModel):
    title: str
    company: str
    description: str

class JDResponse(JDCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    candidate_id: int
    jd_id: int

class AnalysisResponse(BaseModel):
    candidate_id: int
    jd_id: int
    fit_score: float
    gap_analysis: str
    interview_questions: str
    cover_letter: str
    rewritten_resume: str
    class Config:
        from_attributes = True
