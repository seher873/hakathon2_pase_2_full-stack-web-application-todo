from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")

# Create engine - use connect_args={"check_same_thread": False} for SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    # Import all models to register them with Base.metadata
    from ..models.chat_models import Conversation, Message, UserSession
    Base.metadata.create_all(bind=engine)