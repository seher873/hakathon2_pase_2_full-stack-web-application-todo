from typing import Any
import uuid
from datetime import datetime


def generate_unique_id(prefix: str = "") -> str:
    """
    Generate a unique identifier with an optional prefix.
    
    Args:
        prefix: Optional prefix to add to the UUID
        
    Returns:
        Unique identifier string
    """
    unique_id = str(uuid.uuid4())
    return f"{prefix}{unique_id}" if prefix else unique_id


def validate_required_fields(data: dict, required_fields: list) -> list:
    """
    Validate that required fields are present in the data.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Returns:
        List of missing fields
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    return missing_fields


def sanitize_input(input_data: str) -> str:
    """
    Sanitize input string by removing potentially harmful characters.
    
    Args:
        input_data: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    # Remove potentially dangerous characters/sequences
    sanitized = input_data.replace('<script>', '&lt;script&gt;').replace('</script>', '&lt;/script&gt;')
    sanitized = sanitized.replace('javascript:', 'javascript-unsafe:')
    sanitized = sanitized.replace('vbscript:', 'vbscript-unsafe:')
    return sanitized