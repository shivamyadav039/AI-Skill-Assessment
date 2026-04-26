# AI-Powered Skill Assessment & Personalised Learning Plan Agent

> Hackathon Project: Conversational skill assessment with personalized learning plan generation using AI agents.

---

## 📁 Project Structure

```
hackathon_deccan/
├── backend/                          # FastAPI + Python backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # Main FastAPI application & core endpoints
│   │   ├── config.py                # Configuration and settings management
│   │   │
│   │   ├── agents/                  # AI agent implementations
│   │   │   ├── __init__.py
│   │   │   ├── assessment_agent.py  # Adaptive multi-turn conversation logic
│   │   │   ├── scoring_agent.py     # Proficiency scoring with CoT reasoning
│   │   │   ├── planning_agent.py    # Learning plan generation
│   │   │   └── gap_analysis_agent.py# Gap analysis and priority ranking
│   │   │
│   │   ├── services/                # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── skill_extractor.py   # NLP skill extraction from documents
│   │   │   ├── skill_matcher.py     # Semantic skill alignment & taxonomy
│   │   │   ├── rag_service.py       # RAG for resource curation
│   │   │   ├── llm_service.py       # LLM integration (Claude/GPT)
│   │   │   └── session_manager.py   # Session state management
│   │   │
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── session.py           # Session state model
│   │   │   ├── skill.py             # Skill model with embeddings
│   │   │   ├── assessment.py        # Assessment & conversation history
│   │   │   └── learning_plan.py     # Learning plan & milestones
│   │   │
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   │   └── __init__.py          # Data contracts for all API endpoints
│   │   │
│   │   ├── db/                      # Database utilities
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # Database connection & session management
│   │   │   ├── migrations/          # Alembic migrations
│   │   │   └── seed_data.py         # Seed skill taxonomy & resources
│   │   │
│   │   └── utils/                   # Utility functions
│   │       ├── __init__.py
│   │       ├── text_processing.py   # Text cleaning, tokenization
│   │       ├── skill_graph.py       # Adjacent skill traversal
│   │       └── constants.py         # Application constants
│   │
│   ├── tests/                        # Unit and integration tests
│   │   ├── __init__.py
│   │   ├── test_endpoints.py        # API endpoint tests
│   │   ├── test_services.py         # Service logic tests
│   │   └── test_agents.py           # Agent logic tests
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   ├── .env                          # Local environment (git-ignored)
│   ├── .gitignore
│   ├── Dockerfile                    # Docker container setup
│   ├── docker-compose.yml            # PostgreSQL + Backend setup
│   └── README.md                     # Backend-specific documentation
│
├── frontend/                         # React + Chat UI
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── DocumentUpload/       # JD/Resume upload interface
│   │   │   ├── ChatAssessment/       # Conversational assessment chat
│   │   │   ├── SkillScores/          # Score visualization dashboard
│   │   │   ├── GapAnalysis/          # Gap analysis visualization
│   │   │   └── LearningPlanView/     # Learning plan roadmap display
│   │   │
│   │   ├── services/                 # API client services
│   │   │   └── api.js                # Backend API integration
│   │   │
│   │   ├── App.jsx                   # Main app component
│   │   └── App.css
│   │
│   ├── package.json
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── docs/                             # Project documentation
│   ├── architecture.md               # System architecture & design decisions
│   ├── api_specification.md          # Detailed API endpoint specs
│   ├── data_models.md                # Data model documentation
│   ├── skill_taxonomy.md             # Skill classification scheme
│   └── deployment.md                 # Deployment & production setup
│
├── .gitignore
├── docker-compose.yml                # Full stack orchestration
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### Backend Setup

#### 1. Create Python Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and database URL
```

#### 4. Initialize Database
```bash
# Apply migrations
alembic upgrade head

# Seed skill taxonomy and resources
python -m app.db.seed_data
```

#### 5. Run Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### 1. **POST /api/v1/upload** - Upload Documents
Upload Job Description and Resume to initiate assessment.

**Request:**
```json
{
  "jd_content": "We are looking for a Senior Python Engineer...",
  "resume_content": "John Doe, 5 years experience in Python...",
  "candidate_name": "John Doe"
}
```

