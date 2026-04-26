# 🧠 AI Resume Skill Assessment Agent

> **Hackathon Project** — Built by [Shivam Yadav](https://github.com/shivamyadav039)

---

## 🚀 Problem

Resumes **claim** skills but don't prove real proficiency.  
Recruiters waste hours interviewing candidates who can't actually do the work.

---

## 💡 Solution

An AI agent that bridges the gap — automatically:

- 📄 **Analyzes** the Job Description + Candidate Resume
- 🤖 **Conducts** a conversational skill assessment (like a real interview)
- 📊 **Identifies** skill gaps ranked by severity
- 🗺️ **Generates** a personalized, time-bound learning roadmap

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **AI / LLM** | Google Gemini API (`gemini-1.5-flash`) |
| **Backend** | Python + FastAPI |
| **Frontend** | React + Vite (Tailwind CSS) |
| **NLP** | spaCy + sentence-transformers |
| **Session Store** | In-memory (PostgreSQL-ready) |
| **API Docs** | Swagger UI (auto-generated) |

---

## 🔥 Features

| Feature | Description |
|---------|-------------|
| ✅ Skill Extraction | Parses JD + Resume using NLP to find skill gaps |
| ✅ AI Questioning | Multi-turn adaptive interview (Conceptual → Practical → Advanced) |
| ✅ Proficiency Scoring | 1–5 level scoring with confidence % and evidence tags |
| ✅ Gap Analysis | Severity ranking (Critical / High / Medium / Low) |
| ✅ Learning Plan | Personalized roadmap with resources + time estimates |
| ✅ REST API | Full OpenAPI spec, testable via Swagger UI |
| ✅ Frontend UI | React chat interface, proxied to backend |

---

## 🧠 How It Works

```
1. You paste a Job Description + Resume
         ↓
2. AI extracts required skills from JD
   and maps them against your resume
         ↓
3. For each skill gap, the AI asks 3 questions:
   • Turn 1 → Conceptual  ("What is X?")
   • Turn 2 → Practical   ("Describe a project using X")
   • Turn 3 → Advanced    ("How would you optimise X at scale?")
         ↓
4. Each answer is scored on 4 dimensions:
   Relevance (30%) + Depth (35%) + Clarity (20%) + Confidence (15%)
         ↓
5. A personalised learning roadmap is generated
   with curated resources, milestones & time estimates
```

---

## 🏗️ Project Structure

```
hackathon_deccan/
├── backend/                    ← FastAPI Python backend
│   ├── app/
│   │   ├── main.py             ← All API endpoints
│   │   ├── config.py           ← Settings (reads .env)
│   │   ├── agents/             ← AI agent implementations
│   │   │   ├── assessment_agent.py
│   │   │   ├── scoring_agent.py
│   │   │   ├── gap_analysis_agent.py
│   │   │   └── planning_agent.py
│   │   └── services/
│   │       ├── llm_service.py  ← Gemini API wrapper
│   │       └── skill_extractor.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   ← React + Vite UI
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   ├── vite.config.js          ← Proxies /api → backend:8000
│   └── package.json
│
└── README.md                   ← You are here
```

---

## 📸 Demo

### Frontend — AI Skill Assessment Platform
> Running at `http://localhost:5173`

```
┌─────────────────────────────────────────────┐
│  🧠 AI Skill Assessment        ✓ Operational │
│─────────────────────────────────────────────│
│  Intelligent Skill Assessment Platform       │
│                                              │
│  [ Paste Job Description ]                   │
│  [ Paste Resume           ]                  │
│  [ Start Assessment  →    ]                  │
└─────────────────────────────────────────────┘
```

### Backend — Swagger API Docs
> Running at `http://localhost:8000/docs`

```
POST /api/v1/upload   ← Upload JD + Resume
POST /api/v1/chat     ← AI assessment conversation
POST /api/v1/score    ← Score a skill
POST /api/v1/plan     ← Generate learning roadmap
GET  /api/v1/gaps     ← View skill gap analysis
GET  /health          ← Health check
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Gemini API Key](https://aistudio.google.com/app/apikey) (free)

---

### 1. Clone the repo
```bash
git clone https://github.com/shivamyadav039/AI-Skill-Assessment.git
cd AI-Skill-Assessment
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# → Open .env and add your GEMINI_API_KEY

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend live at: **http://localhost:8000**  
API Docs at: **http://localhost:8000/docs**

---

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start frontend dev server
npm run dev
```

Frontend live at: **http://localhost:5173**

> ✅ Vite automatically proxies `/api/*` calls to the backend — no CORS issues.

---

## 🔑 API Key Setup

1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Create a free API key
3. Open `backend/.env` and set:

```env
GEMINI_API_KEY=AIza-your-key-here
MODEL_NAME=gemini-1.5-flash
```

---

## 🔌 API Quick Reference

### Upload Documents
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Shivam Yadav",
    "jd_content": "We need a Python developer with FastAPI and PostgreSQL.",
    "resume_content": "3 years Python, FastAPI experience."
  }'
```

**Response:**
```json
{
  "session_id": "session_72558d311b71",
  "jd_skills": ["FastAPI", "PostgreSQL", "Python"],
  "resume_skills": ["FastAPI", "Python"],
  "total_skills_to_assess": 3
}
```

### Chat Assessment
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_72558d311b71",
    "skill": "Python",
    "user_message": "I have 3 years of Python experience in production.",
    "turn_count": 1
  }'
```

**Response:**
```json
{
  "skill": "Python",
  "assistant_message": "Can you describe a specific project and how you handled performance?",
  "turn_count": 2,
  "assessment_complete": false
}
```

---

## 📊 Scoring Logic

Each answer is scored on **4 dimensions**:

| Dimension | Weight | How |
|-----------|--------|-----|
| **Relevance** | 30% | Semantic similarity to question (sentence-transformers) |
| **Depth** | 35% | Evidence tags: project, metrics, experience, technical |
| **Clarity** | 20% | Structure, coherence, logical flow |
| **Confidence** | 15% | Certainty language ("I built" vs "maybe") |

**Proficiency Levels:**
```
0.0 – 0.2  →  Level 1 🔴 Beginner
0.2 – 0.4  →  Level 2 🟠 Basic
0.4 – 0.6  →  Level 3 🟡 Intermediate
0.6 – 0.8  →  Level 4 🟢 Advanced
0.8 – 1.0  →  Level 5 🟢✨ Expert
```

---

## 🔍 Verify Backend + Frontend Are Connected

```bash
# 1. Backend health check
curl http://localhost:8000/health

# 2. Test via frontend proxy (confirms connection)
curl -X POST http://localhost:5173/api/v1/upload \
  -H "Content-Type: application/json" \
  -d '{"candidate_name":"Test","jd_content":"Python FastAPI","resume_content":"Python 3 years"}'
```

Both should return JSON ✅

---

## 📌 Future Improvements

- 🎙️ **Voice-based interview** — speak your answers instead of typing
- 📊 **Real-time scoring dashboard** — live confidence graphs during interview
- 🔗 **LinkedIn / GitHub integration** — auto-fetch resume from profile
- 🗄️ **PostgreSQL persistence** — store sessions, history, and reports
- 📧 **Email report** — send the learning plan as a PDF

---

## 👨‍💻 Author

**Shivam Yadav**  
GitHub: [@shivamyadav039](https://github.com/shivamyadav039)

---

## 📄 License

MIT License — feel free to use, fork and build on this!
