"""
List Tasks Skill for AI Agent System.

Implements the list_tasks functionality as a standalone skill class.
"""
import requests
import json
from typing import Dict, Any, Optional
from uuid import UUID

from src.config import settings
from .skill_base import SkillBase


class ListTasksSkill(SkillBase):
    """
    Skill for listing user tasks.
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

    def execute(self, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Execute the list tasks operation.

        Args:
            user_id: ID of the user
            jwt_token: JWT token for authentication

        Returns:
            API response with user's tasks
        """
        endpoint = f"/users/{user_id}/tasks"

        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        headers["Content-Type"] = "application/json"

        response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
        return response.json()


if __name__ == "__main__":
    # Example usage
    skill = ListTasksSkill()
    # result = skill.execute(user_id="some-user-id")
    # print(result)