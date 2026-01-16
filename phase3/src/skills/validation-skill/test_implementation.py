import pytest
from datetime import datetime
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.validation_request import ValidationRequest
from src.models.validation_result import ValidationResult, ValidationDetail
from src.services.validation_engine import ValidationEngine
from src.services.security_checker import SecurityChecker


def test_validation_request_model():
    """Test that ValidationRequest model works correctly."""
    request = ValidationRequest(
        request_id="test-123",
        content={"action": "create_task", "parameters": {"title": "Test Task"}},
        content_type="task_plan",
        validation_rules=["security", "format"],
        timestamp=datetime.now()
    )

    assert request.request_id == "test-123"
    assert request.content_type == "task_plan"
    assert "security" in request.validation_rules


def test_validation_result_model():
    """Test that ValidationResult model works correctly."""
    result = ValidationResult(
        request_id="test-123",
        is_valid=True,
        validation_details=[],
        processed_at=datetime.now(),
        execution_time_ms=100,
        security_check_passed=True,
        rejection_reasons=[],
        total_steps=1,
        successful_steps=1,
        failed_steps=0,
        validation_errors=[]
    )

    assert result.request_id == "test-123"
    assert result.is_valid == True
    assert result.execution_time_ms == 100


def test_security_checker_validation():
    """Test that SecurityChecker properly validates requests."""
    checker = SecurityChecker()
    request = ValidationRequest(
        request_id="test-123",
        content={"action": "validate_params", "parameters": {"required_fields": ["title"]}},
        content_type="task_plan",
        validation_rules=[],
        timestamp=datetime.now()
    )

    result = checker.validate_request(request)

    # The validate_params action should be allowed
    assert result["allowed"] == True
    assert "validate_params" in result["allowed_actions"]


def test_validation_engine_basic():
    """Test that ValidationEngine can process a basic request."""
    engine = ValidationEngine()
    request = ValidationRequest(
        request_id="test-123",
        content={
            "steps": [
                {
                    "step_id": "step-1",
                    "description": "Validate parameters",
                    "action": "validate_params",
                    "parameters": {"required_fields": ["title"]},
                    "dependencies": [],
                    "optional": False,
                    "estimated_duration_ms": 10
                }
            ]
        },
        content_type="task_plan",
        validation_rules=[],
        timestamp=datetime.now()
    )

    result = engine.validate_content(request)

    # Should be valid since all actions are allowed
    assert result.is_valid == True
    assert result.request_id == "test-123"
    assert len(result.validation_details) > 0


if __name__ == "__main__":
    test_validation_request_model()
    test_validation_result_model()
    test_security_checker_validation()
    test_validation_engine_basic()
    print("All tests passed!")