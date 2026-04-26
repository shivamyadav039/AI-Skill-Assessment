"""
Assessment model - Stores assessment documents and extracted skills.

Fields:
- id: Unique assessment identifier (UUID)
- session_id: Foreign key to session
- jd_text: Full job description text
- resume_text: Full resume/CV text
- jd_skills: Array of skills extracted from JD
- resume_skills: Array of skills extracted from resume
- created_at: When assessment was created
"""

from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .base import BaseModel


class Assessment(BaseModel):
    """Assessment document storage model."""
    
    __tablename__ = "assessments"
    
    # Foreign key to session
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Full job description text
    jd_text = Column(Text, nullable=False)
    
    # Full resume text
    resume_text = Column(Text, nullable=True)
    
    # Skills extracted from JD (array of strings)
    jd_skills = Column(ARRAY(String(100)), default=[], nullable=False)
    
    # Skills extracted from resume (array of strings)
    resume_skills = Column(ARRAY(String(100)), default=[], nullable=False)
    
    # Relationship to session
    session = relationship(
        "Session",
        back_populates="assessment",
        foreign_keys=[session_id]
    )
    
    __table_args__ = (
        Index('idx_assessments_session_id', 'session_id'),
        Index('idx_assessments_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Assessment(id={self.id}, session={self.session_id}, jd_skills={len(self.jd_skills) or 0})>"
