"""
User service for signup and user management operations.

Handles:
- User creation
- Email validation
- Password validation
- Duplicate user detection
"""

import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlmodel import Session
from fastapi import HTTPException, status

from src.models.user import User, UserCreate, UserResponse


class UserService:
    """Service for user management operations."""

    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            True if valid email format

        Raises:
            HTTPException 400 if invalid email
        """
        if not email or len(email) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email must be between 1 and 255 characters",
            )

        if not UserService.EMAIL_PATTERN.match(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format",
            )

        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password strength.

        Requirements:
        - Minimum 8 characters
        - Maximum 128 characters
        - No additional complexity requirements for MVP

        Args:
            password: Password to validate

        Returns:
            True if valid password

        Raises:
            HTTPException 400 if invalid password
        """
        if not password or len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters",
            )

        if len(password) > 128:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must not exceed 128 characters",
            )

        return True

    @staticmethod
    def validate_password_match(password: str, password_confirm: str) -> bool:
        """
        Validate that password and confirmation match.

        Args:
            password: First password
            password_confirm: Confirmation password

        Returns:
            True if they match

        Raises:
            HTTPException 400 if they don't match
        """
        if password != password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match",
            )

        return True

    @staticmethod
    async def user_exists(
        session: AsyncSession,
        email: str,
    ) -> bool:
        """
        Check if user with email already exists.

        Args:
            session: Database session
            email: Email to check

        Returns:
            True if user exists

        Raises:
            HTTPException 409 if user already exists
        """
        # Query for existing user
        stmt = select(User).where(User.email == email.lower())
        result = await session.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        return False

    @staticmethod
    async def create_user(
        session: AsyncSession,
        user_data: UserCreate,
    ) -> UserResponse:
        """
        Create new user account.

        Validates email and password, checks for duplicates,
        and creates user record.

        Args:
            session: Database session
            user_data: User creation data (email, password, password_confirm)

        Returns:
            Created user as UserResponse

        Raises:
            HTTPException 400 for validation errors
            HTTPException 409 if email already registered
        """
        # Validate inputs
        UserService.validate_email(user_data.email)
        UserService.validate_password(user_data.password)
        UserService.validate_password_match(
            user_data.password,
            user_data.password_confirm,
        )

        # Check for existing user
        await UserService.user_exists(session, user_data.email)

        # Create new user
        # Note: Password is NOT hashed here - Better Auth handles password hashing
        # We only store email for task ownership validation
        new_user = User(
            email=user_data.email.lower(),
        )

        session.add(new_user)
        await session.flush()  # Get the ID before commit
        await session.commit()

        return UserResponse.model_validate(new_user)

    @staticmethod
    async def get_user_by_email(
        session: AsyncSession,
        email: str,
    ) -> User | None:
        """
        Get user by email address.

        Args:
            session: Database session
            email: Email to look up

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.email == email.lower())
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_id(
        session: AsyncSession,
        user_id: str,
    ) -> User | None:
        """
        Get user by ID.

        Args:
            session: Database session
            user_id: User ID to look up

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
