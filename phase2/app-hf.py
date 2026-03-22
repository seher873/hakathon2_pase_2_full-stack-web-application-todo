from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select, Field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

# ============================================================================
# Database
# ============================================================================

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ============================================================================
# Models
# ============================================================================

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    tags: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# Pydantic Schemas
# ============================================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    tags: Optional[str] = None
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(title="Hackathon Todo API", version="1.0.0")

# CORS - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Mock Auth Data
# ============================================================================

MOCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjk5OTk5OTk5OTl9.mock-token-for-demo"

MOCK_USER = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ============================================================================
# Health & Root
# ============================================================================

@app.get("/")
def root():
    return {
        "message": "Hackathon Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Hackathon Todo Backend",
        "version": "1.0.0"
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

@app.get("/api/tasks")
def list_tasks():
    """List all tasks."""
    try:
        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            task_list = []
            for t in tasks:
                task_list.append({
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "priority": t.priority,
                    "tags": t.tags,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "created_at": t.created_at.isoformat(),
                    "updated_at": t.updated_at.isoformat(),
                })
            return {"status": "success", "data": task_list, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    """Create a new task."""
    try:
        with Session(engine) as session:
            new_task = Task(
                title=task.title,
                description=task.description,
                priority=task.priority,
                tags=task.tags,
                due_date=datetime.fromisoformat(task.due_date) if task.due_date else None,
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return {
                "status": "success",
                "data": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "completed": new_task.completed,
                    "priority": new_task.priority,
                    "tags": new_task.tags,
                    "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                    "created_at": new_task.created_at.isoformat(),
                    "updated_at": new_task.updated_at.isoformat(),
                },
                "message": "Task created successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """Get a specific task."""
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return {
                "status": "success",
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": task.tags,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                },
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task."""
    try:
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
            
            return {
                "status": "success",
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": task.tags,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                },
                "message": "Task updated successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task."""
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            session.delete(task)
            session.commit()
            return {
                "status": "success",
                "message": "Task deleted successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.patch("/api/tasks/{task_id}/complete")
def toggle_task_complete(task_id: str, completed: bool = True):
    """Toggle task completion."""
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            task.completed = completed
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            return {
                "status": "success",
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": task.tags,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                },
                "message": "Task completion status updated",
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e), "timestamp": datetime.utcnow().isoformat()}

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
