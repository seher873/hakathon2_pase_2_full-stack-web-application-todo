from fastapi import FastAPI
from .routes import router
from .auth import router as auth_router
from .database import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from . import models  # Import models to register them with SQLModel

# Create all tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Hackathon Phase2 Backend", version="1.0.0")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Next.js default
        "http://localhost:3001",     # Alternative Next.js port
        "http://localhost:5173",     # Vite default port
        "http://localhost:3002",     # Alternative port
        "https://*.vercel.app",      # Allow any vercel deployment
        "http://localhost:8000",     # Our backend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],  # Include Authorization header and wildcard
)

# Include the routes
app.include_router(router, prefix="/api", tags=["api"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

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