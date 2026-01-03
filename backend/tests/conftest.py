"""
Pytest configuration and fixtures.

Provides reusable fixtures for testing database connections,
FastAPI test client, and authentication.
"""

import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timedelta
import jwt

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel, create_engine, Session

from main import app
from src.config import settings
from src.db import get_async_session


# ============================================================================
# Database Fixtures (Async)
# ============================================================================


@pytest_asyncio.fixture
async def async_engine():
    """Create async test database engine."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def async_session_local(async_engine):
    """Create async test database session."""
    async_session = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    yield async_session


@pytest_asyncio.fixture
async def get_test_async_session(async_session_local):
    """Override database session dependency for testing."""

    async def override_get_async_session():
        async with async_session_local() as session:
            yield session

    return override_get_async_session


# ============================================================================
# FastAPI Test Client
# ============================================================================


@pytest.fixture
def test_client(get_test_async_session):
    """Create FastAPI test client with overridden database session."""
    app.dependency_overrides[get_async_session] = get_test_async_session
    return TestClient(app)


@pytest.fixture
def cleanup_dependencies():
    """Cleanup dependency overrides after test."""
    yield
    app.dependency_overrides.clear()


# ============================================================================
# JWT Token Fixtures
# ============================================================================


@pytest.fixture
def test_user_id():
    """Generate test user ID."""
    return str(uuid4())


@pytest.fixture
def test_jwt_token(test_user_id):
    """Generate valid test JWT token."""
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
        "type": "access",
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token


@pytest.fixture
def test_expired_jwt_token(test_user_id):
    """Generate expired test JWT token."""
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=25),
        "type": "access",
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token


@pytest.fixture
def test_invalid_jwt_token():
    """Generate invalid JWT token."""
    return "invalid.token.format"


# ============================================================================
# Authorization Headers
# ============================================================================


@pytest.fixture
def auth_header(test_jwt_token):
    """Valid Authorization header with JWT token."""
    return {"Authorization": f"Bearer {test_jwt_token}"}


@pytest.fixture
def expired_auth_header(test_expired_jwt_token):
    """Authorization header with expired JWT token."""
    return {"Authorization": f"Bearer {test_expired_jwt_token}"}


@pytest.fixture
def invalid_auth_header(test_invalid_jwt_token):
    """Authorization header with invalid JWT token."""
    return {"Authorization": f"Bearer {test_invalid_jwt_token}"}


@pytest.fixture
def missing_auth_header():
    """Empty Authorization header."""
    return {"Authorization": ""}


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def test_user_data():
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "Test1234!",
    }


@pytest.fixture
def test_task_data():
    """Sample task creation data."""
    return {
        "title": "Test Task",
        "description": "Test task description",
    }


@pytest.fixture
def test_task_update_data():
    """Sample task update data."""
    return {
        "title": "Updated Task Title",
        "description": "Updated task description",
    }


# ============================================================================
# Async Test Utilities
# ============================================================================


@pytest.fixture
def anyio_backend():
    """Set async backend for pytest-asyncio."""
    return "asyncio"