**Response:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "jd_skills": ["Python", "System Design", "PostgreSQL", "AWS"],
  "resume_skills": ["Python", "AWS", "JavaScript"],
  "total_skills_to_assess": 4,
  "timestamp": "2024-04-25T10:30:00Z"
}
```

---

### 2. **POST /api/v1/chat** - Conversational Assessment
Run adaptive multi-turn conversation for skill assessment.

**Request:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "skill": "Python",
  "user_message": "I have used Python for 3 years in production...",
  "turn_count": 1
}
```

**Response:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "skill": "Python",
  "assistant_message": "Great! Can you describe a real-world scenario where you used Python?",
  "turn_count": 2,
  "conversation_history": [...],
  "assessment_complete": false,
  "next_skill": null
}
```

---

### 3. **POST /api/v1/score** - Score Skill
Evaluate proficiency level for a completed assessment.

**Request:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "skill": "Python"
}
```

**Response:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "skill_score": {
    "skill": "Python",
    "assessed_level": 3,
    "confidence": 0.75,
    "jd_required_level": 4,
    "gap": 1,
    "evidence_tags": ["demonstrates_concepts", "partial_implementation"],
    "conversation_summary": "Candidate shows good conceptual understanding..."
  },
  "all_scores": null
}
```

---

### 4. **POST /api/v1/plan** - Generate Learning Plan
Generate personalized, time-bound learning roadmap.

**Request:**
```json
{
  "session_id": "session_a1b2c3d4e5f6"
}
```

**Response:**
```json
{
  "learning_plan": {
    "session_id": "session_a1b2c3d4e5f6",
    "candidate_name": "John Doe",
    "total_duration_weeks": 8,
    "priority_skills": ["Python", "System Design"],
    "adjacent_skills": ["Data Structures", "Database Design"],
    "milestones": [
      {
        "week": 1,
        "skill": "Python Advanced Patterns",
        "objective": "Master decorators, metaclasses, async",
        "resources": [...],
        "assessment_criteria": [...]
      }
    ],
    "success_metrics": {...}
  },
  "summary": "Your personalized learning plan is ready!..."
}
```

---

### 5. **GET /api/v1/gaps/{session_id}** - Gap Analysis
Retrieve gap analysis for completed assessments.

**Response:**
```json
{
  "session_id": "session_a1b2c3d4e5f6",
  "gaps": [
    {
      "skill": "System Design",
      "assessed_level": 2,
      "jd_required_level": 4,
      "gap_severity": "critical",
      "priority_rank": 1,
      "upskilling_path": ["Database Design", "API Design"]
    }
  ],
  "overall_readiness": 0.65
}
```

---

## 🛠️ Core Components to Implement

### Phase 2: AI Agents (Coming Next)
- [ ] **Assessment Agent**: Multi-turn adaptive questioning with CoT reasoning
- [ ] **Scoring Agent**: Proficiency scoring with evidence extraction
- [ ] **Planning Agent**: Learning milestone generation with RAG
- [ ] **Gap Analysis Agent**: Priority ranking and adjacent skill traversal

### Phase 3: NLP & Services
- [ ] **Skill Extraction Service**: spaCy + sentence-transformers
- [ ] **Skill Matcher Service**: Semantic similarity & O*NET integration
- [ ] **RAG Service**: Course database integration
- [ ] **Session Manager**: PostgreSQL + pgvector storage

### Phase 4: Frontend
- [ ] **React Chat Interface**: Real-time assessment conversation
- [ ] **Dashboard**: Skill scores visualization
- [ ] **Learning Plan UI**: Interactive roadmap display

---

## 📊 Data Models (Next Steps)

See `/app/models/` for SQLAlchemy ORM definitions:
- `Session`: User assessment session state
- `Skill`: Skill taxonomy with embeddings (pgvector)
- `Assessment`: Conversation history & scoring data
- `LearningPlan`: Generated plans & milestones

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER (React)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Document   │  │     Chat     │  │  Dashboard   │               │
│  │    Upload    │  │  Assessment  │  │   Results    │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                         │
└─────────┼─────────────────┼─────────────────┼─────────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  API LAYER (FastAPI Endpoints)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    /upload   │  │    /chat     │  │    /score    │               │
│  │   /gaps      │  │    /plan     │  │   /health    │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                         │
└─────────┼─────────────────┼─────────────────┼─────────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT LAYER (AI Agents)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ Assessment   │  │   Scoring    │  │   Planning   │               │
│  │    Agent     │  │    Agent     │  │    Agent     │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                         │
│         └─────────────────┼─────────────────┘                         │
│                           ▼                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │         Gap Analysis Agent                                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│              SERVICE & NLP LAYER (Phase 3 - COMPLETE)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    Skill     │  │    LLM       │  │  Response    │               │
│  │ Extractor    │  │  Service     │  │ Evaluator    │               │
│  │(Multi-strat.)│  │(Claude+Cache)│  │(NLP Scoring) │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                         │
└─────────┼─────────────────┼─────────────────┼─────────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    Claude    │  │    spaCy     │  │ Sentence-    │               │
│  │   API 3.5    │  │     NLP      │  │ Transformers │               │
│  │              │  │              │  │ (embeddings) │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│               DATA LAYER (PostgreSQL + pgvector)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    Users     │  │   Sessions   │  │ Assessments  │               │
│  │  Skills      │  │  Scores      │  │  Conversations│              │
│  │  Plans       │  │  Embeddings  │  │  Learning    │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Scoring & Evaluation Logic

### **Multi-Dimensional Response Evaluation**

The system uses a sophisticated **NLP-based scoring mechanism** to evaluate candidate responses:

```
┌─────────────────────────────────────────────────────────────┐
│           RESPONSE EVALUATION PIPELINE                       │
└─────────────────────────────────────────────────────────────┘

