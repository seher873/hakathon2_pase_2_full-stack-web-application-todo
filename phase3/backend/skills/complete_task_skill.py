"""
Complete Task Skill for AI Agent System.

Implements the complete_task functionality as a standalone skill class.
"""
import requests
import json
from typing import Dict, Any, Optional
from uuid import UUID

from src.config import settings
from .skill_base import SkillBase


class CompleteTaskSkill(SkillBase):
    """
    Skill for marking tasks as complete/incomplete.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize the skill.

        Args:
            base_url: Base URL for the backend API (defaults to settings)
        """
        super().__init__(base_url)
        self.base_url = base_url or f"http://localhost:{settings.api_port}/api"
        self.session = requests.Session()

    def execute(self, user_id: UUID, task_id: UUID, completed: bool = True, jwt_token: str = None) -> Dict[str, Any]:
        """
        Execute the complete task operation.

        Args:
            user_id: ID of the user
            task_id: ID of the task
            completed: Whether to mark as completed (True) or incomplete (False)
            jwt_token: JWT token for authentication

        Returns:
            API response with updated task
        """
        endpoint = f"/users/{user_id}/tasks/{task_id}/complete"
        data = {"completed": completed}

        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        headers["Content-Type"] = "application/json"

        response = self.session.patch(f"{self.base_url}{endpoint}", json=data, headers=headers)
        return response.json()


if __name__ == "__main__":
    # Example usage
    skill = CompleteTaskSkill()
    # result = skill.execute(user_id="some-user-id", task_id="some-task-id", completed=True)
    # print(result)