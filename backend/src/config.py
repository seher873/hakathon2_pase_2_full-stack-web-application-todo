"""
Backend configuration management.

Loads environment variables and provides configuration settings
for database, JWT, CORS, and application server.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Database Configuration
    database_url: str
    """PostgreSQL connection string from Neon"""

    # JWT Configuration
    jwt_secret: str
    """Secret key for JWT signing (min 32 characters)"""

    jwt_algorithm: str = "HS256"
    """JWT algorithm for encoding/decoding"""

    jwt_expiration_hours: int = 24
    """JWT token expiration time in hours"""

    # Server Configuration
    api_host: str = "0.0.0.0"
    """API server host"""

    api_port: int = 8000
    """API server port"""

    debug: bool = False
    """Debug mode flag"""

    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000"]
    """List of allowed CORS origins"""

    # Environment
    environment: str = "development"
    """Current environment (development, staging, production)"""

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
