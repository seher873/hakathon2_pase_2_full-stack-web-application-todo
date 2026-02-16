from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Dummy auth endpoints for frontend compatibility
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    status: str = "success"
    data: dict
    message: str
    timestamp: str

# Mock user data
MOCK_USER = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "created_at": "2026-02-15T19:01:57.220568",
    "updated_at": "2026-02-15T19:01:57.220568"
}

MOCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3NzEyNjY1NzN9.cf7qpFSBDoiLxhIc9bUBDxmOK9asFvpkIiM2Y7EJ2SA"

@router.post("/auth/register")
def register(user: RegisterRequest):
    return {
        "status": "success",
        "data": {
            "token": MOCK_TOKEN,
            "user": MOCK_USER
        },
        "message": "Registration successful",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/auth/login")
def login(user_credentials: LoginRequest):
    return {
        "status": "success",
        "data": {
            "token": MOCK_TOKEN,
            "user": MOCK_USER
        },
        "message": "Login successful",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/auth/logout")
def logout():
    return {
        "status": "success",
        "message": "Logged out successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/auth/me")
def get_current_user():
    return {
        "status": "success",
        "data": MOCK_USER,
        "timestamp": datetime.utcnow().isoformat()
    }