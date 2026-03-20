from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class Todo(SQLModel, table=True):
    """Todo task model with intermediate features."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="default-user", nullable=False, index=True)
    title: str = Field(nullable=False, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    url: Optional[str] = Field(default=None)
    priority: str = Field(default="medium", max_length=10)  # low, medium, high
    tags: Optional[str] = Field(default=None, max_length=500)  # Stored as comma-separated string
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def get_tags_list(self) -> List[str]:
        """Convert comma-separated tags string to list."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def set_tags_list(self, tags: List[str]):
        """Convert tags list to comma-separated string."""
        if not tags:
            self.tags = None
        else:
            self.tags = ",".join([tag.strip() for tag in tags if tag.strip()])


class Conversation(SQLModel, table=True):
    """Chat conversation model for Phase 3 chatbot."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="default-user", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Chat message model for Phase 3 chatbot."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="default-user", nullable=False, index=True)
    conversation_id: str = Field(foreign_key="conversation.id", nullable=False, index=True)
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False, max_length=4000)
    created_at: datetime = Field(default_factory=datetime.utcnow)