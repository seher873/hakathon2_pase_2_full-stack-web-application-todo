"""
Authentication endpoints for user signup and login.

Provides:
- POST /auth/signup - Create new user account
- POST /auth/login - Authenticate user and issue JWT (via Better Auth)
"""

from datetime import datetime, timedelta
from uuid import UUID
import jwt
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db import get_async_session
from src.schemas.auth import SignupRequest, AuthResponse, LoginRequest
from src.schemas.error import ERROR_MESSAGES
from src.models.user import UserCreate, UserResponse
from src.services.user_service import UserService
from src.middleware import SuccessResponse

# Create router for auth endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User Signup",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Validation error (invalid email, weak password)"},
        409: {"description": "Email already registered"},
        500: {"description": "Server error"},
    },
)
async def signup(
    request: SignupRequest,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Create new user account.

    Validates email and password, creates user record,
    and issues JWT token.

    Request Body:
    - email: Email address (must be unique)
    - password: Password (minimum 8 characters)
    - password_confirm: Password confirmation

    Returns:
    - token: JWT access token
    - user: User information
    - timestamp: Response timestamp

    Error Codes:
    - 400: Invalid email format, weak password, or passwords don't match
    - 409: Email already registered
    - 500: Server error

    Example:
    ```
    POST /api/auth/signup
    Content-Type: application/json

    {
        "email": "user@example.com",
        "password": "SecurePassword123!",
        "password_confirm": "SecurePassword123!"
    }

    Response (201):
    {
        "status": "success",
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-03T12:00:00Z"
            }
        },
        "timestamp": "2026-01-03T12:00:00Z"
    }
    ```
    """
    # Create user (validates email, password, and checks duplicates)
    user_data = UserCreate(
        email=request.email,
        password=request.password,
        password_confirm=request.password_confirm,
    )
    new_user = await UserService.create_user(session, user_data)

    # Generate JWT token
    payload = {
        "sub": str(new_user.id),  # Subject (user ID)
        "email": new_user.email,
        "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours),
        "iat": datetime.utcnow(),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    # Prepare response
    response = SuccessResponse(
        data={
            "token": token,
            "user": {
                "id": str(new_user.id),
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat(),
            },
        }
    )

    return response.to_dict()


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    responses={
        200: {"description": "User logged in successfully"},
        400: {"description": "Invalid credentials"},
        401: {"description": "Authentication failed"},
        500: {"description": "Server error"},
    },
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Authenticate user and issue JWT token.

    Note: In Phase II, login is handled by Better Auth on the frontend.
    This endpoint is a placeholder for backend verification if needed.

    Typical flow:
    1. Frontend authenticates user via Better Auth
    2. Better Auth returns JWT token
    3. Frontend sends token in Authorization header for all requests
    4. Backend verifies JWT in middleware

    Request Body:
    - email: Email address
    - password: Password

    Returns:
    - token: JWT access token
    - user: User information
    - timestamp: Response timestamp

    Error Codes:
    - 400: Invalid credentials
    - 401: Authentication failed
    - 500: Server error
    """
    # Look up user by email
    user = await UserService.get_user_by_email(session, request.email)

    if not user:
        # User not found
        raise {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": ERROR_MESSAGES.get("INVALID_CREDENTIALS", "Invalid credentials"),
        }

    # In production, verify password hash here
    # For now, this is a placeholder since Better Auth handles passwords

    # Generate JWT token
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours),
        "iat": datetime.utcnow(),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    # Prepare response
    response = SuccessResponse(
        data={
            "token": token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "created_at": user.created_at.isoformat(),
            },
        }
    )

    return response.to_dict()
