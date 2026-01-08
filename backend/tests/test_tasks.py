"""
Task endpoint tests.

Tests task CRUD operations to verify the task management system is working correctly.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from main import app
from src.db import get_async_session
from src.models.user import User
from src.models.task import Task


@pytest.fixture
def client(get_test_async_session):
    """Create test client with database override."""
    app.dependency_overrides[get_async_session] = get_test_async_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def create_test_user(client):
    """Helper function to create a test user and return auth token."""
    signup_data = {
        "email": f"testuser_{uuid4()}@example.com",
        "password": "SecurePassword123!",
        "password_confirm": "SecurePassword123!"
    }
    
    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 201
    
    data = response.json()
    token = data["data"]["token"]
    user_id = data["data"]["user"]["id"]
    
    return token, user_id


class TestTaskCRUD:
    """Tests for task CRUD endpoints."""

    def test_create_task_success(self, client):
        """
        Test successful task creation.

        Acceptance Criteria:
        - POST /api/users/{user_id}/tasks with valid data returns 201
        - Response contains created task data
        - Task is saved in database
        """
        token, user_id = create_test_user(client)
        
        task_data = {
            "title": "Test Task",
            "description": "Test Description"
        }

        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        
        task = data["data"]
        assert task["title"] == "Test Task"
        assert task["description"] == "Test Description"
        assert task["completed"] is False
        assert "id" in task
        assert "created_at" in task
        assert "updated_at" in task

    def test_get_tasks_list(self, client):
        """
        Test getting user's task list.

        Acceptance Criteria:
        - GET /api/users/{user_id}/tasks returns 200
        - Response contains list of user's tasks
        - Other users' tasks are not included
        """
        token, user_id = create_test_user(client)
        
        # Create a few tasks
        task_data = {"title": "Task 1", "description": "First task"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        
        task_data = {"title": "Task 2", "description": "Second task"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201

        response = client.get(
            f"/api/users/{user_id}/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        assert "tasks" in data["data"]
        assert len(data["data"]["tasks"]) == 2

    def test_get_single_task(self, client):
        """
        Test getting a single task.

        Acceptance Criteria:
        - GET /api/users/{user_id}/tasks/{task_id} returns 200
        - Response contains the requested task data
        """
        token, user_id = create_test_user(client)
        
        # Create a task first
        task_data = {"title": "Single Task", "description": "A single task"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        created_task = response.json()["data"]
        task_id = created_task["id"]

        response = client.get(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        
        task = data["data"]
        assert task["id"] == task_id
        assert task["title"] == "Single Task"
        assert task["description"] == "A single task"

    def test_update_task(self, client):
        """
        Test updating a task.

        Acceptance Criteria:
        - PUT /api/users/{user_id}/tasks/{task_id} with valid data returns 200
        - Response contains updated task data
        - Task is updated in database
        """
        token, user_id = create_test_user(client)
        
        # Create a task first
        task_data = {"title": "Original Task", "description": "Original description"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        created_task = response.json()["data"]
        task_id = created_task["id"]

        # Update the task
        update_data = {
            "title": "Updated Task",
            "description": "Updated description"
        }

        response = client.put(
            f"/api/users/{user_id}/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        
        task = data["data"]
        assert task["id"] == task_id
        assert task["title"] == "Updated Task"
        assert task["description"] == "Updated description"

    def test_mark_task_complete(self, client):
        """
        Test marking a task as complete/incomplete.

        Acceptance Criteria:
        - PATCH /api/users/{user_id}/tasks/{task_id}/complete returns 200
        - Response contains updated task with correct completion status
        """
        token, user_id = create_test_user(client)
        
        # Create a task first
        task_data = {"title": "Task to Complete", "description": "Will be marked complete"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        created_task = response.json()["data"]
        task_id = created_task["id"]

        # Mark task as complete
        patch_data = {"completed": True}

        response = client.patch(
            f"/api/users/{user_id}/tasks/{task_id}/complete",
            json=patch_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        
        task = data["data"]
        assert task["id"] == task_id
        assert task["completed"] is True

        # Mark task as incomplete
        patch_data = {"completed": False}

        response = client.patch(
            f"/api/users/{user_id}/tasks/{task_id}/complete",
            json=patch_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()

        task = data["data"]
        assert task["id"] == task_id
        assert task["completed"] is False

    def test_delete_task(self, client):
        """
        Test deleting a task.

        Acceptance Criteria:
        - DELETE /api/users/{user_id}/tasks/{task_id} returns 204
        - Task is removed from database
        """
        token, user_id = create_test_user(client)
        
        # Create a task first
        task_data = {"title": "Task to Delete", "description": "Will be deleted"}
        response = client.post(
            f"/api/users/{user_id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        created_task = response.json()["data"]
        task_id = created_task["id"]

        # Verify task exists
        response = client.get(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

        # Delete the task
        response = client.delete(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 204

        # Verify task is gone
        response = client.get(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404

    def test_task_authorization(self, client):
        """
        Test that users can only access their own tasks.

        Acceptance Criteria:
        - Users cannot access other users' tasks
        - 403 Forbidden returned when trying to access another user's task
        """
        # Create two users
        token1, user_id1 = create_test_user(client)
        token2, user_id2 = create_test_user(client)
        
        # User 1 creates a task
        task_data = {"title": "User 1 Task", "description": "Only accessible by user 1"}
        response = client.post(
            f"/api/users/{user_id1}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert response.status_code == 201
        created_task = response.json()["data"]
        task_id = created_task["id"]

        # User 2 tries to access user 1's task
        response = client.get(
            f"/api/users/{user_id1}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403

        # User 2 tries to update user 1's task
        update_data = {"title": "Attempted Update"}
        response = client.put(
            f"/api/users/{user_id1}/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403

        # User 2 tries to delete user 1's task
        response = client.delete(
            f"/api/users/{user_id1}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403