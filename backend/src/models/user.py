"""
User model for authentication and profile management.

Note: User accounts are managed by Better Auth on the frontend,
but the backend tracks user_id to scope task ownership.
"""

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING, List

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


class User(BaseModel, UserBase, table=True):
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

    # Password hash field
    password_hash: str = Field(
        max_length=255,
        description="Hashed password",
    )

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Schema for user creation (signup request).

    Used when frontend sends signup request with email and password.
    Password is NOT stored in our database - Better Auth handles it.
    """

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


class UserResponse(UserBase):
    """
    Schema for user in API responses.

    Returned after successful signup/login.
    Does NOT include sensitive information.
    """

    id: UUID = Field(description="User ID")
    created_at: datetime = Field(description="Account creation timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Support ORM mode


class UserInDB(User):
    """
    User model as stored in database.

    Used internally by services - not exposed in API responses.
    """

    pass
