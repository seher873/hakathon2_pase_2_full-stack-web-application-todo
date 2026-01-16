# Hakathon Project - Multi-Phase Todo Application

This project follows a spec-driven, multi-phase approach to building a task management application with AI capabilities.

## Project Structure

The project is organized into multiple phases as per the AI Constitution:

### Phase 1: Explore
- Purpose: Understand the problem space and explore ideas
- Status: Completed

### Phase 2: Specify (Current Implementation)
- Purpose: Define WHAT must be built
- Status: Active Development

#### Phase 2 Architecture:
```
phase2/
├── frontend/              # React/Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js app router pages
│   │   ├── components/   # Reusable UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utilities and libraries
│   │   ├── services/     # API service clients
│   │   ├── types/        # TypeScript type definitions
│   │   └── utils/        # Utility functions
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── backend/               # FastAPI backend
│   ├── src/
│   │   ├── api/          # API route handlers (auth.py, tasks.py)
│   │   ├── models/       # Data models (task.py, user.py)
│   │   ├── schemas/      # Pydantic schemas for validation
│   │   └── services/     # Business logic (task_service.py)
│   ├── main.py           # Application entry point
│   └── requirements.txt
├── specs/                # Feature specifications
├── history/              # Prompt history records
├── docs/                 # Documentation
├── tests/                # Test files
├── prompts/              # AI prompt templates
├── config/               # Configuration files
└── CONSTITUTION-PHASE2.md # Phase-specific rules
```

#### Frontend Features:
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS for styling
- Responsive design
- Multiple pages for different phases and functionality
- Task management UI components

#### Backend Features:
- FastAPI framework
- SQLAlchemy ORM
- JWT-based authentication
- Task CRUD operations
- User management
- Pydantic schema validation

### Phase 3: Plan
- Purpose: Define HOW the system will be built
- Status: Planned

### Phase 4: Build/Implement
- Purpose: Implement the planned system
- Status: Planned

### Phase 5: Validate & Polish
- Purpose: Prove the system is correct, safe, and clear
- Status: Planned

## Running the Application

### Backend Setup:
```bash
cd phase2/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup:
```bash
cd phase2/frontend
npm install
npm run dev
```

## Project Constitution

This project follows the ROOT AI CONSTITUTION which defines:
- Spec-Driven Development methodology
- Safety and determinism requirements
- User isolation principles
- Explainability and observability standards
- Phase-based development approach

For details, see `CONSTITUTION.md` in the root directory.

## Current Status

The project is currently in Phase 2 (Specify), with active development on both frontend and backend components. The core task management functionality is being specified and implemented with a focus on creating a beautiful, responsive UI and robust backend APIs.