"""
User Repository - Data access for User model.

Provides:
- Get user by email
- Create new user
- List all users
- User existence checks
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from ..models import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository for database operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize with User model."""
        super().__init__(session, User)
    
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email
            
        Returns:
            User instance or None
        """
        try:
            stmt = select(User).where(User.email == email.lower())
            result = await self.session.execute(stmt)
            user = result.scalars().first()
            logger.debug(f"Found user by email: {email}")
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            raise
    
    
    async def create_user(self, email: str, name: str) -> User:
        """
        Create new user.
        
        Args:
            email: User email (unique)
            name: User's full name
            
        Returns:
            Created user
            
        Raises:
            ValueError: If email already exists
        """
        try:
            # Check if email exists
            if await self.get_by_email(email):
                raise ValueError(f"User with email {email} already exists")
            
            user = await self.create(
                email=email.lower(),
                name=name
            )
            logger.info(f"✅ Created user: {email}")
            return user
        except ValueError as e:
            logger.warning(f"Validation error creating user: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    
    async def get_or_create_user(self, email: str, name: str) -> User:
        """
        Get existing user or create new one.
        
        Args:
            email: User email
            name: User name
            
        Returns:
            Existing or newly created user
        """
        user = await self.get_by_email(email)
        if user:
            logger.debug(f"Using existing user: {email}")
            return user
        
        return await self.create_user(email, name)
