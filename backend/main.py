"""
FastAPI application entry point.

Initializes the FastAPI app with middleware, exception handlers,
routes, and database setup.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.config import settings
from src.middleware import (
    setup_cors_middleware,
    LoggingMiddleware,
    exception_handler,
    http_exception_handler,
    validation_exception_handler,
    SuccessResponse,
)
from src.db import create_db_and_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Handles startup and shutdown events:
    - Startup: Create database tables
    - Shutdown: Cleanup resources
    """
    # Startup
    logger.info("🚀 Starting FastAPI application")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"CORS origins: {settings.allowed_origins}")

    try:
        await create_db_and_tables()
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("🛑 Shutting down FastAPI application")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Hackathon Todo API",
    description="Phase II Full-Stack Todo Web Application API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Setup middleware
setup_cors_middleware(app)
app.add_middleware(LoggingMiddleware)

# Setup exception handlers
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# ============================================================================
# Health Check Endpoint
# ============================================================================


@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        SuccessResponse with status information
    """
    response = SuccessResponse(
        data={
            "status": "healthy",
            "service": "Hackathon Todo API",
            "version": "2.0.0",
            "environment": settings.environment,
        }
    )
    return response.to_dict()


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.

    Redirects to API documentation.
    """
    return {
        "message": "Hackathon Todo API",
        "docs": "/api/docs",
        "version": "2.0.0",
    }


# ============================================================================
# Authentication Routes (will be imported from src.api.auth)
# ============================================================================

# TODO: Import and include auth routes
# from src.api.auth import router as auth_router
# app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])


# ============================================================================
# Task Routes (will be imported from src.api.tasks)
# ============================================================================

# TODO: Import and include task routes
# from src.api.tasks import router as tasks_router
# app.include_router(
#     tasks_router, prefix="/api/users", tags=["tasks"]
# )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )
