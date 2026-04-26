"""
Conversation History model - Stores Q&A conversations during assessment.

Tracks each turn of the assessment conversation including:
- Question asked
- Response given
- Quality score of response
- Turn number

This enables:
- Progress tracking
- Conversation review
- Analytics on response quality progression
"""

from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel


class ConversationHistory(BaseModel):
    """Conversation history for a skill assessment."""
    
    __tablename__ = "conversation_histories"
    
    # Foreign key to session
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Skill being discussed in this turn
    skill = Column(String(100), nullable=False, index=True)
    
    # Turn count (1, 2, 3, ...)
    turn_count = Column(Integer, nullable=False)
    
    # Assessment question asked
    question = Column(Text, nullable=False)
    
    # Candidate's response
    response = Column(Text, nullable=False)
    
    # Quality score (0.0 to 1.0)
    response_quality = Column(Float, default=0.5, nullable=False)
    
    # Relationship to session
    session = relationship(
        "Session",
        back_populates="conversations",
        foreign_keys=[session_id]
    )
    
    __table_args__ = (
        Index('idx_conversations_session_skill', 'session_id', 'skill'),
        Index('idx_conversations_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<ConversationHistory(session={self.session_id}, skill={self.skill}, turn={self.turn_count}, quality={self.response_quality:.2f})>"
