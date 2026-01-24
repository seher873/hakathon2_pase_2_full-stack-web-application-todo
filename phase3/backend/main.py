from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.health import router as health_router
from src.api.chatbot import router as chatbot_router
from src.api.ai import router as ai_router

# Import database setup
from src.services.database import create_tables

app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])
app.include_router(health_router, prefix="/api/health", tags=["health"])

@app.get("/")
def read_root():
    return {"message": "Todo App API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))