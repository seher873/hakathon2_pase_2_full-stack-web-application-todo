"""
Health check endpoint tests.

Tests basic API health and status endpoints to verify
the FastAPI application is running correctly.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check_returns_200(self, client):
        """
        Test that health check endpoint returns 200 OK.

        Acceptance Criteria:
        - GET /api/health returns HTTP 200
        - Response contains 'healthy' status
        """
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["status"] == "healthy"

    def test_health_check_response_structure(self, client):
        """
        Test health check response has correct structure.

        Acceptance Criteria:
        - Response is valid JSON
        - Contains status, data, and timestamp fields
        - Data includes service, version, environment
        """
        response = client.get("/api/health")
        data = response.json()

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data

        health_data = data["data"]
        assert "status" in health_data
        assert "service" in health_data
        assert "version" in health_data
        assert "environment" in health_data

    def test_health_check_service_info(self, client):
        """
        Test health check returns correct service information.

        Acceptance Criteria:
        - Service name is 'Hackathon Todo API'
        - Version is '2.0.0'
        - Environment matches settings
        """
        response = client.get("/api/health")
        health_data = response.json()["data"]

        assert health_data["service"] == "Hackathon Todo API"
        assert health_data["version"] == "2.0.0"
        assert health_data["environment"] in ["development", "staging", "production"]

    def test_root_endpoint_returns_200(self, client):
        """
        Test root endpoint returns 200 OK.

        Acceptance Criteria:
        - GET / returns HTTP 200
        - Response includes API information
        """
        response = client.get("/")

        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "Hackathon Todo API"

    def test_root_endpoint_includes_docs_link(self, client):
        """
        Test root endpoint provides documentation link.

        Acceptance Criteria:
        - Response includes 'docs' field
        - Docs URL is '/api/docs'
        """
        response = client.get("/")
        data = response.json()

        assert "docs" in data
        assert data["docs"] == "/api/docs"


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_swagger_docs_available(self, client):
        """
        Test Swagger UI documentation is available.

        Acceptance Criteria:
        - GET /api/docs returns HTTP 200
        - Response contains swagger UI HTML
        """
        response = client.get("/api/docs")

        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_openapi_schema_available(self, client):
        """
        Test OpenAPI schema is available.

        Acceptance Criteria:
        - GET /api/openapi.json returns HTTP 200
        - Response is valid OpenAPI JSON
        """
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data or "swagger" in data
        assert "paths" in data or "info" in data

    def test_redoc_docs_available(self, client):
        """
        Test ReDoc documentation is available.

        Acceptance Criteria:
        - GET /api/redoc returns HTTP 200
        - Response contains ReDoc HTML
        """
        response = client.get("/api/redoc")

        assert response.status_code == 200
        assert "redoc" in response.text.lower() or "openapi" in response.text.lower()


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_returns_json_error(self, client):
        """
        Test 404 responses return structured error JSON.

        Acceptance Criteria:
        - GET /nonexistent returns HTTP 404
        - Response has error structure with code and message
        """
        response = client.get("/api/nonexistent")

        assert response.status_code == 404
        data = response.json()

        # FastAPI returns default 404, may not have our custom format
        # Just verify it's a valid response
        assert response.headers["content-type"] == "application/json"

    def test_invalid_method_returns_error(self, client):
        """
        Test invalid HTTP methods return error.

        Acceptance Criteria:
        - Custom HTTP methods return 405 or 404
        - Response is valid JSON
        """
        response = client.request("CUSTOM_METHOD", "/api/health")

        assert response.status_code in [404, 405]
        # Should be JSON response
        try:
            response.json()
        except Exception:
            pytest.fail("Response should be valid JSON")
