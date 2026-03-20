from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Literal, Union
from datetime import datetime

# ============================================================================
# Enums and Constants
# ============================================================================

# Priority literal type for Pydantic
PriorityType = Literal["low", "medium", "high"]

# ============================================================================
# Todo Schemas
# ============================================================================

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title (required)")
    description: Optional[str] = Field(default=None, max_length=1000, description="Optional task description")
    completed: bool = False
    url: Optional[str] = Field(default=None, description="Optional URL associated with the task")
    priority: PriorityType = Field(default="medium", description="Task priority level")
    tags: str = Field(default="", max_length=500, description="Comma-separated tags")
    due_date: Optional[datetime] = Field(default=None, description="Optional due date for the task")

class TodoCreate(TodoBase):
    user_id: Optional[str] = Field(default="default-user", description="User ID (will be overridden by auth)")

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    url: Optional[str] = Field(default=None)
    priority: Optional[PriorityType] = None
    tags: Optional[List[str]] = Field(default=None)
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    url: Optional[str] = None
    priority: PriorityType
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, value):
        """Convert comma-separated tags string to list."""
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [tag.strip() for tag in value.split(",") if tag.strip()]
        return value

class TodoListResponse(BaseModel):
    tasks: List[TodoResponse]
    total: int
    skip: int
    limit: int
