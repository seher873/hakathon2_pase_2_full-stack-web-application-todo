from sqlalchemy.orm import Session
from ..models.chat_models import Conversation, Message
from datetime import datetime
import uuid


class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: str, title: str = None) -> Conversation:
        """Create a new conversation for a user"""
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
        conversation = Conversation(
            user_id=user_id,
            title=title,
            is_active=True
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation

    def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Conversation:
        """Get a specific conversation for a user"""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

    def get_user_conversations(self, user_id: str, skip: int = 0, limit: int = 20) -> list:
        """Get all conversations for a user with pagination"""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()

    def update_conversation_title(self, conversation_id: str, user_id: str, new_title: str) -> Conversation:
        """Update conversation title"""
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if conversation:
            conversation.title = new_title
            self.db.commit()
            self.db.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Mark conversation as inactive (soft delete)"""
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if conversation:
            conversation.is_active = False
            self.db.commit()
            return True
        return False


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, conversation_id: str, sender_type: str, content: str) -> Message:
        """Create a new message in a conversation"""
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message

    def get_messages_by_conversation(self, conversation_id: str, skip: int = 0, limit: int = 50) -> list:
        """Get all messages in a conversation with pagination"""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).offset(skip).limit(limit).all()