INPUT: Candidate Response + Question Context
   │
   ├─► 1. RELEVANCE SCORING (30% weight)
   │   ├─ Semantic similarity to question (sentence-transformers)
   │   ├─ Cosine distance threshold: 0.7
   │   └─ Score: 0.0 - 1.0
   │
   ├─► 2. DEPTH SCORING (35% weight)
   │   ├─ Specificity detection (keywords: "example", "project", "implemented")
   │   ├─ Response length (minimum 100 chars for medium score)
   │   ├─ Evidence tag extraction (7 categories):
   │   │  ├─ specific: "In my project at X company..."
   │   │  ├─ project: "Built a Django REST API..."
   │   │  ├─ experience: "5 years working with..."
   │   │  ├─ metrics: "Improved performance by 40%..."
   │   │  ├─ technical: "Used async/await patterns..."
   │   │  ├─ team: "Led a team of 3 engineers..."
   │   │  └─ learning: "Studied O'Reilly books on..."
   │   └─ Score: 0.0 - 1.0
   │
   ├─► 3. CLARITY SCORING (20% weight)
   │   ├─ Structure analysis (coherent paragraphs)
   │   ├─ Signal phrases ("First", "Additionally", "Therefore")
   │   ├─ Sentence complexity (not too simple, not too complex)
   │   └─ Score: 0.0 - 1.0
   │
   ├─► 4. CONFIDENCE SCORING (15% weight)
   │   ├─ Certainty language detection
   │   │  ├─ High: "I", "I built", "I implemented"
   │   │  ├─ Medium: "We did", "We used"
   │   │  └─ Low: "Maybe", "Could be", "Possibly"
   │   ├─ Hedging language penalty: -0.2 for "probably", "somewhat"
   │   └─ Score: 0.0 - 1.0
   │
   └─► FINAL QUALITY SCORE
       ├─ Formula: (R×0.30) + (D×0.35) + (C×0.20) + (Con×0.15)
       ├─ Range: 0.0 - 1.0
       └─ Proficiency Level Mapping:
           ├─ 0.0-0.2  → Level 1 (Beginner)
           ├─ 0.2-0.4  → Level 2 (Basic)
           ├─ 0.4-0.6  → Level 3 (Intermediate)
           ├─ 0.6-0.8  → Level 4 (Advanced)
           └─ 0.8-1.0  → Level 5 (Expert)

