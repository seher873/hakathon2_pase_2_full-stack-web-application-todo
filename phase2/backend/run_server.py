import uvicorn
from app.main import app
import os
import sys
from sqlmodel import SQLModel
from app.database import engine
from contextlib import asynccontextmanager

def create_db_and_tables():
    try:
        print("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Continue anyway - might be a connection issue that doesn't affect startup

if __name__ == "__main__":
    # Create tables on startup
    create_db_and_tables()

    print("Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")

    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )