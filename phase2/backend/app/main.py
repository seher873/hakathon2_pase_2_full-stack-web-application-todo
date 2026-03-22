from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from .routes import router
from .auth import router as auth_router
from .chatbot import router as chatbot_router
from .database import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from . import models  # Import models to register them with SQLModel
import traceback
import json

# Create all tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Hackathon Phase2 Backend", version="1.0.0")

# Add middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "POST" and "/tasks" in request.url.path:
        body = await request.body()
        print(f"Request body: {body.decode()}")
    response = await call_next(request)
    return response

# Add exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": str(exc),
            "traceback": traceback.format_exc()
        }
    )

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Next.js default
        "http://localhost:3001",     # Alternative Next.js port
        "http://localhost:5173",     # Vite default port
        "http://localhost:3002",     # Alternative port
        "https://*.vercel.app",      # Allow any vercel deployment
        "https://*.netlify.app",     # Allow any netlify deployment
        "http://localhost:8000",     # Our backend port
        "*",                         # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(router, prefix="/api", tags=["api"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Hackathon Phase 2 Backend", "version": "1.0.0"}

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Hackathon Phase 2 Backend API",
        "docs": "/docs",
        "version": "1.0.0",
    }

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)