from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class RejectionReason(BaseModel):
    """
    Specifies why content was rejected during validation.
    """

    reason_code: str = Field(
        ...,
        description="Machine-readable code for the rejection reason",
        example="ACTION_NOT_ALLOWED"
    )
    description: str = Field(
        ...,
        description="Human-readable explanation of the rejection",
        example="The action 'execute_system_command' is not allowed by security policy"
    )
    severity: str = Field(
        ...,
        description="How serious this issue is",
        example="critical"
    )
    applied_rules: List[str] = Field(
        default_factory=list,
        description="Which validation rules led to this rejection",
        example=["security_policy_check", "whitelist_validation"]
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the rejection was determined"
    )

    class Config:
        # Validation Rule: severity must be one of the predefined values (low, medium, high, critical)
        # This would be enforced with a custom validator in practice

        # Validation Rule: reason_code must be unique for the system
        # This will be validated at the service level
        pass