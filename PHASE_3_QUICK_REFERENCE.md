# Phase 3: NLP Services - Quick Reference

## What's New in Phase 3

### Three Production-Ready NLP Services:

#### 1️⃣ **Skill Extractor** (`app/services/skill_extractor.py`)
```python
from app.services import extract_skills

# Extract skills from job description or resume
skills = extract_skills("Looking for Python expert with Django, PostgreSQL, and AWS")
# → ['Python', 'Django', 'PostgreSQL', 'AWS']
```

**Features:**
- Taxonomy of 50+ technical skills
- 3-tier extraction (keyword → semantic → NER)
- Categorized output (Languages, Frameworks, Databases, etc.)
- Frequency ranking

---

#### 2️⃣ **LLM Service** (`app/services/llm_service.py`)
```python
from app.services import call_claude

# Real Claude API with caching, retries, and error handling
response = call_claude(
    system_prompt="You are an expert interviewer",
    user_prompt="Generate a Python question",
    max_tokens=500,
    use_cache=True
)
```

**Features:**
- Anthropic Claude 3.5 Sonnet integration
- Response caching (1-hour expiry)
- Exponential backoff retry logic
- Token counting & cost estimation
- Fallback responses on failure

**Cost Tracking:**
```python
from app.services import LLMService

llm = LLMService()
# ... make calls ...
costs = llm.estimate_cost()
# → {"total_cost": 0.25, "input_tokens": 1000, ...}
```

---

#### 3️⃣ **Response Evaluator** (`app/services/response_evaluator.py`)
```python
from app.services import evaluate_response_quality

scores = evaluate_response_quality(
    response="I've used Python for 3 years building data pipelines with Pandas",
    question="Tell us about your Python experience",
    skill="Python"
)

# Returns comprehensive evaluation:
# {
#     "overall_quality": 0.85,
#     "relevance": 0.90,
#     "depth": 0.80,
#     "clarity": 0.85,
#     "confidence": 0.82,
#     "evidence_tags": ["specific", "project", "experience"],
#     "proficiency_level": 4  # Advanced
# }
```

**Scoring Dimensions:**
- **Relevance** (30%): How well answers the question
- **Depth** (35%): Specificity and detail level
- **Clarity** (20%): Structure and organization
- **Confidence** (15%): Confidence indicators in language

---

## Updated Dependencies

All libraries already in `requirements.txt`:
- ✅ `anthropic==0.7.1` (Claude API)
- ✅ `spacy==3.7.2` (NER, NLP)
- ✅ `sentence-transformers==2.2.2` (Semantic similarity)
- ✅ `loguru` (Logging)

### Setup (one-time):
```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file with:
ANTHROPIC_API_KEY=sk-ant-...  # Get from https://console.anthropic.com
```

---

## Next: Integration with Agents

### Update Assessment Agent
Replace placeholder in `_call_claude()`:

**Before:**
```python
async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
    # Placeholder for MVP
    return "Can you explain your experience with this skill..."
```

**After:**
```python
async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
    from app.services import call_claude
    
    try:
        return call_claude(system_prompt, user_prompt, max_tokens=500)
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        raise
```

### Update Upload Endpoint
Replace placeholder in `main.py`:

**Before:**
```python
@router.post("/api/v1/upload")
async def upload_documents(request: DocumentUploadRequest):
    jd_skills = request.jd_content.split()  # Naive
    resume_skills = request.resume_content.split()  # Naive
```

**After:**
```python
@router.post("/api/v1/upload")
async def upload_documents(request: DocumentUploadRequest):
    from app.services import extract_skills
    
    jd_skills = extract_skills(request.jd_content)
    resume_skills = extract_skills(request.resume_content)
```

### Update Scoring Agent
Replace placeholder evaluation:

**Before:**
```python
def extract_response_quality(self, response: str) -> float:
    # Simple heuristic: length-based
    if len(response) < 100:
        return 0.4
    return 0.7
```

**After:**
```python
def extract_response_quality(self, response: str) -> float:
    from app.services import evaluate_response_quality
    
    scores = evaluate_response_quality(response, self.last_question, self.current_skill)
    return scores["overall_quality"]
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│        FastAPI Endpoints (main.py)          │
│  /upload  /chat  /score  /plan  /gaps       │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│         AI Agents (Phase 2)                 │
│  Assessment  Scoring  Planning  Gap Analysis│
└──────────────────┬──────────────────────────┘
                   │
                   ↓ calls
┌─────────────────────────────────────────────┐
│      NLP Services (Phase 3) ← NEW!          │
│  SkillExtractor  LLMService  Evaluator     │
└──────────────────┬──────────────────────────┘
                   │
                   ↓ uses
┌─────────────────────────────────────────────┐
│      External AI/ML Models                  │
│  Claude  spaCy  Sentence-Transformers      │
└─────────────────────────────────────────────┘
```

---

## File Summary

| File | Lines | Purpose |
|------|-------|---------|
| `skill_extractor.py` | 400 | Extract technical skills from text |
| `llm_service.py` | 350 | Claude API wrapper with caching |
| `response_evaluator.py` | 400 | Multi-dimensional response scoring |
| **Total** | **~1150** | Production-grade NLP services |

---

## Testing Commands

```bash
# Test NLP services individually
python -m pytest backend/app/services/ -v

# Test agent integration
python -m pytest backend/test_phase3_nlp_services.py -v

# Full integration test
python test_phase25_integration.py
```

---

## Key Decisions & Tradeoffs

✅ **Multi-tier skill extraction**
- Pro: Fast + accurate + comprehensive
- Cons: More complex code

✅ **In-memory response caching**
- Pro: Fast, no DB dependency, simple
- Cons: Lost on restart, limited by RAM

✅ **Heuristic fallbacks**
- Pro: App works even without external services
- Cons: Degraded performance

---

## Success Indicators

✅ Phase 3 is done when:
1. All services created and working
2. Agents use real Claude API
3. Skills extraction works on real JDs
4. Response evaluation matches manual scoring
5. Full E2E tests pass
6. ~$20/month operating cost

---

**Status**: ✅ **Services Complete** | ⏳ **Awaiting Integration**

**Next Step**: Run agent integration or start Phase 4 (Database)