OUTPUT: Quality Score + Proficiency Level + Evidence Tags
```

### **Proficiency Scoring Algorithm**

For each skill, the system aggregates responses across multiple turns:

```
┌─────────────────────────────────────────────────────────────┐
│        SKILL PROFICIENCY AGGREGATION (Multi-Turn)            │
└─────────────────────────────────────────────────────────────┘

Turn 1 (Conceptual): Q&A → Quality 0.7 → Evidence: [specific, learning]
Turn 2 (Practical):  Q&A → Quality 0.8 → Evidence: [project, metrics, team]
Turn 3 (Advanced):   Q&A → Quality 0.85 → Evidence: [technical, experience]

   └─► AGGREGATION:
       ├─ Average Quality Score: (0.7 + 0.8 + 0.85) / 3 = 0.783
       ├─ Evidence Frequency Analysis:
       │  ├─ project:3, technical:2, metrics:2, experience:1, etc.
       │  └─ High presence = High confidence
       └─ Proficiency Level Calculation:
           ├─ Base Level: quality_score → level (0.783 → Level 4)
           ├─ Confidence Adjustment:
           │  ├─ Evidence < 3 tags: -0.1 (low confidence)
           │  ├─ Evidence 3-5 tags: +0.0 (normal confidence)
           │  └─ Evidence > 5 tags: +0.1 (high confidence)
           └─ Final: Level 4 (Advanced) with 85% confidence
```

### **Gap Analysis & Severity Ranking**

```
┌─────────────────────────────────────────────────────────────┐
│             GAP SEVERITY CALCULATION                         │
└─────────────────────────────────────────────────────────────┘

For each skill:
├─ JD Required Level: 4 (Advanced)
├─ Assessed Level: 2 (Basic)
├─ Gap Level: 4 - 2 = 2 levels
│
└─► Severity Ranking:
    ├─ Gap 3+ levels: CRITICAL (Priority 1) [Deep technical gaps]
    ├─ Gap 2 levels: HIGH (Priority 2) [Major skill gaps]
    ├─ Gap 1 level: MEDIUM (Priority 3) [Minor gaps]
    └─ Gap 0 levels: ALIGNED (Priority 4) [Skill requirement met]

ORDERING: Sorted by (gap_level DESC, confidence DESC)
```

### **Learning Plan Generation**

```
┌─────────────────────────────────────────────────────────────┐
│         PERSONALIZED LEARNING PATH GENERATION                │
└─────────────────────────────────────────────────────────────┘

For each gap (ordered by priority):
│
├─► DURATION ESTIMATION:
│   ├─ Gap 3+ levels: 8-12 weeks @ 20 hrs/week
│   ├─ Gap 2 levels: 4-8 weeks @ 15 hrs/week
│   ├─ Gap 1 level: 2-4 weeks @ 10 hrs/week
│   └─ Total Plan Duration: Sum of all gaps
│
├─► MILESTONE BREAKDOWN:
│   ├─ Week 1-2: Foundational concepts
│   ├─ Week 3-4: Intermediate patterns
│   ├─ Week 5-6: Advanced techniques
│   └─ Week 7-8: Project-based mastery
│
├─► RESOURCE RECOMMENDATIONS:
│   ├─ Courses: Udemy, Coursera (matched to skill)
│   ├─ Books: Technical reads + practice guides
│   ├─ Projects: Real-world implementations
│   └─ Practice: LeetCode, HackerRank problems
│
└─► SUCCESS METRICS:
    ├─ Weekly progress checkpoints
    ├─ Mini-project completions
    ├─ Practice problem pass rate
    └─ Final assessment re-evaluation
```

### **Example Scoring Walkthrough**

```
CANDIDATE RESPONSE to "Describe your Python experience":

"Over 5 years, I've built production Django APIs handling 
1M+ requests/day. I implemented async/await patterns for 
concurrency, reducing latency by 40%. Led a team of 3 junior 
developers, mentoring them on Python best practices. Currently 
studying advanced async patterns from O'Reilly books."

EVALUATION:

1. RELEVANCE (Semantic Similarity)
   └─ Score: 0.92 (highly relevant to Python assessment)

