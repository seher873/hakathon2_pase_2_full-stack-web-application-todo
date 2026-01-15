"""
Intent Agent for AI Agent System.

Analyzes user input to determine intent and extract relevant parameters.
"""
import re
from typing import Dict, Any, Optional
from uuid import UUID

from .agent_base import AgentBase


class IntentAgent(AgentBase):
    """
    Agent responsible for understanding user intent from natural language input.
    """

    def __init__(self):
        """
        Initialize the Intent Agent.
        """
        super().__init__()
        self.patterns = {
            "create_task": [
                r"add\s+(.+)",
                r"create\s+(.+)",
                r"new\s+(.+)",
                r"task\s+(.+)",
                r"add\s+task\s+(.+)",
                r"create\s+task\s+(.+)"
            ],
            "list_tasks": [
                r"show\s+my\s+tasks",
                r"list\s+my\s+tasks",
                r"view\s+my\s+tasks",
                r"what.*tasks.*i.*have",
                r"my\s+tasks",
                r"all\s+tasks"
            ],
            "complete_task": [
                r"complete\s+(.+)",
                r"finish\s+(.+)",
                r"done\s+(.+)",
                r"mark.*complete",
                r"mark.*done",
                r"check\s+(.+)"
            ]
        }

    def analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze the user input to determine intent and extract parameters.

        Args:
            user_input: Natural language input from the user

        Returns:
            Dictionary containing intent and extracted parameters
        """
        user_input_lower = user_input.lower().strip()

        # Check for create task patterns
        for pattern in self.patterns["create_task"]:
            match = re.search(pattern, user_input_lower)
            if match:
                task_description = match.group(1).strip()

                # Try to extract title and description
                parts = task_description.split(" - ", 1)
                title = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else None

                # If no description found, try splitting on colon
                if description is None:
                    parts = task_description.split(": ", 1)
                    if len(parts) > 1:
                        title = parts[0].strip()
                        description = parts[1].strip()

                return {
                    "intent": "create_task",
                    "parameters": {
                        "title": title,
                        "description": description
                    }
                }

        # Check for list tasks patterns
        for pattern in self.patterns["list_tasks"]:
            if re.search(pattern, user_input_lower):
                return {
                    "intent": "list_tasks",
                    "parameters": {}
                }

        # Check for complete task patterns
        for pattern in self.patterns["complete_task"]:
            match = re.search(pattern, user_input_lower)
            if match:
                task_identifier = match.group(1).strip()
                return {
                    "intent": "complete_task",
                    "parameters": {
                        "task_identifier": task_identifier
                    }
                }

        # If no pattern matches, return unknown intent
        return {
            "intent": "unknown",
            "parameters": {
                "original_input": user_input
            },
            "available_intents": ["create_task", "list_tasks", "complete_task"]
        }


if __name__ == "__main__":
    agent = IntentAgent()
    result = agent.analyze_intent("Add a new task to buy groceries")
    print(result)