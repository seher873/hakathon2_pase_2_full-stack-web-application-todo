from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Phase-3 Chatbot API",
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint
    """
    # In a real implementation, you would check if all dependencies are ready
    # For now, we'll just return healthy
    return {
        "status": "ready",
        "service": "Phase-3 Chatbot API"
    }

@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check endpoint
    """
    # In a real implementation, you would check if the service is alive
    # For now, we'll just return healthy
    return {
        "status": "alive",
        "service": "Phase-3 Chatbot API"
    }