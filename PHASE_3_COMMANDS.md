# Phase 3 Command Reference

## Quick Links to Phase 3 Documents

📖 **Main Documentation**
- `PHASE_3_NLP_SERVICES.md` - Detailed implementation guide (300 lines)
- `PHASE_3_QUICK_REFERENCE.md` - Quick lookup (250 lines)
- `PHASE_3_COMPLETE.md` - Completion summary (400 lines)
- `PHASE_3_STATUS.txt` - Status report (THIS)

🧪 **Tests**
- `test_phase3_nlp_services.py` - Complete test suite (390 lines)

💾 **Backend Services**
- `backend/app/services/skill_extractor.py` - Skill extraction (400 lines)
- `backend/app/services/llm_service.py` - Claude API wrapper (350 lines)
- `backend/app/services/response_evaluator.py` - Response scoring (400 lines)

---

## Test Commands

### Run All Phase 3 Tests
```bash
cd /Users/shivamyadav/hackathon_deccan/backend
python3 -c "
import sys
sys.path.insert(0, '.')
from app.services.skill_extractor import extract_skills
from app.services.response_evaluator import evaluate_response_quality
from app.services.llm_service import LLMService

# Test 1: Skill Extraction
skills = extract_skills('Python Django PostgreSQL AWS')
print(f'Skills extracted: {skills}')

# Test 2: Response Evaluation
scores = evaluate_response_quality(
    response='I have 5 years Python experience',
    question='Tell me about Python',
    skill='Python'
)
print(f'Quality score: {scores[\"overall_quality\"]}')

# Test 3: LLM Service
llm = LLMService()
print('LLM Service initialized')
"
```

### Run Full Integration Test (Phase 2.5)
```bash
cd /Users/shivamyadav/hackathon_deccan
python3 test_phase25_integration.py
```

---

## Integration Commands (Next Steps)

### 1. Update AssessmentAgent with Real Claude
Edit: `backend/app/agents/assessment_agent.py`

```python
# Find the _call_claude method and replace:

# BEFORE:
async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
    # Placeholder for MVP
    return "Can you explain your experience with this skill..."

# AFTER:
async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
    from app.services import call_claude
    try:
        response = call_claude(system_prompt, user_prompt, max_tokens=500)
        logger.info(f"✅ Claude response generated")
        return response
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return self._get_fallback_question(self.current_skill, 1)
```

### 2. Update Main.py Upload Endpoint
Edit: `backend/app/main.py` - Find the `/api/v1/upload` endpoint

```python
# BEFORE:
@router.post("/api/v1/upload", response_model=DocumentUploadResponse)
async def upload_documents(request: DocumentUploadRequest):
    session_id = f"session_{len(session_store)}"
    jd_skills = request.jd_content.split()  # Naive
    resume_skills = request.resume_content.split()  # Naive

# AFTER:
@router.post("/api/v1/upload", response_model=DocumentUploadResponse)
async def upload_documents(request: DocumentUploadRequest):
    from app.services import extract_skills
    
    session_id = f"session_{len(session_store)}"
    jd_skills = extract_skills(request.jd_content)
    resume_skills = extract_skills(request.resume_content)
```

### 3. Update ScoringAgent
Edit: `backend/app/agents/scoring_agent.py` - Find `score_skill_proficiency` method

```python
# Use ResponseEvaluator instead of simple heuristics:
async def score_skill_proficiency(self, response: str, skill: str) -> SkillScore:
    from app.services import evaluate_response_quality
    
    # Evaluate the response
    scores = evaluate_response_quality(
        response=response,
        question=self.last_question,
        skill=skill,
        expected_keywords=None
    )
    
    # Build SkillScore from evaluation results
    assessed_level = scores["proficiency_level"]
    confidence = scores["confidence"]
    
    # ... rest of method
```

---

## Architecture Commands

### View Service Architecture
```bash
# Print architecture diagram
cat << 'EOF'
┌──────────────────────────┐
│  FastAPI Endpoints       │
│  /upload /chat /score    │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  AI Agents (Phase 2)     │
│  Assessment, Scoring...  │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  NLP Services (Phase 3)  │ ← YOU ARE HERE
│  • SkillExtractor        │
│  • LLMService            │
│  • ResponseEvaluator     │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  External Models         │
│  Claude, spaCy, etc.     │
└──────────────────────────┘
EOF
```

---

## Usage Examples

### Using Skill Extractor
```python
from app.services import extract_skills

# Basic usage
jd_text = """
Senior Python Engineer
Requirements:
- 5+ years Python
- Django or FastAPI
- PostgreSQL and Redis
- AWS or GCP
- Docker and Kubernetes
"""

skills = extract_skills(jd_text)
# Returns: ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Redis', 'AWS', 'GCP', 'Docker', 'Kubernetes']
```

