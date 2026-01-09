"""
AI Skills API endpoints.

Provides endpoints for the AI skills layer to process natural language requests.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
import logging

from src.api.deps import get_current_user_id
from src.middleware import SuccessResponse
from .todo_skills import todo_skills

# Configure logging
logger = logging.getLogger(__name__)

# Create router for AI skills endpoints
router = APIRouter(prefix="/ai", tags=["ai-skills"])


@router.post("/process", summary="Process Natural Language Request")
async def process_natural_language(
    request: dict,
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Process a natural language request and execute the appropriate skill.

    Args:
        request: Contains 'input' (user's natural language request)
        current_user_id: User ID extracted from JWT token

    Returns:
        Structured response with the result of the operation
    """
    try:
        user_input = request.get("input", "")
        if not user_input:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input is required"
            )

        # Process the natural language request using the skills
        result = todo_skills.process_request(
            user_input=user_input,
            user_id=current_user_id
        )

        # Log the processed request
        logger.info(f"Processed AI request for user {current_user_id}: {user_input} -> {result['skill']}")

        return SuccessResponse(data=result).to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing AI request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing AI request: {str(e)}"
        )


@router.get("/skills", summary="Get Available Skills")
async def get_available_skills(
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Get a list of available AI skills.

    Args:
        current_user_id: User ID extracted from JWT token

    Returns:
        List of available skills
    """
    skills_list = [
        {
            "name": "create_task",
            "description": "Create a new task",
            "examples": [
                "Add buy milk",
                "Create task finish report",
                "New task call mom"
            ]
        },
        {
            "name": "list_tasks",
            "description": "List all your tasks",
            "examples": [
                "Show my tasks",
                "List my tasks",
                "What tasks do I have?"
            ]
        },
        {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "examples": [
                "Complete buy milk",
                "Finish report task",
                "Mark grocery shopping done"
            ]
        }
    ]

    return SuccessResponse(data=skills_list).to_dict()