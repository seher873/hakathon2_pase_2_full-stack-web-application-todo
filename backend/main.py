"""Main entry point for the AI-Powered Todo Chatbot backend."""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat_routes import router as chat_router
from .mcp.auth_wrapper import get_jwt_secret

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="AI-Powered Todo Chatbot API",
    description="Backend API for the AI-Powered Todo Chatbot feature",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat_router)

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {
        "message": "AI-Powered Todo Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-chatbot-backend",
        "version": "1.0.0"
    }

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )