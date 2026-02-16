from sqlmodel import Session, select
from .models import Todo
from .schemas import TodoCreate, TodoUpdate
from datetime import datetime

def get_todos(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Todo).offset(skip).limit(limit)).all()

def get_todo(session: Session, todo_id: int):
    return session.get(Todo, todo_id)

def create_todo(session: Session, todo: TodoCreate):
    db_todo = Todo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def update_todo(session: Session, todo_id: int, todo: TodoUpdate):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return None

    todo_data = todo.dict(exclude_unset=True)
    todo_data["updated_at"] = datetime.utcnow()

    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: int):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True