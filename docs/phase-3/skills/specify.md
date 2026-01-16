# Intent Understanding Skill Specification

## Skill Name
Intent Agent (Intent Understanding Skill)

## Purpose
The Intent Understanding Skill analyzes natural language user input to determine the user's intent and extract relevant parameters. It serves as the first step in the AI agent system workflow, mapping user requests to appropriate backend skills using pattern matching techniques.

## Inputs (User Message Format)
The skill accepts natural language strings as input representing user requests. The input is processed as follows:
- Converted to lowercase for pattern matching
- Leading/trailing whitespace is stripped
- Supports various phrasings for the three core intents:

### Create Task Patterns:
- `add (.+)`
- `create (.+)`
- `new (.+)`
- `task (.+)`
- `add task (.+)`
- `create task (.+)`

### List Tasks Patterns:
- `show my tasks`
- `list my tasks`
- `view my tasks`
- `what.*tasks.*i.*have`
- `my tasks`
- `all tasks`

### Complete Task Patterns:
- `complete (.+)`
- `finish (.+)`
- `done (.+)`
- `mark.*complete`
- `mark.*done`
- `check (.+)`

For create_task, the skill attempts to extract title and description by splitting on `" - "` or `": "` separators.

## Outputs (Normalized Intent Object)
The skill returns a dictionary with the following structure:

```python
{
    "intent": str,           # One of: "create_task", "list_tasks", "complete_task", "unknown"
    "parameters": dict       # Contains extracted parameters based on intent
}
```

### For create_task intent:
```python
{
    "intent": "create_task",
    "parameters": {
        "title": str,        # Extracted task title
        "description": str   # Extracted task description (optional, may be None)
    }
}
```

### For list_tasks intent:
```python
{
    "intent": "list_tasks", 
    "parameters": {}
}
```

### For complete_task intent:
```python
{
    "intent": "complete_task",
    "parameters": {
        "task_identifier": str   # Text identifying the task to complete
    }
}
```

### For unknown intent:
```python
{
    "intent": "unknown",
    "parameters": {
        "original_input": str    # Original user input
    },
    "available_intents": list    # List of supported intents: ["create_task", "list_tasks", "complete_task"]
}
```

## Constraints (What the Skill Must NOT Do)
- Must NOT execute any external API calls or database operations
- Must NOT perform any side effects beyond pattern matching and parameter extraction
- Must NOT interpret or validate the extracted parameters beyond basic parsing
- Must NOT handle authentication or authorization
- Must NOT execute skills or perform actual task operations
- Must NOT maintain state between calls
- Must NOT connect to external services or databases
- Must NOT modify the original user input beyond normalization (lowercase/trim)

## Error Cases
- **Unknown Intent**: When user input doesn't match any defined patterns, returns intent "unknown" with available intents list
- **Malformed Input**: When input matches a pattern but parameter extraction fails, returns the best available parsed data
- **Empty Input**: When input is empty or only whitespace, treated as unknown intent
- **Ambiguous Matches**: When multiple patterns could match, the first matching pattern determines the intent (following the order defined in the patterns dictionary)