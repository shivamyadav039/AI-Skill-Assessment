"""
Skill Score Repository - Data access for SkillScore model.

Provides:
- Save proficiency score for skill
- Get score for skill in session
- List all scores for session
- Update scores
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import SkillScore
from .base import BaseRepository


class SkillScoreRepository(BaseRepository[SkillScore]):
    """Skill score repository for database operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize with SkillScore model."""
        super().__init__(session, SkillScore)
    
    
    async def save_score(
        self,
        session_id: UUID,
        skill: str,
        proficiency_level: int,
        confidence: float = 0.0,
        gap_from_required: Optional[int] = None
    ) -> SkillScore:
        """
        Save proficiency score for a skill.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            proficiency_level: Level 1-5
            confidence: Confidence % (0-100)
            gap_from_required: Levels below required (optional)
            
        Returns:
            Created score record
        """
        try:
            score = await self.create(
                session_id=session_id,
                skill=skill,
                proficiency_level=proficiency_level,
                confidence=confidence,
                gap_from_required=gap_from_required
            )
            logger.info(
                f"✅ Saved score: skill={skill}, level={proficiency_level}, "
                f"confidence={confidence:.0f}%"
            )
            return score
        except Exception as e:
            logger.error(f"Error saving skill score: {e}")
            raise
    
    
    async def get_score_for_skill(
        self,
        session_id: UUID,
        skill: str
    ) -> Optional[SkillScore]:
        """
        Get proficiency score for skill in session.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            
        Returns:
            SkillScore or None
        """
        try:
            stmt = (
                select(SkillScore)
                .where(
                    (SkillScore.session_id == session_id) &
                    (SkillScore.skill == skill)
                )
            )
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting skill score: {e}")
            raise
    
    
    async def get_all_for_session(
        self,
        session_id: UUID
    ) -> List[SkillScore]:
        """
        Get all proficiency scores for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of skill scores
        """
        try:
            stmt = (
                select(SkillScore)
                .where(SkillScore.session_id == session_id)
                .order_by(SkillScore.skill)
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting session scores: {e}")
            raise
    
    
    async def get_skills_with_gaps(
        self,
        session_id: UUID
    ) -> List[SkillScore]:
        """
        Get all skills with identified gaps in session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of scores where gap_from_required > 0
        """
        try:
            stmt = (
                select(SkillScore)
                .where(
                    (SkillScore.session_id == session_id) &
                    (SkillScore.gap_from_required > 0)
                )
                .order_by(SkillScore.gap_from_required.desc())
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting skills with gaps: {e}")
            raise
    
    
    async def update_score(
        self,
        session_id: UUID,
        skill: str,
        proficiency_level: Optional[int] = None,
        confidence: Optional[float] = None,
        gap_from_required: Optional[int] = None
    ) -> Optional[SkillScore]:
        """
        Update a skill score.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            proficiency_level: New level (if provided)
            confidence: New confidence (if provided)
            gap_from_required: New gap (if provided)
            
        Returns:
            Updated score or None
        """
        try:
            score = await self.get_score_for_skill(session_id, skill)
            if not score:
                return None
            
            updates = {}
            if proficiency_level is not None:
                updates['proficiency_level'] = proficiency_level
            if confidence is not None:
                updates['confidence'] = confidence
            if gap_from_required is not None:
                updates['gap_from_required'] = gap_from_required
            
            updated = await self.update(score.id, **updates)
            logger.debug(f"✅ Updated score for skill: {skill}")
            return updated
        except Exception as e:
            logger.error(f"Error updating score: {e}")
            raise
