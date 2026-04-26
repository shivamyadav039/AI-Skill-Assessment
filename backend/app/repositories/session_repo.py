"""
Session Repository - Data access for Session model.

Provides:
- Create assessment session
- Get session by ID
- List sessions for user
- Update session status
- Get active sessions
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import Session, User
from .base import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """Session repository for database operations."""
    
    def __init__(self, session_db: AsyncSession):
        """Initialize with Session model."""
        super().__init__(session_db, Session)
    
    
    async def create_session(
        self,
        user_id: UUID,
        skill_assessed: str,
        status: str = "active"
    ) -> Session:
        """
        Create new assessment session.
        
        Args:
            user_id: User UUID
            skill_assessed: Skill being assessed
            status: Session status (default: active)
            
        Returns:
            Created session
        """
        try:
            session = await self.create(
                user_id=user_id,
                skill_assessed=skill_assessed,
                status=status
            )
            logger.info(f"✅ Created session for skill: {skill_assessed}")
            return session
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    
    async def get_sessions_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Session]:
        """
        Get all sessions for a user.
        
        Args:
            user_id: User UUID
            skip: Pagination offset
            limit: Pagination limit
            
        Returns:
            List of user's sessions
        """
        try:
            stmt = (
                select(Session)
                .where(Session.user_id == user_id)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            raise
    
    
    async def get_active_sessions(
        self,
        user_id: UUID
    ) -> List[Session]:
        """
        Get active (non-completed) sessions for user.
        
        Args:
            user_id: User UUID
            
        Returns:
            List of active sessions
        """
        try:
            stmt = (
                select(Session)
                .where(
                    (Session.user_id == user_id) &
                    (Session.status == "active")
                )
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting active sessions: {e}")
            raise
    
    
    async def complete_session(self, session_id: UUID) -> Session:
        """
        Mark session as completed.
        
        Args:
            session_id: Session UUID
            
        Returns:
            Updated session
        """
        try:
            session = await self.update(session_id, status="completed")
            logger.info(f"✅ Completed session: {session_id}")
            return session
        except Exception as e:
            logger.error(f"Error completing session: {e}")
            raise
