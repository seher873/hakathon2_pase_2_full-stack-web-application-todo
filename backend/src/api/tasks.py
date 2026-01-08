"""
Task endpoints for CRUD operations.

Provides REST API endpoints for task management with proper
authentication and authorization checks.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.api.deps import get_current_user_id
from src.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
    TaskFilterParams
)
from src.services.task_service import TaskService
from src.middleware import SuccessResponse
from src.schemas.error import ERROR_MESSAGES

# Create router for task endpoints
router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=SuccessResponse[TaskResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def create_task(
    user_id: UUID,
    task_data: TaskCreateRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Create a new task for the authenticated user.

    This endpoint creates a new task associated with the authenticated user.
    The user ID in the JWT token must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        task_data: Task creation data (title, description)
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session

    Returns:
        SuccessResponse[TaskResponse]: Created task data

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        400: If the request data is invalid
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Create the task using the service
    created_task = await TaskService.create_task(
        session=session,
        user_id=current_user_id,
        task_data=task_data,
    )

    # Prepare response
    response = SuccessResponse[TaskResponse](
        data=created_task
    )

    return response.to_dict()


@router.get(
    "/",
    response_model=SuccessResponse[TaskListResponse],
    status_code=status.HTTP_200_OK,
    summary="Get User Tasks",
    responses={
        200: {"description": "Tasks retrieved successfully"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def get_tasks(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
    completed: bool = Query(
        None,
        description="Filter by completion status (true/false, omit for all)"
    ),
    search: str = Query(
        None,
        min_length=1,
        max_length=255,
        description="Search term for title or description (optional)"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=1000,
        description="Maximum number of tasks to return (1-1000)"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of tasks to skip"
    ),
) -> dict:
    """
    Get all tasks for the authenticated user with optional filtering and search.

    This endpoint retrieves all tasks associated with the authenticated user.
    The user ID in the JWT token must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session
        completed: Filter by completion status (true/false, omit for all)
        search: Search term for title or description (optional)
        limit: Maximum number of tasks to return (1-1000)
        offset: Number of tasks to skip

    Returns:
        SuccessResponse[TaskListResponse]: List of user's tasks and total count

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Get tasks using the service - use search if provided, otherwise use regular get
    if search:
        tasks = await TaskService.search_tasks_by_user(
            session=session,
            user_id=current_user_id,
            search_term=search,
            completed=completed,
            limit=limit,
            offset=offset
        )
        # Get total count for search results
        total = await TaskService.get_task_count_by_search(
            session=session,
            user_id=current_user_id,
            search_term=search,
            completed=completed
        )
    else:
        tasks = await TaskService.get_tasks_by_user(
            session=session,
            user_id=current_user_id,
            completed=completed,
            limit=limit,
            offset=offset
        )
        # Get total count for pagination info
        total = await TaskService.get_task_count_by_user(
            session=session,
            user_id=current_user_id,
            completed=completed
        )

    # Prepare response
    response_data = TaskListResponse(
        tasks=tasks,
        total=total
    )

    response = SuccessResponse[TaskListResponse](
        data=response_data
    )

    return response.to_dict()


@router.get(
    "/{task_id}",
    response_model=SuccessResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Task",
    responses={
        200: {"description": "Task retrieved successfully"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get a specific task for the authenticated user.

    This endpoint retrieves a specific task associated with the authenticated user.
    The user ID in the JWT token must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        task_id: The task ID to retrieve
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session

    Returns:
        SuccessResponse[TaskResponse]: Requested task data

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        404: If the task doesn't exist or doesn't belong to the user
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Get the task using the service
    task = await TaskService.get_task_by_id(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
    )

    if not task:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.get("TASK_NOT_FOUND", "Task not found"),
        )

    # Prepare response
    response = SuccessResponse[TaskResponse](
        data=task
    )

    return response.to_dict()


@router.put(
    "/{task_id}",
    response_model=SuccessResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Update Task",
    responses={
        200: {"description": "Task updated successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdateRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Update a specific task for the authenticated user.

    This endpoint updates a specific task associated with the authenticated user.
    The user ID in the JWT token must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        task_id: The task ID to update
        task_data: Task update data
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session

    Returns:
        SuccessResponse[TaskResponse]: Updated task data

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        404: If the task doesn't exist or doesn't belong to the user
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Update the task using the service
    updated_task = await TaskService.update_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
        task_data=task_data,
    )

    if not updated_task:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.get("TASK_NOT_FOUND", "Task not found"),
        )

    # Prepare response
    response = SuccessResponse[TaskResponse](
        data=updated_task
    )

    return response.to_dict()


@router.patch(
    "/{task_id}/complete",
    response_model=SuccessResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Mark Task Complete/Incomplete",
    responses={
        200: {"description": "Task completion status updated successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def update_task_completion(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdateRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Update a specific task's completion status for the authenticated user.

    This endpoint updates a specific task's completion status associated with the authenticated user.
    The user ID in the JWT token must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        task_id: The task ID to update
        task_data: Task update data (only completed field is processed)
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session

    Returns:
        SuccessResponse[TaskResponse]: Updated task data

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        404: If the task doesn't exist or doesn't belong to the user
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Validate that completed field is provided
    if task_data.completed is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.get("INVALID_REQUEST", "Completed field is required"),
        )

    # Update the task completion status using the dedicated service method
    updated_task = await TaskService.update_task_completion(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
        completed=task_data.completed,
    )

    if not updated_task:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.get("TASK_NOT_FOUND", "Task not found"),
        )

    # Prepare response
    response = SuccessResponse[TaskResponse](
        data=updated_task
    )

    return response.to_dict()


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
    responses={
        204: {"description": "Task deleted successfully"},
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - user cannot access this resource"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    },
)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """
    Delete a specific task for the authenticated user.

    This endpoint deletes a specific task associated with the authenticated user.
    The user ID in the URL path must match the user ID in the URL path
    for security purposes.

    Args:
        user_id: The user ID from the URL path (must match JWT user ID)
        task_id: The task ID to delete
        current_user_id: User ID extracted from JWT token (via dependency)
        session: Database session

    Returns:
        None: 204 No Content on successful deletion

    Raises:
        403: If the user ID in the URL doesn't match the JWT user ID
        404: If the task doesn't exist or doesn't belong to the user
        500: If there's a server error
    """
    # Verify that the user ID in the URL matches the authenticated user
    if user_id != current_user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.get("FORBIDDEN_ACCESS", "Access denied"),
        )

    # Delete the task using the service
    deleted = await TaskService.delete_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
    )

    if not deleted:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.get("TASK_NOT_FOUND", "Task not found"),
        )

    # Return 204 No Content
    return None