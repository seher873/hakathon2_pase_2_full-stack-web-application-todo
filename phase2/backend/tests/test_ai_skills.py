"""
Unit tests for AI Skills functionality.
Tests for all three skills: create_task, list_tasks, complete_task
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from uuid import UUID
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.skills.todo_skills import TodoSkills


class TestTodoSkills(unittest.TestCase):
    """Test class for TodoSkills functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.skills = TodoSkills(base_url="http://test-api:8000/api")
        self.user_id = "123e4567-e89b-12d3-a456-426614174000"
        self.jwt_token = "test-jwt-token"

    def test_create_task_method(self):
        """Test the create_task method."""
        with patch.object(self.skills.session, 'request') as mock_request:
            # Mock API response
            mock_response = Mock()
            mock_response.json.return_value = {
                "id": "task-123",
                "title": "Buy milk",
                "description": "Get whole milk",
                "completed": False
            }
            mock_request.return_value = mock_response

            result = self.skills.create_task(
                user_id=self.user_id,
                title="Buy milk",
                description="Get whole milk",
                jwt_token=self.jwt_token
            )

            # Verify the request was made correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            method, url = args

            self.assertEqual(method, "POST")
            self.assertEqual(url, f"http://test-api:8000/api/users/{self.user_id}/tasks")

            # Verify the data and headers
            self.assertEqual(kwargs['json']['title'], "Buy milk")
            self.assertEqual(kwargs['json']['description'], "Get whole milk")
            self.assertIn("Authorization", kwargs['headers'])
            self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.jwt_token}")

    def test_create_task_without_description(self):
        """Test the create_task method without description."""
        with patch.object(self.skills.session, 'request') as mock_request:
            # Mock API response
            mock_response = Mock()
            mock_response.json.return_value = {
                "id": "task-123",
                "title": "Buy milk",
                "completed": False
            }
            mock_request.return_value = mock_response

            result = self.skills.create_task(
                user_id=self.user_id,
                title="Buy milk",
                jwt_token=self.jwt_token
            )

            # Verify the request was made correctly without description
            args, kwargs = mock_request.call_args
            _, _ = args

            # Verify the data doesn't contain description
            self.assertEqual(kwargs['json']['title'], "Buy milk")
            self.assertNotIn('description', kwargs['json'])

    def test_list_tasks_method(self):
        """Test the list_tasks method."""
        with patch.object(self.skills.session, 'request') as mock_request:
            # Mock API response
            mock_response = Mock()
            mock_response.json.return_value = {
                "tasks": [
                    {"id": "1", "title": "Task 1", "completed": False},
                    {"id": "2", "title": "Task 2", "completed": True}
                ]
            }
            mock_request.return_value = mock_response

            result = self.skills.list_tasks(
                user_id=self.user_id,
                jwt_token=self.jwt_token
            )

            # Verify the request was made correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            method, url = args

            self.assertEqual(method, "GET")
            self.assertEqual(url, f"http://test-api:8000/api/users/{self.user_id}/tasks")

            # Verify the headers
            self.assertIn("Authorization", kwargs['headers'])
            self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.jwt_token}")

    def test_complete_task_method(self):
        """Test the complete_task method."""
        task_id = "task-123"

        with patch.object(self.skills.session, 'request') as mock_request:
            # Mock API response
            mock_response = Mock()
            mock_response.json.return_value = {
                "id": task_id,
                "title": "Buy milk",
                "completed": True
            }
            mock_request.return_value = mock_response

            result = self.skills.complete_task(
                user_id=self.user_id,
                task_id=task_id,
                completed=True,
                jwt_token=self.jwt_token
            )

            # Verify the request was made correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            method, url = args

            self.assertEqual(method, "PATCH")
            self.assertEqual(url, f"http://test-api:8000/api/users/{self.user_id}/tasks/{task_id}/complete")

            # Verify the data and headers
            self.assertEqual(kwargs['json']['completed'], True)
            self.assertIn("Authorization", kwargs['headers'])
            self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.jwt_token}")

    def test_process_request_create_task_intent(self):
        """Test process_request with create_task intent."""
        with patch.object(self.skills, 'create_task') as mock_create:
            mock_create.return_value = {"id": "task-123", "title": "Buy milk"}

            result = self.skills.process_request(
                user_input="Add buy milk",
                user_id=self.user_id,
                jwt_token=self.jwt_token
            )

            # Verify create_task was called
            mock_create.assert_called_once_with(self.user_id, "buy milk", None, self.jwt_token)

            # Verify the response structure
            self.assertEqual(result["skill"], "create_task")
            self.assertTrue(result["success"])
            self.assertIn("created successfully", result["message"])

    def test_process_request_list_tasks_intent(self):
        """Test process_request with list_tasks intent."""
        with patch.object(self.skills, 'list_tasks') as mock_list:
            mock_list.return_value = {"data": {"tasks": [{"id": "1", "title": "Task 1"}]}}

            result = self.skills.process_request(
                user_input="Show my tasks",
                user_id=self.user_id,
                jwt_token=self.jwt_token
            )

            # Verify list_tasks was called
            mock_list.assert_called_once_with(self.user_id, self.jwt_token)

            # Verify the response structure
            self.assertEqual(result["skill"], "list_tasks")
            self.assertTrue(result["success"])
            self.assertIn("1 tasks", result["message"])

    def test_process_request_complete_task_intent(self):
        """Test process_request with complete_task intent."""
        with patch.object(self.skills, 'list_tasks') as mock_list, \
             patch.object(self.skills, 'complete_task') as mock_complete:

            mock_list.return_value = {
                "data": {
                    "tasks": [
                        {"id": "task-123", "title": "buy milk", "completed": False}
                    ]
                }
            }
            mock_complete.return_value = {"id": "task-123", "title": "buy milk", "completed": True}

            result = self.skills.process_request(
                user_input="Complete buy milk",
                user_id=self.user_id,
                jwt_token=self.jwt_token
            )

            # Verify list_tasks was called to find the task
            mock_list.assert_called_once_with(self.user_id, self.jwt_token)

            # Verify complete_task was called with the correct task ID
            mock_complete.assert_called_once_with(self.user_id, "task-123", completed=True, jwt_token=self.jwt_token)

            # Verify the response structure
            self.assertEqual(result["skill"], "complete_task")
            self.assertTrue(result["success"])
            self.assertIn("marked as complete", result["message"])

    def test_process_request_unknown_intent(self):
        """Test process_request with unknown intent."""
        result = self.skills.process_request(
            user_input="Unknown command",
            user_id=self.user_id,
            jwt_token=self.jwt_token
        )

        # Verify the response structure for unknown intent
        self.assertEqual(result["skill"], "unknown")
        self.assertFalse(result["success"])
        self.assertIn("could not understand", result["message"].lower())

    def test_make_request_internal_method(self):
        """Test the internal _make_request method."""
        with patch.object(self.skills.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = {"status": "ok"}
            mock_request.return_value = mock_response

            result = self.skills._make_request(
                method="GET",
                endpoint="/test",
                jwt_token=self.jwt_token
            )

            # Verify the request was made correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            method, url = args

            self.assertEqual(method, "GET")
            self.assertEqual(url, "http://test-api:8000/api/test")

            # Verify headers
            self.assertIn("Authorization", kwargs['headers'])
            self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.jwt_token}")
            self.assertEqual(kwargs['headers']['Content-Type'], "application/json")


if __name__ == '__main__':
    unittest.main()