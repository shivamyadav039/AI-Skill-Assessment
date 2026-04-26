"""
Base repository - Abstract base for all data access operations.

Provides common CRUD operations:
- Create
- Read (by ID, all)
- Update
- Delete
- Count
- Exists
"""

from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger

# Generic type for ORM models
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Generic repository for CRUD operations on any model.
    
    Usage:
        class UserRepository(BaseRepository[User]):
            pass
        
        repo = UserRepository(session, User)
        user = await repo.get(user_id)
    """
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        """
        Initialize repository.
        
        Args:
            session: AsyncSession for database operations
            model: SQLAlchemy model class
        """
        self.session = session
        self.model = model
    
    
    async def create(self, **kwargs) -> T:
        """
        Create and save a new record.
        
        Args:
            **kwargs: Model fields and values
            
        Returns:
            Created model instance
        """
        try:
            obj = self.model(**kwargs)
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            logger.debug(f"✅ Created {self.model.__name__}: {obj.id}")
            return obj
        except Exception as e:
            logger.error(f"❌ Error creating {self.model.__name__}: {e}")
            raise
    
    
    async def get(self, id: Any) -> Optional[T]:
        """
        Get record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"❌ Error getting {self.model.__name__}: {e}")
            raise
    
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"❌ Error getting all {self.model.__name__}: {e}")
            raise
    
    
    async def update(self, id: Any, **kwargs) -> Optional[T]:
        """
        Update a record.
        
        Args:
            id: Record ID
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            obj = await self.get(id)
            if not obj:
                return None
            
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            logger.debug(f"✅ Updated {self.model.__name__}: {id}")
            return obj
        except Exception as e:
            logger.error(f"❌ Error updating {self.model.__name__}: {e}")
            raise
    
    
    async def delete(self, id: Any) -> bool:
        """
        Delete a record.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            obj = await self.get(id)
            if not obj:
                return False
            
            await self.session.delete(obj)
            await self.session.flush()
            logger.debug(f"✅ Deleted {self.model.__name__}: {id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error deleting {self.model.__name__}: {e}")
            raise
    
    
    async def count(self) -> int:
        """
        Count total records.
        
        Returns:
            Total record count
        """
        try:
            stmt = select(func.count(self.model.id))
            result = await self.session.execute(stmt)
            return result.scalar() or 0
        except Exception as e:
            logger.error(f"❌ Error counting {self.model.__name__}: {e}")
            raise
    
    
    async def exists(self, **kwargs) -> bool:
        """
        Check if record exists with given criteria.
        
        Args:
            **kwargs: Filter criteria (field=value pairs)
            
        Returns:
            True if record exists, False otherwise
        """
        try:
            stmt = select(self.model)
            for key, value in kwargs.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
            
            result = await self.session.execute(stmt)
            return result.scalars().first() is not None
        except Exception as e:
            logger.error(f"❌ Error checking existence in {self.model.__name__}: {e}")
            raise
