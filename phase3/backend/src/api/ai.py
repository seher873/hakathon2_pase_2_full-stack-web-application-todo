from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session
from ..services.chatbot_service import ChatbotService, ChatRequest, ChatResponse
from ..services.database import get_db
from ..services.conversation_service import ConversationService, MessageService

router = APIRouter()
security = HTTPBearer()

# Initialize chatbot service
chatbot_service = ChatbotService()

# Secret key for JWT decoding (should match Phase-2)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"

class AIProcessRequest(BaseModel):
    input: str

class AIProcessResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str

def verify_token(token: str):
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@router.post("/process")
async def process_ai_command(
    request: AIProcessRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Process an AI command from the frontend
    Matches the expected interface from the Next.js frontend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")

    try:
        # Process the command using the chatbot service
        result = await chatbot_service.process_message(
            message=request.input,
            user_id=user_id
        )

        # Format response to match frontend expectations
        response_data = {
            "message": result.get("response", ""),
            "intent": result.get("intent", ""),
            "conversation_id": result.get("conversation_id", ""),
            "metadata": result.get("metadata", {})
        }

        return AIProcessResponse(
            success=True,
            data=response_data,
            message=result.get("response", "Command processed successfully")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing AI command: {str(e)}"
        )

