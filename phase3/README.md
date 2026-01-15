# Phase-3 AI Agent System

This directory contains the advanced AI agent system with orchestration capabilities for the hackathon project.

## Architecture Overview

The Phase-3 system implements a three-layer architecture:

### 1. Skills Layer (`phase3/backend/skills/`)
- Individual, self-contained skill classes
- Each skill has an `execute()` method
- Skills are independent and reusable

### 2. Agents Layer (`phase3/backend/agents/`)
- **Intent Agent**: Analyzes user input to determine intent
- **Planning Agent**: Decides which skills to run and in what order
- **Execution Agent**: Executes the planned skills

### 3. Orchestration Layer (`phase3/backend/orchestration/`)
- **Router**: Main orchestrator that connects API endpoints to agents
- Manages the complete workflow: specify → plan → task → implement

## Skills

### Available Skills
- `CreateTaskSkill`: Creates new tasks for users
- `ListTasksSkill`: Lists all tasks for a user
- `CompleteTaskSkill`: Marks tasks as complete/incomplete

## Agents

### Intent Agent
- Analyzes natural language input
- Extracts intent and parameters
- Uses pattern matching for intent recognition

### Planning Agent
- Maps intents to appropriate skills
- Creates execution plans
- Handles complex workflows (e.g., complete_task requires first listing tasks)

### Execution Agent
- Executes the planned skills in sequence
- Handles dynamic parameter resolution
- Manages authentication tokens

## Usage

```python
from phase3.backend import create_ai_agent_system

# Create the AI agent system
ai_system = create_ai_agent_system()

# Process a user request
user_input = "Add a new task to buy groceries"
user_id = "some-user-id-uuid"
result = ai_system.route_request(user_input, user_id, jwt_token="optional-token")
```

## Key Features

1. **Modular Design**: Skills, agents, and orchestration are cleanly separated
2. **Extensible**: Easy to add new skills and agents
3. **Workflow Management**: Handles complex multi-step operations
4. **Error Handling**: Comprehensive error handling throughout the system
5. **Authentication Support**: JWT token handling for secure operations