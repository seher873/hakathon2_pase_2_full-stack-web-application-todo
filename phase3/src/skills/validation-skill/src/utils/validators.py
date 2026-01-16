from typing import Any, Dict, List
import json


def validate_json_format(data: Any) -> bool:
    """
    Validates if the given data is in proper JSON format.
    """
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False


def validate_required_fields(data: Dict[str, Any], required_fields: list) -> list:
    """
    Validates if all required fields are present in the data.
    
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


def validate_content_structure(content: Any, expected_structure: Dict[str, Any]) -> List[str]:
    """
    Validates if content matches the expected structure.
    
    Args:
        content: Content to validate
        expected_structure: Expected structure to match
        
    Returns:
        List of validation errors
    """
    errors = []
    
    if not isinstance(content, dict):
        errors.append("Content must be a dictionary/object")
        return errors
    
    # Check required keys
    for key, value_type in expected_structure.items():
        if key not in content:
            errors.append(f"Missing required key: {key}")
        elif not isinstance(content[key], value_type):
            errors.append(f"Key '{key}' has wrong type. Expected {value_type.__name__}, got {type(content[key]).__name__}")
    
    return errors


def validate_action_against_whitelist(action: str, allowed_actions: List[str]) -> bool:
    """
    Validates if an action is in the allowed actions list.
    
    Args:
        action: Action to validate
        allowed_actions: List of allowed actions
        
    Returns:
        Boolean indicating if action is allowed
    """
    return action in allowed_actions


def validate_no_circular_dependencies(steps: List[Dict[str, Any]]) -> bool:
    """
    Validates that there are no circular dependencies in a list of steps.
    
    Args:
        steps: List of step dictionaries with 'step_id' and 'dependencies' keys
        
    Returns:
        Boolean indicating if there are no circular dependencies
    """
    # Create a mapping of step_id to its dependencies
    dependencies_map = {}
    for step in steps:
        step_id = step.get('step_id')
        deps = step.get('dependencies', [])
        dependencies_map[step_id] = deps
    
    # Check for circular dependencies using DFS
    visited = set()
    rec_stack = set()
    
    def has_cycle(node):
        if node not in visited:
            visited.add(node)
            rec_stack.add(node)
            
            # Check dependencies of current node
            for neighbor in dependencies_map.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
        
        rec_stack.discard(node)
        return False
    
    # Check each node
    for step_id in dependencies_map:
        if step_id not in visited:
            if has_cycle(step_id):
                return False
    
    return True