from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select, Field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid
import re

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

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="550e8400-e29b-41d4-a716-446655440000")
    title: str = Field(default="New Conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(default="550e8400-e29b-41d4-a716-446655440000")
    conversation_id: str = Field(...)
    role: str = Field(...)  # "user" or "assistant"
    content: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

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

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: Optional[List[dict]] = None

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
        "message": "Hackathon Todo API with AI Chatbot",
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
# Phase 3: AI Chatbot Endpoints (Rule-based NLP)
# ============================================================================

def format_task_response(task: Task) -> dict:
    """Format task for response."""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority,
        "tags": task.tags,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }

def ai_chat_processor(message: str, user_id: str = MOCK_USER["id"]) -> dict:
    """
    Rule-based AI chat processor (Phase 3).
    Processes natural language commands and executes task operations.
    """
    message_lower = message.lower().strip()
    tool_calls = []
    
    # Create task: "add buy milk", "create task: buy milk", "remember to pay bills"
    create_patterns = [
        r'(?:add|create|new task|remember)\s*(?:to\s*)?(?:task:\s*)?(.+)',
        r'i need to (.+)',
        r'i want to (.+)',
    ]
    
    for pattern in create_patterns:
        match = re.search(pattern, message_lower)
        if match:
            title = match.group(1).strip()
            # Capitalize first letter
            title = title.capitalize()
            
            try:
                with Session(engine) as session:
                    new_task = Task(
                        title=title,
                        description="Created via chatbot",
                        priority="medium",
                    )
                    session.add(new_task)
                    session.commit()
                    session.refresh(new_task)
                    
                    tool_calls.append({
                        "tool": "add_task",
                        "result": {"task_id": new_task.id, "status": "created", "title": title}
                    })
                    
                    return {
                        "response": f"✅ I've added '{title}' to your tasks!",
                        "tool_calls": tool_calls
                    }
            except Exception as e:
                return {"response": f"❌ Failed to create task: {str(e)}", "tool_calls": []}
    
    # List tasks: "show tasks", "list my tasks", "what's pending", "show all tasks"
    list_patterns = [
        r'(?:show|list|get)\s*(?:my\s*)?(?:all\s*)?(?:tasks?)',
        r'what(?:\'s| is)\s*(?:pending|my tasks|all tasks)',
        r'my tasks',
    ]
    
    for pattern in list_patterns:
        if re.search(pattern, message_lower):
            try:
                with Session(engine) as session:
                    tasks = session.exec(select(Task)).all()
                    task_list = list(tasks)
                    
                    if not task_list:
                        return {
                            "response": "📋 You don't have any tasks yet. Start by adding one!",
                            "tool_calls": [{"tool": "list_tasks", "result": {"count": 0}}]
                        }
                    
                    completed = sum(1 for t in task_list if t.completed)
                    pending = len(task_list) - completed
                    
                    task_titles = ", ".join([t.title for t in task_list[:5]])
                    if len(task_list) > 5:
                        task_titles += f" and {len(task_list) - 5} more..."
                    
                    return {
                        "response": f"📋 You have {len(task_list)} task(s) ({pending} pending, {completed} completed):\n\n{task_titles}",
                        "tool_calls": [{"tool": "list_tasks", "result": {"count": len(task_list)}}]
                    }
            except Exception as e:
                return {"response": f"❌ Failed to list tasks: {str(e)}", "tool_calls": []}
    
    # Complete task: "complete buy milk", "mark task as done", "done with groceries"
    complete_patterns = [
        r'(?:complete|finish|done with|mark)\s*(?:task\s*)?(?:as\s*done)?\s*(?:-?\s*)?(.+)',
    ]
    
    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_search = match.group(1).strip()
            
            try:
                with Session(engine) as session:
                    # Search by title
                    tasks = session.exec(select(Task).where(Task.title.contains(task_search))).all()
                    
                    if tasks:
                        task = tasks[0]
                        task.completed = True
                        task.updated_at = datetime.utcnow()
                        session.add(task)
                        session.commit()
                        
                        tool_calls.append({
                            "tool": "complete_task",
                            "result": {"task_id": task.id, "status": "completed", "title": task.title}
                        })
                        
                        return {
                            "response": f"✅ Great job! I've marked '{task.title}' as complete!",
                            "tool_calls": tool_calls
                        }
                    else:
                        return {"response": f"❌ I couldn't find a task matching '{task_search}'", "tool_calls": []}
            except Exception as e:
                return {"response": f"❌ Failed to complete task: {str(e)}", "tool_calls": []}
    
    # Delete task: "delete buy milk", "remove task", "cancel groceries"
    delete_patterns = [
        r'(?:delete|remove|cancel)\s*(?:task\s*)?(?:-?\s*)?(.+)',
    ]
    
    for pattern in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_search = match.group(1).strip()
            
            try:
                with Session(engine) as session:
                    tasks = session.exec(select(Task).where(Task.title.contains(task_search))).all()
                    
                    if tasks:
                        task = tasks[0]
                        task_title = task.title
                        session.delete(task)
                        session.commit()
                        
                        tool_calls.append({
                            "tool": "delete_task",
                            "result": {"task_id": task.id, "status": "deleted", "title": task_title}
                        })
                        
                        return {
                            "response": f"🗑️ I've deleted '{task_title}'",
                            "tool_calls": tool_calls
                        }
                    else:
                        return {"response": f"❌ I couldn't find a task matching '{task_search}'", "tool_calls": []}
            except Exception as e:
                return {"response": f"❌ Failed to delete task: {str(e)}", "tool_calls": []}
    
    # Help command
    if any(word in message_lower for word in ["help", "commands", "what can you do", "how to use"]):
        return {
            "response": """🤖 I can help you manage tasks! Try these commands:

• **Add task**: "Add buy milk" or "Remember to pay bills"
• **List tasks**: "Show my tasks" or "What's pending?"
• **Complete task**: "Complete buy milk" or "Done with groceries"
• **Delete task**: "Delete old task" or "Remove meeting"

Just talk naturally and I'll understand! 😊""",
            "tool_calls": [{"tool": "help", "result": {"action": "showed_help"}}]
        }
    
    # Greeting
    if any(word in message_lower for word in ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return {
            "response": "👋 Hello! I'm your AI task assistant. How can I help you today? Try saying 'Add a task' or 'Show my tasks'!",
            "tool_calls": []
        }
    
    # Default response
    return {
        "response": """🤔 I'm not sure I understood that. Try one of these:

• "Add buy milk" - Create a new task
• "Show my tasks" - List all tasks
• "Complete buy milk" - Mark task as done
• "Help" - Show all commands

What would you like to do?""",
        "tool_calls": []
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Phase 3: AI Chatbot endpoint.
    Process natural language commands for task management.
    """
    try:
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Save user message
        with Session(engine) as session:
            user_message = Message(
                conversation_id=conversation_id,
                role="user",
                content=request.message,
            )
            session.add(user_message)
            
            # Process with AI
            result = ai_chat_processor(request.message)
            
            # Save assistant response
            assistant_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=result["response"],
            )
            session.add(assistant_message)
            session.commit()
            
            return ChatResponse(
                conversation_id=conversation_id,
                response=result["response"],
                tool_calls=result.get("tool_calls")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/help")
def chat_help():
    """Get chatbot help information."""
    return {
        "status": "success",
        "data": {
            "commands": [
                {"command": "Add [task]", "example": "Add buy milk", "description": "Create a new task"},
                {"command": "Show tasks", "example": "Show my tasks", "description": "List all tasks"},
                {"command": "Complete [task]", "example": "Complete buy milk", "description": "Mark task as done"},
                {"command": "Delete [task]", "example": "Delete old task", "description": "Remove a task"},
                {"command": "Help", "example": "Help", "description": "Show available commands"},
            ],
            "examples": [
                "Add a task to buy groceries",
                "Show me all my tasks",
                "Mark task 3 as complete",
                "Delete the meeting task",
            ]
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/conversations")
def list_conversations():
    """List user's conversations."""
    try:
        with Session(engine) as session:
            conversations = session.exec(select(Conversation)).all()
            return {
                "status": "success",
                "data": [
                    {
                        "id": c.id,
                        "title": c.title,
                        "created_at": c.created_at.isoformat(),
                        "updated_at": c.updated_at.isoformat(),
                    }
                    for c in conversations
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/conversations/{conv_id}/messages")
def get_conversation_messages(conv_id: str):
    """Get messages for a conversation."""
    try:
        with Session(engine) as session:
            messages = session.exec(
                select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at)
            ).all()
            
            return {
                "status": "success",
                "data": [
                    {
                        "id": m.id,
                        "role": m.role,
                        "content": m.content,
                        "created_at": m.created_at.isoformat(),
                    }
                    for m in messages
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.delete("/api/conversations/{conv_id}")
def delete_conversation(conv_id: str):
    """Delete a conversation."""
    try:
        with Session(engine) as session:
            conversation = session.get(Conversation, conv_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            # Delete associated messages
            messages = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
            for message in messages:
                session.delete(message)
            
            session.delete(conversation)
            session.commit()
            
            return {
                "status": "success",
                "message": "Conversation deleted successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
