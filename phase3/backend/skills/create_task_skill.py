"""
Create Task Skill for AI Agent System.

Implements the create_task functionality as a standalone skill class.
"""
import requests
import json
from typing import Dict, Any, Optional
from uuid import UUID

from src.config import settings
from .skill_base import SkillBase


class CreateTaskSkill(SkillBase):
    """
    Skill for creating new tasks.
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

    def execute(self, user_id: UUID, title: str, description: str = None, jwt_token: str = None) -> Dict[str, Any]:
        """
        Execute the create task operation.

        Args:
            user_id: ID of the user
            title: Task title
            description: Task description (optional)
            jwt_token: JWT token for authentication

        Returns:
            API response with created task
        """
        endpoint = f"/users/{user_id}/tasks"
        data = {
            "title": title,
            "description": description
        }

        if description is None:
            data.pop("description")

        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        headers["Content-Type"] = "application/json"

        response = self.session.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        return response.json()


if __name__ == "__main__":
    # Example usage
    skill = CreateTaskSkill()
    # result = skill.execute(user_id="some-user-id", title="Test task", description="Test description")
    # print(result)