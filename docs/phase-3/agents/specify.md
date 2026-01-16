# Agents Specification

## Overview
The agents layer consists of specialized AI components that handle different aspects of request processing. Each agent has a specific role in interpreting user input and coordinating system responses.

## Agent Types
- **Intent Agent**: Analyzes user input to determine intent and extract parameters
- **Planning Agent**: Decides which skills to execute and in what order
- **Execution Agent**: Executes the planned skills with proper parameter resolution

## Intent Agent Specification
- Purpose: Understand user intent from natural language input
- Input: Raw user input string
- Output: Structured intent object with parameters
- Method: Pattern matching using regex expressions

### Intent Recognition Patterns
- Create Task: "add", "create", "new", "task"
- List Tasks: "show my tasks", "list my tasks", "my tasks"
- Complete Task: "complete", "finish", "done", "mark"

## Planning Agent Specification
- Purpose: Map intents to appropriate skills
- Input: Intent object from Intent Agent
- Output: Execution plan with skill selection and parameters
- Method: Intent-to-skill mapping

## Execution Agent Specification
- Purpose: Execute planned skills in sequence
- Input: Execution plan from Planning Agent
- Output: Results from skill executions
- Method: Sequential skill execution with error handling