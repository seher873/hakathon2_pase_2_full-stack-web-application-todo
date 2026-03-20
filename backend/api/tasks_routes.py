"""API routes for task management functionality."""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from mcp.tool_models import TaskCreateModel, TaskUpdateModel, TaskModel

# Create API router
router = APIRouter(prefix="/api", tags=["tasks"])

# In-memory storage for tasks (in production, this would be a database)
tasks_db = []
next_task_id = 1

# Helper function to find task by ID
def find_task_by_id(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    return None

# GET /api/tasks - List all tasks with optional filtering
@router.get("/tasks", response_model=List[TaskModel])
async def list_tasks(
    filter_by: Optional[str] = Query(None, alias="filter_by"),
    status: Optional[str] = Query(None)
):
    """List all tasks with optional filtering."""
    filtered_tasks = tasks_db

    if filter_by:
        filtered_tasks = [
            task for task in filtered_tasks
            if filter_by.lower() in task.title.lower() or
            (task.description and filter_by.lower() in task.description.lower())
        ]

    if status:
        filtered_tasks = [task for task in filtered_tasks if task.status == status]

    return filtered_tasks

# POST /api/tasks - Create a new task
@router.post("/tasks", response_model=TaskModel)
async def create_task(task_create: TaskCreateModel):
    """Create a new task."""
    global next_task_id

    new_task = TaskModel(
        id=next_task_id,
        title=task_create.title,
        description=task_create.description,
        due_date=task_create.due_date,
        status=task_create.status or "pending",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    tasks_db.append(new_task)
    next_task_id += 1

    return new_task

# GET /api/tasks/{task_id} - Get a specific task
@router.get("/tasks/{task_id}", response_model=TaskModel)
async def get_task(task_id: int):
    """Get a specific task by ID."""
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

# PUT /api/tasks/{task_id} - Update a specific task
@router.put("/tasks/{task_id}", response_model=TaskModel)
async def update_task(task_id: int, task_update: TaskUpdateModel):
    """Update a specific task by ID."""
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    if task_update.status is not None:
        task.status = task_update.status

    task.updated_at = datetime.now()

    return task

# PATCH /api/tasks/{task_id} - Partially update task (for toggling status)
@router.patch("/tasks/{task_id}", response_model=TaskModel)
async def patch_task(task_id: int, task_update: TaskUpdateModel):
    """Partially update a task."""
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    if task_update.status is not None:
        task.status = task_update.status

    task.updated_at = datetime.now()

    return task


# PATCH /api/tasks/{task_id}/complete - Update task completion status specifically
@router.patch("/tasks/{task_id}/complete", response_model=TaskModel)
async def patch_task_complete(task_id: int, task_update: TaskUpdateModel):
    """Update task completion status specifically."""
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only the status field based on the 'completed' boolean passed
    if task_update.completed is not None:
        # If the frontend is sending a 'completed' field (boolean), convert it to status
        task.status = "completed" if task_update.completed else "pending"
    elif task_update.status is not None:
        task.status = task_update.status

    task.updated_at = datetime.now()

    return task

# DELETE /api/tasks/{task_id} - Delete a specific task
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a specific task by ID."""
    global tasks_db
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_db = [task for task in tasks_db if task.id != task_id]

    return {"success": True, "task_id": task_id}

# Health check endpoint
@router.get("/tasks/health")
async def tasks_health():
    """Health check endpoint for the tasks API."""
    return {
        "status": "healthy",
        "service": "tasks-api",
        "version": "1.0.0",
        "task_count": len(tasks_db)
    }