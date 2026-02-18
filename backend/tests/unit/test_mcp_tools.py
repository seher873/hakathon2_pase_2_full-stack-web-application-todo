"""Unit tests for MCP Tools."""
import pytest
from unittest.mock import patch, MagicMock
from mcp.task_tools import TaskTools


@pytest.fixture
def task_tools():
    """Create a TaskTools instance for testing."""
    return TaskTools(token="fake_token")


def test_task_tools_initialization():
    """Test TaskTools initialization."""
    tools = TaskTools(token="test_token")

    assert tools.token == "test_token"
    assert "Authorization" in tools.headers
    assert tools.headers["Authorization"] == "Bearer test_token"


@patch('mcp.task_tools.requests.post')
def test_create_task_success(mock_post, task_tools):
    """Test successful task creation."""
    # Mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Task",
        "status": "pending"
    }
    mock_post.return_value = mock_response

    result = task_tools.create_task(
        title="Test Task",
        description="Test Description"
    )

    assert result["id"] == 1
    assert result["title"] == "Test Task"
    mock_post.assert_called_once()


@patch('mcp.task_tools.requests.get')
def test_list_tasks_success(mock_get, task_tools):
    """Test successful task listing."""
    # Mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {"id": 1, "title": "Task 1", "status": "pending"},
        {"id": 2, "title": "Task 2", "status": "completed"}
    ]
    mock_get.return_value = mock_response

    result = task_tools.list_tasks()

    assert len(result) == 2
    assert result[0]["title"] == "Task 1"
    mock_get.assert_called_once()


@patch('mcp.task_tools.requests.put')
def test_update_task_success(mock_put, task_tools):
    """Test successful task update."""
    # Mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": 1,
        "title": "Updated Task",
        "status": "pending"
    }
    mock_put.return_value = mock_response

    result = task_tools.update_task(
        task_id=1,
        title="Updated Task"
    )

    assert result["id"] == 1
    assert result["title"] == "Updated Task"
    mock_put.assert_called_once()


@patch('mcp.task_tools.requests.delete')
def test_delete_task_success(mock_delete, task_tools):
    """Test successful task deletion."""
    # Mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"success": True, "task_id": 1}
    mock_delete.return_value = mock_response

    result = task_tools.delete_task(task_id=1)

    assert result["success"] is True
    assert result["task_id"] == 1
    mock_delete.assert_called_once()


@patch('mcp.task_tools.requests.get')
@patch('mcp.task_tools.requests.patch')
def test_toggle_complete_success(mock_patch, mock_get, task_tools):
    """Test successful task toggle."""
    # Mock responses
    mock_get_response = MagicMock()
    mock_get_response.raise_for_status.return_value = None
    mock_get_response.json.return_value = {
        "id": 1, "title": "Test Task", "status": "pending"
    }
    mock_get.return_value = mock_get_response

    mock_patch_response = MagicMock()
    mock_patch_response.raise_for_status.return_value = None
    mock_patch_response.json.return_value = {
        "id": 1, "title": "Test Task", "status": "completed"
    }
    mock_patch.return_value = mock_patch_response

    result = task_tools.toggle_complete(task_id=1)

    assert result["status"] == "completed"
    mock_get.assert_called_once()
    mock_patch.assert_called_once()


@patch('mcp.task_tools.requests.post')
def test_create_task_error(mock_post, task_tools):
    """Test task creation with error."""
    # Mock error response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("Request failed")
    mock_post.return_value = mock_response

    with pytest.raises(Exception):
        task_tools.create_task(title="Test Task")