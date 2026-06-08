from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from database import Base, engine, get_db
from models import Candidate, JobDescription, AnalysisResult
from schemas import (
    CandidateCreate, CandidateResponse,
    JDCreate, JDResponse,
    AnalysisRequest, AnalysisResponse
)
from rag_service import add_resume_to_rag, search_similar_candidates
from ai_service import (
    get_fit_score, get_gap_analysis,
    get_interview_questions, get_cover_letter,
    get_rewritten_resume
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Recruitment Platform",
    description="RAG-powered recruitment platform using Claude API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ──────────────────────────────────────────
# CANDIDATE ROUTES
# ──────────────────────────────────────────

@app.post("/candidates", response_model=CandidateResponse, tags=["Candidates"])
def add_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    """Add a new candidate and embed their resume into ChromaDB."""
    existing = db.query(Candidate).filter(Candidate.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Candidate with this email already exists.")

    candidate = Candidate(**data.dict())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Add to RAG
    add_resume_to_rag(candidate.id, candidate.resume_text)

    return candidate

@app.get("/candidates", tags=["Candidates"])
def list_candidates(db: Session = Depends(get_db)):
    """List all candidates."""
    return db.query(Candidate).all()

@app.get("/candidates/{candidate_id}", tags=["Candidates"])
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get a specific candidate."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    return candidate

# ──────────────────────────────────────────
# JOB DESCRIPTION ROUTES
# ──────────────────────────────────────────

@app.post("/jobs", response_model=JDResponse, tags=["Jobs"])
def add_job(data: JDCreate, db: Session = Depends(get_db)):
    """Post a new job description."""
    jd = JobDescription(**data.dict())
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd

@app.get("/jobs", tags=["Jobs"])
def list_jobs(db: Session = Depends(get_db)):
    """List all job descriptions."""
    return db.query(JobDescription).all()

# ──────────────────────────────────────────
# RAG - CANDIDATE RANKING
# ──────────────────────────────────────────

@app.get("/jobs/{jd_id}/rank-candidates", tags=["RAG Ranking"])
def rank_candidates(jd_id: int, db: Session = Depends(get_db)):
    """Use RAG to rank all candidates against a job description."""
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job not found.")

    results = search_similar_candidates(jd.description)

    if not results["ids"][0]:
        return {"message": "No candidates in database yet."}

    ranked = []
    for i, candidate_id in enumerate(results["ids"][0]):
        candidate = db.query(Candidate).filter(
            Candidate.id == int(candidate_id)
        ).first()
        if candidate:
            ranked.append({
                "rank": i + 1,
                "candidate_id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "similarity_distance": results["distances"][0][i]
            })

    return {"job_title": jd.title, "ranked_candidates": ranked}

# ──────────────────────────────────────────
# AI ANALYSIS
# ──────────────────────────────────────────

@app.post("/analyze", tags=["AI Analysis"])
def analyze(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Full AI analysis pipeline:
    - Fit Score
    - Gap Analysis
    - Interview Questions
    - Cover Letter
    - Rewritten Resume
    """
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == request.jd_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    if not jd:
        raise HTTPException(status_code=404, detail="Job not found.")

    resume = candidate.resume_text
    job = jd.description

    fit_score       = get_fit_score(resume, job)
    gap_analysis    = get_gap_analysis(resume, job)
    questions       = get_interview_questions(resume, job)
    cover_letter    = get_cover_letter(resume, job)
    rewritten       = get_rewritten_resume(resume, job)

    # Save to DB
    result = AnalysisResult(
        candidate_id     = candidate.id,
        jd_id            = jd.id,
        fit_score        = fit_score,
        gap_analysis     = gap_analysis,
        interview_questions = questions,
        cover_letter     = cover_letter,
        rewritten_resume = rewritten
    )
    db.add(result)
    db.commit()

    return {
        "candidate": candidate.name,
        "job": jd.title,
        "fit_score": fit_score,
        "gap_analysis": gap_analysis,
        "interview_questions": questions,
        "cover_letter": cover_letter,
        "rewritten_resume": rewritten
    }

@app.get("/results/{candidate_id}", tags=["AI Analysis"])
def get_results(candidate_id: int, db: Session = Depends(get_db)):
    """Get all past analysis results for a candidate."""
    results = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == candidate_id
    ).all()
    return results

# ──────────────────────────────────────────
# HEALTH CHECK
# ──────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "✅ AI Recruitment Platform is running", "docs": "/docs"}
