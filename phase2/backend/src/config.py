"""
Backend configuration management.

Loads environment variables and provides configuration settings
for database, JWT, CORS, and application server.
"""

from pydantic import field_validator, computed_field
from pydantic_settings import BaseSettings
from typing import List, Union


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

    # CORS Configuration - stored as string, converted to list
    allowed_origins_str: str = "http://localhost:3000"
    """Raw allowed origins string from environment (comma-separated)"""

    # Environment
    environment: str = "development"
    """Current environment (development, staging, production)"""

    @field_validator('allowed_origins_str', mode='before')
    @classmethod
    def validate_allowed_origins_str(cls, v: Union[str, List[str]]) -> str:
        """Validate and convert allowed_origins to string format."""
        if isinstance(v, list):
            return ','.join(v)
        if isinstance(v, str):
            return v
        return str(v)

    @property
    def allowed_origins(self) -> List[str]:
        """List of allowed CORS origins (computed from string)."""
        if self.allowed_origins_str:
            return [origin.strip() for origin in self.allowed_origins_str.split(",") if origin.strip()]
        return ["http://localhost:3000"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
        "env_prefix": ""  # Use empty prefix so field names map directly
    }


# Global settings instance
settings = Settings()
