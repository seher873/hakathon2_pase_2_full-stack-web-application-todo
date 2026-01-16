from datetime import datetime
from typing import List, Dict, Any
from ..models.validation_request import ValidationRequest
from ..models.validation_result import ValidationResult, ValidationDetail
from ..models.validation_rule import ValidationRule, RejectionReason
from ..utils.helpers import generate_unique_id


class ValidationEngine:
    """
    Core service that orchestrates the validation process.
    Implements step-by-step validation with security policy enforcement.
    """
    
    def __init__(self):
        self.completed_validations = {}
        self.validated_request = None
        
        # Define default validation rules
        self.default_rules = [
            ValidationRule(
                rule_id="security-policy-1",
                name="Security Policy Validation",
                description="Validates that content does not contain potentially harmful actions",
                rule_type="security",
                parameters={
                    "allowed_actions": [
                        "validate_params",
                        "create_record", 
                        "update_record",
                        "delete_record", 
                        "query_records",
                        "send_notification"
                    ],
                    "blocked_actions": [
                        "execute_system_command",
                        "access_file_system", 
                        "modify_user_permissions"
                    ]
                },
                enabled=True
            ),
            ValidationRule(
                rule_id="format-validation-1",
                name="Format Validation",
                description="Validates that content follows the expected format",
                rule_type="format",
                parameters={
                    "required_fields": ["intent_type", "parameters"],
                    "allowed_content_types": ["task_plan", "intent_object", "execution_plan"]
                },
                enabled=True
            ),
            ValidationRule(
                rule_id="business-logic-1",
                name="Business Logic Validation",
                description="Validates that content follows business rules",
                rule_type="business_logic",
                parameters={
                    "max_steps": 50,
                    "max_execution_time": 30000
                },
                enabled=True
            )
        ]
    
    def validate_content(self, validation_request: ValidationRequest) -> ValidationResult:
        """
        Validate content for safety and correctness.

        Args:
            validation_request: The content to validate

        Returns:
            ValidationResult: Result of the validation with status and details
        """
        start_time = datetime.now()
        request_id = validation_request.request_id

        # Initialize result tracking
        validation_details = []
        rejection_reasons = []
        validation_errors = []

        # Select rules to apply (use specified rules or all enabled rules)
        rules_to_apply = []
        if validation_request.validation_rules:
            # Apply only the specified rules
            for rule_name in validation_request.validation_rules:
                matching_rules = [rule for rule in self.default_rules if rule.name == rule_name]
                if matching_rules:
                    rules_to_apply.extend(matching_rules)
                else:
                    validation_errors.append(f"No validation rule found with name: {rule_name}")
        else:
            # Apply all enabled rules
            rules_to_apply = [rule for rule in self.default_rules if rule.enabled]

        # Apply validation rules
        for rule in rules_to_apply:
            try:
                # Apply the rule to the content
                rule_result = self._apply_validation_rule(validation_request.content, rule)

                validation_details.append(ValidationDetail(
                    rule_name=rule.name,
                    passed=rule_result["passed"],
                    message=rule_result["message"],
                    timestamp=datetime.now(),
                    severity=rule_result.get("severity", "info")
                ))

                # If rule failed, add to rejection reasons
                if not rule_result["passed"]:
                    rejection_reasons.append(rule_result["message"])

            except Exception as e:
                validation_errors.append(f"Error applying rule '{rule.name}': {str(e)}")

        # Determine overall validity
        is_valid = len(rejection_reasons) == 0 and len(validation_errors) == 0

        # Calculate execution time
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)  # Convert to milliseconds

        # Calculate validation statistics
        total_steps = len(rules_to_apply)
        successful_steps = len([vd for vd in validation_details if vd.passed])
        failed_steps = len([vd for vd in validation_details if not vd.passed])

        # Determine security check status
        security_check_passed = all(
            vd.passed for vd in validation_details
            if "security" in vd.rule_name.lower()
        )

        return ValidationResult(
            request_id=request_id,
            is_valid=is_valid,
            validation_details=validation_details,
            processed_at=datetime.now(),
            execution_time_ms=execution_time_ms,
            security_check_passed=security_check_passed,
            rejection_reasons=rejection_reasons,
            total_steps=total_steps,
            successful_steps=successful_steps,
            failed_steps=failed_steps,
            validation_errors=validation_errors
        )
    
    def _apply_validation_rule(self, content: Any, rule: ValidationRule) -> Dict[str, Any]:
        """
        Apply a specific validation rule to content.
        
        Args:
            content: The content to validate
            rule: The rule to apply
            
        Returns:
            Dict with validation result information
        """
        if rule.rule_type == "security":
            return self._apply_security_rule(content, rule)
        elif rule.rule_type == "format":
            return self._apply_format_rule(content, rule)
        elif rule.rule_type == "business_logic":
            return self._apply_business_logic_rule(content, rule)
        else:
            return {
                "passed": False,
                "message": f"Unknown rule type: {rule.rule_type}",
                "severity": "critical"
            }
    
    def _apply_security_rule(self, content: Any, rule: ValidationRule) -> Dict[str, Any]:
        """
        Apply security validation rule to content.
        
        Args:
            content: The content to validate
            rule: The security rule to apply
            
        Returns:
            Dict with validation result information
        """
        # Check if content is a dictionary-like object with steps
        if isinstance(content, dict) and "steps" in content:
            steps = content["steps"]
        elif isinstance(content, dict) and "actions" in content:
            steps = content["actions"]
        else:
            # If it's a simple action, wrap it in a list
            steps = [content] if isinstance(content, dict) else []
        
        # Check each step/action against blocked actions
        blocked_actions = rule.parameters.get("blocked_actions", [])
        allowed_actions = rule.parameters.get("allowed_actions", [])
        
        for step in steps:
            if isinstance(step, dict):
                action = step.get("action") or step.get("intent_type") or step.get("step_type")
                
                if action:
                    # Check if action is explicitly blocked
                    if action in blocked_actions:
                        return {
                            "passed": False,
                            "message": f"Action '{action}' is blocked by security policy",
                            "severity": "critical"
                        }
                    
                    # If allowed actions list is specified, check if action is in it
                    if allowed_actions and action not in allowed_actions:
                        return {
                            "passed": False,
                            "message": f"Action '{action}' is not in the allowed actions list",
                            "severity": "critical"
                        }
        
        return {
            "passed": True,
            "message": "Content passed security policy validation",
            "severity": "info"
        }
    
    def _apply_format_rule(self, content: Any, rule: ValidationRule) -> Dict[str, Any]:
        """
        Apply format validation rule to content.
        
        Args:
            content: The content to validate
            rule: The format rule to apply
            
        Returns:
            Dict with validation result information
        """
        # Check if content is a dictionary
        if not isinstance(content, dict):
            return {
                "passed": False,
                "message": "Content must be a dictionary/object",
                "severity": "critical"
            }
        
        # Check required fields
        required_fields = rule.parameters.get("required_fields", [])
        for field in required_fields:
            if field not in content:
                return {
                    "passed": False,
                    "message": f"Required field '{field}' is missing from content",
                    "severity": "critical"
                }
        
        # Check content type if specified
        content_type = content.get("content_type") or content.get("intent_type") or content.get("type")
        allowed_types = rule.parameters.get("allowed_content_types", [])
        
        if allowed_types and content_type and content_type not in allowed_types:
            return {
                "passed": False,
                "message": f"Content type '{content_type}' is not allowed. Allowed types: {allowed_types}",
                "severity": "critical"
            }
        
        return {
            "passed": True,
            "message": "Content passed format validation",
            "severity": "info"
        }
    
    def _apply_business_logic_rule(self, content: Any, rule: ValidationRule) -> Dict[str, Any]:
        """
        Apply business logic validation rule to content.
        
        Args:
            content: The content to validate
            rule: The business logic rule to apply
            
        Returns:
            Dict with validation result information
        """
        # Check number of steps if content has steps
        max_steps = rule.parameters.get("max_steps", 100)
        
        if isinstance(content, dict) and "steps" in content:
            steps = content["steps"]
            if len(steps) > max_steps:
                return {
                    "passed": False,
                    "message": f"Content has {len(steps)} steps, which exceeds the maximum of {max_steps}",
                    "severity": "critical"
                }
        
        # Additional business logic checks can be added here
        
        return {
            "passed": True,
            "message": "Content passed business logic validation",
            "severity": "info"
        }