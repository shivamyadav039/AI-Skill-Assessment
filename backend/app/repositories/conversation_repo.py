"""
Conversation History Repository - Data access for ConversationHistory model.

Provides:
- Save conversation turns
- Get conversation for session/skill
- List all conversations
- Track response quality progression
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import ConversationHistory
from .base import BaseRepository


class ConversationRepository(BaseRepository[ConversationHistory]):
    """Conversation history repository for database operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize with ConversationHistory model."""
        super().__init__(session, ConversationHistory)
    
    
    async def save_conversation(
        self,
        session_id: UUID,
        skill: str,
        turn_count: int,
        question: str,
        response: str,
        response_quality: float = 0.5
    ) -> ConversationHistory:
        """
        Save a conversation turn.
        
        Args:
            session_id: Session UUID
            skill: Skill being discussed
            turn_count: Question number (1-indexed)
            question: Question asked
            response: Candidate's response
            response_quality: Quality score (0-1)
            
        Returns:
            Created conversation record
        """
        try:
            conversation = await self.create(
                session_id=session_id,
                skill=skill,
                turn_count=turn_count,
                question=question,
                response=response,
                response_quality=response_quality
            )
            logger.info(
                f"✅ Saved conversation: session={session_id}, skill={skill}, turn={turn_count}"
            )
            return conversation
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            raise
    
    
    async def get_for_session_skill(
        self,
        session_id: UUID,
        skill: str
    ) -> List[ConversationHistory]:
        """
        Get all conversations for a session and skill.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            
        Returns:
            List of conversations
        """
        try:
            stmt = (
                select(ConversationHistory)
                .where(
                    (ConversationHistory.session_id == session_id) &
                    (ConversationHistory.skill == skill)
                )
                .order_by(ConversationHistory.turn_count)
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting conversations: {e}")
            raise
    
    
    async def get_all_for_session(
        self,
        session_id: UUID
    ) -> List[ConversationHistory]:
        """
        Get all conversations for a session.
        
        Args:
            session_id: Session UUID
            
        Returns:
            List of conversations
        """
        try:
            stmt = (
                select(ConversationHistory)
                .where(ConversationHistory.session_id == session_id)
                .order_by(
                    ConversationHistory.skill,
                    ConversationHistory.turn_count
                )
            )
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting session conversations: {e}")
            raise
    
    
    async def get_latest_turns(
        self,
        session_id: UUID,
        skill: str,
        limit: int = 5
    ) -> List[ConversationHistory]:
        """
        Get latest conversation turns for a skill.
        
        Args:
            session_id: Session UUID
            skill: Skill name
            limit: Number of turns to return
            
        Returns:
            List of latest conversations
        """
        try:
            stmt = (
                select(ConversationHistory)
                .where(
                    (ConversationHistory.session_id == session_id) &
                    (ConversationHistory.skill == skill)
                )
                .order_by(ConversationHistory.turn_count.desc())
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            conversations = list(result.scalars().all())
            # Return in chronological order
            return conversations[::-1]
        except Exception as e:
            logger.error(f"Error getting latest turns: {e}")
            raise
