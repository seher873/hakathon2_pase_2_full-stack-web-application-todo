"""
Task API schemas for request/response validation.

Defines the data structures for task-related API endpoints.
"""

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new task.

    Used to validate incoming task creation requests.
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

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, fruits",
            }
        }


class TaskUpdateRequest(BaseModel):
    """
    Schema for updating an existing task.

    Used to validate incoming task update requests.
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

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "title": "Updated task title",
                "completed": True,
            }
        }


class TaskResponse(BaseModel):
    """
    Schema for single task response.

    Used to serialize task data in API responses.
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

        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, fruits",
                "completed": False,
                "user_id": "550e8400-e29b-41d4-a716-446655440001",
                "created_at": "2026-01-03T12:00:00Z",
                "updated_at": "2026-01-03T12:00:00Z",
            }
        }


class TaskListResponse(BaseModel):
    """
    Schema for task list response.

    Used to serialize multiple task data in API responses.
    """

    tasks: List[TaskResponse]
    total: int

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread, fruits",
                        "completed": False,
                        "user_id": "550e8400-e29b-41d4-a716-446655440001",
                        "created_at": "2026-01-03T12:00:00Z",
                        "updated_at": "2026-01-03T12:00:00Z",
                    }
                ],
                "total": 1,
            }
        }


class TaskFilterParams(BaseModel):
    """
    Schema for task filtering parameters.

    Used to validate query parameters for task filtering.
    """

    completed: Optional[bool] = Field(
        default=None,
        description="Filter by completion status (true/false, omit for all)",
    )
    search: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Search term for title or description (optional)",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of tasks to return (1-1000)",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of tasks to skip",
    )