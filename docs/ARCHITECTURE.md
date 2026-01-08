# Architecture Documentation

## Overview
This document describes the architecture of the Hackathon Todo application, a full-stack web application built with Next.js and FastAPI.

## System Components

### Frontend (Next.js App Router)
- **Pages**: Login, Signup, Dashboard
- **Components**: TaskForm, TaskList, TaskItem, Header, AuthForm
- **Hooks**: useAuth, useTasks
- **Services**: API client with JWT injection
- **Types**: TypeScript definitions for all domain models

### Backend (FastAPI)
- **Endpoints**: Authentication and Task management APIs
- **Models**: User and Task entities using SQLModel
- **Services**: Business logic for auth and task operations
- **Middleware**: CORS, logging, error handling
- **Database**: Neon PostgreSQL with async SQLAlchemy

### Database (Neon PostgreSQL)
- **Users table**: Stores user information
- **Tasks table**: Stores tasks with user_id foreign key for isolation

## Authentication Flow

1. User registers via signup form
2. Credentials sent to backend via POST /api/auth/signup
3. Backend creates user record and generates JWT
4. JWT returned to frontend and stored in localStorage
5. JWT automatically injected in Authorization header for protected requests
6. Backend verifies JWT on each request and extracts user_id

## Data Isolation Strategy

- User ID embedded in JWT token
- All task endpoints validate JWT user_id matches URL parameter
- Database queries filtered by user_id from JWT
- 403 Forbidden returned if user tries to access another user's data

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Authenticate user

### Tasks
- `GET /api/users/{user_id}/tasks` - List all user's tasks
- `POST /api/users/{user_id}/tasks` - Create new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get single task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/users/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Security Measures

- JWT-based authentication
- CORS configured for specific origins
- Input validation via Pydantic schemas
- SQL injection prevention via SQLModel
- Password hashing with bcrypt
- User isolation at database and API levels