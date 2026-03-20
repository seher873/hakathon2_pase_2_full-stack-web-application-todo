from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from .database import get_session
from .models import Todo
from .schemas_new import TodoCreate, TodoUpdate, TodoResponse, PriorityType
from . import crud

router = APIRouter()

# Helper function to format response
def format_response(data, message=None):
    return {
        "status": "success",
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

# Helper function to get current user ID from JWT (mock for now)
def get_current_user_id() -> str:
    """Extract user ID from JWT token. Currently returns mock user ID."""
    # TODO: Implement actual JWT extraction from Authorization header
    return "550e8400-e29b-41d4-a716-446655440000"

# Todo routes
@router.get("/tasks", response_model=dict)
def get_tasks(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, alias="status"),  # all, pending, completed
    priority: Optional[PriorityType] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("created_at"),  # created_at, title, priority, due_date
    sort_order: str = Query("desc", pattern="^(asc|desc)$")
):
    """Get all tasks for the current user with filtering and sorting."""
    # Get user ID from mock auth
    user_id = get_current_user_id()
    todos = crud.get_todos(session, user_id, skip=skip, limit=limit)
    
    # Apply status filter
    if status_filter == "pending":
        todos = [t for t in todos if not t.completed]
    elif status_filter == "completed":
        todos = [t for t in todos if t.completed]
    
    # Apply priority filter
    if priority:
        todos = [t for t in todos if t.priority == priority]
    
    # Apply tags filter (comma-separated)
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        filtered = []
        for todo in todos:
            todo_tags = todo.get_tags_list()
            if any(tag in todo_tags for tag in tag_list):
                filtered.append(todo)
        todos = filtered
    
    # Apply search filter
    if search:
        search_lower = search.lower()
        todos = [
            t for t in todos 
            if search_lower in t.title.lower() or 
               (t.description and search_lower in t.description.lower())
        ]
    
    # Apply sorting
    reverse = sort_order == "desc"
    if sort_by == "title":
        todos.sort(key=lambda x: x.title.lower(), reverse=reverse)
    elif sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        todos.sort(key=lambda x: priority_order.get(x.priority, 1), reverse=reverse)
    elif sort_by == "due_date":
        todos.sort(key=lambda x: x.due_date or datetime.max, reverse=reverse)
    else:  # created_at
        todos.sort(key=lambda x: x.created_at, reverse=reverse)
    
    return format_response(todos)

@router.post("/tasks", response_model=dict)
def create_task(
    task: TodoCreate,
    session: Session = Depends(get_session)
):
    """Create a new task for the current user."""
    try:
        user_id = get_current_user_id()
        todo = crud.create_todo(session, task, user_id)
        return format_response(todo, "Task created successfully")
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "detail": str(e),
            "traceback": traceback.format_exc()
        }

@router.get("/tasks/{task_id}", response_model=dict)
def get_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    """Get a single task by ID."""
    user_id = get_current_user_id()
    todo = crud.get_todo(session, task_id, user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return format_response(todo)

@router.put("/tasks/{task_id}", response_model=dict)
def update_task(
    task_id: str,
    task: TodoUpdate,
    session: Session = Depends(get_session)
):
    """Update an existing task."""
    user_id = get_current_user_id()
    db_todo = crud.update_todo(session, task_id, task, user_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return format_response(db_todo, "Task updated successfully")

@router.patch("/tasks/{task_id}/complete", response_model=dict)
def mark_task_complete(
    task_id: str,
    session: Session = Depends(get_session)
):
    """Toggle task completion status."""
    user_id = get_current_user_id()
    db_todo = crud.toggle_todo_complete(session, task_id, user_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return format_response(db_todo, "Task completion status updated")

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    """Delete a task."""
    user_id = get_current_user_id()
    success = crud.delete_todo(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return format_response(None, "Task deleted successfully")