"""Authentication wrapper for MCP tools to ensure proper JWT token forwarding."""
import os
import jwt
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Security scheme for JWT
security = HTTPBearer()

class AuthValidationResult(BaseModel):
    """Result of authentication validation."""
    user_id: str
    is_valid: bool
    error_message: Optional[str] = None

def get_jwt_secret():
    """Get JWT secret from environment variables."""
    return os.getenv("JWT_SECRET_KEY", "default_secret_key_for_development")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify JWT token and return user ID.

    Args:
        credentials: HTTP authorization credentials containing the token

    Returns:
        str: User ID from the token

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode the JWT token
        payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def validate_jwt_for_mcp_tools(token: str) -> AuthValidationResult:
    """
    Validate JWT token specifically for MCP tools usage.

    Args:
        token: JWT token to validate

    Returns:
        AuthValidationResult: Contains user ID and validation status
    """
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
        user_id = payload.get("sub")

        if user_id is None:
            return AuthValidationResult(
                user_id="",
                is_valid=False,
                error_message="Invalid token: no user ID found"
            )

        return AuthValidationResult(
            user_id=user_id,
            is_valid=True
        )
    except jwt.ExpiredSignatureError:
        return AuthValidationResult(
            user_id="",
            is_valid=False,
            error_message="Token has expired"
        )
    except jwt.JWTError as e:
        return AuthValidationResult(
            user_id="",
            is_valid=False,
            error_message=f"JWT validation error: {str(e)}"
        )

def forward_token_to_mcp_tools(original_token: str) -> str:
    """
    Prepare token for forwarding to MCP tools.
    This can include any necessary transformations or validation.

    Args:
        original_token: The original JWT token from the request

    Returns:
        str: Token ready for MCP tools
    """
    # Validate the token before forwarding
    result = validate_jwt_for_mcp_tools(original_token)

    if not result.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.error_message
        )

    # For now, we just return the original token
    # In the future, we might need to add additional claims or transform the token
    return original_token