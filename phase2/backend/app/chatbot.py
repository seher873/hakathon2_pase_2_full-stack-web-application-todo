"""
Phase 3: AI Chatbot with MCP-style tools for task management.
Implements conversational interface using rule-based NLP and MCP tool pattern.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional, Dict, Any, List
from datetime import datetime
import re
import uuid

from .database import get_session
from .models import Todo, Conversation, Message
from .schemas import TodoCreate, TodoUpdate
from . import crud

router = APIRouter()

# Mock user ID (replace with JWT extraction in production)
def get_current_user_id() -> str:
    return "550e8400-e29b-41d4-a716-446655440000"


# ============================================================================
# MCP-Style Tool Definitions
# ============================================================================

class MCPTools:
    """MCP-style tools for task management."""
    
    @staticmethod
    def add_task(session: Session, user_id: str, title: str, description: str = "") -> Dict[str, Any]:
        """Create a new task."""
        try:
            todo = crud.create_todo(
                session, 
                TodoCreate(title=title, description=description), 
                user_id
            )
            return {
                "task_id": str(todo.id),
                "status": "created",
                "title": todo.title
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def list_tasks(session: Session, user_id: str, status_filter: str = "all") -> List[Dict[str, Any]]:
        """List tasks with optional status filter."""
        try:
            todos = crud.get_todos(session, user_id, skip=0, limit=50)
            
            if status_filter == "pending":
                todos = [t for t in todos if not t.completed]
            elif status_filter == "completed":
                todos = [t for t in todos if t.completed]
            
            return [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "completed": t.completed,
                    "priority": t.priority
                }
                for t in todos
            ]
        except Exception as e:
            return []
    
    @staticmethod
    def complete_task(session: Session, user_id: str, task_id: str) -> Dict[str, Any]:
        """Mark a task as complete."""
        try:
            # Find task by ID or partial match
            todos = crud.get_todos(session, user_id)
            target_todo = None
            
            for todo in todos:
                if str(todo.id) == task_id or str(todo.id)[:8] == task_id or task_id.lower() in todo.title.lower():
                    target_todo = todo
                    break
            
            if target_todo:
                updated = crud.toggle_todo_complete(session, str(target_todo.id), user_id)
                return {
                    "task_id": str(target_todo.id),
                    "status": "completed",
                    "title": target_todo.title
                }
            return {"error": "Task not found"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        try:
            todos = crud.get_todos(session, user_id)
            target_todo = None
            
            for todo in todos:
                if str(todo.id) == task_id or str(todo.id)[:8] == task_id or task_id.lower() in todo.title.lower():
                    target_todo = todo
                    break
            
            if target_todo:
                crud.delete_todo(session, str(target_todo.id), user_id)
                return {
                    "task_id": str(target_todo.id),
                    "status": "deleted",
                    "title": target_todo.title
                }
            return {"error": "Task not found"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def update_task(session: Session, user_id: str, task_id: str, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update a task."""
        try:
            todos = crud.get_todos(session, user_id)
            target_todo = None
            
            for todo in todos:
                if str(todo.id) == task_id or str(todo.id)[:8] == task_id:
                    target_todo = todo
                    break
            
            if target_todo:
                update_data = TodoUpdate()
                if title:
                    update_data.title = title
                if description:
                    update_data.description = description
                
                updated = crud.update_todo(session, str(target_todo.id), update_data, user_id)
                return {
                    "task_id": str(target_todo.id),
                    "status": "updated",
                    "title": updated.title
                }
            return {"error": "Task not found"}
        except Exception as e:
            return {"error": str(e)}


# ============================================================================
# NLP Intent Processor
# ============================================================================

