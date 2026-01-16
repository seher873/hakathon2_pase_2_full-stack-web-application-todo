from typing import Dict, Any, List
from ..models.validation_request import ValidationRequest
from ..models.validation_result import ValidationResult
from ..utils.validators import validate_content_structure, validate_required_fields


class ContentValidator:
    """
    Validates content for correctness and proper format compliance.
    """
    
    def __init__(self):
        # Define expected structures for different content types
        self.expected_structures = {
            "task_plan": {
                "plan_id": str,
                "intent_type": str,
                "steps": list,
                "created_at": str
            },
            "intent_object": {
                "intent_type": str,
                "confidence_score": (int, float),
                "parameters": dict
            },
            "execution_plan": {
                "plan_id": str,
                "intent_type": str,
                "steps": list,
                "created_at": str
            }
        }
    
    def validate_content_correctness(self, validation_request: ValidationRequest) -> Dict[str, Any]:
        """
        Validate content for correctness and format compliance.
        
        Args:
            validation_request: The request containing content to validate
            
        Returns:
            Dict with validation results
        """
        content = validation_request.content
        content_type = validation_request.content_type
        
        # Check if content type is recognized
        if content_type not in self.expected_structures:
            return {
                "is_valid": False,
                "errors": [f"Unrecognized content type: {content_type}"],
                "warnings": [],
                "validated_at": self._get_current_timestamp()
            }
        
        # Validate content structure
        expected_structure = self.expected_structures[content_type]
        validation_errors = validate_content_structure(content, expected_structure)

        # Validate required fields
        if content_type == "task_plan":
            required_fields = ["plan_id", "intent_type", "steps"]
        elif content_type == "intent_object":
            required_fields = ["intent_type", "confidence_score", "parameters"]
        elif content_type == "execution_plan":
            required_fields = ["plan_id", "intent_type", "steps"]
        else:
            required_fields = []

        missing_fields = validate_required_fields(content, required_fields)
        validation_errors.extend([f"Missing required field: {field}" for field in missing_fields])

        # Additional content-specific validations
        if content_type == "task_plan" or content_type == "execution_plan":
            # Validate steps structure
            steps = content.get("steps", [])
            if not isinstance(steps, list):
                validation_errors.append("Steps must be a list/array")
            else:
                for i, step in enumerate(steps):
                    if not isinstance(step, dict):
                        validation_errors.append(f"Step {i} must be an object/dict")
                        continue

                    if "step_id" not in step:
                        validation_errors.append(f"Step {i} missing required 'step_id' field")

                    if "action" not in step:
                        validation_errors.append(f"Step {i} missing required 'action' field")

        # Check for any validation errors
        is_valid = len(validation_errors) == 0
        
        return {
            "is_valid": is_valid,
            "errors": validation_errors,
            "warnings": [],
            "validated_at": self._get_current_timestamp()
        }
    
    def _get_current_timestamp(self) -> str:
        """Get the current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()