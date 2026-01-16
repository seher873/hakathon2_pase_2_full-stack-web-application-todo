"""
AI Skills API endpoints.
Exposes the AI skills functionality through HTTP endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from uuid import UUID

from ..api.deps import get_current_user_id
from ..middleware import SuccessResponse
from ..schemas.error import ERROR_MESSAGES

# Import the TodoSkills class - wrap in try/except to avoid circular imports
try:
    from .todo_skills import TodoSkills
except ImportError:
    # Fallback for when the skills module is not available
    class TodoSkills:
        def __init__(self, base_url: str = "http://localhost:8000/api"):
            pass

        def process_request(self, user_input: str, user_id: str, jwt_token: str) -> Dict[str, Any]:
            raise NotImplementedError("TodoSkills module not available")

# Create router for AI skills endpoints
router = APIRouter(prefix="/ai", tags=["ai-skills"])


@router.post(
    "/process",
    summary="Process AI Request",
    description="Process natural language requests and convert to appropriate actions"
)
async def process_ai_request(
    request_data: Dict[str, Any],
    current_user_id: UUID = Depends(get_current_user_id),
):
    """
    Process natural language requests from the AI interface.

    Args:
        request_data: Contains 'input' field with natural language text
        current_user_id: User ID extracted from JWT token (via dependency)

    Returns:
        Processed result based on the natural language input
    """
    try:
        # Extract the input text
        user_input = request_data.get("input", "").strip()
        if not user_input:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.get("INVALID_REQUEST", "Input text is required")
            )

        # Get JWT token from the request context (this would come from the auth middleware)
        # For now, we'll get it from the dependency
        # In a real implementation, we'd extract this properly

        # Initialize the skills processor
        skills = TodoSkills(base_url="http://localhost:8000/api")

        # Process the request using the skills
        # Note: In a real implementation, we'd need to pass the actual JWT token
        # For now, we'll simulate by using the user_id string
        result = skills.process_request(
            user_input=user_input,
            user_id=str(current_user_id),
            jwt_token=""  # This would need to be obtained from the request context
        )

        # Prepare response
        response = SuccessResponse(
            data=result
        )

        return response.to_dict()

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(
            status_code=500,
            detail=f"Error processing AI request: {str(e)}"
        )


@router.post(
    "/skills/create_task",
    summary="Create Task via AI",
    description="Create a task using AI processing of natural language input"
)
async def ai_create_task(
    request_data: Dict[str, Any],
    current_user_id: UUID = Depends(get_current_user_id),
):
    """
    Create a task based on natural language input.

    Args:
        request_data: Contains 'input' field with natural language text
        current_user_id: User ID extracted from JWT token (via dependency)

    Returns:
        Created task data
    """
    try:
        # Extract the input text
        user_input = request_data.get("input", "").strip()
        if not user_input:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.get("INVALID_REQUEST", "Input text is required")
            )

        # Initialize the skills processor
        skills = TodoSkills(base_url="http://localhost:8000/api")

        # Extract task info using the skills
        task_info = skills._extract_task_info(user_input)

        # Create the task
        result = skills.create_task(
            user_id=str(current_user_id),
            title=task_info["title"],
            description=task_info.get("description"),
            jwt_token=""  # Would need actual token in real implementation
        )

        # Prepare response
        response = SuccessResponse(
            data=result
        )

        return response.to_dict()

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(
            status_code=500,
            detail=f"Error creating task: {str(e)}"
        )


@router.post(
    "/skills/list_tasks",
    summary="List Tasks via AI",
    description="List tasks with AI-enhanced filtering based on natural language"
)
async def ai_list_tasks(
    request_data: Dict[str, Any],
    current_user_id: UUID = Depends(get_current_user_id),
):
    """
    List tasks based on natural language filters.

    Args:
        request_data: Contains optional 'filter' field with natural language text
        current_user_id: User ID extracted from JWT token (via dependency)

    Returns:
        List of filtered tasks
    """
    try:
        # Initialize the skills processor
        skills = TodoSkills(base_url="http://localhost:8000/api")

        # List the tasks
        result = skills.list_tasks(
            user_id=str(current_user_id),
            jwt_token=""  # Would need actual token in real implementation
        )

        # Prepare response
        response = SuccessResponse(
            data=result
        )

        return response.to_dict()

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(
            status_code=500,
            detail=f"Error listing tasks: {str(e)}"
        )