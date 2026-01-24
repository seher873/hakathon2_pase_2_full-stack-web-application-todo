# Phase-3: AI Chatbot Implementation

## Overview
This directory contains the AI chatbot implementation that extends the existing Phase-2 application. The chatbot allows users to interact with the task management system using natural language.

## Architecture
- **Backend**: Python FastAPI application with Cohere AI integration
- **Frontend**: React application with chat interface

## Features
- Natural language processing for task management
- Intent classification (create/list/update/delete tasks)
- Conversation history
- Integration with existing authentication system

## Setup

### Backend
1. Navigate to the backend directory:
   ```bash
   cd phase3/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python main.py
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd phase3/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the application:
   ```bash
   npm start
   ```

## API Endpoints

### Chat Endpoint
- **POST** `/api/chatbot/chat`
- Headers: `Authorization: Bearer {jwt_token}`
- Request Body:
  ```json
  {
    "message": "string",
    "conversation_id": "string (optional)"
  }
  ```
- Response:
  ```json
  {
    "conversation_id": "string",
    "response": "string",
    "intent": "string",
    "confidence": "float",
    "metadata": "object"
  }
  ```

## Environment Variables

### Backend
- `COHERE_API_KEY`: Your Cohere API key
- `JWT_SECRET_KEY`: Secret key for JWT token verification
- `DATABASE_URL`: PostgreSQL database connection string
- `PORT`: Port to run the server on (default: 8000)

### Frontend
- `REACT_APP_BACKEND_BASE_URL`: URL of the backend server
- `REACT_APP_COHERE_API_KEY`: Your Cohere API key (if needed on frontend)

## Intent Classification
The chatbot recognizes the following intents:
- `create_todo`: Creating new tasks
- `list_todos`: Listing existing tasks
- `delete_todo`: Deleting tasks
- `update_todo`: Updating task status/completion
- `chitchat`: General conversation

## Security
- All chat endpoints require valid JWT authentication
- API keys are stored securely in environment variables
- Input validation is performed on all user inputs