from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any

from ..models.validation_request import ValidationRequest
from ..models.validation_result import ValidationResult
from ...services.validation_engine import ValidationEngine
from ...services.security_checker import SecurityChecker

# Initialize the validation engine and security checker
validation_engine = ValidationEngine()
security_checker = SecurityChecker()

@router.post("/validate-content", response_model=ValidationResult)
async def validate_content(validation_request: ValidationRequest):
    """
    Validate content for safety and correctness.
    Takes content and validates it against security policies and correctness rules.
    """
    try:
        # Validate the request against security policies first
        security_check_result = security_checker.validate_request(validation_request)
        
        if not security_check_result["allowed"]:
            # If the request contains blocked actions, return a 403 Forbidden response
            raise HTTPException(
                status_code=403,
                detail={
                    "error_code": "UNAUTHORIZED_ACTION",
                    "message": "Content contains unauthorized actions",
                    "details": {
                        "blocked_actions": security_check_result["blocked_actions"],
                        "validation_errors": security_check_result["validation_errors"]
                    }
                }
            )
        
        # Execute the validation
        result = validation_engine.validate_content(validation_request)
        
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions (like 403 above)
        raise
    except Exception as e:
        # Handle any other errors during validation
        raise HTTPException(status_code=500, detail=f"Error validating content: {str(e)}")


@router.get("/validation-status/{request_id}", response_model=ValidationResult)
async def get_validation_status(request_id: str = Path(..., description="ID of the validation request to check")):
    """
    Get validation status.
    Retrieves the current status of an ongoing validation.
    """
    # This is a placeholder implementation
    # In a real implementation, this would retrieve status from a store
    raise HTTPException(status_code=501, detail="Not Implemented Yet")


@router.post("/validate-plan", response_model=ValidationResult)
async def validate_plan(validation_request: ValidationRequest):
    """
    Validate a task plan for execution.
    Checks if a task plan is executable according to security policies.
    """
    try:
        # Validate the request against security policies first
        security_check_result = security_checker.validate_request(validation_request)
        
        if not security_check_result["allowed"]:
            # If the plan contains blocked actions, return a 403 Forbidden response
            raise HTTPException(
                status_code=403,
                detail={
                    "error_code": "UNAUTHORIZED_ACTION",
                    "message": "Task plan contains unauthorized actions",
                    "details": {
                        "blocked_actions": security_check_result["blocked_actions"],
                        "validation_errors": security_check_result["validation_errors"]
                    }
                }
            )
        
        # Execute the validation
        result = validation_engine.validate_content(validation_request)
        
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions (like 403 above)
        raise
    except Exception as e:
        # Handle any other errors during validation
        raise HTTPException(status_code=500, detail=f"Error validating plan: {str(e)}")