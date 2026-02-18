"""MCP tool interface layer that wraps existing FastAPI endpoints."""
import os
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from .tool_models import TaskCreateModel, TaskUpdateModel
import requests
import logging

logger = logging.getLogger(__name__)

# Base URL for the existing FastAPI endpoints
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

class TaskTools:
    """MCP tools that wrap existing FastAPI task endpoints."""

    def __init__(self, token: str):
        """Initialize with user's JWT token for authentication."""
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_task(self, title: str, description: Optional[str] = None, due_date: Optional[str] = None) -> dict:
        """Create a new task via the existing FastAPI endpoint."""
        try:
            url = f"{BASE_URL}/api/tasks"
            payload = TaskCreateModel(
                title=title,
                description=description,
                due_date=due_date
            ).dict()

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            logger.info(f"Task created successfully: {title}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating task: {str(e)}")
            raise Exception(f"Failed to create task: {str(e)}")

    def list_tasks(self, filter_by: Optional[str] = None, status: Optional[str] = None) -> List[dict]:
        """List tasks via the existing FastAPI endpoint."""
        try:
            url = f"{BASE_URL}/api/tasks"
            params = {}
            if filter_by:
                params["filter_by"] = filter_by
            if status:
                params["status"] = status

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            tasks = response.json()
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing tasks: {str(e)}")
            raise Exception(f"Failed to list tasks: {str(e)}")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                   due_date: Optional[str] = None, status: Optional[str] = None) -> dict:
        """Update a task via the existing FastAPI endpoint."""
        try:
            url = f"{BASE_URL}/api/tasks/{task_id}"
            payload = TaskUpdateModel(
                title=title,
                description=description,
                due_date=due_date,
                status=status
            ).dict(exclude_none=True)

            response = requests.put(url, json=payload, headers=self.headers)
            response.raise_for_status()

            logger.info(f"Task {task_id} updated successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            raise Exception(f"Failed to update task: {str(e)}")

    def delete_task(self, task_id: int) -> dict:
        """Delete a task via the existing FastAPI endpoint."""
        try:
            url = f"{BASE_URL}/api/tasks/{task_id}"

            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()

            logger.info(f"Task {task_id} deleted successfully")
            return {"success": True, "task_id": task_id}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            raise Exception(f"Failed to delete task: {str(e)}")

    def toggle_complete(self, task_id: int) -> dict:
        """Toggle task completion status via the existing FastAPI endpoint."""
        try:
            # First get the current task to check its status
            url = f"{BASE_URL}/api/tasks/{task_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            current_task = response.json()
            current_status = current_task.get("status", "pending")
            new_status = "completed" if current_status != "completed" else "pending"

            # Update the task status
            update_url = f"{BASE_URL}/api/tasks/{task_id}"
            payload = {"status": new_status}

            response = requests.patch(update_url, json=payload, headers=self.headers)
            response.raise_for_status()

            logger.info(f"Task {task_id} status toggled to {new_status}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error toggling task {task_id} status: {str(e)}")
            raise Exception(f"Failed to toggle task status: {str(e)}")