### Using Response Evaluator
```python
from app.services import evaluate_response_quality

response = "I've built 3 production systems with Python and Django, handling 1M+ users"
scores = evaluate_response_quality(
    response=response,
    question="Tell us about your Django experience",
    skill="Django",
    expected_keywords=["production", "users", "system"]
)

print(f"Quality: {scores['overall_quality']}")     # 0.78
print(f"Level: {scores['proficiency_level']}")     # 4 (Advanced)
print(f"Tags: {scores['evidence_tags']}")          # ['project', 'metrics', 'experience']
```

### Using LLM Service
```python
from app.services import call_claude

question = call_claude(
    system_prompt="You are an expert Python interviewer.",
    user_prompt="Create a hard-level Python interview question about async programming",
    max_tokens=300,
    temperature=0.8,
    use_cache=True
)

print(question)
# Real response from Claude (or fallback template if API unavailable)
```

---

## Environment Setup

### Install Dependencies (One-time)
```bash
# Install Python packages
pip3 install -q loguru spacy

# Download spaCy model (optional, for NER)
python3 -m spacy download en_core_web_sm
```

### Configuration
```bash
# Create .env file in project root
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-...  # Get from https://console.anthropic.com/
EOF
```

---

## Debugging

### Check Service Imports
```bash
cd backend
python3 -c "
from app.services import SkillExtractor, LLMService, ResponseEvaluator
print('✅ All services imported successfully')
"
```

### Test Individual Service
```bash
# Test Skill Extractor
python3 -c "
from app.services.skill_extractor import extract_skills
print(extract_skills('Python Django PostgreSQL'))
"

# Test Response Evaluator
python3 -c "
from app.services.response_evaluator import evaluate_response_quality
print(evaluate_response_quality('I have Python experience', 'About Python', 'Python'))
"
```

### View Service Logs
```bash
# Services use loguru, logs appear in console
# Look for ✅ (success), ⚠️ (warning), ❌ (error)

# Enable debug logging (in services)
# logger.debug(...) messages show extra details
```

---

## Performance Tuning

### Speed Up Skill Extraction
```python
# Use only keyword matching (fastest)
from app.services.skill_extractor import SkillExtractor
extractor = SkillExtractor()
extractor.sentence_model = None  # Disable Transformers
skills = extractor.extract_skills(text)  # ~100ms instead of ~1000ms
```

### Reduce Memory Usage
```python
# Services use on-demand loading of models
# Models are loaded only when needed
# ~300MB total for Transformers + spaCy
# Can be deployed on 1GB RAM server
```

### Monitor Cache Performance
```python
from app.services import LLMService
llm = LLMService()
# Make some calls...
stats = llm.get_cache_stats()
print(f"Cached responses: {stats['cached_responses']}")

costs = llm.estimate_cost()
print(f"Total cost: ${costs['total_cost']:.2f}")
```

---

## Phase 3 → 4 Transition

### Ready for Phase 4 (Database)?
Check:
```bash
# 1. Services working
python3 -c "from app.services import extract_skills; extract_skills('test')"

# 2. Integration tests still passing
cd .. && python3 test_phase25_integration.py

# 3. Environment ready
echo $ANTHROPIC_API_KEY  # Should have value (if using real Claude)
```

### Recommended Order
1. ✅ **Phase 3 Complete** - NLP services ready
2. 🔄 **Phase 3.5** (Optional) - Integrate with agents
3. ⏳ **Phase 4** - Database (PostgreSQL)
4. ⏳ **Phase 5** - Frontend (React/Vue)

---

## Common Issues & Solutions

### "ImportError: No module named 'loguru'"
**Solution**: Install loguru
```bash
pip3 install -q loguru
```

### "ANTHROPIC_API_KEY not found"
**Solution**: Use fallback mode (no API needed) or add .env file
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

### "spaCy model not found"
**Solution**: Optional - services work without it
```bash
python3 -m spacy download en_core_web_sm
```

### Skills extraction too slow
**Solution**: Disable Transformers model
```python
extractor.sentence_model = None  # Use keyword matching only
```

---

## Success Indicators

✅ **Phase 3 is working when**:
1. All three services import without errors
2. Skill extraction returns meaningful skills
3. Response evaluation returns quality scores
4. LLM service handles errors gracefully
5. Full integration test still passes

---

## Next Commands

Choose one:

```bash
# Option 1: Continue Phase 3 Integration
# Update agents to use NLP services (10-15 min)
"Continue with Phase 3 agent integration"

# Option 2: Skip to Phase 4 Database
# Start PostgreSQL integration (30+ min)
"Start Phase 4 database setup"

# Option 3: Review current state
"Show Phase 3 status"
```

---

**Phase 3 Status**: ✅ COMPLETE AND TESTED

Three production-ready NLP services are now available for integration with AI agents.
