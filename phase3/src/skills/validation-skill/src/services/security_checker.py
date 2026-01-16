from typing import Dict, List, Any
from ..models.validation_request import ValidationRequest
from ..models.validation_rule import ValidationRule


class SecurityChecker:
    """
    Validates actions against security policies before execution.
    Implements a whitelist-based security model that validates each action against a predefined list of allowed operations.
    """
    
    def __init__(self):
        # Define the security policy with allowed and blocked actions
        self.security_policy = {
            "policy_id": "default-security-policy-1",
            "name": "Default Security Policy",
            "allowed_actions": [
                "validate_params",
                "create_record",
                "update_record", 
                "delete_record",
                "query_records",
                "send_notification",
                "format_output",
                "validate_format",
                "check_permissions",
                "log_activity"
            ],
            "blocked_actions": [
                "execute_system_command",
                "access_file_system",
                "modify_user_permissions",
                "direct_database_access",
                "modify_system_settings",
                "access_encrypted_data"
            ],
            "conditions": {
                "max_execution_time": 30000,  # 30 seconds
                "max_retries_per_step": 3
            }
        }
    
    def validate_request(self, validation_request: ValidationRequest) -> Dict[str, Any]:
        """
        Validate a request against security policies.

        Args:
            validation_request: The request to validate

        Returns:
            Dict with validation results including allowed/blocked actions and errors
        """
        allowed_actions = []
        blocked_actions = []
        validation_errors = []

        # Check content for actions that need validation
        content = validation_request.content

        # Extract actions from content (this depends on the structure of the content)
        actions = self._extract_actions_from_content(content)

        for action in actions:
            is_allowed, reason = self._is_action_allowed(action)

            if is_allowed:
                allowed_actions.append(action)
            else:
                blocked_actions.append(action)
                validation_errors.append(f"Action '{action}' is not allowed: {reason}")

        return {
            "allowed": len(blocked_actions) == 0,
            "allowed_actions": list(set(allowed_actions)),  # Remove duplicates
            "blocked_actions": list(set(blocked_actions)),  # Remove duplicates
            "validation_errors": validation_errors,
            "validated_at": self._get_current_timestamp()
        }
    
    def _is_action_allowed(self, action: str) -> tuple[bool, str]:
        """
        Check if an action is allowed based on the security policy.
        
        Args:
            action: The action to check
            
        Returns:
            Tuple of (is_allowed: bool, reason: str)
        """
        # Check if action is in blocked actions
        if action in self.security_policy["blocked_actions"]:
            return False, "Action is explicitly blocked by security policy"
        
        # Check if action is in allowed actions
        if self.security_policy["allowed_actions"]:
            # If allowed actions list is not empty, only allow actions in the list
            if action in self.security_policy["allowed_actions"]:
                return True, "Action is allowed by security policy"
            else:
                return False, "Action is not in the allowed actions list"
        
        # If no allowed actions are specified but no blocked actions match, allow by default
        # (This is a fallback - ideally, allowed actions should be explicitly defined)
        return True, "Action allowed by default (no specific policy)"
    
    def _extract_actions_from_content(self, content: Any) -> List[str]:
        """
        Extract actions from content for validation.
        
        Args:
            content: The content to extract actions from
            
        Returns:
            List of action strings found in the content
        """
        actions = []
        
        # If content is a dictionary with steps
        if isinstance(content, dict):
            if "steps" in content:
                # Extract actions from steps
                for step in content["steps"]:
                    if isinstance(step, dict) and "action" in step:
                        actions.append(step["action"])
                    elif isinstance(step, dict) and "intent_type" in step:
                        # Sometimes the action is called intent_type
                        actions.append(step["intent_type"])
            elif "action" in content:
                # Content is a single action
                actions.append(content["action"])
            elif "intent_type" in content:
                # Content is a single intent
                actions.append(content["intent_type"])
            elif "steps" not in content and isinstance(content, dict):
                # Look for actions in other possible fields
                for key, value in content.items():
                    if isinstance(value, dict) and "action" in value:
                        actions.append(value["action"])
        
        # If content is a list of steps
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if "action" in item:
                        actions.append(item["action"])
                    elif "intent_type" in item:
                        actions.append(item["intent_type"])
        
        return actions
    
    def _get_current_timestamp(self) -> str:
        """Get the current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()