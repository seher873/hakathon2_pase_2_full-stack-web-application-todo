"""
Execution Agent for AI Agent System.

Executes the planned skills in the specified order.
"""
from typing import Dict, Any, List
from uuid import UUID
import importlib

from .agent_base import AgentBase
from ..skills.create_task_skill import CreateTaskSkill
from ..skills.list_tasks_skill import ListTasksSkill
from ..skills.complete_task_skill import CompleteTaskSkill


class ExecutionAgent(AgentBase):
    """
    Agent responsible for executing the planned skills.
    """

    def __init__(self):
        """
        Initialize the Execution Agent.
        """
        self.skill_instances = {
            "CreateTaskSkill": CreateTaskSkill(),
            "ListTasksSkill": ListTasksSkill(),
            "CompleteTaskSkill": CompleteTaskSkill()
        }

    def execute_plan(self, execution_plan: List[Dict[str, Any]], jwt_token: str = None) -> Dict[str, Any]:
        """
        Execute the planned skills in sequence.

        Args:
            execution_plan: List of skill execution plans
            jwt_token: JWT token for authentication

        Returns:
            Dictionary containing execution results
        """
        results = []
        stored_results = {}

        for step in execution_plan:
            skill_name = step.get("skill")

            if skill_name is None:
                # This is a response step, not a skill execution
                results.append(step)
                continue

            if skill_name not in self.skill_instances:
                results.append({
                    "error": f"Unknown skill: {skill_name}",
                    "step": step
                })
                continue

            skill_instance = self.skill_instances[skill_name]
            method_name = step.get("method", "execute")
            arguments = step.get("arguments", {})

            # Add JWT token to arguments if available
            if jwt_token:
                arguments["jwt_token"] = jwt_token

            # Handle dynamic resolution of task_id for complete_task
            if skill_name == "CompleteTaskSkill" and "task_identifier" in arguments:
                task_identifier = arguments.pop("task_identifier")

                # Get the stored tasks list to find the matching task
                tasks_list = stored_results.get("tasks_list", {})
                tasks = tasks_list.get("data", {}).get("tasks", [])

                # Find the task that matches the identifier
                target_task = None
                for task in tasks:
                    if task_identifier.lower() in task.get("title", "").lower():
                        target_task = task
                        break

                if not target_task:
                    # If no task matches by title, try to find by index if user provided a number
                    try:
                        task_index = int(task_identifier) - 1
                        if 0 <= task_index < len(tasks):
                            target_task = tasks[task_index]
                    except ValueError:
                        pass  # Not a number, continue

                if target_task:
                    arguments["task_id"] = target_task["id"]
                else:
                    results.append({
                        "error": f"Could not find task matching '{task_identifier}'",
                        "step": step
                    })
                    continue

            # Execute the skill
            try:
                method = getattr(skill_instance, method_name)
                result = method(**arguments)

                # Store result if requested
                store_as = step.get("store_result_as")
                if store_as:
                    stored_results[store_as] = result

                results.append({
                    "success": True,
                    "result": result,
                    "step": step
                })
            except Exception as e:
                results.append({
                    "error": str(e),
                    "step": step
                })

        return {
            "results": results,
            "stored_results": stored_results,
            "success": all("error" not in result for result in results if isinstance(result, dict))
        }


if __name__ == "__main__":
    agent = ExecutionAgent()

    # Example execution plan for creating a task
    plan = [{
        "skill": "CreateTaskSkill",
        "method": "execute",
        "arguments": {
            "user_id": "some-user-id",
            "title": "Test task",
            "description": "Test description"
        }
    }]

    result = agent.execute_plan(plan)
    print(result)