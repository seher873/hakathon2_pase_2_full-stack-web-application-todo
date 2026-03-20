from app.database import get_session
from app.routes import router
from app.main import app
print('All imports successful', flush=True)

# Test the dependency
from sqlmodel import Session
from app.database import engine
from app import models

# Create tables
models.SQLModel.metadata.create_all(engine)
print('Tables created', flush=True)

# Test session
session = Session(engine)
print(f'Session created: {session}', flush=True)

# Test query using SQLModel select
from sqlmodel import select
result = session.exec(select(models.Todo).limit(1))
print(f'Query executed: {result.all()}', flush=True)
session.close()
print('Done!', flush=True)
