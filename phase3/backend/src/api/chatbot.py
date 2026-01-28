from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session
from ..services.chatbot_service import ChatbotService, ChatRequest, ChatResponse
from ..services.database import SessionLocal, get_db
from ..services.conversation_service import ConversationService, MessageService

router = APIRouter()
security = HTTPBearer()

# Initialize chatbot service
chatbot_service = ChatbotService()

# Secret key for JWT decoding (should match Phase-2)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key_for_dev")
ALGORITHM = "HS256"

class ChatRequestPayload(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponsePayload(BaseModel):
    conversation_id: str
    response: str
    intent: str
    confidence: float
    metadata: dict

class CreateConversationRequest(BaseModel):
    title: Optional[str] = None

class UpdateConversationRequest(BaseModel):
    title: str

def verify_token(token: str):
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Check for user_id (snake_case) OR userId (camelCase, from Node backend)
        user_id = payload.get("user_id") or payload.get("userId")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: user_id missing"
            )
            
        # Ensure we return a consistent payload with user_id
        if "user_id" not in payload:
            payload["user_id"] = user_id
            
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@router.post("/chat", response_model=ChatResponsePayload)
async def chat_endpoint(
    request: ChatRequestPayload,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint that processes user messages and returns AI responses
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")

    try:
        # Process the message using the chatbot service
        result = await chatbot_service.process_message(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=user_id
        )

        return ChatResponsePayload(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

@router.get("/conversations")
async def get_conversations(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=50),
    sort: str = Query(default="updatedAt"),
    order: str = Query(default="desc")
):
    """
    Get conversation history for the authenticated user
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    conversation_service = ConversationService(db)
    
    # Calculate offset for pagination
    skip = (page - 1) * limit
    
    # Get user conversations
    conversations = conversation_service.get_user_conversations(user_id, skip=skip, limit=limit)
    
    # Prepare response data
    conversations_data = []
    for conv in conversations:
        # Count messages in each conversation
        message_service = MessageService(db)
        messages = message_service.get_messages_by_conversation(conv.id)
        
        conversations_data.append({
            "id": conv.id,
            "title": conv.title,
            "createdAt": conv.created_at.isoformat() if conv.created_at else None,
            "updatedAt": conv.updated_at.isoformat() if conv.updated_at else None,
            "messageCount": len(messages)
        })
    
    # Get total count for pagination
    total_count = len(conversation_service.get_user_conversations(user_id))
    total_pages = (total_count + limit - 1) // limit  # Ceiling division
    
    return {
        "success": True,
        "data": {
            "conversations": conversations_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": total_pages
            }
        }
    }

@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get a specific conversation with all its messages
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    conversation_service = ConversationService(db)
    message_service = MessageService(db)
    
    # Get the conversation
    conversation = conversation_service.get_conversation_by_id(conversation_id, user_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or doesn't belong to user"
        )
    
    # Get messages in the conversation
    messages = message_service.get_messages_by_conversation(conversation_id)
    
    # Format messages
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "senderType": msg.sender_type,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
        })
    
    return {
        "success": True,
        "data": {
            "conversation": {
                "id": conversation.id,
                "title": conversation.title,
                "createdAt": conversation.created_at.isoformat() if conversation.created_at else None,
                "updatedAt": conversation.updated_at.isoformat() if conversation.updated_at else None,
                "messages": formatted_messages
            }
        }
    }

@router.post("/conversation")
async def create_conversation(
    request: CreateConversationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Create a new conversation
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    conversation_service = ConversationService(db)
    
    conversation = conversation_service.create_conversation(
        user_id=user_id,
        title=request.title
    )
    
    return {
        "success": True,
        "data": {
            "conversation": {
                "id": conversation.id,
                "title": conversation.title,
                "createdAt": conversation.created_at.isoformat() if conversation.created_at else None,
                "updatedAt": conversation.updated_at.isoformat() if conversation.updated_at else None
            }
        }
    }

@router.put("/conversation/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    request: UpdateConversationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Update a conversation (e.g., change title)
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    conversation_service = ConversationService(db)
    
    updated_conversation = conversation_service.update_conversation_title(
        conversation_id=conversation_id,
        user_id=user_id,
        new_title=request.title
    )
    
    if not updated_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or doesn't belong to user"
        )
    
    return {
        "success": True,
        "data": {
            "conversation": {
                "id": updated_conversation.id,
                "title": updated_conversation.title,
                "createdAt": updated_conversation.created_at.isoformat() if updated_conversation.created_at else None,
                "updatedAt": updated_conversation.updated_at.isoformat() if updated_conversation.updated_at else None
            }
        }
    }

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Delete/archive a conversation
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    conversation_service = ConversationService(db)
    
    success = conversation_service.delete_conversation(
        conversation_id=conversation_id,
        user_id=user_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or doesn't belong to user"
        )
    
    return {
        "success": True,
        "data": {
            "message": "Conversation deleted successfully"
        }
    }

@router.get("/session")
async def get_session_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get user session information
    """
    user_payload = verify_token(credentials.credentials)
    user_id = user_payload.get("user_id")
    
    # For now, return basic session info
    # In a real implementation, you would track active conversations, etc.
    return {
        "success": True,
        "data": {
            "session": {
                "userId": user_id,
                "activeConversationId": None,  # Would track the current active conversation
                "lastActiveAt": __import__('datetime').datetime.now().isoformat(),
                "rateLimitInfo": {
                    "remaining": 10,  # Default rate limit
                    "resetTime": (__import__('datetime').datetime.now() + __import__('datetime').timedelta(minutes=1)).isoformat()
                }
            }
        }
    }

@router.get("/health")
async def chat_health():
    """
    Health check for the chatbot service
    """
    return {"status": "healthy", "service": "chatbot"}