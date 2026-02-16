# FastAPI Todo Backend

A simple FastAPI backend for a Todo application using SQLModel and PostgreSQL (Neon).

## Features

- CRUD operations for todos
- PostgreSQL support with Neon
- SQLite support for local development
- Auto-generated Swagger UI documentation
- CORS enabled for frontend integration

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Update `DATABASE_URL` with your Neon PostgreSQL connection string
3. For local development, you can use SQLite by setting: `DATABASE_URL=sqlite:///./todo.db`

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- Base URL: http://localhost:8000
- Swagger UI: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

## API Endpoints

- `GET /api/todos` - List all todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

## Todo Model

```json
{
  "id": 1,
  "title": "Todo title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2026-02-15T19:01:57.220568",
  "updated_at": "2026-02-15T19:01:57.220632"
}
```