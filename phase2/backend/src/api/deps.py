"""
Dependency injection functions for FastAPI endpoints.

Provides JWT verification, database session access, and
user context extraction for protected routes.
"""

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from src.config import settings
from src.db import get_async_session


async def get_current_user_id(
    authorization: Optional[str] = Header(None),
) -> UUID:
    """
    Extract and verify user ID from JWT token in Authorization header.

    Expected header format: Authorization: Bearer {token}

    Returns:
        UUID: User ID from JWT payload

    Raises:
        HTTPException 401: If token is missing, invalid, or expired
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Parse "Bearer {token}" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]

    try:
        # Verify JWT signature and decode
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        # Extract user_id from token payload
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: invalid user_id format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_user_access(
    user_id_param: UUID,
    user_id_token: UUID = Depends(get_current_user_id),
) -> UUID:
    """
    Verify that authenticated user can access the requested user's data.

    Compares user_id in URL path with user_id from JWT token.
    If they don't match, returns 403 Forbidden.

    Args:
        user_id_param: User ID from URL path
        user_id_token: User ID from JWT token

    Returns:
        UUID: Verified user ID

    Raises:
        HTTPException 403: If user_id doesn't match token
    """
    if user_id_param != user_id_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return user_id_token


def get_db_session():
    """
    Get database session for dependency injection.

    Usage in FastAPI routes:
        @app.get("/tasks")
        async def get_tasks(session: AsyncSession = Depends(get_db_session)):
            ...
    """
    return Depends(get_async_session)
