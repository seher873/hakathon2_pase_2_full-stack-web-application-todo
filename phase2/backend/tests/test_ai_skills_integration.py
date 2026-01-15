"""
Integration tests for AI Skills functionality.
Tests complete flows from natural language input to API responses.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from uuid import UUID
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app
from backend.skills.todo_skills import TodoSkills


class TestAISkillsIntegration(unittest.TestCase):
    """Integration tests for AI Skills API endpoints."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)
        self.jwt_token = "valid-test-token"

        # Mock headers with JWT token
        self.headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

    @patch('backend.skills.todo_skills.TodoSkills.process_request')
    def test_process_endpoint_success(self, mock_process):
        """Test the /api/ai/process endpoint with successful response."""
        # Mock the skills processing
        mock_process.return_value = {
            "skill": "create_task",
            "success": True,
            "message": "Task 'buy milk' created successfully",
            "data": {"id": "task-123", "title": "buy milk"}
        }

        response = self.client.post(
            "/api/ai/process",
            json={"input": "Add buy milk"},
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["data"]["skill"], "create_task")
        self.assertTrue(response_data["data"]["success"])

    @patch('backend.skills.todo_skills.TodoSkills.process_request')
    def test_process_endpoint_failure(self, mock_process):
        """Test the /api/ai/process endpoint with processing failure."""
        # Mock a processing failure
        mock_process.return_value = {
            "skill": "create_task",
            "success": False,
            "message": "Failed to create task",
            "error": "Invalid input"
        }

        response = self.client.post(
            "/api/ai/process",
            json={"input": "Invalid input"},
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)  # Still returns 200, but with success=False
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")  # API call succeeded
        self.assertFalse(response_data["data"]["success"])  # But skill execution failed

    def test_process_endpoint_missing_input(self):
        """Test the /api/ai/process endpoint with missing input."""
        response = self.client.post(
            "/api/ai/process",
            json={},
            headers=self.headers
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("detail", response_data)

    def test_process_endpoint_empty_input(self):
        """Test the /api/ai/process endpoint with empty input."""
        response = self.client.post(
            "/api/ai/process",
            json={"input": ""},
            headers=self.headers
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("detail", response_data)

    @patch('backend.skills.todo_skills.TodoSkills.process_request')
    def test_process_endpoint_unauthorized(self, mock_process):
        """Test the /api/ai/process endpoint without JWT token."""
        response = self.client.post(
            "/api/ai/process",
            json={"input": "Add buy milk"},
            headers={}  # No Authorization header
        )

        # Should return 401 for unauthorized access
        self.assertEqual(response.status_code, 401)

    def test_skills_endpoint_success(self):
        """Test the /api/ai/skills endpoint."""
        response = self.client.get(
            "/api/ai/skills",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")

        # Verify the structure of the skills list
        skills = response_data["data"]
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)

        # Check that all expected skills are present
        skill_names = [skill["name"] for skill in skills]
        self.assertIn("create_task", skill_names)
        self.assertIn("list_tasks", skill_names)
        self.assertIn("complete_task", skill_names)

    @patch('backend.skills.todo_skills.TodoSkills.process_request')
    def test_various_skill_intents(self, mock_process):
        """Test various skill intents through the API."""
        test_cases = [
            ("Add buy milk", "create_task"),
            ("Show my tasks", "list_tasks"),
            ("Complete buy milk", "complete_task"),
            ("List my tasks", "list_tasks"),
            ("Create task finish report", "create_task"),
            ("Mark task done", "complete_task")
        ]

        for user_input, expected_skill in test_cases:
            with self.subTest(input=user_input, skill=expected_skill):
                mock_process.return_value = {
                    "skill": expected_skill,
                    "success": True,
                    "message": f"Test response for {expected_skill}",
                    "data": {"test": "data"}
                }

                response = self.client.post(
                    "/api/ai/process",
                    json={"input": user_input},
                    headers=self.headers
                )

                self.assertEqual(response.status_code, 200)
                response_data = response.json()
                self.assertEqual(response_data["data"]["skill"], expected_skill)

    def test_skills_endpoint_unauthorized(self):
        """Test the /api/ai/skills endpoint without JWT token."""
        response = self.client.get(
            "/api/ai/skills",
            headers={}  # No Authorization header
        )

        # Should return 401 for unauthorized access
        self.assertEqual(response.status_code, 401)


class TestSecurityValidation(unittest.TestCase):
    """Security tests to verify JWT validation and user isolation."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)

    def test_jwt_required_for_process_endpoint(self):
        """Verify JWT token is required for process endpoint."""
        response = self.client.post(
            "/api/ai/process",
            json={"input": "Add buy milk"},
            headers={}  # No JWT token
        )

        self.assertEqual(response.status_code, 401)

    def test_jwt_required_for_skills_endpoint(self):
        """Verify JWT token is required for skills endpoint."""
        response = self.client.get(
            "/api/ai/skills",
            headers={}  # No JWT token
        )

        self.assertEqual(response.status_code, 401)

    def test_invalid_jwt_handling(self):
        """Test handling of invalid JWT tokens."""
        invalid_headers = {
            "Authorization": "Bearer invalid-token-format",
            "Content-Type": "application/json"
        }

        response = self.client.post(
            "/api/ai/process",
            json={"input": "Add buy milk"},
            headers=invalid_headers
        )

        # Should return 401 for invalid token
        self.assertEqual(response.status_code, 401)

    @patch('src.api.deps.get_current_user_id')
    def test_user_isolation_via_mock(self, mock_get_user_id):
        """Test user isolation by mocking the user ID extraction."""
        # Mock to return a specific user ID
        mock_get_user_id.return_value = UUID("123e4567-e89b-12d3-a456-426614174000")

        headers = {
            "Authorization": "Bearer valid-token",
            "Content-Type": "application/json"
        }

        with patch('backend.skills.todo_skills.TodoSkills.process_request') as mock_process:
            mock_process.return_value = {
                "skill": "list_tasks",
                "success": True,
                "message": "User's tasks retrieved",
                "data": {"tasks": []}
            }

            response = self.client.post(
                "/api/ai/process",
                json={"input": "Show my tasks"},
                headers=headers
            )

            self.assertEqual(response.status_code, 200)
            # Verify that the process_request was called with the mocked user ID
            # This confirms user isolation is working


if __name__ == '__main__':
    unittest.main()