class IntentProcessor:
    """Process natural language and map to MCP tools."""
    
    INTENT_PATTERNS = {
        'add_task': [
            r'add\s+(a\s+)?task\s+(to\s+)?(.+)',
            r'create\s+(a\s+)?task\s+(to\s+)?(.+)',
            r'i\s+need\s+to\s+(.+)',
            r'i\s+want\s+to\s+(.+)',
            r'remember\s+to\s+(.+)',
            r'add\s+(.+)',
            r'create\s+(.+)',
        ],
        'list_tasks': [
            r'show\s+(my\s+)?tasks',
            r'list\s+(my\s+)?tasks',
            r'what\s+(are\s+)?my\s+tasks',
            r'pending\s+tasks',
            r'completed\s+tasks',
            r'my\s+tasks',
            r'view\s+tasks',
        ],
        'complete_task': [
            r'complete\s+(task\s+)?(.+)',
            r'mark\s+(.+)\s+as\s+complete',
            r'done\s+(.+)',
            r'finished\s+(.+)',
            r"i'?ve\s+finished\s+(.+)",
        ],
        'delete_task': [
            r'delete\s+(task\s+)?(.+)',
            r'remove\s+(.+)',
            r'get\s+rid\s+of\s+(.+)',
        ],
    }
    
    @classmethod
    def process(cls, text: str) -> Dict[str, Any]:
        """Process text and return intent with extracted data."""
        text_lower = text.lower().strip()
        
        for intent, patterns in cls.INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    # Extract task title/description from groups
                    task_text = None
                    if match.groups():
                        # Get the last non-None group
                        for group in reversed(match.groups()):
                            if group:
                                task_text = group.strip()
                                break
                    
                    return {
                        'intent': intent,
                        'task_text': task_text,
                        'original': text
                    }
        
        return {'intent': 'unknown', 'task_text': None, 'original': text}


# ============================================================================
# Conversation Manager
# ============================================================================

