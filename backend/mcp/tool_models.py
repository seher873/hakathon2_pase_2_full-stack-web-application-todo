"""Pydantic models for MCP tool parameters."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreateModel(BaseModel):
    """Model for creating a new task."""
    title: str = Field(..., description="The title of the task", min_length=1)
    description: Optional[str] = Field(None, description="Optional description of the task")
    due_date: Optional[str] = Field(None, description="Optional due date in YYYY-MM-DD format")

    class Config:
        schema_extra = {
            "example": {
                "title": "Submit report",
                "description": "Submit the monthly report to the manager",
                "due_date": "2024-12-31"
            }
        }

class TaskUpdateModel(BaseModel):
    """Model for updating an existing task."""
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    due_date: Optional[str] = Field(None, description="New due date in YYYY-MM-DD format")
    status: Optional[str] = Field(None, description="New status for the task", pattern="^(pending|completed)$")

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated task title",
                "status": "completed"
            }
        }

class TaskToggleModel(BaseModel):
    """Model for toggling task completion status."""
    task_id: int = Field(..., description="ID of the task to toggle", gt=0)

    class Config:
        schema_extra = {
            "example": {
                "task_id": 1
            }
        }

class ChatMessageModel(BaseModel):
    """Model for chat messages."""
    message: str = Field(..., description="The user's message", min_length=1)
    user_id: str = Field(..., description="ID of the user sending the message")

    class Config:
        schema_extra = {
            "example": {
                "message": "Add a task to submit report tomorrow",
                "user_id": "user123"
            }
        }

class ChatResponseModel(BaseModel):
    """Model for chat responses."""
    response: str = Field(..., description="The agent's response to the user")
    success: bool = Field(True, description="Whether the operation was successful")
    data: Optional[dict] = Field(None, description="Additional data related to the response")

    class Config:
        schema_extra = {
            "example": {
                "response": "Task 'Submit report' created successfully",
                "success": True,
                "data": {
                    "task_id": 1,
                    "title": "Submit report",
                    "status": "pending"
                }
            }
        }