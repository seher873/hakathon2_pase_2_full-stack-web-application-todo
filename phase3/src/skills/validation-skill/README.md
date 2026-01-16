# Validation Skill

The Validation Skill takes task plans and content as input and validates them for safety and correctness before allowing them to proceed through the system. The implementation follows a security-first approach with strict action whitelisting, comprehensive error handling, and detailed logging. The skill operates as a standalone service that validates each action against security policies before allowing it to pass to downstream services, handles failures gracefully, and returns detailed validation results.

## Features

- Content validation for safety and correctness
- Security policy enforcement with whitelist-based validation
- Detailed validation result reporting
- Rejection rule application for unsafe content
- Performance monitoring and metrics
- Comprehensive logging for audit purposes

## Tech Stack

- Python 3.9+
- FastAPI for web framework
- Pydantic for data validation
- JSONSchema for validation

## Installation

1. Clone the repository
2. Navigate to the src/skills/validation-skill directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

### Development Mode
```bash
# Run the service
uvicorn src.api.main:app --reload --port 8000
```

The service will be available at `http://localhost:8000`

## API Usage

### Validate Content
```bash
curl -X POST http://localhost:8000/api/v1/validate-content \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req-123",
    "content": {
      "intent_type": "create_task",
      "parameters": {
        "title": "Buy groceries",
        "due_date": "2023-12-25"
      }
    },
    "content_type": "task_plan",
    "validation_rules": ["security", "format", "business_logic"],
    "timestamp": "2023-10-27T10:00:00Z",
    "source": "task_planning_skill"
  }'
```

### Check Validation Status
```bash
curl -X GET http://localhost:8000/api/v1/validation-status/{request-id} \
  -H "Content-Type: application/json"
```

### Validate a Plan
```bash
curl -X POST http://localhost:8000/api/v1/validate-plan \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req-456",
    "content": {
      "plan_id": "plan-789",
      "intent_type": "create_task",
      "steps": [
        {
          "step_id": "step-1",
          "description": "Validate task parameters",
          "action": "validate_params",
          "parameters": {
            "required_fields": ["title"]
          },
          "dependencies": [],
          "optional": false,
          "estimated_duration_ms": 10
        },
        {
          "step_id": "step-2",
          "description": "Create task record",
          "action": "create_record",
          "parameters": {
            "table": "tasks",
            "data": {
              "title": "Sample Task",
              "description": "A sample task created via execution skill"
            }
          },
          "dependencies": ["step-1"],
          "optional": false,
          "estimated_duration_ms": 50
        }
      ],
      "created_at": "2023-10-27T10:00:00Z",
      "valid": true,
      "validation_errors": []
    },
    "content_type": "task_plan",
    "timestamp": "2023-10-27T10:00:00Z"
  }'
```

## Security Policy Configuration

The Validation Skill uses a security policy to determine which actions are allowed. The default policy can be customized by modifying the security policy configuration:

```json
{
  "policy_id": "default-policy-1",
  "name": "Default Security Policy",
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
  ],
  "conditions": {
    "max_execution_time": 30000,
    "max_retries_per_step": 3
  },
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

## Error Recovery

The Validation Skill implements the following error recovery mechanisms:
- Retry with exponential backoff for transient failures
- Detailed error logging for troubleshooting
- Ability to resume validation after failures
- Graceful degradation when non-critical validation steps fail

## Logging Strategy

All validation activities are logged with the following information:
- Timestamp of validation
- Request ID and content type
- Action validated
- Validation result (pass/fail)
- Duration of validation
- Any errors encountered
- Security validation outcomes