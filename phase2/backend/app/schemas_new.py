"""Fresh schemas file for Todo API."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime

PriorityType = Literal["low", "medium", "high"]

class TodoCreate(BaseModel):
    """Schema for creating a todo."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    url: Optional[str] = None
    priority: PriorityType = "medium"
    tags: str = Field(default="", max_length=500)  # Comma-separated tags
    due_date: Optional[datetime] = None
    user_id: Optional[str] = "default-user"

class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    url: Optional[str] = None
    priority: Optional[PriorityType] = None
    tags: Optional[str] = Field(default=None, max_length=500)
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    """Schema for todo response."""
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    url: Optional[str] = None
    priority: PriorityType
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
