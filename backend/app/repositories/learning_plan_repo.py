"""
Learning Plan Repository - Data access for LearningPlan model.

Provides:
- Create learning plan
- Get plan for session
- Update recommendations
- Query plans by skill
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import LearningPlan
from .base import BaseRepository


class LearningPlanRepository(BaseRepository[LearningPlan]):
    """Learning plan repository for database operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize with LearningPlan model."""
        super().__init__(session, LearningPlan)
    
    
    async def create_plan(
        self,
        session_id: UUID,
        skill: str,
        gap_level: int,
        recommended_actions: List[str],
        estimated_hours: int = 40
    ) -> LearningPlan:
        """
        Create learning plan for a skill gap.
        
        Args:
            session_id: Session UUID
            skill: Skill to improve
            gap_level: Levels below required
            recommended_actions: Learning recommendations
            estimated_hours: Hours to close gap
            
        Returns:
            Created learning plan
        """
        try:
            plan = await self.create(
                session_id=session_id,
                skill=skill,
                gap_level=gap_level,
                recommended_actions=recommended_actions,
                estimated_hours=estimated_hours
            )
            logger.info(
                f"✅ Created learning plan: skill={skill}, gap={gap_level}, "
                f"hours={estimated_hours}"
            )
            return plan
        except Exception as e:
            logger.error(f"Error creating learning plan: {e}")
            raise
    
    
    async def get_for_session(
        self,
        session_id: UUID
    ) -> List[LearningPlan]:
        """
        Get all learning plans for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of learning plans
        """
        try:
            stmt = (
                select(LearningPlan)
                .where(LearningPlan.session_id == session_id)
                .order_by(LearningPlan.gap_level.desc())
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting learning plans: {e}")
            raise
    
    
    async def get_for_skill(
        self,
        session_id: UUID,
        skill: str
    ) -> Optional[LearningPlan]:
        """
        Get learning plan for specific skill in session.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            
        Returns:
            Learning plan or None
        """
        try:
            stmt = (
                select(LearningPlan)
                .where(
                    (LearningPlan.session_id == session_id) &
                    (LearningPlan.skill == skill)
                )
            )
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting learning plan for skill: {e}")
            raise
    
    
    async def update_recommendations(
        self,
        session_id: UUID,
        skill: str,
        recommended_actions: List[str],
        estimated_hours: Optional[int] = None
    ) -> Optional[LearningPlan]:
        """
        Update learning plan recommendations.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            recommended_actions: New recommendations
            estimated_hours: New estimate (optional)
            
        Returns:
            Updated plan or None
        """
        try:
            plan = await self.get_for_skill(session_id, skill)
            if not plan:
                return None
            
            updates = {'recommended_actions': recommended_actions}
            if estimated_hours is not None:
                updates['estimated_hours'] = estimated_hours
            
            updated = await self.update(plan.id, **updates)
            logger.debug(
                f"✅ Updated learning plan: skill={skill}, "
                f"actions={len(recommended_actions)}"
            )
            return updated
        except Exception as e:
            logger.error(f"Error updating learning plan: {e}")
            raise
    
    
    async def get_all_high_priority_plans(
        self,
        session_id: UUID,
        min_gap_level: int = 2
    ) -> List[LearningPlan]:
        """
        Get high-priority learning plans (larger gaps).
        
        Args:
            session_id: Session UUID
            min_gap_level: Minimum gap level to include
            
        Returns:
            List of high-priority plans
        """
        try:
            stmt = (
                select(LearningPlan)
                .where(
                    (LearningPlan.session_id == session_id) &
                    (LearningPlan.gap_level >= min_gap_level)
                )
                .order_by(LearningPlan.gap_level.desc())
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting high-priority plans: {e}")
            raise
