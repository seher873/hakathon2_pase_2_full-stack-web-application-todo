# Data Model: Validation Skill

## Core Entities

### ValidationRequest
Represents the input to the validation skill containing content to validate.

**Fields:**
- `request_id` (string): Unique identifier for the validation request
- `content` (any): The content to be validated (could be text, structured data, etc.)
- `content_type` (string): The type/format of the content being validated
- `validation_rules` (list): Specific validation rules to apply (optional, defaults to all rules)
- `timestamp` (datetime): When the request was made
- `source` (string): The source of the content being validated (optional)

**Validation Rules:**
- `content` must be present
- `request_id` must be unique for the system
- `content_type` must be a recognized content type

### ValidationResult
Represents the output of the validation process.

**Fields:**
- `request_id` (string): ID of the request this result corresponds to
- `is_valid` (boolean): Whether the content passed all validation checks
- `validation_details` (list): Detailed results for each validation rule applied
- `processed_at` (datetime): When validation was completed
- `execution_time_ms` (int): Time taken to complete validation
- `security_check_passed` (boolean): Whether security validation passed
- `rejection_reasons` (list): If invalid, reasons why content was rejected

**Validation Rules:**
- `is_valid` must be consistent with `validation_details` and `rejection_reasons`
- `execution_time_ms` must be positive
- If `is_valid` is false, `rejection_reasons` must not be empty

### ValidationDetail
Represents the result of applying a single validation rule.

**Fields:**
- `rule_name` (string): Name of the validation rule applied
- `passed` (boolean): Whether this validation rule passed
- `message` (string): Description of the validation result
- `timestamp` (datetime): When this validation was performed
- `severity` (string): How critical this validation is ('critical', 'warning', 'info')

**Validation Rules:**
- `rule_name` must be a recognized validation rule
- `severity` must be one of the predefined values

### ValidationRule
Defines a specific validation rule that can be applied to content.

**Fields:**
- `rule_id` (string): Unique identifier for this rule
- `name` (string): Human-readable name for the rule
- `description` (string): Explanation of what this rule validates
- `rule_type` (string): Category of validation ('security', 'format', 'business_logic', etc.)
- `parameters` (dict): Configuration parameters for this rule
- `enabled` (boolean): Whether this rule is currently active
- `created_at` (datetime): When the rule was created
- `updated_at` (datetime): When the rule was last modified

**Validation Rules:**
- `rule_id` must be unique across all rules
- `rule_type` must be a recognized validation category
- `enabled` defaults to true

### RejectionReason
Specifies why content was rejected during validation.

**Fields:**
- `reason_code` (string): Machine-readable code for the rejection reason
- `description` (string): Human-readable explanation of the rejection
- `severity` (string): How serious this issue is ('low', 'medium', 'high', 'critical')
- `applied_rules` (list): Which validation rules led to this rejection
- `timestamp` (datetime): When the rejection was determined

**Validation Rules:**
- `severity` must be one of the predefined values
- `reason_code` must be unique for the system