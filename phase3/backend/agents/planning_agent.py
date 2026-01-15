"""
Planning Agent for AI Agent System.

Decides which skills to run and in what order based on intent.
"""
from typing import Dict, Any, List
from uuid import UUID

from .agent_base import AgentBase


class PlanningAgent(AgentBase):
    """
    Agent responsible for deciding which skills to execute and in what sequence.
    """

    def __init__(self):
        """
        Initialize the Planning Agent.
        """
        self.skill_mapping = {
            "create_task": "CreateTaskSkill",
            "list_tasks": "ListTasksSkill",
            "complete_task": "CompleteTaskSkill"
        }

    def plan_execution(self, intent_result: Dict[str, Any], user_id: UUID) -> List[Dict[str, Any]]:
        """
        Plan the execution sequence based on intent and parameters.

        Args:
            intent_result: Result from IntentAgent containing intent and parameters
            user_id: ID of the user

        Returns:
            List of skill execution plans with parameters
        """
        intent = intent_result.get("intent")

        if intent == "unknown":
            return [{
                "skill": None,
                "action": "response",
                "message": f"Could not understand the request: '{intent_result['parameters']['original_input']}'",
                "available_skills": intent_result.get("available_intents", [])
            }]

        execution_plan = []

        if intent == "create_task":
            params = intent_result.get("parameters", {})
            execution_plan.append({
                "skill": "CreateTaskSkill",
                "method": "execute",
                "arguments": {
                    "user_id": user_id,
                    "title": params.get("title"),
                    "description": params.get("description")
                }
            })

        elif intent == "list_tasks":
            execution_plan.append({
                "skill": "ListTasksSkill",
                "method": "execute",
                "arguments": {
                    "user_id": user_id
                }
            })

        elif intent == "complete_task":
            params = intent_result.get("parameters", {})
            task_identifier = params.get("task_identifier")

            # First, we need to list tasks to find the target task
            execution_plan.append({
                "skill": "ListTasksSkill",
                "method": "execute",
                "arguments": {
                    "user_id": user_id
                },
                "store_result_as": "tasks_list"
            })

            # Then we can complete the specific task - task_id will be resolved dynamically
            execution_plan.append({
                "skill": "CompleteTaskSkill",
                "method": "execute",
                "arguments": {
                    "user_id": user_id,
                    "task_identifier": task_identifier,  # Will be resolved to actual task_id during execution
                    "completed": True
                }
            })

        return execution_plan


if __name__ == "__main__":
    agent = PlanningAgent()
    intent_result = {
        "intent": "create_task",
        "parameters": {
            "title": "Buy groceries",
            "description": "Get milk and bread"
        }
    }
    plan = agent.plan_execution(intent_result, "some-user-id")
    print(plan)