"""API routes for the AI chatbot functionality."""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
import json
import logging
from typing import Dict, Any, AsyncGenerator
from mcp.auth_wrapper import verify_token, forward_token_to_mcp_tools
from agents.chatbot_agent import process_user_message
from mcp.tool_models import ChatMessageModel, ChatResponseModel

# Set up logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponseModel)
async def chat_message(
    message_data: ChatMessageModel,
    token: str = Depends(verify_token)
) -> ChatResponseModel:
    """
    Process a single chat message from the user.

    Args:
        message_data: The user's message and metadata
        token: Verified JWT token for authentication

    Returns:
        ChatResponseModel: The agent's response to the user
    """
    try:
        # Forward the token to MCP tools to maintain user context
        user_token = forward_token_to_mcp_tools(token)

        # Process the user message through the agent
        result = await process_user_message(
            message=message_data.message,
            user_token=user_token,
            user_id=message_data.user_id
        )

        logger.info(f"Processed chat message for user {message_data.user_id}: {message_data.message[:50]}...")

        return ChatResponseModel(
            response=result.get("response", "I processed your request successfully."),
            success=result.get("success", True),
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )

@router.post("/stream")
async def chat_stream(
    message_data: ChatMessageModel,
    token: str = Depends(verify_token)
) -> StreamingResponse:
    """
    Stream chat responses back to the client.

    Args:
        message_data: The user's message and metadata
        token: Verified JWT token for authentication

    Returns:
        StreamingResponse: Streaming response of the agent's output
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            # Forward the token to MCP tools to maintain user context
            user_token = forward_token_to_mcp_tools(token)

            # Process the user message through the agent with streaming
            async for chunk in stream_process_user_message(
                message=message_data.message,
                user_token=user_token,
                user_id=message_data.user_id
            ):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            logger.error(f"Error in chat streaming: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

async def stream_process_user_message(
    message: str,
    user_token: str,
    user_id: str
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Process a user message with streaming response capability.

    Args:
        message: The user's message
        user_token: User's JWT token for MCP tools
        user_id: The ID of the user

    Yields:
        Dict: Chunks of the response
    """
    try:
        # This is a simplified streaming implementation
        # In a real implementation, this would connect to OpenAI's streaming API
        result = await process_user_message(
            message=message,
            user_token=user_token,
            user_id=user_id
        )

        # Yield the result in chunks for streaming
        yield {"type": "response", "content": result.get("response", "")}
        if result.get("data"):
            yield {"type": "data", "content": result.get("data")}
        yield {"type": "done", "content": ""}
    except Exception as e:
        logger.error(f"Error in streaming message processing: {str(e)}")
        yield {"type": "error", "content": f"Error processing message: {str(e)}"}

@router.get("/health")
async def chat_health() -> Dict[str, str]:
    """
    Health check endpoint for the chat API.

    Returns:
        Dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "chatbot-agent-api",
        "version": "1.0.0"
    }

# Additional routes can be added here as needed:
# @router.get("/history") - to get conversation history
# @router.post("/clear") - to clear conversation context
# @router.get("/tools") - to list available tools