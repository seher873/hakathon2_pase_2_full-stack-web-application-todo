"""
User model for authentication and profile management.

Note: User accounts are managed by Better Auth on the frontend,
but the backend tracks user_id to scope task ownership.
"""

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from .base import BaseModel

if TYPE_CHECKING:
    from .task import Task


class UserBase(SQLModel):
    """Base user fields shared between database and API models."""

    email: str = Field(
        index=True,
        unique=True,
        max_length=255,
        description="User email address (unique)",
    )


class User(BaseModel, table=True):
    """
    User database model.

    Represents a registered user. The user is created when they
    sign up via Better Auth on the frontend, and the backend
    stores their email to validate task ownership.

    Fields:
    - id: UUID (primary key, from parent BaseModel)
    - email: str (unique, indexed)
    - password_hash: str (hashed password)
    - created_at: datetime (from parent BaseModel)
    - updated_at: datetime (from parent BaseModel)
    """

    __tablename__ = "users"

    # Email index for fast lookups
    # Index automatically created by Field(index=True)

    # Email field
    email: str = Field(
        index=True,
        unique=True,
        max_length=255,
        description="User email address (unique)",
    )

    # Password hash field
    password_hash: str = Field(
        max_length=255,
        description="Hashed password",
    )

    # Relationship to tasks - using string reference to avoid circular import
    tasks: List["Task"] = Relationship(
        back_populates="user"
    )


class UserCreate(SQLModel):
    """
    Schema for user creation (signup request).

    Used when frontend sends signup request with email and password.
    Password is NOT stored in our database - Better Auth handles it.
    """

    email: str = Field(
        index=True,
        unique=True,
        max_length=255,
        description="User email address (unique)",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password (min 8 characters)",
    )
    password_confirm: str = Field(
        min_length=8,
        max_length=128,
        description="Password confirmation",
    )


class UserResponse(SQLModel):
    """
    Schema for user in API responses.

    Returned after successful signup/login.
    Does NOT include sensitive information.
    """

    id: UUID = Field(description="User ID")
    email: str = Field(
        description="User email address",
    )
    created_at: datetime = Field(description="Account creation timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Support ORM mode


# UserInDB is not needed anymore since User already serves as the database model
# We can just use User directly where UserInDB was referenced
