---
title: Hackathon Phase 2 & 3 - Todo App with AI Chatbot
emoji: 🤖
colorFrom: purple
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# Hackathon Phase 2 & 3 - AI-Powered Todo App

A full-stack todo application with:
- **Phase 2**: Intermediate features (Priority, Tags, Due Date, Search, Filter, Sort)
- **Phase 3**: AI Chatbot with natural language processing

## Features

### Task Management
- ✅ Create, Read, Update, Delete tasks
- ✅ Priority levels (Low, Medium, High)
- ✅ Tags/Categories
- ✅ Due dates
- ✅ Search and filter
- ✅ Sort by various fields

### AI Chatbot
- 🤖 Natural language task management
- 💬 Conversational interface
- 📝 MCP-style tools for task operations
- 💾 Conversation persistence

## Quick Start

### Using the Space

1. **Frontend**: Click on the "Application" tab at the top
2. **Sign Up**: Create an account
3. **Start Adding Tasks**: Use the dashboard or AI chatbot!

### AI Chatbot Commands

Try these natural language commands:
- "Add buy milk"
- "Show my tasks"
- "Complete buy milk"
- "Delete old task"
- "Show pending tasks"

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks` | List tasks |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/{id}/complete` | Toggle complete |
| POST | `/api/chat` | AI chatbot |
| GET | `/api/chat/help` | Chat help |

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python, SQLModel
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **AI**: Rule-based NLP with MCP pattern

## Project Structure

```
phase2/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   ├── routes.py        # Task routes
│   │   ├── chatbot.py       # AI chatbot
│   │   └── auth.py          # Authentication
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages
│   │   ├── components/      # React components
│   │   └── hooks/           # Custom hooks
│   └── package.json
└── specs/
    └── features/
        └── phase3-chatbot.md
```

## Testing

### Backend Tests
```bash
cd backend
py test_chatbot.py
```

### API Testing
```bash
# Health check
curl http://localhost:4001/health

# Create task
curl -X POST http://localhost:4001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","priority":"high"}'

# Chat with AI
curl -X POST http://localhost:4001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Add buy milk"}'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | SQLite |
| `NEXT_PUBLIC_API_URL` | Backend API URL | http://localhost:4001 |

## License

MIT License - See LICENSE file for details

## Credits

Built for Hackathon Phase 2 & 3
- Spec-Driven Development
- MCP Pattern for AI Tools
- Natural Language Processing
