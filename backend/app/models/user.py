"""
User model - Represents platform users/candidates.

Fields:
- id: Unique identifier (UUID)
- email: User email (unique)
- name: User's full name
- created_at: Account creation timestamp
- updated_at: Last profile update
"""

from sqlalchemy import Column, String, UniqueConstraint, Index
from .base import BaseModel


class User(BaseModel):
    """User/candidate account model."""
    
    __tablename__ = "users"
    
    # Unique email for login
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    # User's full name
    name = Column(String(255), nullable=False)
    
    # Relationship to sessions (one user -> many sessions)
    # Defined in session.py to avoid circular imports
    
    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
        Index('idx_users_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
