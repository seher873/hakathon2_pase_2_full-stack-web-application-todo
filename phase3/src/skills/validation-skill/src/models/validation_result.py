from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ValidationRule(BaseModel):
    """
    Defines a specific validation rule that can be applied to content.
    """

    rule_id: str = Field(
        ...,
        description="Unique identifier for this rule",
        example="security-rule-1"
    )
    name: str = Field(
        ...,
        description="Human-readable name for the rule",
        example="Security Policy Validation"
    )
    description: str = Field(
        ...,
        description="Explanation of what this rule validates",
        example="Validates that content does not contain potentially harmful actions"
    )
    rule_type: str = Field(
        ...,
        description="Category of validation ('security', 'format', 'business_logic', etc.)",
        example="security"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration parameters for this rule",
        example={"max_execution_time": 30000, "allowed_actions": ["validate_params", "create_record"]}
    )
    enabled: bool = Field(
        True,
        description="Whether this rule is currently active"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When the rule was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="When the rule was last modified"
    )

    class Config:
        # Validation Rule: rule_id must be unique across all rules
        # This will be validated at the service level

        # Validation Rule: rule_type must be a recognized validation category
        # This will be validated in the service implementation

        # Validation Rule: enabled defaults to true
        # Handled by the default value in the field definition
        pass


class ValidationDetail(BaseModel):
    """
    Represents the result of applying a single validation rule.
    """
    
    rule_name: str = Field(
        ..., 
        description="Name of the validation rule applied",
        example="security_policy_check"
    )
    passed: bool = Field(
        ..., 
        description="Whether this validation rule passed",
        example=True
    )
    message: str = Field(
        ..., 
        description="Description of the validation result",
        example="Content passed security policy validation"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When this validation was performed"
    )
    severity: str = Field(
        "info",
        description="How critical this validation is",
        example="critical"
    )

    class Config:
        # Validation Rule: severity must be one of the predefined values
        # This would be enforced with a custom validator in practice
        pass


class ValidationResult(BaseModel):
    """
    Represents the output of the validation process.
    """
    
    request_id: str = Field(
        ..., 
        description="ID of the request this result corresponds to",
        example="req-1234567890"
    )
    is_valid: bool = Field(
        ..., 
        description="Whether the content passed all validation checks",
        example=True
    )
    validation_details: List[ValidationDetail] = Field(
        default_factory=list,
        description="Detailed results for each validation rule applied"
    )
    processed_at: datetime = Field(
        default_factory=datetime.now,
        description="When validation was completed"
    )
    execution_time_ms: int = Field(
        ...,
        description="Time taken to complete validation in milliseconds",
        example=150
    )
    security_check_passed: bool = Field(
        ...,
        description="Whether security validation passed",
        example=True
    )
    rejection_reasons: List[str] = Field(
        default_factory=list,
        description="If invalid, reasons why content was rejected",
        example=["Action 'execute_system_command' is not allowed"]
    )
    total_steps: int = Field(
        0,
        description="Total number of validation steps performed"
    )
    successful_steps: int = Field(
        0,
        description="Number of validation steps that passed"
    )
    failed_steps: int = Field(
        0,
        description="Number of validation steps that failed"
    )
    validation_errors: List[str] = Field(
        default_factory=list,
        description="Any errors encountered during validation process",
        example=[]
    )

    class Config:
        # Validation Rule: is_valid must be consistent with validation_details and rejection_reasons
        # This would be enforced with a custom validator in practice
        
        # Validation Rule: execution_time_ms must be positive
        # This would be validated with a custom validator
        
        # Validation Rule: If is_valid is false, rejection_reasons must not be empty
        # This would be enforced with a custom validator
        pass