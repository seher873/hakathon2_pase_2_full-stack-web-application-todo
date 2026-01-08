# Setup Guide

This guide explains how to set up the development environment for the Hackathon Todo application.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.10 or higher)
- pip (Python package manager)
- Git
- A Neon PostgreSQL account (free tier available)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup

#### Navigate to the backend directory:
```bash
cd backend
```

#### Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Create environment file:
```bash
cp .env.example .env
```

#### Update the .env file with your settings:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
API_HOST=localhost
API_PORT=8000
DEBUG=true
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Frontend Setup

#### Navigate to the frontend directory:
```bash
cd ../frontend  # From backend directory
```

#### Install dependencies:
```bash
npm install
```

#### Create environment file:
```bash
cp .env.example .env.local
```

#### Update the .env.local file with your settings:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Running the Application

#### Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

#### In a new terminal, start the frontend:
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Backend API Docs: http://localhost:8000/api/docs

## Database Setup

The application uses Neon PostgreSQL with SQLModel. Tables are automatically created when the application starts up.

For manual database management, you can use the SQLModel CLI or connect directly to your Neon database.

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: Connection string for Neon PostgreSQL
- `JWT_SECRET`: Secret key for JWT signing (use a strong random value)
- `JWT_ALGORITHM`: Algorithm for JWT signing (default: HS256)
- `JWT_EXPIRATION_HOURS`: Hours until JWT expires (default: 24)
- `API_HOST`: Host for the API server (default: localhost)
- `API_PORT`: Port for the API server (default: 8000)
- `DEBUG`: Enable debug mode (default: true in development)
- `ENVIRONMENT`: Environment name (development, staging, production)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Base URL for the backend API

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure you've activated the Python virtual environment and installed dependencies.

2. **Database connection errors**: Verify your Neon PostgreSQL connection string and ensure the database is accessible.

3. **CORS errors**: Check that your frontend URL is included in the `ALLOWED_ORIGINS` environment variable.

4. **JWT errors**: Ensure the `JWT_SECRET` is consistent between restarts during development.

### Useful Commands

- **Run backend tests**: `cd backend && python -m pytest`
- **Format backend code**: `cd backend && black . && isort .`
- **Run frontend linting**: `cd frontend && npm run lint`
- **Build frontend**: `cd frontend && npm run build`

## Development Workflow

1. Start the backend server
2. Start the frontend server
3. Access the application at http://localhost:3000
4. API documentation is available at http://localhost:8000/api/docs