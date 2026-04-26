# Development Roadmap

## 🎯 Hackathon Phases & Timeline

### ✅ Phase 1: Project Setup (COMPLETED)
**Status:** DONE

What's been delivered:
- ✅ Monorepo folder structure
- ✅ `requirements.txt` with all dependencies
- ✅ Foundational FastAPI `main.py` with 5 core endpoints
- ✅ Complete Pydantic schemas for data contracts
- ✅ Configuration management
- ✅ Comprehensive documentation

**Files created:** 10+ files, 440+ lines of FastAPI code

---

## 🔄 Phase 2: AI Agents & Core Logic (NEXT - HIGH PRIORITY)
**Estimated Time:** 4-6 hours

### 2.1 Assessment Agent
**File:** `app/agents/assessment_agent.py`

Tasks:
- [ ] Implement adaptive multi-turn questioning logic
- [ ] Create question difficulty progression (conceptual → scenario → applied)
- [ ] Use Claude API with system prompts for domain expertise
- [ ] Extract confidence scores from responses
- [ ] Implement fallback to simpler questions if answers unclear
- [ ] Add turn count limiting and graceful completion

**Key Functions:**
```python
async def generate_assessment_question(
    skill: str,
    turn_count: int,
    conversation_history: List[ChatMessage],
    jd_context: str
) -> str
```

**Implementation Notes:**
- Use Claude 3.5 Sonnet for quality reasoning
- Chain-of-Thought prompting for adaptive logic
- Consider temperature=0.7 for consistency
- Cache system prompts for efficiency

---

### 2.2 Scoring Agent
**File:** `app/agents/scoring_agent.py`

Tasks:
- [ ] Analyze full conversation history to score proficiency
- [ ] Extract evidence tags from responses
- [ ] Generate reasoning for score using CoT
- [ ] Compute confidence based on answer clarity and consistency
- [ ] Compare assessed vs JD-required levels
- [ ] Create human-readable score summary

**Key Functions:**
```python
async def score_skill_proficiency(
    skill: str,
    conversation_history: List[ChatMessage],
    jd_required_level: int
) -> SkillScore
```

**Implementation Notes:**
- Use structured prompts with scoring rubric
- Extract 3-5 evidence tags per score
- Confidence = (clarity + consistency + depth) / 3
- Include reasoning for transparency

---

### 2.3 Gap Analysis Agent
**File:** `app/agents/gap_analysis_agent.py`

Tasks:
- [ ] Compare all assessed scores vs JD requirements
- [ ] Rank gaps by severity (critical > high > medium > low)
- [ ] Calculate overall JD readiness percentage
- [ ] Create upskilling paths for each gap
- [ ] Identify skills with zero gap (strengths)
- [ ] Suggest skill combinations for accelerated learning

**Key Functions:**
```python
async def analyze_skill_gaps(
    skill_scores: List[SkillScore],
    jd_skills: List[str]
) -> GapAnalysisResult
```

**Implementation Notes:**
- Gap severity: gap >= 3 → critical, 2 → high, 1 → medium, 0 → low
- Readiness = (sum of assessed / sum of required) * 100
- Use skill_graph for adjacent skills

---

### 2.4 Learning Plan Agent
**File:** `app/agents/planning_agent.py`

Tasks:
- [ ] Generate weekly milestones for skill improvement
- [ ] Create SMART objectives for each milestone
- [ ] Calculate total duration (estimate 4-6 weeks per high-gap skill)
- [ ] Include prerequisite tracking
- [ ] Add assessment criteria for milestone completion
- [ ] Integrate with RAG for resource recommendations
- [ ] Create success metrics for the plan

**Key Functions:**
```python
async def generate_learning_plan(
    skill_scores: List[SkillScore],
    jd_skills: List[str],
    available_resources: List[Resource]
) -> LearningPlan
```

**Implementation Notes:**
- Priority skills = gaps >= 1 (sorted by severity)
- Adjacent skills = skills that increase readiness for priority skills
- Week calculation: high-gap (2 weeks), medium-gap (1.5 weeks), low-gap (optional)
- Include buffer weeks for practice and review

---

## 🔄 Phase 3: NLP Services & LLM Integration (MEDIUM PRIORITY)
**Estimated Time:** 4-6 hours

### 3.1 Skill Extraction Service
**File:** `app/services/skill_extractor.py`

