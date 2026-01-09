# app.py - Main application entry point for deployment
import os
import sys
from pathlib import Path

# Add backend to path so we can import from it
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI app from backend
from main import app as application

# For deployment environments
app = application

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False
    )