"""
Base class for all AI agents in the Phase-3 system.

All agents should inherit from this base class to ensure consistent interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from uuid import UUID


class AgentBase(ABC):
    """
    Abstract base class for all agents in the AI system.
    """

    def __init__(self):
        """
        Initialize the agent.
        """
        pass

    @abstractmethod
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process the input and return the result.

        Args:
            **kwargs: Agent-specific parameters

        Returns:
            Dictionary containing the result of the processing
        """
        pass


class WorkflowManager:
    """
    Manages the workflow following the specify → plan → task → implement methodology.
    """

    def __init__(self):
        """
        Initialize the workflow manager.
        """
        pass

    def execute_workflow(self, user_input: str, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Execute the complete workflow: specify → plan → task → implement.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the user making the request
            jwt_token: JWT token for authentication

        Returns:
            Dictionary containing the result of the workflow execution
        """
        from .intent_agent import IntentAgent
        from .planning_agent import PlanningAgent
        from .execution_agent import ExecutionAgent

        # Create agent instances
        intent_agent = IntentAgent()
        planning_agent = PlanningAgent()
        execution_agent = ExecutionAgent()

        # Specify: Define the user's intent and requirements
        specification = self.specify(user_input, user_id)

        # Get intent from intent agent
        intent_result = intent_agent.analyze_intent(user_input)
        specification["intent_result"] = intent_result

        # Plan: Determine the sequence of actions needed
        plan = self.plan(specification, user_id)

        # Create execution plan using planning agent
        if intent_result["intent"] != "unknown":
            execution_plan = planning_agent.plan_execution(intent_result, user_id)
            plan["execution_plan"] = execution_plan

        # Task: Break down into specific tasks/skills
        tasks = self.task(plan)

        # Use the execution plan as tasks
        tasks = execution_plan if intent_result["intent"] != "unknown" else []

        # Implement: Execute the planned actions
        result = self.implement(tasks, user_id, jwt_token)

        # Execute the tasks using execution agent
        if tasks:
            execution_result = execution_agent.execute_plan(tasks, jwt_token)
            result = execution_agent._format_response(intent_result, execution_result)

        return result

    def specify(self, user_input: str, user_id: UUID) -> Dict[str, Any]:
        """
        Specify the user's intent and requirements.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the user

        Returns:
            Specification of the user's intent
        """
        return {
            "user_input": user_input,
            "user_id": user_id,
            "intent": "unspecified"
        }

    def plan(self, specification: Dict[str, Any], user_id: UUID) -> Dict[str, Any]:
        """
        Plan the sequence of actions needed.

        Args:
            specification: Specification of the user's intent
            user_id: ID of the user

        Returns:
            Planned sequence of actions
        """
        return {
            "specification": specification,
            "actions": []
        }

    def task(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break down the plan into specific tasks/skills.

        Args:
            plan: Planned sequence of actions

        Returns:
            List of specific tasks to execute
        """
        return plan.get("actions", [])

    def implement(self, tasks: List[Dict[str, Any]], user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Implement the planned actions.

        Args:
            tasks: List of specific tasks to execute
            user_id: ID of the user
            jwt_token: JWT token for authentication

        Returns:
            Result of implementing the tasks
        """
        return {
            "tasks_executed": len(tasks),
            "success": True,
            "results": []
        }