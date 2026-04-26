"""
Learning Plan model - Stores personalized learning recommendations.

After assessment completes and gaps identified, stores:
- Skill with gap
- Gap level (how many levels below required)
- Recommended actions (array of learning recommendations)
- Estimated hours to close gap

Enables:
- Personalized learning path tracking
- Progress monitoring
- Resource recommendations
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TEXT
from .base import BaseModel


class LearningPlan(BaseModel):
    """Learning plan for addressing skill gaps."""
    
    __tablename__ = "learning_plans"
    
    # Foreign key to session
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Skill to improve
    skill = Column(String(100), nullable=False, index=True)
    
    # Gap level (e.g., 1 = one level below, 2 = two levels below)
    gap_level = Column(Integer, nullable=False)
    
    # Recommended learning actions (array of strings)
    # Example: ["Complete Python Basics course", "Build 3 projects", "Read Real Python articles"]
    recommended_actions = Column(ARRAY(TEXT), default=[], nullable=False)
    
    # Estimated hours to close gap
    estimated_hours = Column(Integer, default=40, nullable=False)
    
    # Relationship to session
    session = relationship(
        "Session",
        back_populates="learning_plan",
        foreign_keys=[session_id]
    )
    
    __table_args__ = (
        Index('idx_learning_plans_session_id', 'session_id'),
        Index('idx_learning_plans_skill', 'skill'),
        Index('idx_learning_plans_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<LearningPlan(skill={self.skill}, gap={self.gap_level}, hours={self.estimated_hours})>"
