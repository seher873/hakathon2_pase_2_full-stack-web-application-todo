"""
Middleware for FastAPI application.

Handles CORS, request logging, error responses, and other
cross-cutting concerns for the API.
"""

import logging
import time
import json
from typing import Callable, Generic, TypeVar, Dict, Any
from datetime import datetime
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.config import settings

# Define type variable for generic responses
T = TypeVar('T')

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def setup_cors_middleware(app):
    """
    Configure CORS middleware for the FastAPI app.

    Allows requests from frontend origins specified in ALLOWED_ORIGINS
    environment variable.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "User-Agent",
        ],
        expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"],
        max_age=3600,
    )


class LoggingMiddleware:
    """
    Middleware for logging HTTP requests and responses.

    Logs request method, path, query parameters, response status,
    and execution time for all requests.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Process request and response with logging.

        Args:
            scope: ASGI scope
            receive: ASGI receive function
            send: ASGI send function
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)

        # Record start time
        start_time = time.time()

        # Log request information
        logger.info(
            f"→ {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                "client": request.client.host if request.client else "unknown",
            },
        )

        # Create a custom sender to capture response status
        response_status = None

        async def capture_sender(message):
            nonlocal response_status
            if message["type"] == "http.response.start":
                response_status = message["status"]
            await send(message)

        # Process the request
        await self.app(scope, receive, capture_sender)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Log response information
        logger.info(
            f"← {response_status or 'unknown'} {request.url.path} ({execution_time:.3f}s)",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response_status,
                "execution_time": execution_time,
            },
        )


class ErrorResponse:
    """Standard error response format."""

    def __init__(
        self,
        status: str = "error",
        code: str = "INTERNAL_ERROR",
        message: str = "An error occurred",
        details: dict = None,
        timestamp: str = None,
    ):
        self.status = status
        self.code = code
        self.message = message
        self.details = details or {}
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def to_dict(self):
        """Convert error response to dictionary."""
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "details": self.details if self.details else None,
            "timestamp": self.timestamp,
        }


from typing import Generic

class SuccessResponse(Generic[T]):
    """Standard success response format."""

    def __init__(
        self,
        data: T = None,
        status: str = "success",
        timestamp: str = None,
    ):
        self.status = status
        self.data = data
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert success response to dictionary."""
        return {
            "status": self.status,
            "data": self.data,
            "timestamp": self.timestamp,
        }


async def exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for uncaught exceptions.

    Args:
        request: FastAPI request
        exc: Exception that was raised

    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    error_response = ErrorResponse(
        status="error",
        code="INTERNAL_SERVER_ERROR",
        message="An internal server error occurred",
    )

    return JSONResponse(
        status_code=500,
        content=error_response.to_dict(),
    )


async def http_exception_handler(request: Request, exc):
    """
    Handler for FastAPI HTTPException.

    Args:
        request: FastAPI request
        exc: HTTPException that was raised

    Returns:
        JSON response with error details
    """
    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
        },
    )

    # Map status code to error code
    status_code_to_error = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR",
    }

    error_code = status_code_to_error.get(exc.status_code, "UNKNOWN_ERROR")

    error_response = ErrorResponse(
        status="error",
        code=error_code,
        message=exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict(),
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc):
    """
    Handler for Pydantic validation errors.

    Args:
        request: FastAPI request
        exc: RequestValidationError that was raised

    Returns:
        JSON response with validation error details
    """
    logger.warning(
        f"Validation error on {request.url.path}",
        extra={
            "path": request.url.path,
            "errors": exc.errors(),
        },
    )

    # Extract field-level error details
    details = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        details[field] = error["msg"]

    error_response = ErrorResponse(
        status="error",
        code="VALIDATION_ERROR",
        message="Validation failed",
        details=details,
    )

    return JSONResponse(
        status_code=422,
        content=error_response.to_dict(),
    )
