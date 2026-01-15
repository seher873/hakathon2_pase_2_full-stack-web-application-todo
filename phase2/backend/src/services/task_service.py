"""
Task service for CRUD operations.

Provides business logic for task management including
validation, authorization, and database operations.
"""

from typing import List, Optional
from uuid import UUID
from sqlmodel import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from src.models.user import User


class TaskService:
    """
    Service class for task-related operations.

    Handles all business logic for task management including:
    - Creating new tasks
    - Retrieving tasks (single and list)
    - Updating existing tasks
    - Deleting tasks
    - Authorization checks
    """

    @staticmethod
    async def create_task(
        session: AsyncSession,
        user_id: UUID,
        task_data: TaskCreate
    ) -> TaskResponse:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            task_data: Task creation data

        Returns:
            TaskResponse: Created task data

        Raises:
            Exception: If database operation fails
        """
        # Create task instance
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=False,  # New tasks are not completed by default
            user_id=user_id
        )

        # Add to session and commit
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Return as response model
        return TaskResponse.model_validate(task)

    @staticmethod
    async def get_task_by_id(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID
    ) -> Optional[TaskResponse]:
        """
        Get a specific task by ID for a user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            TaskResponse: Task data if found and authorized, None otherwise
        """
        # Query for task with user_id filter for authorization
        statement = (
            select(Task)
            .where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if task:
            return TaskResponse.model_validate(task)

        return None

    @staticmethod
    async def get_tasks_by_user(
        session: AsyncSession,
        user_id: UUID,
        completed: Optional[bool] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[TaskResponse]:
        """
        Get all tasks for a user with optional filters.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            completed: Filter by completion status (None = all)
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            List[TaskResponse]: List of user's tasks
        """
        # Build query with user_id filter
        statement = select(Task).where(Task.user_id == user_id)

        # Add completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Add pagination
        statement = statement.offset(offset).limit(limit)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Convert to response models
        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
        task_data: TaskUpdate
    ) -> Optional[TaskResponse]:
        """
        Update an existing task for a user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user requesting the update
            task_data: Task update data

        Returns:
            TaskResponse: Updated task data if successful, None if not found or unauthorized
        """
        # Get the existing task with user_id filter for authorization
        statement = (
            select(Task)
            .where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update fields that are provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed

        # Commit changes
        await session.commit()
        await session.refresh(task)

        return TaskResponse.model_validate(task)

    @staticmethod
    async def update_task_completion(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID,
        completed: bool
    ) -> Optional[TaskResponse]:
        """
        Update an existing task's completion status for a user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user requesting the update
            completed: New completion status

        Returns:
            TaskResponse: Updated task data if successful, None if not found or unauthorized
        """
        # Get the existing task with user_id filter for authorization
        statement = (
            select(Task)
            .where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update completion status
        task.completed = completed

        # Commit changes
        await session.commit()
        await session.refresh(task)

        return TaskResponse.model_validate(task)

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        task_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a task for a user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion

        Returns:
            bool: True if task was deleted, False if not found or unauthorized
        """
        # Get the existing task with user_id filter for authorization
        statement = (
            select(Task)
            .where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        # Delete the task
        await session.delete(task)
        await session.commit()

        return True

    @staticmethod
    async def search_tasks_by_user(
        session: AsyncSession,
        user_id: UUID,
        search_term: str,
        completed: Optional[bool] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[TaskResponse]:
        """
        Search tasks for a user by title or description with optional filters.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to search
            search_term: Term to search for in title or description
            completed: Filter by completion status (None = all)
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            List[TaskResponse]: List of matching user's tasks
        """
        # Build query with user_id filter and search term
        statement = select(Task).where(
            and_(
                Task.user_id == user_id,
                (
                    Task.title.ilike(f"%{search_term}%") |
                    Task.description.ilike(f"%{search_term}%")
                )
            )
        )

        # Add completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Add pagination
        statement = statement.offset(offset).limit(limit)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Convert to response models
        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    async def get_task_count_by_search(
        session: AsyncSession,
        user_id: UUID,
        search_term: str,
        completed: Optional[bool] = None
    ) -> int:
        """
        Get the count of tasks for a user that match the search term with optional filter.

        Args:
            session: Database session
            user_id: ID of the user whose task count to retrieve
            search_term: Term to search for in title or description
            completed: Filter by completion status (None = all)

        Returns:
            int: Number of tasks matching criteria
        """
        # Build query with user_id filter and search term
        statement = select(Task).where(
            and_(
                Task.user_id == user_id,
                (
                    Task.title.ilike(f"%{search_term}%") |
                    Task.description.ilike(f"%{search_term}%")
                )
            )
        )

        # Add completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Count the results
        count_statement = select(func.count()).select_from(statement.subquery())
        result = await session.execute(count_statement)
        count = result.scalar_one()

        return count

    @staticmethod
    async def get_task_count_by_user(
        session: AsyncSession,
        user_id: UUID,
        completed: Optional[bool] = None
    ) -> int:
        """
        Get the count of tasks for a user with optional filter.

        Args:
            session: Database session
            user_id: ID of the user whose task count to retrieve
            completed: Filter by completion status (None = all)

        Returns:
            int: Number of tasks matching criteria
        """
        # Build query with user_id filter
        statement = select(Task).where(Task.user_id == user_id)

        # Add completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Count the results
        count_statement = select(func.count()).select_from(statement.subquery())
        result = await session.execute(count_statement)
        count = result.scalar_one()

        return count