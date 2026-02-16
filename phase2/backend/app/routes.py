from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from datetime import datetime
from .database import get_session
from .models import Todo
from .schemas import TodoCreate, TodoUpdate, TodoResponse
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

# Todo routes
@router.get("/tasks", response_model=dict)
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    todos = crud.get_todos(session, skip=skip, limit=limit)
    return format_response(todos)

@router.post("/tasks", response_model=dict)
def create_task(
    task: TodoCreate,
    session: Session = Depends(get_session)
):
    todo = crud.create_todo(session, task)
    return format_response(todo, "Task created successfully")

@router.get("/tasks/{task_id}", response_model=dict)
def get_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    todo = crud.get_todo(session, task_id)
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
    db_todo = crud.update_todo(session, task_id, task)
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
    # Get current task
    todo = crud.get_todo(session, task_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    update_data = TodoUpdate(completed=not todo.completed)
    db_todo = crud.update_todo(session, task_id, update_data)

    return format_response(db_todo, "Task completion status updated")

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    success = crud.delete_todo(session, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return format_response(None, "Task deleted successfully")