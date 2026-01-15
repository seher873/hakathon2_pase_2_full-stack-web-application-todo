# How to Run the Hackathon Project

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Node.js** (for frontend) - version 18 or higher
3. **npm** or **yarn** package manager

## Installation Steps

### 1. Backend Setup (Phase-2 Core)

```bash
# Navigate to the backend directory
cd backend/

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at: `http://localhost:8000`

### 2. Frontend Setup (Phase-2 UI)

```bash
# Navigate to the frontend directory
cd frontend/

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

### 3. Phase-3 AI Enhancement Layer

The Phase-3 components are located in the `phase3/` directory and can be integrated with the Phase-2 backend once both are running.

## Alternative Quick Start (if dependencies are already installed)

If you have FastAPI and other dependencies already installed globally:

```bash
# Backend
cd backend/
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend/
npm run dev
```

## Environment Configuration

Copy the example environment file and configure your settings:

```bash
# Backend
cp .env.example .env
# Edit .env with your database and API settings

# Frontend
cp .env.example .env.local
# Edit with your backend API URL
```

## API Documentation

Once the backend is running, API documentation is available at:
- `http://localhost:8000/api/docs` (Swagger UI)
- `http://localhost:8000/api/redoc` (ReDoc)

## Phase-3 AI Agent System

To run the Phase-3 AI agent system:

```bash
cd phase3/
python -c "
from backend import create_ai_agent_system
ai_system = create_ai_agent_system()
print('AI Agent System ready!')
# Example usage:
# result = ai_system.route_request('Add a task to buy groceries', 'user-id-here')
"
```

## Project Structure Reference

- `phase2/` - Phase-2: Core application (frontend + backend)
- `phase3/` - Phase-3: AI enhancement layer
- `CONSTITUTION.md` - Architecture document
- `UI_GUIDANCE.md` - UI design guidelines

## Troubleshooting

1. **Port already in use**: Change the port in `backend/src/config.py` or kill the process using the port
2. **Database connection errors**: Verify your database configuration in `.env`
3. **Frontend cannot connect to backend**: Ensure both services are running and CORS is configured correctly
4. **Dependency conflicts**: Use a virtual environment to isolate dependencies

## Demo Commands

```bash
# Test the API health endpoint
curl http://localhost:8000/api/health

# Example AI command (once both phases are running)
curl -X POST http://localhost:8000/api/ai-skills/process \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Add a task to buy groceries", "user_id": "your-user-id"}'
```