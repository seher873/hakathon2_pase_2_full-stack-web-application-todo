"""
Task model definition.

Defines the Task entity with all required fields and relationships.
"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from uuid import UUID
from datetime import datetime

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User


class Task(BaseModel, table=True):
    """
    Task model representing a user's task.

    Attributes:
        title (str): Task title (required)
        description (str): Task description (optional)
        completed (bool): Task completion status (default: False)
        user_id (UUID): Foreign key linking to the user who owns the task
        user (User): Relationship to the user who owns the task
    """

    __tablename__ = "tasks"

    title: str = Field(
        sa_column_kwargs={"nullable": False},
        description="Task title",
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = Field(
        sa_column_kwargs={"nullable": True},
        description="Task description (optional)",
        max_length=1000,
    )
    completed: bool = Field(
        default=False,
        sa_column_kwargs={"nullable": False},
        description="Task completion status",
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        sa_column_kwargs={"nullable": False},
        description="ID of the user who owns this task",
    )

    # Relationship to User - using string reference to avoid circular import
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Used for validating incoming task creation requests.
    """

    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required, 1-255 characters)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, up to 1000 characters)",
    )


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Used for validating incoming task update requests.
    All fields are optional to allow partial updates.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Task title (1-255 characters, optional)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (up to 1000 characters, optional)",
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Task completion status (optional)",
    )


class TaskResponse(BaseModel):
    """
    Schema for task responses.

    Used for serializing task data in API responses.
    """

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Support ORM mode