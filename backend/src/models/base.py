"""
Base model for all SQLModel entities.

Provides common fields (id, created_at, updated_at) and
configuration for all database models.
"""

from datetime import datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from typing import Optional


class BaseModel(SQLModel):
    """
    Base class for all database models.

    Includes:
    - id: UUID primary key
    - created_at: Timestamp when record was created
    - updated_at: Timestamp when record was last modified
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    """Unique identifier for the record"""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    """Timestamp when record was created"""

    updated_at: datetime = Field(default_factory=datetime.utcnow)
    """Timestamp when record was last modified"""

    class Config:
        """SQLModel configuration."""

        # Allow population by field name in addition to alias
        populate_by_name = True
        # Use enum values instead of names
        use_enum_values = True
