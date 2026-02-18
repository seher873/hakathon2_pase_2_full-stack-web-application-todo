"""OpenAI Agent for the Todo Chatbot."""
import os
import asyncio
import logging
from typing import Dict, Any, AsyncGenerator, Optional
from openai import AsyncOpenAI
from ..mcp.tool_registry import tool_registry

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatbotAgent:
    """AI agent that processes natural language and uses MCP tools."""

    def __init__(self):
        self.client = client
        self.tools = self._get_registered_tools()

    def _get_registered_tools(self) -> list:
        """Get the list of registered tools in OpenAI-compatible format."""
        tools_list = []
        for tool_name in tool_registry.list_tools():
            try:
                tool_signature = tool_registry.get_tool_signature(tool_name)
                tools_list.append(tool_signature)
            except Exception as e:
                print(f"Error getting tool signature for {tool_name}: {str(e)}")
        return tools_list

    async def process_message(self, message: str, user_token: str, user_id: str) -> Dict[str, Any]:
        """
        Process a user message using OpenAI and MCP tools.

        Args:
            message: The user's natural language message
            user_token: User's JWT token for authentication
            user_id: The ID of the user

        Returns:
            Dict with response, success status, and optional data
        """
        logger.info(f"Processing message for user {user_id}: {message[:50]}...")

        try:
            # Create a conversation with tool use
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful todo list assistant. Use the available functions to manage tasks when the user asks. Only call functions when the user is trying to create, update, list, or delete tasks."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                tools=self.tools,
                tool_choice="auto"
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                logger.info(f"Executing {len(tool_calls)} tool calls for user {user_id}")

                # Execute tool calls
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)

                    logger.info(f"Calling tool {function_name} with args: {function_args}")

                    # Get the tool function with user context
                    try:
                        tool_func = tool_registry.get_tool(function_name, user_token)

                        # Call the tool with the provided arguments
                        result = tool_func(**function_args)

                        logger.info(f"Tool {function_name} executed successfully")

                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "result": result
                        })
                    except Exception as e:
                        logger.error(f"Error executing tool {function_name}: {str(e)}")
                        return {
                            "response": f"Error executing tool {function_name}: {str(e)}",
                            "success": False,
                            "data": {"error": str(e)}
                        }

                # If there were tool calls, create a follow-up request with the results
                followup_response = await client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful todo list assistant. Use the available functions to manage tasks when the user asks."
                        },
                        {
                            "role": "user",
                            "content": message
                        },
                        {
                            "role": "assistant",
                            "content": response_message.content or ""
                        }
                    ] + [
                        {
                            "role": "tool",
                            "content": str(tool_result["result"]),
                            "tool_call_id": tool_result["tool_call_id"]
                        }
                        for tool_result in tool_results
                    ]
                )

                # Extract final response
                final_content = followup_response.choices[0].message.content
                logger.info(f"Completed processing for user {user_id}")

                return {
                    "response": final_content or "Operation completed successfully.",
                    "success": True,
                    "data": {result["tool_call_id"]: result["result"] for result in tool_results}
                }
            else:
                logger.info(f"No tool calls needed, responding directly to user {user_id}")

                # If no tool calls were made, return the assistant's response
                return {
                    "response": response_message.content or "I'm not sure how I can help with that.",
                    "success": True,
                    "data": None
                }

        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {str(e)}")
            return {
                "response": f"Error processing your request: {str(e)}",
                "success": False,
                "data": {"error": str(e)}
            }

    async def stream_process_message(self, message: str, user_token: str, user_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process a user message with streaming response.

        Args:
            message: The user's natural language message
            user_token: User's JWT token for authentication
            user_id: The ID of the user

        Yields:
            Dict: Chunks of the response
        """
        try:
            # Create a streaming conversation with tool use
            stream = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful todo list assistant. Use the available functions to manage tasks when the user asks."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                tools=self.tools,
                tool_choice="auto",
                stream=True
            )

            # Process the stream
            async for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    yield {"type": "content", "content": delta.content}

                if delta and delta.tool_calls:
                    # Process tool calls when they appear in the stream
                    for tool_call in delta.tool_calls:
                        if tool_call.function:
                            # For now, just yield the tool call info
                            yield {
                                "type": "tool_call",
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }

            yield {"type": "done", "content": ""}

        except Exception as e:
            yield {"type": "error", "content": f"Error: {str(e)}"}

# Global instance of the agent
chatbot_agent = ChatbotAgent()

# Async wrapper functions for use in API routes
async def process_user_message(message: str, user_token: str, user_id: str) -> Dict[str, Any]:
    """
    Wrapper function to process a user message.

    Args:
        message: The user's natural language message
        user_token: User's JWT token for authentication
        user_id: The ID of the user

    Returns:
        Dict with response, success status, and optional data
    """
    return await chatbot_agent.process_message(message, user_token, user_id)

async def stream_process_user_message(message: str, user_token: str, user_id: str) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Wrapper function to stream process a user message.

    Args:
        message: The user's natural language message
        user_token: User's JWT token for authentication
        user_id: The ID of the user

    Yields:
        Dict: Chunks of the response
    """
    async for chunk in chatbot_agent.stream_process_message(message, user_token, user_id):
        yield chunk