Tasks:
- [ ] Use spaCy for entity recognition
- [ ] Implement sentence-transformers for semantic similarity
- [ ] Create skill normalization to standard taxonomy
- [ ] Handle skill aliases (e.g., "ML" → "Machine Learning")
- [ ] Score extraction confidence
- [ ] Filter low-confidence extractions

**Key Functions:**
```python
def extract_skills(text: str) -> List[ExtractedSkill]
def normalize_skill(raw_skill: str) -> str
```

---

### 3.2 Skill Matching Service
**File:** `app/services/skill_matcher.py`

Tasks:
- [ ] Implement semantic similarity matching
- [ ] Align JD skills with resume skills
- [ ] Use O*NET for skill standardization
- [ ] Create skill similarity matrix
- [ ] Handle partial matches (e.g., "Python" matches "Python 3.8")
- [ ] Rank matched skills by confidence

**Key Functions:**
```python
def match_skills(jd_skills: List[str], resume_skills: List[str]) -> Dict
def compute_similarity(skill1: str, skill2: str) -> float
```

---

### 3.3 LLM Service
**File:** `app/services/llm_service.py`

Tasks:
- [ ] Implement Anthropic Claude API integration
- [ ] Implement OpenAI GPT API as fallback
- [ ] Create standardized prompt templates
- [ ] Implement rate limiting and retry logic
- [ ] Add response caching
- [ ] Error handling and graceful degradation

**Key Functions:**
```python
async def call_llm(prompt: str, model: str) -> str
async def call_llm_with_system_prompt(system: str, user: str) -> str
```

---

### 3.4 RAG Service
**File:** `app/services/rag_service.py`

Tasks:
- [ ] Integrate with course databases (Coursera, Udemy APIs)
- [ ] Implement semantic search over course embeddings
- [ ] Create resource relevance scoring
- [ ] Filter resources by difficulty and duration
- [ ] Add cost/pricing information
- [ ] Rank by popularity and ratings

**Key Functions:**
```python
async def find_resources(skill: str, difficulty: str) -> List[Resource]
def rank_resources(resources: List[Resource], criteria: Dict) -> List[Resource]
```

---

## 🔄 Phase 4: Database & Session Management (HIGH PRIORITY)
**Estimated Time:** 3-4 hours

### 4.1 Database Models
**Files:** `app/models/*.py`

Tasks:
- [ ] Implement `Session` model (session state tracking)
- [ ] Implement `Skill` model with pgvector embeddings
- [ ] Implement `Assessment` model (conversations, scores)
- [ ] Implement `LearningPlan` model (plans, milestones)
- [ ] Create database indexes for performance
- [ ] Implement cascade deletes and constraints

---

### 4.2 Session Manager Service
**File:** `app/services/session_manager.py`

Tasks:
- [ ] Replace in-memory session_store with PostgreSQL
- [ ] Implement session lifecycle management
- [ ] Add session expiration (24 hours)
- [ ] Create session backup to S3 (optional)
- [ ] Implement concurrent session handling

---

### 4.3 Database Migrations
**File:** `backend/app/db/migrations/`

Tasks:
- [ ] Initialize Alembic
- [ ] Create initial migration for all models
- [ ] Add seed data (skill taxonomy)
- [ ] Document migration process

---

## 🔄 Phase 5: Frontend Development (LOWER PRIORITY FOR MVP)
**Estimated Time:** 4-5 hours

### 5.1 React Setup
**Files:** `frontend/src/`

Tasks:
- [ ] Initialize React + TypeScript project
- [ ] Setup API client service
- [ ] Create auth/session management
- [ ] Setup routing and navigation

---

### 5.2 Components
**Files:** `frontend/src/components/`

Tasks:
- [ ] DocumentUpload component (file upload)
- [ ] ChatAssessment component (real-time chat)
- [ ] SkillScores component (visualization)
- [ ] GapAnalysis component (charts)
- [ ] LearningPlanView component (roadmap)
- [ ] Dashboard component (overview)

---

### 5.3 Styling
Tasks:
- [ ] Setup Tailwind CSS
- [ ] Create design system
- [ ] Implement responsive design
- [ ] Add dark mode support

---

## 🎯 Recommended Priority Order

For maximum hackathon impact:

