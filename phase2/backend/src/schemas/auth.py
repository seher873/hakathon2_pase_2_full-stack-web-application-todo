"""
Authentication request/response schemas.

Defines Pydantic models for signup and login operations
with validation rules.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class SignupRequest(BaseModel):
    """
    Signup request payload.

    Fields:
    - email: Email address (validated format)
    - password: Password (min 8 characters)
    - password_confirm: Password confirmation for validation
    """

    email: EmailStr = Field(
        ...,
        description="Email address",
        max_length=255,
    )
    password: str = Field(
        ...,
        description="Password (min 8 characters)",
        min_length=8,
        max_length=128,
    )
    password_confirm: str = Field(
        ...,
        description="Password confirmation",
        min_length=8,
        max_length=128,
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!",
                "password_confirm": "SecurePassword123!",
            }
        }


class LoginRequest(BaseModel):
    """
    Login request payload.

    Fields:
    - email: Email address
    - password: Password
    """

    email: EmailStr = Field(
        ...,
        description="Email address",
        max_length=255,
    )
    password: str = Field(
        ...,
        description="Password",
        min_length=8,
        max_length=128,
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!",
            }
        }


class UserData(BaseModel):
    """User information in auth response."""

    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class AuthResponse(BaseModel):
    """
    Successful authentication response.

    Contains JWT token and user information.
    """

    status: str = Field("success", description="Response status")
    data: dict = Field(
        ...,
        description="Response data with token and user",
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp",
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "email": "user@example.com",
                        "created_at": "2026-01-03T12:00:00Z",
                    },
                },
                "timestamp": "2026-01-03T12:00:00Z",
            }
        }


class TokenResponse(BaseModel):
    """JWT token in response."""

    token: str = Field(
        ...,
        description="JWT access token",
    )
    token_type: str = Field(
        "bearer",
        description="Token type (always 'bearer')",
    )
    expires_in: int = Field(
        ...,
        description="Token expiration time in seconds",
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
            }
        }
