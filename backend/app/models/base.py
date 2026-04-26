"""
Base model with common fields and utilities.

All domain models inherit from this base to ensure consistency in:
- UUID primary keys
- Timestamps (created_at, updated_at)
- Soft deletes (if needed)
- JSON serialization
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

# Create declarative base for all models
Base = declarative_base()


class BaseModel(Base):
    """
    Abstract base model for all domain models.
    
    Provides:
    - UUID primary key
    - created_at timestamp
    - updated_at timestamp for all records
    """
    
    __abstract__ = True
    
    # UUID primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in ['created_at', 'updated_at']
        }
    
    def __repr__(self) -> str:
        """String representation of model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
