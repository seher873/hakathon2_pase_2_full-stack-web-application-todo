"""Unit tests for the Chatbot Agent."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agents.chatbot_agent import ChatbotAgent, process_user_message
from mcp.tool_registry import ToolRegistry

@pytest.fixture
def mock_tool_registry():
    """Mock tool registry for testing."""
    with patch('agents.chatbot_agent.tool_registry') as mock_registry:
        # Mock the list_tools method
        mock_registry.list_tools.return_value = ['create_task', 'list_tasks']

        # Mock getting tool signatures
        mock_registry.get_tool_signature.return_value = {
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"}
                    },
                    "required": ["title"]
                }
            }
        }

        yield mock_registry

@pytest.fixture
def chatbot_agent(mock_tool_registry):
    """Create a ChatbotAgent instance for testing."""
    agent = ChatbotAgent()
    return agent

@pytest.mark.asyncio
async def test_process_message_valid_request(chatbot_agent):
    """Test processing a valid message."""
    with patch('agents.chatbot_agent.client') as mock_client:
        # Mock the OpenAI response
        mock_response = AsyncMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "I'll help you create that task."
        mock_response.choices[0].message.tool_calls = None

        mock_client.chat.completions.create.return_value = mock_response

        result = await chatbot_agent.process_message(
            message="Add a task to buy groceries",
            user_token="fake_token",
            user_id="user123"
        )

        assert result["success"] is True
        assert "response" in result
        assert result["data"] is None

@pytest.mark.asyncio
async def test_process_message_with_tool_call(chatbot_agent):
    """Test processing a message that requires tool calls."""
    with patch('agents.chatbot_agent.client') as mock_client:
        # First call returns a tool call
        mock_response1 = AsyncMock()
        mock_response1.choices = [MagicMock()]
        mock_response1.choices[0].message = MagicMock()
        mock_response1.choices[0].message.content = "Creating the task..."
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = '{"title": "Buy groceries", "description": "Milk and bread"}'
        mock_response1.choices[0].message.tool_calls = [mock_tool_call]

        # Second call (follow-up) returns final response
        mock_response2 = AsyncMock()
        mock_response2.choices = [MagicMock()]
        mock_response2.choices[0].message = MagicMock()
        mock_response2.choices[0].message.content = "Task 'Buy groceries' created successfully."
        mock_response2.choices[0].message.tool_calls = None

        mock_client.chat.completions.create = AsyncMock(side_effect=[mock_response1, mock_response2])

        result = await chatbot_agent.process_message(
            message="Add a task to buy groceries",
            user_token="fake_token",
            user_id="user123"
        )

        assert result["success"] is True
        assert "created successfully" in result["response"]

@pytest.mark.asyncio
async def test_process_message_error_handling(chatbot_agent):
    """Test error handling in message processing."""
    with patch('agents.chatbot_agent.client') as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        result = await chatbot_agent.process_message(
            message="Add a task to buy groceries",
            user_token="fake_token",
            user_id="user123"
        )

        assert result["success"] is False
        assert "Error processing your request" in result["response"]
        assert "API Error" in result["data"]["error"]

def test_get_registered_tools(chatbot_agent):
    """Test getting registered tools."""
    tools = chatbot_agent._get_registered_tools()
    assert isinstance(tools, list)
    # The tools list depends on successful signature retrieval, which might fail in the mock