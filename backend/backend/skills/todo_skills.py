"""
AI Skills for Todo Application.

Maps natural language user requests to backend API calls.
"""
import re
import requests
import json
from typing import Dict, Any, Optional
from uuid import UUID

from src.config import settings


class TodoSkills:
    """
    AI Skills for Todo Application.

    Maps natural language user requests to backend API calls.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize the TodoSkills.

        Args:
            base_url: Base URL for the backend API (defaults to settings)
        """
        self.base_url = base_url or f"http://localhost:{settings.api_port}/api"
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None, jwt_token: str = None) -> Dict[str, Any]:
        """
        Make a request to the backend API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint
            data: Request data
            headers: Request headers
            jwt_token: JWT token for authentication

        Returns:
            Response data from the API
        """
        url = f"{self.base_url}{endpoint}"
        headers = headers or {}

        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        headers["Content-Type"] = "application/json"

        response = self.session.request(method, url, json=data, headers=headers)
        return response.json()

    def create_task(self, user_id: UUID, title: str, description: str = None, jwt_token: str = None) -> Dict[str, Any]:
        """
        Create a new task for the user.

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

        return self._make_request("POST", endpoint, data, jwt_token=jwt_token)

    def list_tasks(self, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        List all tasks for the user.

        Args:
            user_id: ID of the user
            jwt_token: JWT token for authentication

        Returns:
            API response with user's tasks
        """
        endpoint = f"/users/{user_id}/tasks"
        return self._make_request("GET", endpoint, jwt_token=jwt_token)

    def complete_task(self, user_id: UUID, task_id: UUID, completed: bool = True, jwt_token: str = None) -> Dict[str, Any]:
        """
        Mark a task as complete or incomplete.

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
        return self._make_request("PATCH", endpoint, data, jwt_token=jwt_token)

    def process_request(self, user_input: str, user_id: UUID, jwt_token: str = None) -> Dict[str, Any]:
        """
        Process a natural language request and map it to the appropriate skill.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the user
            jwt_token: JWT token for authentication

        Returns:
            Structured response with the result of the operation
        """
        user_input_lower = user_input.lower().strip()

        # Create task patterns
        create_patterns = [
            r"add\s+(.+)",
            r"create\s+(.+)",
            r"new\s+(.+)",
            r"task\s+(.+)",
            r"add\s+task\s+(.+)",
            r"create\s+task\s+(.+)"
        ]

        for pattern in create_patterns:
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

                try:
                    result = self.create_task(user_id, title, description, jwt_token)
                    return {
                        "skill": "create_task",
                        "success": True,
                        "message": f"Task '{title}' created successfully",
                        "data": result
                    }
                except Exception as e:
                    return {
                        "skill": "create_task",
                        "success": False,
                        "message": f"Failed to create task: {str(e)}",
                        "error": str(e)
                    }

        # List tasks patterns
        list_patterns = [
            r"show\s+my\s+tasks",
            r"list\s+my\s+tasks",
            r"view\s+my\s+tasks",
            r"what.*tasks.*i.*have",
            r"my\s+tasks",
            r"all\s+tasks"
        ]

        for pattern in list_patterns:
            if re.search(pattern, user_input_lower):
                try:
                    result = self.list_tasks(user_id, jwt_token)
                    task_count = len(result.get("data", {}).get("tasks", []))
                    return {
                        "skill": "list_tasks",
                        "success": True,
                        "message": f"You have {task_count} tasks",
                        "data": result
                    }
                except Exception as e:
                    return {
                        "skill": "list_tasks",
                        "success": False,
                        "message": f"Failed to list tasks: {str(e)}",
                        "error": str(e)
                    }

        # Complete task patterns
        complete_patterns = [
            r"complete\s+(.+)",
            r"finish\s+(.+)",
            r"done\s+(.+)",
            r"mark.*complete",
            r"mark.*done",
            r"check\s+(.+)"
        ]

        for pattern in complete_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                task_identifier = match.group(1).strip()

                try:
                    # First, get the user's tasks to find the matching task
                    tasks_result = self.list_tasks(user_id, jwt_token)
                    tasks = tasks_result.get("data", {}).get("tasks", [])

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
                        task_id = target_task["id"]
                        result = self.complete_task(user_id, task_id, completed=True, jwt_token=jwt_token)
                        return {
                            "skill": "complete_task",
                            "success": True,
                            "message": f"Task '{target_task['title']}' marked as complete",
                            "data": result
                        }
                    else:
                        return {
                            "skill": "complete_task",
                            "success": False,
                            "message": f"Could not find task matching '{task_identifier}'",
                        }
                except Exception as e:
                    return {
                        "skill": "complete_task",
                        "success": False,
                        "message": f"Failed to complete task: {str(e)}",
                        "error": str(e)
                    }

        # If no pattern matches, return a default response
        return {
            "skill": "unknown",
            "success": False,
            "message": f"Could not understand the request: '{user_input}'",
            "available_skills": ["create_task", "list_tasks", "complete_task"]
        }


# Singleton instance
todo_skills = TodoSkills()