"""
Session model - Represents a single assessment session.

A session is created when a candidate starts an assessment for a skill.

Fields:
- id: Unique session identifier (UUID)
- user_id: Foreign key to user
- skill_assessed: The skill being assessed (e.g., "Python", "Kubernetes")
- status: Session status (active, completed, abandoned)
- created_at: Session start time
- updated_at: Last activity time
"""

from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel


class Session(BaseModel):
    """Assessment session for a skill."""
    
    __tablename__ = "sessions"
    
    # Foreign key to user
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Skill being assessed (e.g., "Python", "Kubernetes", "AWS")
    skill_assessed = Column(String(100), nullable=False, index=True)
    
    # Session status
    status = Column(
        String(20),  # active, completed, abandoned
        default="active",
        nullable=False,
        index=True
    )
    
    # Relationships
    user = relationship(
        "User",
        backref="sessions",
        foreign_keys=[user_id]
    )
    
    assessment = relationship(
        "Assessment",
        uselist=False,
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    conversations = relationship(
        "ConversationHistory",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    skill_scores = relationship(
        "SkillScore",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    learning_plan = relationship(
        "LearningPlan",
        uselist=False,
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('idx_sessions_user_skill', 'user_id', 'skill_assessed'),
        Index('idx_sessions_status', 'status'),
        Index('idx_sessions_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user={self.user_id}, skill={self.skill_assessed}, status={self.status})>"
