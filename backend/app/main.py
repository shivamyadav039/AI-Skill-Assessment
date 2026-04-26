"""
Main FastAPI application for AI-Powered Skill Assessment & Learning Plan Agent.

This is the entry point for the backend API with foundational endpoints
for document upload, conversational assessment, scoring, and learning plan generation.

Phase 2.5 Integration: Connected to AI Agents for assessment, scoring, gap analysis, and planning.
"""
import logging
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

# Import schemas
try:
    from app.schemas import (
        DocumentUploadRequest,
        DocumentUploadResponse,
        ChatRequest,
        ChatResponse,
        ScoreRequest,
        ScoreResponse,
        LearningPlanRequest,
        LearningPlanResponse,
        GapAnalysisResponse,
        SkillScore,
        LearningPlan,
        LearningMilestone,
        ResourceRecommendation,
        ChatMessage,
    )
except ImportError:
    logger.warning("Schemas not yet available - using mock responses")

# Import Phase 2 AI Agents
try:
    from app.agents import (
        AssessmentAgent,
        ScoringAgent,
        GapAnalysisAgent,
        PlanningAgent,
    )
    logger.info("✅ Phase 2 AI Agents imported successfully")
    AGENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️  AI Agents not available: {str(e)}")
    AGENTS_AVAILABLE = False


# ============ Logger Setup ============
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)


# ============ In-Memory Session Storage (Mock) ============
# In production, replace with PostgreSQL + pgvector
session_store: dict = {}
MAX_TURNS_PER_SKILL = 5


# ============ Lifespan Manager ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    logger.info("🚀 Starting AI Skill Assessment Agent...")
    # Initialize models, databases, etc. here
    yield
    logger.info("🛑 Shutting down AI Skill Assessment Agent...")


# ============ FastAPI App Initialization ============
app = FastAPI(
    title="AI-Powered Skill Assessment & Learning Plan Agent",
    description="Conversational skill assessment with personalized learning plan generation",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Health Check ============
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Skill Assessment Agent"
    }


