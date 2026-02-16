from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import Pool
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    # Use SQLite for development/testing if no proper DB URL is provided
    DATABASE_URL = "sqlite:///./test.db"
    print("Using SQLite database for development/testing")
else:
    print("Using PostgreSQL database")

# Create engine with connection pooling settings for Neon
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

def get_session():
    with Session(engine) as session:
        yield session