2. DEPTH ANALYSIS
   ├─ Specificity: "1M+ requests/day", "40% reduction"
   ├─ Evidence Tags: [project, experience, metrics, team, technical, learning]
   ├─ Evidence Count: 6 (excellent)
   └─ Score: 0.88

3. CLARITY
   ├─ Well-structured, logical flow
   ├─ Clear signal phrases: "Over 5 years", "Led a team"
   └─ Score: 0.85

4. CONFIDENCE
   ├─ High confidence language: "I've built", "I implemented"
   ├─ No hedging: "Currently studying" = active learning
   └─ Score: 0.90

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL CALCULATION:
(0.92×0.30) + (0.88×0.35) + (0.85×0.20) + (0.90×0.15)
= 0.276 + 0.308 + 0.170 + 0.135
= 0.889

RESULT: Level 4 (Advanced) | Confidence: 89%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🧠 Technology Highlights

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | FastAPI | High-performance API |
| **AI/LLM** | Claude 3.5 Sonnet / GPT-4o | Conversational assessment & reasoning |
| **NLP** | spaCy + sentence-transformers | Skill extraction & semantic matching |
| **Evaluation** | Multi-dimensional NLP scoring | Response quality assessment |
| **Database** | PostgreSQL + pgvector | Session state & skill embeddings |
| **RAG** | LangChain | Resource recommendation |
| **Frontend** | React | Interactive chat UI |

---

## � Assessment Journey Flowchart

```
┌──────────────────────────────────────────────────────────────────────┐
│ START: Candidate Upload Documents                                     │
│ Input: Job Description + Resume                                      │
└────────────────────┬─────────────────────────────────────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 1. SKILL EXTRACTION (Phase 3)  │
        │ └─ Parse JD: 4 skills found    │
        │ └─ Parse Resume: 3 skills      │
        │ └─ Union: 6 unique skills      │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 2. SESSION INITIALIZATION       │
        │ └─ Create session_id            │
        │ └─ Store documents in DB        │
        │ └─ Start timer                  │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 3. MULTI-TURN CONVERSATION      │
        │ For each skill (ordered by gap):│
        │                                 │
        │ Turn 1: Conceptual question     │
        │ ├─ Q: "What is Python?"         │
        │ ├─ A: [Candidate response]      │
        │ ├─ Score: 0.7 (Intermediate)    │
        │ └─ Evidence: [specific, learning]
        │                                 │
        │ Turn 2: Practical question      │
        │ ├─ Q: "Describe a project..."   │
        │ ├─ A: [Candidate response]      │
        │ ├─ Score: 0.85 (Advanced)       │
        │ └─ Evidence: [project, metrics] │
        │                                 │
        │ Turn 3: Advanced question       │
        │ ├─ Q: "How would you optimize?"│
        │ ├─ A: [Candidate response]      │
        │ ├─ Score: 0.88 (Expert)         │
        │ └─ Evidence: [technical, team]  │
        │                                 │
        │ Aggregation: Avg 0.811 → Level 4
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 4. SCORING & GAP ANALYSIS       │
        │ For each skill:                 │
        │ ├─ Assessed: Level 4            │
        │ ├─ Required: Level 5            │
        │ ├─ Gap: 1 level (MEDIUM)        │
        │ └─ Confidence: 85%              │
        │                                 │
        │ All Skills Scored ✓             │
        │ Sort by gap severity            │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 5. LEARNING PLAN GENERATION     │
        │ For priority gaps:              │
        │ ├─ Gap 1: Django Advanced       │
        │ │  └─ Duration: 4 weeks         │
        │ │  └─ Resources: 5 courses      │
        │ │  └─ Milestones: 4 weeks       │
        │ │                               │
        │ ├─ Gap 2: System Design         │
        │ │  └─ Duration: 8 weeks         │
        │ │  └─ Resources: 8 courses      │
        │ │  └─ Milestones: 8 weeks       │
        │ │                               │
        │ └─ Total Duration: 12 weeks     │
        │                                 │
        │ Plan Generated ✓                │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 6. RESULTS & RECOMMENDATIONS   │
        │ ├─ Overall Readiness: 82%      │
        │ ├─ Strengths: Python (L4)      │
        │ ├─ Critical Gaps: System (L1)  │
        │ ├─ Learning Path: 12 weeks     │
        │ └─ Action Items: Start today   │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ END: Assessment Complete       │
        │ Generate Report & Export Plan   │
        └────────────────────────────────┘
```

