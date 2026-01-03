"""
Database connection and session management.

Handles SQLAlchemy connection to Neon PostgreSQL with
connection pooling for serverless environments.
"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel, create_engine, Session
from typing import AsyncGenerator

from src.config import settings


# Async engine for FastAPI async endpoints
async_engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections are alive
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Async session factory
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session for dependency injection.

    Usage in FastAPI routes:
        @app.get("/tasks")
        async def get_tasks(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    Run once on application startup to initialize database schema.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables():
    """
    Drop all database tables.

    WARNING: Use only for testing or development. Will delete all data.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
