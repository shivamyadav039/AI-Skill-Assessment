# Phase 3: NLP Services - Implementation Plan

## Overview
Phase 3 introduces real NLP services to replace placeholder logic throughout the application. This phase establishes the foundation for intelligent skill extraction, adaptive questioning, and response evaluation.

## Completed in Phase 3

### 1. **Skill Extractor Service** (`app/services/skill_extractor.py`)
- **Purpose**: Extract technical skills from JD and Resume using NLP
- **Features**:
  - Keyword matching against 50+ technical skills taxonomy
  - Semantic similarity matching using Sentence Transformers
  - spaCy NER-based extraction for domain-specific terms
  - Skill categorization (Languages, Frameworks, Databases, Cloud, etc.)
  - Frequency-based ranking of extracted skills
  
- **Usage**:
  ```python
  from app.services import extract_skills
  
  skills = extract_skills("Looking for Python expert with Django and PostgreSQL")
  # Returns: ['Python', 'Django', 'PostgreSQL']
  ```

- **Implementation Strategy**:
  - **Tier 1 (Fastest)**: Direct keyword matching against taxonomy
  - **Tier 2 (Accurate)**: Semantic similarity for variations
  - **Tier 3 (Comprehensive)**: NER extraction for custom terms

### 2. **LLM Service** (`app/services/llm_service.py`)
- **Purpose**: Unified wrapper around Anthropic Claude API
- **Features**:
  - Real Claude 3.5 Sonnet API integration
  - Response caching (in-memory, 1-hour expiry)
  - Retry logic with exponential backoff
  - Token counting and cost estimation
  - Fallback responses on API failure
  - Thread-safe singleton pattern

- **Usage**:
  ```python
  from app.services import call_claude
  
  response = call_claude(
      system_prompt="You are an expert interviewer.",
      user_prompt="What's a good Python question?"
  )
  ```

- **Cost Estimation**:
  - Input: $0.003 per 1K tokens
  - Output: $0.015 per 1K tokens
  - Real tracking: `llm_service.estimate_cost()`

### 3. **Response Evaluator Service** (`app/services/response_evaluator.py`)
- **Purpose**: NLP-based evaluation of candidate responses
- **Features**:
  - Multi-dimensional scoring:
    - **Relevance** (30%): How well does it answer the question?
    - **Depth** (35%): How specific and detailed?
    - **Clarity** (20%): How well-structured?
    - **Confidence** (15%): How confident does candidate sound?
  - Evidence tag extraction (specific, project, experience, metrics, etc.)
  - Automatic proficiency level mapping (1-5)
  - Response comparison capability
  - Semantic similarity scoring with sentence transformers

- **Usage**:
  ```python
  from app.services import evaluate_response_quality
  
  scores = evaluate_response_quality(
      response="I used Python for 3 years building data pipelines...",
      question="Tell us about your Python experience",
      skill="Python"
  )
  # Returns: {
  #     "overall_quality": 0.85,
  #     "proficiency_level": 4,
  #     "evidence_tags": ["specific", "project", "experience"],
  #     ...
  # }
  ```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Endpoints                         │
│  /api/v1/upload  /api/v1/chat  /api/v1/score  /api/v1/plan │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI Agents (Phase 2)                       │
│  AssessmentAgent  ScoringAgent  GapAnalysisAgent  etc.      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   NLP Services (Phase 3)  ← YOU ARE HERE     │
│  SkillExtractor  LLMService  ResponseEvaluator             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 External Services & Models                   │
│  Anthropic Claude  spaCy  Sentence Transformers            │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

### 1. Update `assessment_agent.py` to use real Claude
Replace the `_call_claude()` method with:

```python
async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
    from app.services import call_claude
    
    try:
        response = call_claude(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=500
        )
        return response
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return self._get_fallback_question(...)
```

### 2. Update `main.py` document upload endpoint
Replace placeholder skill extraction with real NLP:

