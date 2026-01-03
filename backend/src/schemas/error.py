"""
Error response schemas for API endpoints.

Defines Pydantic models for standardized error responses
across all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ErrorDetails(BaseModel):
    """Additional error details (e.g., validation errors)."""

    field: Optional[str] = Field(None, description="Field name if validation error")
    message: Optional[str] = Field(None, description="Detailed error message")
    value: Optional[Any] = Field(None, description="Value that caused the error")


class ErrorResponse(BaseModel):
    """Standard error response format for all API errors."""

    status: str = Field("error", description="Response status (always 'error')")
    code: str = Field(..., description="Error code (e.g., BAD_REQUEST, UNAUTHORIZED)")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details (e.g., validation errors by field)",
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp when error occurred",
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "status": "error",
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": {
                    "title": "Title is required",
                    "email": "Invalid email format",
                },
                "timestamp": "2026-01-03T12:00:00Z",
            }
        }


class BadRequestError(ErrorResponse):
    """400 Bad Request error response."""

    code: str = Field("BAD_REQUEST", description="Error code")


class UnauthorizedError(ErrorResponse):
    """401 Unauthorized error response."""

    code: str = Field("UNAUTHORIZED", description="Error code")


class ForbiddenError(ErrorResponse):
    """403 Forbidden error response."""

    code: str = Field("FORBIDDEN", description="Error code")


class NotFoundError(ErrorResponse):
    """404 Not Found error response."""

    code: str = Field("NOT_FOUND", description="Error code")


class ConflictError(ErrorResponse):
    """409 Conflict error response."""

    code: str = Field("CONFLICT", description="Error code")


class ValidationError(ErrorResponse):
    """422 Validation Error response."""

    code: str = Field("VALIDATION_ERROR", description="Error code")
    details: Dict[str, str] = Field(..., description="Validation errors by field")


class InternalServerError(ErrorResponse):
    """500 Internal Server Error response."""

    code: str = Field("INTERNAL_SERVER_ERROR", description="Error code")


# Error code constants
ERROR_CODES = {
    "BAD_REQUEST": "400",
    "UNAUTHORIZED": "401",
    "FORBIDDEN": "403",
    "NOT_FOUND": "404",
    "CONFLICT": "409",
    "VALIDATION_ERROR": "422",
    "INTERNAL_SERVER_ERROR": "500",
}

# Error messages
ERROR_MESSAGES = {
    "BAD_REQUEST": "The request contains invalid data",
    "UNAUTHORIZED": "Authentication required or token invalid",
    "FORBIDDEN": "You do not have permission to access this resource",
    "NOT_FOUND": "The requested resource was not found",
    "CONFLICT": "The request conflicts with existing data",
    "VALIDATION_ERROR": "The request data failed validation",
    "INTERNAL_SERVER_ERROR": "An unexpected error occurred on the server",
    "MISSING_TITLE": "Task title is required",
    "INVALID_EMAIL": "Invalid email format",
    "WEAK_PASSWORD": "Password must be at least 8 characters",
    "DUPLICATE_EMAIL": "Email is already registered",
    "INVALID_CREDENTIALS": "Invalid email or password",
}
