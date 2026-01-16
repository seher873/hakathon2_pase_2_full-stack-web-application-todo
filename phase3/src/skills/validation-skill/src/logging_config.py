"""
Structured logging configuration for the Validation Skill.
Sets up JSON-formatted logging for production and human-readable format for development.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from .config import config


def setup_logging():
    """Set up logging configuration for the application."""
    
    # Get log level from config
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Choose formatter based on environment
    if config.LOG_FORMAT.lower() == "json" and not config.is_development():
        # Use JSON formatter in production
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
        )
    else:
        # Use simple formatter in development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Also configure uvicorn access logs at appropriate level
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.setLevel(log_level)


# Initialize logging when module is imported
setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance."""
    return logging.getLogger(name)


# Initialize logging when module is imported
setup_logging()