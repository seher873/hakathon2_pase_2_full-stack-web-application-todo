# Data Model: AI Chatbot for Phase-3

## Overview
This document defines the data models for the AI Chatbot feature, detailing entities, relationships, and validation rules.

## Entity Definitions

### 1. Conversation
Represents a single session between a user and the AI chatbot, including all message exchanges.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `userId` (UUID, Foreign Key): Reference to the authenticated user
- `title` (VARCHAR(255)): Auto-generated or user-defined title for the conversation
- `createdAt` (TIMESTAMP): Timestamp when the conversation was initiated
- `updatedAt` (TIMESTAMP): Timestamp of the last activity in the conversation
- `isActive` (BOOLEAN): Indicates if the conversation is currently active

**Validation Rules**:
- `userId` must reference an existing user in the system
- `title` must not exceed 255 characters
- `createdAt` is set automatically on creation
- `updatedAt` is updated automatically on any message activity

**Relationships**:
- One-to-many with Message entity (one conversation contains many messages)
- Many-to-one with User entity (many conversations belong to one user)

### 2. Message
Individual text exchanges within a conversation, including metadata like timestamp and sender type.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversationId` (UUID, Foreign Key): Reference to the parent conversation
- `senderType` (ENUM: 'user' | 'ai'): Identifies whether the message is from user or AI
- `content` (TEXT): The actual message content
- `timestamp` (TIMESTAMP): When the message was sent/received
- `parentId` (UUID, Foreign Key, Nullable): Reference to parent message for threading
- `metadata` (JSONB): Additional data like AI model used, tokens consumed, etc.

**Validation Rules**:
- `conversationId` must reference an existing conversation
- `senderType` must be either 'user' or 'ai'
- `content` must not be empty
- `timestamp` is set automatically on creation
- `parentId` must reference a message in the same conversation if provided

**Relationships**:
- Many-to-one with Conversation entity (many messages belong to one conversation)
- Self-referencing for message threading (optional)

### 3. UserSession
Links conversations to authenticated users, maintaining continuity across visits.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the session
- `userId` (UUID, Foreign Key): Reference to the authenticated user
- `sessionId` (VARCHAR(255)): Session identifier from the authentication system
- `lastActiveAt` (TIMESTAMP): Timestamp of the last activity in this session
- `expiresAt` (TIMESTAMP): When this session expires
- `activeConversationId` (UUID, Foreign Key, Nullable): Currently active conversation

**Validation Rules**:
- `userId` must reference an existing user
- `sessionId` must be unique
- `expiresAt` must be in the future
- `activeConversationId` must reference an existing conversation if provided

**Relationships**:
- Many-to-one with User entity (many sessions can belong to one user)
- Many-to-one with Conversation entity (optional active conversation)

## State Transitions

### Conversation States
- **Active**: New messages can be added; appears in user's active conversations list
- **Inactive**: No recent activity; may be archived after a period of inactivity
- **Archived**: User-requested archive or system-archived due to inactivity

**Transitions**:
- Active → Inactive: After 30 days of inactivity
- Inactive → Active: When user resumes conversation
- Active → Archived: User chooses to archive
- Inactive → Archived: After 90 days of inactivity

## Indexes

### Required Indexes
1. `conversations_user_id_idx`: Index on `userId` for efficient user conversation retrieval
2. `messages_conversation_id_idx`: Index on `conversationId` for efficient conversation message retrieval
3. `messages_timestamp_idx`: Index on `timestamp` for chronological message ordering
4. `user_sessions_session_id_idx`: Index on `sessionId` for efficient session lookup
5. `conversations_updated_at_idx`: Index on `updatedAt` for sorting conversations by recency

## Constraints

### Referential Integrity
- All foreign key relationships enforce cascading deletes where appropriate
- Messages are deleted when their parent conversation is deleted
- Conversations remain when a user is deleted (for audit purposes)

### Business Constraints
- A user cannot have more than one active conversation simultaneously
- Message content must be between 1 and 10,000 characters
- Conversation titles are auto-generated from the first user message if not explicitly set

## Audit Trail

### Required Auditing
- All conversation creations and deletions
- All message creations and modifications
- Changes to conversation titles or archival status

## Performance Considerations

### Query Optimization
- Pagination support for conversations list (default 20 per page)
- Pagination support for messages within a conversation (default 50 per page)
- Efficient retrieval of most recent message in each conversation for list views