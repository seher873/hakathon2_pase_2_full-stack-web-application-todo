from sqlmodel import Session, select
from .models import Todo
from .schemas import TodoCreate, TodoUpdate
from datetime import datetime
from typing import Optional, List

def get_todos(session: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Todo]:
    """Get all todos for a specific user with pagination."""
    return session.exec(
        select(Todo)
        .where(Todo.user_id == user_id)
        .offset(skip)
        .limit(limit)
    ).all()

def get_todo(session: Session, todo_id: str, user_id: Optional[str] = None) -> Optional[Todo]:
    """Get a single todo by ID, optionally filtered by user_id for security."""
    todo = session.get(Todo, todo_id)
    # If user_id is provided, verify ownership
    if todo and user_id and todo.user_id != user_id:
        return None
    return todo

def create_todo(session: Session, todo: TodoCreate, user_id: str) -> Todo:
    """Create a new todo for a specific user."""
    # Create todo directly
    db_todo = Todo(
        user_id=user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        url=todo.url,
        priority=todo.priority,
        tags=todo.tags if todo.tags else None,
        due_date=todo.due_date
    )
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def update_todo(session: Session, todo_id: str, todo: TodoUpdate, user_id: str) -> Optional[Todo]:
    """Update a todo, verifying ownership by user_id."""
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return None

    # Verify ownership
    if db_todo.user_id != user_id:
        return None

    todo_data = todo.model_dump(exclude_unset=True)
    
    # Convert tags list to comma-separated string if present
    if 'tags' in todo_data:
        if todo_data['tags']:
            todo_data['tags'] = ",".join([tag.strip() for tag in todo_data['tags'] if tag.strip()])
        else:
            todo_data['tags'] = None
    
    todo_data["updated_at"] = datetime.utcnow()

    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: str, user_id: str) -> bool:
    """Delete a todo, verifying ownership by user_id."""
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return False
    
    # Verify ownership
    if db_todo.user_id != user_id:
        return False

    session.delete(db_todo)
    session.commit()
    return True

def toggle_todo_complete(session: Session, todo_id: str, user_id: str) -> Optional[Todo]:
    """Toggle the completion status of a todo."""
    db_todo = get_todo(session, todo_id, user_id)
    if not db_todo:
        return None
    
    db_todo.completed = not db_todo.completed
    db_todo.updated_at = datetime.utcnow()
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo