"""
Assessment Repository - Data access for Assessment model.

Provides:
- Create assessment
- Get assessment by session
- Update skill lists
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import Assessment
from .base import BaseRepository


class AssessmentRepository(BaseRepository[Assessment]):
    """Assessment repository for database operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize with Assessment model."""
        super().__init__(session, Assessment)
    
    
    async def create_assessment(
        self,
        session_id: UUID,
        jd_text: str,
        resume_text: Optional[str] = None,
        jd_skills: Optional[List[str]] = None,
        resume_skills: Optional[List[str]] = None
    ) -> Assessment:
        """
        Create new assessment.
        
        Args:
            session_id: Session UUID
            jd_text: Job description text
            resume_text: Resume text (optional)
            jd_skills: Skills extracted from JD
            resume_skills: Skills extracted from resume
            
        Returns:
            Created assessment
        """
        try:
            assessment = await self.create(
                session_id=session_id,
                jd_text=jd_text,
                resume_text=resume_text or "",
                jd_skills=jd_skills or [],
                resume_skills=resume_skills or []
            )
            logger.info(f"✅ Created assessment for session: {session_id}")
            return assessment
        except Exception as e:
            logger.error(f"Error creating assessment: {e}")
            raise
    
    
    async def get_by_session(self, session_id: UUID) -> Optional[Assessment]:
        """
        Get assessment for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            Assessment instance or None
        """
        try:
            stmt = select(Assessment).where(Assessment.session_id == session_id)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting assessment by session: {e}")
            raise
    
    
    async def update_skills(
        self,
        session_id: UUID,
        jd_skills: Optional[List[str]] = None,
        resume_skills: Optional[List[str]] = None
    ) -> Optional[Assessment]:
        """
        Update extracted skills for an assessment.
        
        Args:
            session_id: Session UUID
            jd_skills: Skills to update from JD
            resume_skills: Skills to update from resume
            
        Returns:
            Updated assessment
        """
        try:
            assessment = await self.get_by_session(session_id)
            if not assessment:
                return None
            
            updates = {}
            if jd_skills is not None:
                updates['jd_skills'] = jd_skills
            if resume_skills is not None:
                updates['resume_skills'] = resume_skills
            
            updated = await self.update(assessment.id, **updates)
            logger.debug(f"✅ Updated skills for assessment: {assessment.id}")
            return updated
        except Exception as e:
            logger.error(f"Error updating assessment skills: {e}")
            raise