1. **Phase 2.1 & 2.2** → Assessment + Scoring (Core logic)
2. **Phase 3.1 & 3.3** → Skill Extraction + LLM (NLP foundation)
3. **Phase 4** → Database & Session Management (Data persistence)
4. **Phase 2.3 & 2.4** → Gap Analysis + Planning (Recommendations)
5. **Phase 3.2 & 3.4** → Skill Matching + RAG (Polish)
6. **Phase 5** → Frontend (UI/UX)

---

## 📊 Development Checklist

### Phase 2 Agents
- [ ] Assessment Agent (generate_assessment_question)
- [ ] Scoring Agent (score_skill_proficiency)
- [ ] Gap Analysis Agent (analyze_skill_gaps)
- [ ] Planning Agent (generate_learning_plan)
- [ ] Integration tests for all agents

### Phase 3 Services
- [ ] Skill Extraction (spaCy + transformers)
- [ ] Skill Matching (semantic similarity)
- [ ] LLM Service (Claude + GPT)
- [ ] RAG Service (course recommendations)
- [ ] Unit tests for all services

### Phase 4 Database
- [ ] SQLAlchemy models defined
- [ ] Alembic migrations created
- [ ] Session Manager implemented
- [ ] Database seeded with skill taxonomy
- [ ] Connection pooling configured

### Phase 5 Frontend
- [ ] React components created
- [ ] API integration complete
- [ ] UI/UX polish
- [ ] Responsive design
- [ ] Error handling UI

---

## 🚀 Launch Criteria

For a successful hackathon submission:

### MVP (Minimum Viable Product)
- ✅ All 5 API endpoints functional
- ✅ Assessment logic working (multi-turn chat)
- ✅ Scoring implemented
- ✅ Learning plan generation working
- ✅ API documentation complete
- ⭐ Demonstrates full end-to-end workflow

### Nice to Have
- Basic React frontend
- Database persistence
- Resource recommendations
- Gap visualization
- Session state recovery

### Stretch Goals
- Real LLM integration (Claude/GPT)
- RAG for resource curation
- Advanced analytics dashboard
- Multi-language support
- Mobile app

---

## 🛠️ Tech Stack Reminders

**Backend Essentials:**
```bash
fastapi==0.104.1
pydantic==2.5.0
anthropic==0.7.1  # or openai==1.3.9
sqlalchemy==2.0.23
```

**NLP Essentials:**
```bash
spacy==3.7.2
sentence-transformers==2.2.2
```

**Database Essentials:**
```bash
psycopg2-binary==2.9.9
pgvector==0.2.4
alembic==1.13.0
```

---

## 📚 Key Implementation Notes

### Assessment Flow
```
1. User sends response → chat endpoint
2. Assessment agent evaluates response
3. Agent generates next question (adaptive)
4. Store in conversation history
5. After MAX_TURNS: mark assessment complete
6. Move to next skill
```

### Scoring Flow
```
1. User requests score for skill
2. Scoring agent reads conversation history
3. CoT reasoning extracts proficiency level
4. Extract evidence tags
5. Compare vs JD requirements
6. Return SkillScore with gap
```

### Learning Plan Flow
```
1. All scores collected
2. Gap analysis identifies priority skills
3. Planning agent generates milestones
4. RAG service finds resources
5. Wrap in LearningPlan response
6. Return to frontend for visualization
```

---

## 🎓 Learning Resources

**LLM Integration:**
- Anthropic Docs: https://docs.anthropic.com
- OpenAI Docs: https://platform.openai.com/docs
- LangChain Docs: https://python.langchain.com

**NLP:**
- spaCy: https://spacy.io
- Sentence Transformers: https://huggingface.co/sentence-transformers

**FastAPI:**
- FastAPI Docs: https://fastapi.tiangolo.com
- Pydantic: https://docs.pydantic.dev

**PostgreSQL + pgvector:**
- pgvector Docs: https://github.com/pgvector/pgvector
- SQLAlchemy: https://sqlalchemy.org

---

## 🎉 Success Metrics

- **Functionality:** All 5 endpoints return data contracts correctly
- **AI Quality:** Assessment questions are contextual and adaptive
- **Scoring:** Proficiency scores backed by evidence with confidence
- **Plan Quality:** Learning plans are realistic and personalized
- **Performance:** API responds in < 2 seconds per request
- **Reliability:** Zero crashes, graceful error handling

---

**You're all set! Start with Phase 2 (AI Agents) for the most value. Good luck! 🚀**
