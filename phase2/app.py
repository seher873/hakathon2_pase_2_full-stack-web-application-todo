"""
Hugging Face Spaces Backend - Complete API with Auth
This is the main entry point for HF Spaces deployment.
"""

import os
import json
import uuid
import traceback
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select, Field
from pydantic import BaseModel
import uvicorn

# ============================================================================
# Configuration
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
SECRET_KEY = os.getenv("SECRET_KEY", "hackathon-secret-key-change-in-production")

# ============================================================================
# Database Setup
# ============================================================================

def get_connection_args():
    if DATABASE_URL.startswith("postgresql"):
        return {"connect_args": {"sslmode": "prefer"}}
    return {}

engine = create_engine(DATABASE_URL, **get_connection_args())

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ============================================================================
# Models
# ============================================================================

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="550e8400-e29b-41d4-a716-446655440000")
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    due_date: Optional[datetime] = Field(default=None)
    tags: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(..., unique=True)
    password_hash: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# Pydantic Schemas
# ============================================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None
    tags: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    status: str = "success"
    data: dict
    message: str
    timestamp: str

# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="Hackathon Todo API",
    description="Todo App Backend with Authentication",
    version="1.0.0"
)

# CORS - Allow all origins for HF Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Helper Functions
# ============================================================================

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def format_response(data, message=None):
    return {
        "status": "success",
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

def error_response(detail: str, status_code: int = 500):
    return {
        "status": "error",
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat()
    }

# Mock token for demo
MOCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjk5OTk5OTk5OTl9.mock-token"

MOCK_USER = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

# ============================================================================
# Auth Endpoints
# ============================================================================

@app.post("/api/auth/login")
def login(request: LoginRequest):
    """Login endpoint - mock authentication for demo."""
    return {
        "status": "success",
        "data": {
            "token": MOCK_TOKEN,
            "user": MOCK_USER
        },
        "message": "Login successful",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/register")
def register(request: RegisterRequest):
    """Register endpoint - mock registration for demo."""
    return {
        "status": "success",
        "data": {
            "token": MOCK_TOKEN,
            "user": MOCK_USER
        },
        "message": "Registration successful",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/logout")
def logout():
    """Logout endpoint."""
    return {
        "status": "success",
        "message": "Logged out successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/auth/me")
def get_current_user():
    """Get current user."""
    return {
        "status": "success",
        "data": MOCK_USER,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# Task Endpoints
# ============================================================================

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Hackathon Todo Backend",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "Hackathon Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/tasks")
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$")
):
    """List all tasks with filtering and sorting."""
    try:
        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            
            # Apply filters
            if status_filter == "pending":
                tasks = [t for t in tasks if not t.completed]
            elif status_filter == "completed":
                tasks = [t for t in tasks if t.completed]
            
            if priority:
                tasks = [t for t in tasks if t.priority == priority]
            
            if search:
                search_lower = search.lower()
                tasks = [t for t in tasks if search_lower in t.title.lower()]
            
            # Sort
            reverse = sort_order == "desc"
            if sort_by == "title":
                tasks.sort(key=lambda x: x.title.lower(), reverse=reverse)
            elif sort_by == "priority":
                order = {"high": 0, "medium": 1, "low": 2}
                tasks.sort(key=lambda x: order.get(x.priority, 1), reverse=reverse)
            elif sort_by == "due_date":
                tasks.sort(key=lambda x: x.due_date or datetime.max, reverse=reverse)
            else:
                tasks.sort(key=lambda x: x.created_at, reverse=reverse)
            
            return format_response(tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks")
def create_task(task_data: TaskCreate):
    """Create a new task."""
    try:
        with Session(engine) as session:
            task = Task(
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                due_date=datetime.fromisoformat(task_data.due_date) if task_data.due_date else None,
                tags=task_data.tags,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return format_response({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }, "Task created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """Get a specific task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return format_response({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        })

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "due_date" and value:
                value = datetime.fromisoformat(value)
            setattr(task, field, value)
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return format_response({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }, "Task updated successfully")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return format_response(None, "Task deleted successfully")

@app.patch("/api/tasks/{task_id}/complete")
def toggle_task_complete(task_id: str, completed: bool = True):
    """Toggle task completion."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.completed = completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return format_response({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }, "Task completion status updated")

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
