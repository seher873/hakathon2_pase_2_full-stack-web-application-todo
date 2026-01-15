"""
Orchestration Router for AI Agent System.

Connects API endpoints to agents and manages the workflow following
the specify → plan → task → implement methodology.
"""
from typing import Dict, Any
from uuid import UUID

from ..agents.agent_base import WorkflowManager
from ..agents.intent_agent import IntentAgent
from ..agents.planning_agent import PlanningAgent
from ..agents.execution_agent import ExecutionAgent


class Router:
    """
    Main orchestrator that connects API endpoints to the agent system.
    Manages the workflow: specify → plan → task → implement.
    """

    def __init__(self):
        """
        Initialize the Router with agent instances.
        """
        self.workflow_manager = WorkflowManager()
        self.intent_agent = IntentAgent()
        self.planning_agent = PlanningAgent()
        self.execution_agent = ExecutionAgent()

    def route_request(self, user_input: str, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Route a user request through the agent system following the
        specify → plan → task → implement methodology.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the user making the request
            jwt_token: JWT token for authentication

        Returns:
            Dictionary containing the result of processing the request
        """
        # Apply the specify → plan → task → implement methodology
        return self.workflow_manager.execute_workflow(user_input, user_id, jwt_token)

    def legacy_route_request(self, user_input: str, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Legacy routing method for backward compatibility.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the user making the request
            jwt_token: JWT token for authentication

        Returns:
            Dictionary containing the result of processing the request
        """
        # Step 1: Analyze intent
        intent_result = self.intent_agent.analyze_intent(user_input)

        # If intent is unknown, return early
        if intent_result["intent"] == "unknown":
            return {
                "success": False,
                "message": intent_result["parameters"]["original_input"],
                "available_intents": intent_result.get("available_intents", [])
            }

        # Step 2: Plan execution
        execution_plan = self.planning_agent.plan_execution(intent_result, user_id)

        # Step 3: Execute the plan
        execution_result = self.execution_agent.execute_plan(execution_plan, jwt_token)

        # Format and return the final result
        return self._format_response(intent_result, execution_result)

    def _format_response(self, intent_result: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the final response based on intent and execution results.

        Args:
            intent_result: Result from intent analysis
            execution_result: Result from plan execution

        Returns:
            Formatted response dictionary
        """
        intent = intent_result["intent"]

        if not execution_result["success"]:
            return {
                "success": False,
                "message": "Execution failed",
                "errors": [r.get("error") for r in execution_result["results"] if "error" in r]
            }

        if intent == "create_task":
            # Extract the created task from results
            create_results = [r for r in execution_result["results"] if r.get("success")]
            if create_results:
                task_data = create_results[0]["result"]
                return {
                    "success": True,
                    "message": f"Task '{task_data.get('data', {}).get('title', 'Unknown')}' created successfully",
                    "data": task_data,
                    "intent": intent
                }

        elif intent == "list_tasks":
            # Extract the tasks list from results
            list_results = [r for r in execution_result["results"] if r.get("success")]
            if list_results:
                tasks_data = list_results[0]["result"]
                task_count = len(tasks_data.get("data", {}).get("tasks", []))
                return {
                    "success": True,
                    "message": f"You have {task_count} tasks",
                    "data": tasks_data,
                    "intent": intent
                }

        elif intent == "complete_task":
            # For complete task, check if it was successful
            complete_results = [r for r in execution_result["results"] if r.get("success")]
            if complete_results:
                # This is a simplified response - in reality we'd check the actual completion result
                return {
                    "success": True,
                    "message": "Task marked as complete",
                    "data": complete_results[-1]["result"] if complete_results else {},
                    "intent": intent
                }

        return {
            "success": execution_result["success"],
            "message": "Request processed",
            "data": execution_result,
            "intent": intent
        }


# Example usage
if __name__ == "__main__":
    router = Router()
    result = router.route_request("Add a task to buy groceries", "some-user-id")
    print(result)