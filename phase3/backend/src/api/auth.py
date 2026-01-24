from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

# Secret key for JWT decoding (should match Phase-2)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"

class TokenData(BaseModel):
    user_id: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# This is a placeholder - in a real implementation, you would validate against the Phase-2 auth system
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # In a real implementation, you would call the Phase-2 auth API to validate credentials
    # For now, we'll simulate a successful login and generate a token
    # This is just for demonstration purposes
    
    # Create a mock user ID (in reality, this would come from the user database)
    user_id = "mock-user-id-12345"
    
    # Create JWT token
    expire = datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
    to_encode = {
        "sub": user_id,
        "email": request.email,
        "exp": expire.timestamp()
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return LoginResponse(access_token=encoded_jwt)

@router.get("/me")
async def get_current_user(token: str):
    """
    Get current user info based on the provided token
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        return {
            "user_id": user_id,
            "email": email
        }
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )