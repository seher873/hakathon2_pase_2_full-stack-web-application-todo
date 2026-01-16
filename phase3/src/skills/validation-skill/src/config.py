"""
Configuration module for the Validation Skill.
Contains all configuration settings and environment-based overrides.
"""

import os
from typing import Optional


class Config:
    """Main configuration class for the Validation Skill."""
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Validation Skill")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "1"))
    
    # Security settings
    SECURITY_POLICY_FILE: str = os.getenv("SECURITY_POLICY_FILE", "config/default_security_policy.json")
    ALLOWED_ACTIONS_FILE: str = os.getenv("ALLOWED_ACTIONS_FILE", "config/allowed_actions.json")
    
    # Performance settings
    EXECUTION_TIMEOUT_MS: int = int(os.getenv("EXECUTION_TIMEOUT_MS", "5000"))  # 5 seconds default
    VALIDATION_TIMEOUT_MS: int = int(os.getenv("VALIDATION_TIMEOUT_MS", "2000"))  # 2 seconds default
    MAX_CONCURRENT_EXECUTIONS: int = int(os.getenv("MAX_CONCURRENT_EXECUTIONS", "100"))
    
    # Retry settings
    MAX_RETRY_ATTEMPTS: int = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
    BACKOFF_FACTOR: float = float(os.getenv("BACKOFF_FACTOR", "2.0"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")  # "json" or "text"
    
    # Validation settings
    ENABLE_DETAILED_LOGGING: bool = os.getenv("ENABLE_DETAILED_LOGGING", "true").lower() == "true"
    REQUIRE_SECURITY_VALIDATION: bool = os.getenv("REQUIRE_SECURITY_VALIDATION", "true").lower() == "true"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() in ["dev", "development", "local"]
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() in ["prod", "production"]
    
    @classmethod
    def is_testing(cls) -> bool:
        """Check if running in testing environment."""
        return cls.ENVIRONMENT.lower() in ["test", "testing"]


# Create a global config instance
config = Config()