---

## 📊 Key Metrics & KPIs

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DASHBOARD METRICS                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📈 Assessment Metrics:                                             │
│  ├─ Overall Readiness Score: 0-100%                                 │
│  ├─ Skills Assessed: Count of unique skills                         │
│  ├─ Average Proficiency: Mean of all skill levels                   │
│  ├─ Confidence Score: Avg confidence across assessments              │
│  └─ Assessment Duration: Total time taken                           │
│                                                                     │
│  🎯 Gap Analysis:                                                   │
│  ├─ Total Skill Gaps: Count of assessed < required                  │
│  ├─ Critical Gaps: Count of gap >= 3 levels                         │
│  ├─ High-Priority Skills: Sorted by gap severity                    │
│  ├─ Gap Severity Distribution: [Critical, High, Medium, Low]        │
│  └─ Adjacent Skills: Skills to develop next                         │
│                                                                     │
│  📚 Learning Plan:                                                  │
│  ├─ Total Duration: Sum of all gap durations (weeks)                │
│  ├─ Milestone Count: Number of learning checkpoints                 │
│  ├─ Resource Count: Total courses + books + projects                │
│  ├─ Weekly Commitment: Estimated hours per week                     │
│  └─ Success Rate: % of milestones completed (after follow-up)       │
│                                                                     │
│  ⏱️  Performance Metrics:                                           │
│  ├─ Assessment Speed: Avg time per skill (minutes)                  │
│  ├─ Response Quality: Avg quality score (0-1)                       │
│  ├─ Learning Velocity: Milestones completed per week                │
│  └─ System Uptime: % availability                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 💡 Scoring Logic - Quick Summary

| Component | Weight | Method | Output |
|-----------|--------|--------|--------|
| **Relevance** | 30% | Sentence-transformers cosine similarity | 0.0-1.0 |
| **Depth** | 35% | Evidence tag detection + response length | 0.0-1.0 |
| **Clarity** | 20% | NLP structure analysis + coherence | 0.0-1.0 |
| **Confidence** | 15% | Certainty language detection | 0.0-1.0 |
| **FINAL** | 100% | Weighted sum of all components | **Level 1-5** |

**Quality → Proficiency Mapping:**
- 0.0-0.2: Level 1 (Beginner) 🔴
- 0.2-0.4: Level 2 (Basic) 🟠
- 0.4-0.6: Level 3 (Intermediate) 🟡
- 0.6-0.8: Level 4 (Advanced) 🟢
- 0.8-1.0: Level 5 (Expert) 🟢✨

Copy `.env.example` to `.env` and fill in:

```bash
# OpenAI / Anthropic API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/skill_assessment

# LLM Configuration
LLM_MODEL=claude-3-5-sonnet-20241022
```

---

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app
```

---

## 📚 Documentation

- **Architecture**: See `docs/architecture.md`
- **API Spec**: See `docs/api_specification.md`
- **Data Models**: See `docs/data_models.md`
- **Skill Taxonomy**: See `docs/skill_taxonomy.md`

---

## 🐳 Docker Setup (Optional)

```bash
# Build and run full stack
docker-compose up --build

# Verify services
curl http://localhost:8000/health
```

---

## 📝 Next Steps

1. ✅ **Project Setup** (COMPLETED)
   - Folder structure
   - Dependencies
   - API contracts

2. 🔄 **Phase 2 - AI Agents** (NEXT)
   - Implement assessment_agent.py
   - Implement scoring_agent.py
   - Test agent integration

3. 🔄 **Phase 3 - NLP Services**
   - Skill extraction
   - Semantic matching
   - RAG integration

4. 🔄 **Phase 4 - Frontend**
   - React components
   - Chat UI
   - Dashboard

---

## 👥 Contributors

- Shivam Yadav

---

## 📄 License

MIT License - Feel free to use for hackathon and beyond!

---


# AI-Skill-Assessment
