from app.main import app
from app.routes import router
from app.crud import create_todo
from app.schemas import TodoCreate
from app.database import get_session, engine
from sqlmodel import SQLModel, Session
from app import models
import traceback

# Create tables
SQLModel.metadata.create_all(engine)
print('Tables created', flush=True)

# Test creating a task with tags
session = Session(engine)
todo_data = TodoCreate(title='Test', tags=['work', 'urgent'], priority='high')
print(f'Todo data: {todo_data}', flush=True)
print(f'Tags type: {type(todo_data.tags)}', flush=True)
print(f'Tags value: {todo_data.tags}', flush=True)

# Try to create
try:
    todo = create_todo(session, todo_data, 'test-user')
    print(f'Created: {todo.title}, tags={todo.tags}', flush=True)
except Exception as e:
    print(f'Error: {e}', flush=True)
    traceback.print_exc()
finally:
    session.close()

print('Done!', flush=True)
