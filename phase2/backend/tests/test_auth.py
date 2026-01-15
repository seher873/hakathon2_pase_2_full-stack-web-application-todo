"""
Authentication endpoint tests.

Tests user signup and login functionality to verify
the authentication system is working correctly.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from main import app
from src.db import get_async_session
from src.models.user import User


@pytest.fixture
def client(get_test_async_session):
    """Create test client with database override."""
    app.dependency_overrides[get_async_session] = get_test_async_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


class TestSignup:
    """Tests for user signup endpoint."""

    def test_signup_success(self, client):
        """
        Test successful user signup.

        Acceptance Criteria:
        - POST /api/auth/signup with valid data returns 201
        - Response contains JWT token and user info
        - User is created in database
        """
        signup_data = {
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }

        response = client.post("/api/auth/signup", json=signup_data)

        assert response.status_code == 201
        data = response.json()
        
        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        assert "token" in data["data"]
        assert "user" in data["data"]
        
        user_data = data["data"]["user"]
        assert user_data["email"] == "newuser@example.com"
        assert "id" in user_data
        assert "created_at" in user_data

    def test_signup_with_invalid_email(self, client):
        """
        Test signup with invalid email format.

        Acceptance Criteria:
        - POST /api/auth/signup with invalid email returns 400
        - Response contains validation error
        """
        signup_data = {
            "email": "invalid-email",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }

        response = client.post("/api/auth/signup", json=signup_data)

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_signup_with_weak_password(self, client):
        """
        Test signup with weak password.

        Acceptance Criteria:
        - POST /api/auth/signup with weak password returns 400
        - Response contains validation error
        """
        signup_data = {
            "email": "user@example.com",
            "password": "weak",
            "password_confirm": "weak"
        }

        response = client.post("/api/auth/signup", json=signup_data)

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_signup_password_mismatch(self, client):
        """
        Test signup with mismatched passwords.

        Acceptance Criteria:
        - POST /api/auth/signup with mismatched passwords returns 400
        - Response contains validation error
        """
        signup_data = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "DifferentPassword123!"
        }

        response = client.post("/api/auth/signup", json=signup_data)

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_signup_duplicate_email(self, client):
        """
        Test signup with already registered email.

        Acceptance Criteria:
        - POST /api/auth/signup with existing email returns 409
        - Response contains conflict error
        """
        # First signup
        signup_data = {
            "email": "duplicate@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }

        response = client.post("/api/auth/signup", json=signup_data)
        assert response.status_code == 201

        # Second signup with same email
        response = client.post("/api/auth/signup", json=signup_data)

        assert response.status_code == 409
        data = response.json()
        assert "detail" in data


class TestLogin:
    """Tests for user login endpoint."""

    def test_login_success(self, client):
        """
        Test successful user login.

        Acceptance Criteria:
        - POST /api/auth/login with valid credentials returns 200
        - Response contains JWT token and user info
        """
        # First, create a user
        signup_data = {
            "email": "loginuser@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }
        signup_response = client.post("/api/auth/signup", json=signup_data)
        assert signup_response.status_code == 201

        # Then try to login
        login_data = {
            "email": "loginuser@example.com",
            "password": "SecurePassword123!"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert data["status"] == "success"
        assert "data" in data
        assert "token" in data["data"]
        assert "user" in data["data"]
        
        user_data = data["data"]["user"]
        assert user_data["email"] == "loginuser@example.com"
        assert "id" in user_data

    def test_login_invalid_credentials(self, client):
        """
        Test login with invalid credentials.

        Acceptance Criteria:
        - POST /api/auth/login with wrong password returns 400
        - POST /api/auth/login with non-existent user returns 400
        """
        # Try to login with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anyPassword123!"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

        # Create a user first
        signup_data = {
            "email": "testlogin@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }
        signup_response = client.post("/api/auth/signup", json=signup_data)
        assert signup_response.status_code == 201

        # Try to login with wrong password
        login_data = {
            "email": "testlogin@example.com",
            "password": "wrongPassword123!"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data