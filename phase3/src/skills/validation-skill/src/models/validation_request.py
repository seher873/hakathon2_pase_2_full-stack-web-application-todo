from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ValidationRequest(BaseModel):
    """
    Represents the input to the validation skill containing content to validate.
    """

    request_id: str = Field(
        ...,
        description="Unique identifier for the validation request",
        example="req-1234567890"
    )
    content: Any = Field(
        ...,
        description="The content to be validated (can be any JSON-serializable object)",
        example={"intent_type": "create_task", "parameters": {"title": "Sample Task"}}
    )
    content_type: str = Field(
        ...,
        description="The type/format of the content being validated",
        example="task_plan"
    )
    validation_rules: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific validation rules to apply (defaults to all rules if not specified)",
        example=["security", "format", "business_logic"]
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the request was made"
    )
    source: Optional[str] = Field(
        None,
        description="The source of the content being validated",
        example="task_planning_skill"
    )

    class Config:
        # Validation Rule: content must be present
        # This is handled by not setting default value for content field

        # Validation Rule: request_id must be unique for the system
        # This will be validated at the service level

        # Validation Rule: content_type must be a recognized content type
        # This will be validated in the service implementation
        pass