class ConversationManager:
    """Manage conversations and messages in database."""
    
    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """Create a new conversation."""
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv
    
    @staticmethod
    def get_conversation(session: Session, conv_id: str, user_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        return session.get(Conversation, conv_id)
    
    @staticmethod
    def add_message(session: Session, user_id: str, conv_id: str, role: str, content: str) -> Message:
        """Add a message to conversation."""
        msg = Message(
            user_id=user_id,
            conversation_id=conv_id,
            role=role,
            content=content
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return msg
    
    @staticmethod
    def get_messages(session: Session, conv_id: str, limit: int = 20) -> List[Message]:
        """Get recent messages from conversation."""
        return session.exec(
            select(Message)
            .where(Message.conversation_id == conv_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()


# ============================================================================
# AI Agent
# ============================================================================

class ChatAgent:
    """AI Agent that processes commands and invokes MCP tools."""
    
    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id
        self.tools = MCPTools()
    
    def process(self, message: str) -> Dict[str, Any]:
        """Process a message and return response with tool calls."""
        # Process intent
        intent_data = IntentProcessor.process(message)
        intent = intent_data['intent']
        task_text = intent_data.get('task_text')
        
        tool_calls = []
        response = ""
        
        if intent == 'add_task':
            if task_text:
                result = self.tools.add_task(self.session, self.user_id, task_text)
                tool_calls.append({"tool": "add_task", "result": result})
                if "error" in result:
                    response = f"❌ Failed to add task: {result['error']}"
                else:
                    response = f"✅ Added task: '{task_text}'"
            else:
                response = "❓ What task would you like to add?"
        
        elif intent == 'list_tasks':
            # Determine status filter from message
            status_filter = "all"
            if "pending" in message.lower():
                status_filter = "pending"
            elif "completed" in message.lower():
                status_filter = "completed"
            
            tasks = self.tools.list_tasks(self.session, self.user_id, status_filter)
            tool_calls.append({"tool": "list_tasks", "result": tasks})
            
            if not tasks:
                response = "📭 You have no tasks yet!"
            else:
                response = f"📋 You have {len(tasks)} task(s):\n\n"
                for i, task in enumerate(tasks[:10], 1):
                    status_icon = "✅" if task['completed'] else "⏳"
                    response += f"{i}. {status_icon} {task['title']} ({task['priority']} priority)\n"
                if len(tasks) > 10:
                    response += f"... and {len(tasks) - 10} more"
        
        elif intent == 'complete_task':
            if task_text:
                result = self.tools.complete_task(self.session, self.user_id, task_text)
                tool_calls.append({"tool": "complete_task", "result": result})
                if "error" in result:
                    response = f"❌ {result['error']}"
                else:
                    response = f"✅ Marked '{result['title']}' as complete!"
            else:
                response = "❓ Which task would you like to complete?"
        
        elif intent == 'delete_task':
            if task_text:
                result = self.tools.delete_task(self.session, self.user_id, task_text)
                tool_calls.append({"tool": "delete_task", "result": result})
                if "error" in result:
                    response = f"❌ {result['error']}"
                else:
                    response = f"🗑️ Deleted '{result['title']}'"
            else:
                response = "❓ Which task would you like to delete?"
        
        elif intent == 'unknown':
            response = """❓ I didn't understand. Try:
• "Add buy milk"
• "Show my tasks"
• "Complete buy milk"
• "Delete old task\""""
        
        return {
            "response": response,
            "tool_calls": tool_calls,
            "intent": intent
        }


# ============================================================================
# API Routes
# ============================================================================

@router.post("/chat")
def chat(
    request_data: Dict[str, Any],
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Chat endpoint for AI-powered task management.
    
    Request:
    - conversation_id: Optional existing conversation ID
    - message: User's natural language message
    """
    message = request_data.get('message', '').strip()
    conversation_id = request_data.get('conversation_id')
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Get or create conversation
    if conversation_id:
        conv = ConversationManager.get_conversation(session, conversation_id, user_id)
        if not conv:
            conv = ConversationManager.create_conversation(session, user_id)
            conversation_id = str(conv.id)
    else:
        conv = ConversationManager.create_conversation(session, user_id)
        conversation_id = str(conv.id)
    
    # Store user message
    ConversationManager.add_message(session, user_id, conversation_id, "user", message)
    
    # Process with AI agent
    agent = ChatAgent(session, user_id)
    result = agent.process(message)
    
    # Store assistant response
    ConversationManager.add_message(
        session, 
        user_id, 
        conversation_id, 
        "assistant", 
        result['response']
    )
    
    return {
        "conversation_id": conversation_id,
        "response": result['response'],
        "tool_calls": result['tool_calls'],
        "intent": result['intent'],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/conversations")
def list_conversations(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """List user's conversations."""
    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(50)
    ).all()
    
    return {
        "conversations": [
            {
                "id": str(c.id),
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            }
            for c in conversations
        ]
    }


@router.get("/conversations/{conv_id}/messages")
def get_conversation_messages(
    conv_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Get messages from a conversation."""
    conv = ConversationManager.get_conversation(session, conv_id, user_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = ConversationManager.get_messages(session, conv_id, limit=50)
    
    return {
        "messages": [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat()
            }
            for m in reversed(messages)  # Return in chronological order
        ]
    }


@router.delete("/conversations/{conv_id}")
def delete_conversation(
    conv_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """Delete a conversation and its messages."""
    conv = ConversationManager.get_conversation(session, conv_id, user_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete messages
    messages = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
    for msg in messages:
        session.delete(msg)
    
    # Delete conversation
    session.delete(conv)
    session.commit()
    
    return {"status": "deleted", "conversation_id": conv_id}


@router.get("/chat/help")
def chat_help():
    """Get help information about chatbot commands."""
    return {
        "description": "AI-Powered Task Management Chatbot",
        "commands": [
            {"command": "Add [task]", "example": "Add buy milk", "description": "Create a new task"},
            {"command": "Show my tasks", "example": "Show my tasks", "description": "List all tasks"},
            {"command": "Show pending tasks", "example": "Show pending tasks", "description": "List pending tasks"},
            {"command": "Complete [task]", "example": "Complete buy milk", "description": "Mark task complete"},
            {"command": "Delete [task]", "example": "Delete old task", "description": "Delete a task"},
        ],
        "tips": [
            "Use natural language",
            "Reference tasks by name",
            "Be specific with task names",
        ]
    }