```python
@router.post("/api/v1/upload", response_model=DocumentUploadResponse)
async def upload_documents(request: DocumentUploadRequest):
    from app.services import extract_skills
    
    jd_skills = extract_skills(request.jd_content)
    resume_skills = extract_skills(request.resume_content)
    # ...rest of endpoint
```

### 3. Update `scoring_agent.py` to use real response evaluation
Replace placeholder scoring with:

```python
async def score_skill_proficiency(self, response: str, skill: str) -> SkillScore:
    from app.services import evaluate_response_quality
    
    scores = evaluate_response_quality(response, self.last_question, skill)
    
    proficiency_level = scores["proficiency_level"]
    confidence = scores.get("confidence", 0.5)
    # ...build SkillScore from scores
```

## Next Steps for Phase 3 Integration

### Immediate Actions (5 min each):
1. ✅ Created NLP services (Skill Extractor, LLM Service, Response Evaluator)
2. ⏳ Update agents to use real NLP services
3. ⏳ Create integration test for Phase 3
4. ⏳ Update `/api/v1/upload` to use real skill extraction

### Recommended Order:
1. **First**: Update `main.py` upload endpoint (external dependency, low risk)
2. **Second**: Update `assessment_agent.py` with real Claude calls
3. **Third**: Update `scoring_agent.py` with response evaluation
4. **Fourth**: Run integration tests to verify everything works

## Environment Setup

### Required Environment Variables:
```bash
# .env
ANTHROPIC_API_KEY=sk-ant-... (get from Anthropic console)
```

### Required Models (auto-download on first use):
```bash
# spaCy English model (~40MB)
python -m spacy download en_core_web_sm

# Sentence Transformers (~80MB, auto-downloads)
# No manual setup needed - downloads automatically on first use
```

## Testing Phase 3

Create `test_phase3_nlp_services.py`:

```python
import pytest
from app.services import extract_skills, call_claude, evaluate_response_quality

@pytest.mark.asyncio
async def test_skill_extraction():
    text = "We need a Python expert with Django and PostgreSQL"
    skills = extract_skills(text)
    assert "Python" in skills
    assert "Django" in skills

@pytest.mark.asyncio  
async def test_llm_service():
    response = call_claude(
        system_prompt="You are a test",
        user_prompt="Say hello"
    )
    assert len(response) > 0

def test_response_evaluation():
    scores = evaluate_response_quality(
        response="I have 5 years Python experience building data pipelines",
        question="Tell us about Python",
        skill="Python"
    )
    assert scores["overall_quality"] > 0.6
    assert scores["proficiency_level"] >= 3
```

## Performance Considerations

### Caching Strategy:
- **LLM Service**: In-memory cache (1 hour expiry)
- **Skill Extraction**: Compute on demand (fast with heuristics)
- **Response Evaluation**: Compute on demand (under 100ms)

### Token Usage Estimates:
- Assessment question: ~200 tokens
- Response evaluation: ~150 tokens
- Learning plan generation: ~500 tokens

**Daily budget estimate** (50 assessments):
- Input: ~35K tokens = $0.11
- Output: ~35K tokens = $0.53
- **Daily cost: ~$0.64 | Monthly: ~$19**

## Rollback Plan

If NLP services fail:
1. Skill Extractor falls back to keyword matching (no ML)
2. LLM Service uses templated fallback responses
3. Response Evaluator uses simple heuristics
4. Application continues functioning (degraded performance)

## Success Criteria

✅ Phase 3 is complete when:
1. All three services created and tested independently
2. Services integrated with at least 2 agents
3. Integration tests pass (E2E workflow)
4. No breaking changes to Phase 2 functionality
5. Clear documentation and usage examples

## Timeline Estimate

- Creating services: ✅ **DONE** (20 min)
- Integrating with agents: ⏳ **5-10 min**
- Testing & debugging: ⏳ **10-15 min**
- Documentation: ⏳ **5 min**

**Total Phase 3 Time: ~1 hour**

---

**Next Command**: "Continue with Phase 3 agent integration" to proceed with integrating these services into the AI agents.
