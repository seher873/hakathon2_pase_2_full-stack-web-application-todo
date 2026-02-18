"""Configuration for the AI Chatbot Agent."""
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Configuration model for the AI Chatbot Agent."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    openai_temperature: float = 0.7  # Controls randomness in responses
    openai_max_tokens: int = 1000    # Maximum tokens in response

    # Agent Behavior Configuration
    agent_name: str = "TodoAssistant"
    agent_instructions: str = """
    You are a helpful todo list assistant. Your job is to understand user requests for todo list management and use the appropriate tools to fulfill these requests.

    When a user asks to create a task, use the create_task tool.
    When a user asks to see their tasks, use the list_tasks tool.
    When a user asks to update a task, use the update_task or toggle_complete tool.
    When a user asks to delete a task, use the delete_task tool.

    Always ask clarifying questions if the user's request is ambiguous.
    Be concise and helpful in your responses.
    """

    # MCP Tools Configuration
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    # Task Management Configuration
    max_tasks_per_user: int = 100  # Maximum number of tasks per user
    enable_natural_language_processing: bool = True
    enable_task_suggestions: bool = False

    # Security Configuration
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "default_secret_key_for_development")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Performance Configuration
    enable_caching: bool = True
    cache_ttl_seconds: int = 300  # 5 minutes
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

class ConversationConfig(BaseModel):
    """Configuration for conversation management."""

    # Conversation state management
    max_conversation_history: int = 20  # Maximum number of messages to keep in context
    conversation_timeout_minutes: int = 30  # Minutes before conversation context expires

    # Context awareness
    enable_context_awareness: bool = True
    context_lookback_messages: int = 5  # Number of previous messages to consider for context

def get_agent_config() -> AgentConfig:
    """Get the agent configuration instance."""
    return AgentConfig()

def get_conversation_config() -> ConversationConfig:
    """Get the conversation configuration instance."""
    return ConversationConfig()

# Default configuration instances
default_agent_config = get_agent_config()
default_conversation_config = get_conversation_config()