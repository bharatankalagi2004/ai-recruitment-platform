# 🎯 AI Recruitment Platform

An end-to-end AI-powered recruitment platform built with **FastAPI**, **RAG (ChromaDB)**, and **Claude API** — automating candidate screening, ranking, and analysis.

---

## 🚀 Features

- 📥 **Resume Ingestion** — Upload and embed resumes into a vector database
- 🏆 **RAG-Based Ranking** — Rank candidates against job descriptions using semantic search
- 🤖 **Full AI Pipeline** — Fit score, gap analysis, interview questions, cover letter, resume rewrite
- 💾 **PostgreSQL / SQLite** — Persistent storage for candidates, jobs, and results
- 🐳 **Docker Ready** — Fully containerized with docker-compose
- 📄 **Swagger Docs** — Auto-generated API documentation at `/docs`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| AI/LLM | Claude API (Anthropic) |
| Vector DB / RAG | ChromaDB |
| Database | SQLite / PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Frontend | Streamlit |
| Containerization | Docker + docker-compose |

---

## 📁 Project Structure

```
jobagent/
├── backend/
│   ├── main.py           # All FastAPI routes
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # DB connection
│   ├── ai_service.py     # Claude API calls
│   └── rag_service.py    # ChromaDB RAG logic
├── frontend/
│   └── app.py            # Streamlit UI
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
└── .gitignore
```

---

## ⚙️ Local Setup (Without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-recruitment-platform.git
cd ai-recruitment-platform
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment
```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY in .env
```

### 5. Run Backend
```bash
cd backend
uvicorn main:app --reload
```

### 6. Run Frontend (new terminal)
```bash
cd frontend
streamlit run app.py
```

---

## 🐳 Docker Setup

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY in .env

docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`
- API Docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Candidates
| Method | Endpoint | Description |
|---|---|---|
| POST | `/candidates` | Add candidate + embed resume |
| GET | `/candidates` | List all candidates |
| GET | `/candidates/{id}` | Get specific candidate |

### Jobs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs` | Post a job description |
| GET | `/jobs` | List all jobs |

### RAG Ranking
| Method | Endpoint | Description |
|---|---|---|
| GET | `/jobs/{jd_id}/rank-candidates` | Rank candidates by semantic similarity |

### AI Analysis
| Method | Endpoint | Description |
|---|---|---|
| POST | `/analyze` | Full AI pipeline for a candidate + job |
| GET | `/results/{candidate_id}` | Get past analysis results |

---

## 🤖 AI Pipeline Flow

```
Resume Upload → ChromaDB Embedding
        ↓
JD Posted → RAG Semantic Search → Ranked Candidates
        ↓
Selected Candidate + JD → Claude API
        ↓
Fit Score + Gap Analysis + Interview Questions + Cover Letter + Resume Rewrite
        ↓
Results saved to Database
```

---

## 🔮 Future Improvements

- [ ] Migrate to PostgreSQL on AWS RDS
- [ ] Deploy backend on AWS EC2
- [ ] Store resumes on AWS S3
- [ ] Add HR login with role-based access
- [ ] Email notifications to shortlisted candidates
- [ ] LangChain multi-step agent pipeline

---

## 👨‍💻 Author

**Bharat Kumar S Ankalagi**
- GitHub: [@bharatankalagi2004](https://github.com/bharatankalagi2004)
- LinkedIn: [bharat-ankalagi](https://linkedin.com/in/bharat-ankalagi-123008333)
- Email: bharatankalagi2004@gmail.com
