"""
Skill Score model - Stores proficiency scores for each skill.

After assessment completes, stores:
- Proficiency level (1-5)
- Confidence score (0-100%)
- Gap from required level
- Timestamp

Enables:
- Score tracking and history
- Analytics on skill progression
- Comparison of required vs. actual
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel


class SkillScore(BaseModel):
    """Proficiency score for a skill in a session."""
    
    __tablename__ = "skill_scores"
    
    # Foreign key to session
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Skill name
    skill = Column(String(100), nullable=False, index=True)
    
    # Proficiency level (1-5)
    # 1: Beginner, 2: Basic, 3: Intermediate, 4: Advanced, 5: Expert
    proficiency_level = Column(Integer, nullable=False)
    
    # Confidence in score (0-100%)
    confidence = Column(Float, default=0.0, nullable=False)
    
    # Gap from required level (e.g., -2, 0, +1)
    gap_from_required = Column(Integer, nullable=True)
    
    # Relationship to session
    session = relationship(
        "Session",
        back_populates="skill_scores",
        foreign_keys=[session_id]
    )
    
    __table_args__ = (
        Index('idx_skill_scores_session_skill', 'session_id', 'skill'),
        Index('idx_skill_scores_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<SkillScore(skill={self.skill}, level={self.proficiency_level}, confidence={self.confidence:.0f}%)>"