# ============ Favicon ============
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Serve favicon to prevent 404 errors from browser requests.
    Returns a simple response to satisfy browser requests.
    """
    return JSONResponse(
        content={"status": "ok"},
        status_code=204  # No Content - prevents browser from trying to display
    )


# ============ ENDPOINT 1: DOCUMENT UPLOAD ============
@app.post("/api/v1/upload", response_model=DocumentUploadResponse)
async def upload_documents(request: DocumentUploadRequest):
    """
    Upload Job Description and Resume for assessment.
    
    This endpoint:
    1. Accepts JD and Resume text
    2. Extracts skills using NLP
    3. Creates a session for the assessment
    4. Returns initial skill list for assessment
    
    Args:
        request: DocumentUploadRequest containing JD and Resume
        
    Returns:
        DocumentUploadResponse with session ID and extracted skills
    """
    try:
        logger.info(f"📄 Received upload request for candidate: {request.candidate_name}")
        
        # TODO: Parse and extract skills from JD and Resume
        # This will use spaCy + sentence-transformers for semantic skill extraction
        jd_skills = extract_skills_from_text(request.jd_content, "jd")  # Placeholder
        resume_skills = extract_skills_from_text(request.resume_content, "resume")  # Placeholder
        
        # Generate unique session ID
        import uuid
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        
        # Initialize session state
        session_store[session_id] = {
            "candidate_name": request.candidate_name,
            "jd_content": request.jd_content,
            "resume_content": request.resume_content,
            "jd_skills": jd_skills,
            "resume_skills": resume_skills,
            "assessment_progress": {skill: False for skill in jd_skills},
            "skill_scores": {},
            "conversation_history": {skill: [] for skill in jd_skills},
            "current_skill_index": 0,
            "created_at": datetime.utcnow(),
        }
        
        logger.success(f"✅ Session created: {session_id} with {len(jd_skills)} skills to assess")
        
        return DocumentUploadResponse(
            session_id=session_id,
            jd_skills=jd_skills,
            resume_skills=resume_skills,
            total_skills_to_assess=len(jd_skills),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ============ ENDPOINT 2: CONVERSATIONAL ASSESSMENT ============
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_assessment(request: ChatRequest):
    """
    Run adaptive multi-turn conversation for skill assessment.
    
    This endpoint:
    1. Receives user response to current assessment question
    2. Uses AssessmentAgent to generate next contextual question
    3. Adapts difficulty based on responses (conceptual -> scenario -> applied)
    4. Tracks conversation history and confidence scores
    5. Determines when to move to next skill
    
    Phase 2.5: Now integrated with AssessmentAgent
    
    Args:
        request: ChatRequest with session_id, skill, and user message
        
    Returns:
        ChatResponse with next assessment question and conversation state
    """
    try:
        logger.info(f"💬 Assessment chat for skill: {request.skill}")
        
        # Validate session
        if request.session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_store[request.session_id]
        
        # Add user message to conversation history
        user_msg = ChatMessage(
            role="user",
            content=request.user_message
        )
        session["conversation_history"][request.skill].append(user_msg)
        
        # Initialize assessment agent
        assessment_agent = AssessmentAgent()
        
        # Convert stored messages to ChatMessage objects
        conversation_history = [
            ChatMessage(**msg) if isinstance(msg, dict) else msg 
            for msg in session["conversation_history"][request.skill]
        ]
        
        # Use AssessmentAgent to generate next question
        next_question = await assessment_agent.generate_assessment_question(
            skill=request.skill,
            turn_count=request.turn_count,
            conversation_history=conversation_history,
            jd_context=session["jd_content"],
            resume_context=session["resume_content"]
        )
        
        # Extract response quality for later scoring
        response_quality = assessment_agent.extract_response_quality(request.user_message)
        
        # Determine if assessment should continue
        assessment_complete = not assessment_agent.should_continue_assessment(
            turn_count=request.turn_count,
            response_quality=response_quality,
            max_turns=MAX_TURNS_PER_SKILL
        )
        
        # Add assistant message to conversation history
        assistant_msg = ChatMessage(
            role="assistant",
            content=next_question
        )
        session["conversation_history"][request.skill].append(assistant_msg)
        
        # Determine next skill if current is complete
        next_skill = None
        if assessment_complete:
            session["assessment_progress"][request.skill] = True
            remaining_skills = [s for s in session["jd_skills"] if not session["assessment_progress"].get(s, False)]
            next_skill = remaining_skills[0] if remaining_skills else None
            logger.info(f"✅ {request.skill} assessment complete. Next skill: {next_skill}")
        
        # Rebuild conversation history for response
        conversation_history_response = [
            ChatMessage(**msg) if isinstance(msg, dict) else msg 
            for msg in session["conversation_history"][request.skill]
        ]
        
        return ChatResponse(
            session_id=request.session_id,
            skill=request.skill,
            assistant_message=next_question,
            turn_count=request.turn_count + 1,
            conversation_history=conversation_history_response,
            assessment_complete=assessment_complete,
            next_skill=next_skill
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Chat assessment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# ============ ENDPOINT 3: SKILL SCORING ============
@app.post("/api/v1/score", response_model=ScoreResponse)
async def score_skill(request: ScoreRequest):
    """
    Evaluate proficiency level for a completed assessment.
    
    This endpoint:
    1. Analyzes the full conversation history for a skill
    2. Uses ScoringAgent to score proficiency (1-5)
    3. Computes confidence level based on answer clarity and consistency
    4. Extracts evidence tags to back the score
    5. Compares assessed vs JD-required level
    
    Phase 2.5: Now integrated with ScoringAgent
    
    Args:
        request: ScoreRequest with session_id and skill
        
    Returns:
        ScoreResponse with detailed skill score and gap analysis
    """
    try:
        logger.info(f"🎯 Scoring skill: {request.skill}")
        
        # Validate session
        if request.session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_store[request.session_id]
        
        # Get conversation history
        conversation = session["conversation_history"].get(request.skill, [])
        
        # Convert to ChatMessage objects if needed
        conversation_msgs = [
            ChatMessage(**msg) if isinstance(msg, dict) else msg 
            for msg in conversation
        ]
        
        # Initialize scoring agent
        scoring_agent = ScoringAgent()
        
        # Get JD context for required level
        jd_required_level = 4  # TODO: Extract from JD analysis using NLP service
        
        # Use ScoringAgent to score proficiency
        skill_score = await scoring_agent.score_skill_proficiency(
            skill=request.skill,
            conversation_history=conversation_msgs,
            jd_required_level=jd_required_level
        )
        
        # Store score
        session["skill_scores"][request.skill] = skill_score
        
        logger.success(f"✅ {request.skill} scored: Level {skill_score.assessed_level} (Confidence: {skill_score.confidence:.2%}, Gap: {skill_score.gap})")
        
        # Check if all skills scored
        all_scored = all(s in session["skill_scores"] for s in session["jd_skills"])
        all_scores = list(session["skill_scores"].values()) if all_scored else None
        
        return ScoreResponse(
            session_id=request.session_id,
            skill_score=skill_score,
            all_scores=all_scores
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Scoring failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


# ============ ENDPOINT 4: LEARNING PLAN GENERATION ============
@app.post("/api/v1/plan", response_model=LearningPlanResponse)
async def generate_learning_plan(request: LearningPlanRequest, background_tasks: BackgroundTasks):
    """
    Generate personalized, time-bound learning roadmap.
    
    This endpoint:
    1. Analyzes all skill scores and gaps using GapAnalysisAgent
    2. Ranks gaps by severity (critical -> high -> medium -> low)
    3. Identifies adjacent skills using skill graph traversal
    4. Generates time-bound milestones using PlanningAgent
    5. Includes success metrics and assessment criteria
    
    Phase 2.5: Now integrated with GapAnalysisAgent and PlanningAgent
    
    Args:
        request: LearningPlanRequest with session_id
        background_tasks: For async resource curation
        
    Returns:
        LearningPlanResponse with full learning plan and summary
    """
    try:
        logger.info(f"📚 Generating learning plan for session: {request.session_id}")
        
        # Validate session
        if request.session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_store[request.session_id]
        skill_scores_dict = session.get("skill_scores", {})
        
        if not skill_scores_dict:
            raise HTTPException(status_code=400, detail="No scores available - complete assessments first")
        
        # Convert to list of SkillScore objects
        skill_scores = [
            skill_scores_dict[skill] if isinstance(skill_scores_dict[skill], SkillScore) 
            else SkillScore(**skill_scores_dict[skill])
            for skill in skill_scores_dict
        ]
        
        # Initialize agents
        gap_analysis_agent = GapAnalysisAgent()
        planning_agent = PlanningAgent()
        
        # Step 1: Analyze gaps using GapAnalysisAgent
        logger.info("🔍 Analyzing skill gaps...")
        gap_analysis = await gap_analysis_agent.analyze_skill_gaps(
            skill_scores=skill_scores,
            jd_skills=session["jd_skills"]
        )
        
        logger.info(f"  Overall Readiness: {gap_analysis.overall_readiness:.1f}%")
        logger.info(f"  Critical Gaps: {len(gap_analysis.critical_gaps)}")
        logger.info(f"  High Gaps: {len(gap_analysis.high_gaps)}")
        
        # Step 2: Generate learning plan using PlanningAgent
        logger.info("📋 Generating personalized learning plan...")
        learning_plan = await planning_agent.generate_learning_plan(
            skill_scores=skill_scores,
            jd_skills=session["jd_skills"],
            available_resources=[],
            weekly_hours=20.0
        )
        
        # Store plan and gaps in session
        session["learning_plan"] = learning_plan
        session["gap_analysis"] = gap_analysis
        
        # Build summary with key insights
        total_gap_weeks = sum([m.week for m in learning_plan.milestones]) if learning_plan.milestones else 0
        summary = f"""
        🎯 Your Personalized Learning Plan is Ready!
        
        📊 Current Assessment:
        - Overall JD Readiness: {gap_analysis.overall_readiness:.1f}%
        - Skills at Strength: {len(gap_analysis.strengths)}
        - Critical Gaps: {len(gap_analysis.critical_gaps)}
        
        🚀 Focus Areas:
        - Priority Skills: {', '.join(learning_plan.priority_skills[:3]) if learning_plan.priority_skills else 'N/A'}
        - Adjacent Skills: {', '.join(learning_plan.adjacent_skills[:3]) if learning_plan.adjacent_skills else 'N/A'}
        
        ⏰ Timeline:
        - Total Duration: {learning_plan.total_duration_weeks} weeks
        - Milestones: {len(learning_plan.milestones) if learning_plan.milestones else 0}
        - Time Commitment: 4-5 hours/week
        
        ✅ Success Metrics:
        - Target Readiness: {learning_plan.success_metrics.get('target_readiness', 'N/A')}
        - Milestone Completion: {learning_plan.success_metrics.get('milestone_completion', 'N/A')}
        """
        
        logger.success(f"✅ Learning plan generated with {len(learning_plan.milestones) if learning_plan.milestones else 0} milestones")
        
        return LearningPlanResponse(
            learning_plan=learning_plan,
            summary=summary.strip()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Learning plan generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


# ============ BONUS ENDPOINT: GAP ANALYSIS ============
@app.get("/api/v1/gaps/{session_id}", response_model=GapAnalysisResponse)
async def get_gap_analysis(session_id: str):
    """
    Retrieve gap analysis for completed assessments.
    
    Shows:
    1. Skills with highest gaps (priority order)
    2. Gap severity categorization (critical, high, medium, low)
    3. Recommended adjacent skills for upskilling
    4. Overall JD readiness percentage
    
    Phase 2.5: Uses cached gap analysis from learning plan generation
    """
    try:
        logger.info(f"📊 Retrieving gap analysis for session: {session_id}")
        
        if session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_store[session_id]
        
        # Check if gap analysis was already computed during plan generation
        if "gap_analysis" in session:
            gap_analysis = session["gap_analysis"]
            
            # Format gaps from the analysis
            all_gaps = (gap_analysis.critical_gaps + gap_analysis.high_gaps + 
                       gap_analysis.medium_gaps + gap_analysis.low_gaps)
            
            logger.success(f"✅ Gap analysis retrieved - Overall readiness: {gap_analysis.overall_readiness:.2%}")
            
            return GapAnalysisResponse(
                session_id=session_id,
                gaps=all_gaps,
                overall_readiness=gap_analysis.overall_readiness
            )
        
        # If no cached gap analysis, return a placeholder for now
        # This will be called if gap analysis is requested before learning plan generation
        logger.info("  Gap analysis not yet computed (learning plan not run yet)")
        
        return GapAnalysisResponse(
            session_id=session_id,
            gaps=[],
            overall_readiness=0.0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Gap analysis retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gap analysis failed: {str(e)}")


# ============ PLACEHOLDER FUNCTIONS ============
def extract_skills_from_text(text: str, text_type: str) -> List[str]:
    """
    Extract and align skills from text using NLP.
    
    Phase 3: Uses SkillExtractor service with multi-strategy approach.
    
    Args:
        text: Text to extract skills from (JD or Resume)
        text_type: Type of text ("jd" or "resume")
        
    Returns:
        List of extracted technical skills
    """
    try:
        from app.services import extract_skills
        
        skills = extract_skills(text)
        logger.info(f"✅ Extracted {len(skills)} skills from {text_type}: {skills}")
        return skills
        
    except Exception as e:
        logger.warning(f"Skill extraction failed, using fallback: {e}")
        # Fallback - return mock skills
        if text_type == "jd":
            return ["Python", "System Design", "PostgreSQL", "AWS", "API Design"]
        else:
            return ["Python", "AWS", "JavaScript", "Docker", "Git"]


def generate_next_assessment_question(
    skill: str,
    turn_count: int,
    user_response: str,
    conversation_history: List
) -> str:
    """
    TODO: Generate adaptive assessment question using Claude/GPT.
    
    Strategy:
    - Turn 1-2: Conceptual understanding (definitions, concepts)
    - Turn 3-4: Scenario-based (how would you handle...)
    - Turn 5: Applied task (implement, design, troubleshoot)
    
    Uses Chain-of-Thought prompting to evaluate response quality.
    """
    # Placeholder
    if turn_count == 1:
        return f"Great! Now, can you describe a real-world scenario where you've used {skill}?"
    elif turn_count == 2:
        return f"Interesting. How did you handle performance optimization with {skill}?"
    elif turn_count == 3:
        return f"Let me ask a more applied question: Design a solution using {skill} that handles 1M concurrent users."
    else:
        return f"Excellent. We have enough information about your {skill} proficiency."


async def curate_additional_resources(session_id: str):
    """
    TODO: Background task to curate additional learning resources using RAG.
    
    Uses:
    - Semantic search over course databases
    - Relevance ranking
    - User preference scoring
    """
    logger.info(f"🔍 Curating additional resources for session: {session_id}")
    # Placeholder implementation


# ============ Root Endpoint ============
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI-Powered Skill Assessment & Learning Plan Agent",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
