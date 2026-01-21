# Data Model: Phase-III AI Layer for Todo Application

## Core Entities

### Natural Language Command
- **Description**: Represents user input in everyday language
- **Fields**: 
  - `input_text`: string (raw user command)
  - `parsed_intent`: IntentObject (extracted actionable parameters)
  - `timestamp`: datetime (when command was received)
  - `user_id`: string (authenticated user identifier)
- **Validation**: Input text must be non-empty, user must be authenticated
- **Relationships**: Belongs to authenticated user session

### Intent Object
- **Description**: Structured representation of user intent after NLP processing
- **Fields**:
  - `action_type`: enum (create, list, update, delete, complete)
  - `parameters`: object (extracted command parameters)
  - `confidence_score`: float (0.0-1.0 confidence in intent recognition)
  - `context`: object (date/time/location context extracted)
- **Validation**: Action type must be recognized, parameters must be valid for action
- **Relationships**: Linked to original command, associated with execution plan

### Execution Plan
- **Description**: Structured sequence of skills to fulfill user request
- **Fields**:
  - `sequence`: array (ordered list of skill calls)
  - `parameters`: object (validated parameters for each skill)
  - `auth_token`: string (JWT token for API calls)
  - `status`: enum (pending, executing, completed, failed)
- **Validation**: All skills must be registered, parameters must match skill schemas
- **Relationships**: Created from Intent Object, executed by Execution Agent

### Skill Interface
- **Description**: Standardized API for backend operations
- **Fields**:
  - `name`: string (unique skill identifier)
  - `input_schema`: object (expected input parameters)
  - `output_schema`: object (expected output structure)
  - `constraints`: array (validation rules)
  - `linked_api`: string (corresponding backend endpoint)
- **Validation**: Schema must be valid JSON Schema, linked API must exist
- **Relationships**: Defines contract for Execution Agent

## State Transitions

### Command Processing Flow
1. `Received` → `Processing` (when Intent Agent receives command)
2. `Processing` → `Parsed` (when intent is identified)
3. `Parsed` → `Planned` (when execution plan is created)
4. `Planned` → `Executing` (when skills are executed)
5. `Executing` → `Completed` (when all skills succeed)
6. `Executing` → `Failed` (when any skill fails)

### Error Recovery
- `Failed` → `Retry` (when retry logic is applicable)
- `Retry` → `Completed` (on successful retry)
- `Failed` → `Needs Clarification` (when user input is ambiguous)

## Validation Rules

### Natural Language Command
- Must not exceed 500 characters
- Must contain recognizable intent pattern
- Must be associated with authenticated user session

### Intent Object
- Action type must be one of: create, list, update, delete, complete
- Confidence score must be between 0.0 and 1.0
- Parameters must match expected schema for action type

### Execution Plan
- All referenced skills must be registered and available
- JWT token must be valid and unexpired
- User must have permissions for requested operations

### Skill Interface
- Input/output schemas must conform to JSON Schema specification
- Linked API endpoints must exist and be accessible
- Constraints must be enforceable and testable
