"""
Pydantic schemas for API request/response contracts.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


# ============ Enum Types ============
class ProficiencyLevel(str, Enum):
    """Proficiency level enumeration."""
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


# ============ Document Upload Schemas ============
class DocumentUploadRequest(BaseModel):
    """Request schema for uploading JD and Resume."""
    jd_content: str = Field(..., description="Job Description text content")
    resume_content: str = Field(..., description="Resume text content")
    candidate_name: Optional[str] = Field(None, description="Candidate name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "jd_content": "We are looking for a Senior Python Engineer...",
                "resume_content": "John Doe, 5 years experience in Python...",
                "candidate_name": "John Doe"
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload."""
    session_id: str = Field(..., description="Unique session ID for this assessment")
    jd_skills: List[str] = Field(..., description="Extracted skills from JD")
    resume_skills: List[str] = Field(..., description="Extracted skills from resume")
    total_skills_to_assess: int = Field(..., description="Total skills to assess")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============ Chat/Assessment Schemas ============
class ChatMessage(BaseModel):
    """Schema for a chat message."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    session_id: str = Field(..., description="Session ID from upload")
    skill: str = Field(..., description="Current skill being assessed")
    user_message: str = Field(..., description="User's response to assessment question")
    turn_count: int = Field(default=1, description="Conversation turn number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "skill": "Python",
                "user_message": "I have used Python for 3 years in production...",
                "turn_count": 1
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    session_id: str
    skill: str
    assistant_message: str = Field(..., description="Next assessment question or feedback")
    turn_count: int
    conversation_history: List[ChatMessage]
    assessment_complete: bool = Field(False, description="Is this skill assessment complete?")
    next_skill: Optional[str] = Field(None, description="Next skill to assess")


# ============ Scoring Schemas ============
class SkillScore(BaseModel):
    """Schema for individual skill score."""
    skill: str
    assessed_level: int = Field(..., ge=1, le=5, description="Proficiency level 1-5")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence of assessment 0-1")
    jd_required_level: int = Field(..., ge=1, le=5, description="Required level from JD")
    gap: int = Field(..., description="Gap = jd_required - assessed")
    evidence_tags: List[str] = Field(default_factory=list, description="Tags supporting the score")
    conversation_summary: Optional[str] = Field(None, description="Summary of assessment conversation")


class ScoreRequest(BaseModel):
    """Request schema for scoring endpoint."""
    session_id: str = Field(..., description="Session ID")
    skill: str = Field(..., description="Skill to score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "skill": "Python"
            }
        }


class ScoreResponse(BaseModel):
    """Response schema for scoring endpoint."""
    session_id: str
    skill_score: SkillScore
    all_scores: Optional[List[SkillScore]] = Field(None, description="All scores if complete")


# ============ Learning Plan Schemas ============
class ResourceRecommendation(BaseModel):
    """Schema for recommended learning resource."""
    title: str
    description: str
    url: Optional[str]
    resource_type: str = Field(..., description="e.g., 'course', 'book', 'tutorial', 'practice'")
    estimated_duration_hours: int
    difficulty_level: str = Field(..., description="beginner, intermediate, advanced")
    relevance_score: float = Field(..., ge=0.0, le=1.0)


class LearningMilestone(BaseModel):
    """Schema for a learning milestone in the plan."""
    week: int
    skill: str
    objective: str
    resources: List[ResourceRecommendation]
    prerequisite_skills: List[str] = Field(default_factory=list)
    assessment_criteria: List[str] = Field(default_factory=list)


class LearningPlan(BaseModel):
    """Schema for personalized learning plan."""
    session_id: str
    candidate_name: Optional[str]
    total_duration_weeks: int
    priority_skills: List[str] = Field(..., description="High-gap skills to focus on")
    adjacent_skills: List[str] = Field(..., description="Adjacent skills to build on existing knowledge")
    milestones: List[LearningMilestone]
    success_metrics: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LearningPlanRequest(BaseModel):
    """Request schema for learning plan endpoint."""
    session_id: str = Field(..., description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123"
            }
        }


class LearningPlanResponse(BaseModel):
    """Response schema for learning plan endpoint."""
    learning_plan: LearningPlan
    summary: str = Field(..., description="Executive summary of the learning plan")


# ============ Session State Schemas ============
class SessionState(BaseModel):
    """Schema for session state tracking."""
    session_id: str
    candidate_name: Optional[str]
    jd_content: str
    resume_content: str
    extracted_skills: List[str]
    assessment_progress: Dict[str, bool] = Field(default_factory=dict, description="skill -> assessment_complete")
    skill_scores: List[SkillScore] = Field(default_factory=list)
    conversation_history: Dict[str, List[ChatMessage]] = Field(
        default_factory=dict, description="skill -> conversation messages"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    learning_plan: Optional[LearningPlan] = None


# ============ Gap Analysis Schemas ============
class GapAnalysis(BaseModel):
    """Schema for gap analysis results."""
    skill: str
    assessed_level: int
    jd_required_level: int
    gap_severity: str = Field(..., description="critical, high, medium, low")
    priority_rank: int
    upskilling_path: List[str] = Field(..., description="Adjacent skills to learn first")


class GapAnalysisResponse(BaseModel):
    """Response schema for gap analysis."""
    session_id: str
    gaps: List[GapAnalysis]
    overall_readiness: float = Field(..., ge=0.0, le=1.0, description="Overall JD readiness %")
