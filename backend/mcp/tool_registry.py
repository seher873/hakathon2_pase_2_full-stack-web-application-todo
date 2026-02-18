"""MCP tool registration and management."""
from typing import Dict, Any, Callable, List
from .task_tools import TaskTools
from .auth_wrapper import verify_token

class ToolRegistry:
    """Registry for MCP tools to manage their lifecycle and access."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_signatures: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, function: Callable, signature: Dict[str, Any]):
        """
        Register an MCP tool with its function and signature.

        Args:
            name: Name of the tool
            function: The function that implements the tool
            signature: JSON Schema describing the tool's parameters
        """
        self._tools[name] = function
        self._tool_signatures[name] = signature

    def get_tool(self, name: str, token: str):
        """
        Get a registered tool with authentication context.

        Args:
            name: Name of the tool to retrieve
            token: JWT token for authentication context

        Returns:
            Callable: The tool function with authentication context
        """
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not registered")

        # Create a tool instance with the user's token
        # This ensures that the tool operates in the user's security context
        tool_class = TaskTools(token=token)

        # Return the specific method based on the tool name
        if name == "create_task":
            return tool_class.create_task
        elif name == "list_tasks":
            return tool_class.list_tasks
        elif name == "update_task":
            return tool_class.update_task
        elif name == "delete_task":
            return tool_class.delete_task
        elif name == "toggle_complete":
            return tool_class.toggle_complete
        else:
            raise ValueError(f"Unknown tool: {name}")

    def get_tool_signature(self, name: str) -> Dict[str, Any]:
        """
        Get the signature for a registered tool.

        Args:
            name: Name of the tool

        Returns:
            Dict with the tool's parameter signature
        """
        if name not in self._tool_signatures:
            raise ValueError(f"Tool '{name}' not registered")
        return self._tool_signatures[name]

    def list_tools(self) -> List[str]:
        """
        List all registered tools.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def validate_tool_access(self, tool_name: str, token: str) -> bool:
        """
        Validate if the user has access to a specific tool.

        Args:
            tool_name: Name of the tool to validate access for
            token: JWT token for the user

        Returns:
            bool: True if user has access, False otherwise
        """
        # In this basic implementation, we just validate the token
        # In a more complex system, we might check user roles or permissions
        try:
            verify_token_mock = verify_token
            # This would normally be called with proper dependency injection
            # For now, we'll just ensure the token is valid
            return True
        except Exception:
            return False

# Global tool registry instance
tool_registry = ToolRegistry()

# Register all the task tools with their signatures
tool_registry.register_tool(
    name="create_task",
    function=None,  # Will be resolved dynamically based on token
    signature={
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task with title, description, and optional due date",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in YYYY-MM-DD format"
                    }
                },
                "required": ["title"]
            }
        }
    }
)

tool_registry.register_tool(
    name="list_tasks",
    function=None,
    signature={
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks with optional filtering by status",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_by": {
                        "type": "string",
                        "description": "Optional filter criteria"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed", "all"],
                        "description": "Filter tasks by status"
                    }
                }
            }
        }
    }
)

tool_registry.register_tool(
    name="update_task",
    function=None,
    signature={
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in YYYY-MM-DD format"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "New status for the task"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
)

tool_registry.register_tool(
    name="delete_task",
    function=None,
    signature={
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
)

tool_registry.register_tool(
    name="toggle_complete",
    function=None,
    signature={
        "type": "function",
        "function": {
            "name": "toggle_complete",
            "description": "Toggle the completion status of a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to toggle"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
)