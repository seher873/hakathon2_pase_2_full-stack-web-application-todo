from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)  # This would reference the users table
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationship
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey('conversations.id'), nullable=False)
    sender_type = Column(String(10), nullable=False)  # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    parent_id = Column(String, nullable=True)  # For threading messages
    metadata_json = Column(Text, nullable=True)  # JSONB equivalent

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    session_id = Column(String(255), nullable=False, unique=True)
    last_active_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    active_conversation_id = Column(String, nullable=True)  # References conversations.id