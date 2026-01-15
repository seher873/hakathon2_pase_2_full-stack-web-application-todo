"""
Main entry point for Phase-3 AI Agent System.

This module provides the complete AI agent orchestration system with:
- Intent recognition
- Planning
- Execution
- Workflow management
"""
from .orchestration.router import Router
from .agents.intent_agent import IntentAgent
from .agents.planning_agent import PlanningAgent
from .agents.execution_agent import ExecutionAgent
from .skills.create_task_skill import CreateTaskSkill
from .skills.list_tasks_skill import ListTasksSkill
from .skills.complete_task_skill import CompleteTaskSkill


__all__ = [
    'Router',
    'IntentAgent',
    'PlanningAgent',
    'ExecutionAgent',
    'CreateTaskSkill',
    'ListTasksSkill',
    'CompleteTaskSkill'
]


def create_ai_agent_system():
    """
    Factory function to create a complete AI agent system.

    Returns:
        Router: The main orchestrator for the AI agent system
    """
    return Router()


# Example usage
if __name__ == "__main__":
    # Create the AI agent system
    ai_system = create_ai_agent_system()

    # Example request
    user_input = "Add a new task to buy groceries"
    user_id = "123e4567-e89b-12d3-a456-426614174000"  # Example UUID

    result = ai_system.route_request(user_input, user_id)
    print("Result:", result)