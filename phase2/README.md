# Phase 2: Specification

This phase focuses on defining WHAT must be built for the task management application according to the AI Constitution.

## Purpose
- Define specifications for the core task management application
- Establish AI Constitution extensions
- Define skill definitions (if AI involved)
- Set security rules and constraints

## Structure
```
phase2/
├── frontend/          # React/Next.js frontend
│   ├── src/
│   │   ├── app/      # Next.js app router pages
│   │   ├── components/ # Reusable UI components
│   │   ├── hooks/    # Custom React hooks
│   │   ├── lib/      # Libraries and utilities
│   │   ├── services/ # API service clients
│   │   ├── types/    # TypeScript type definitions
│   │   └── utils/    # Utility functions
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── backend/           # FastAPI backend
│   ├── src/
│   │   ├── api/      # API route handlers (auth.py, tasks.py)
│   │   ├── models/   # Data models (task.py, user.py)
│   │   ├── schemas/  # Pydantic schemas for validation
│   │   └── services/ # Business logic (task_service.py)
│   ├── main.py       # Application entry point
│   └── requirements.txt
├── specs/            # Feature specifications
│   ├── 001-fullstack-todo/ # Example specification
│   └── ...
├── history/          # Prompt history records
│   └── 001-intent-understanding-skill/ # Example PHR
├── docs/             # Documentation
├── tests/            # Test files
├── prompts/          # AI prompt templates
├── config/           # Configuration files
└── CONSTITUTION-PHASE2.md # Phase-specific rules
```

## Rules and Guidelines
1. **Direct API Logic**: No agent layer - direct API → business logic
2. **CRUD Functionality**: Create, Read, Update, Delete tasks with proper validation
3. **UI Requirements**:
   - Beautiful, aligned, responsive, and compact
   - Task cards with consistent styling
   - Uniform buttons with proper spacing
   - Consistent color scheme and typography
4. **Code Quality**:
   - Modular and maintainable code
   - Proper error handling
   - Type hints where applicable
   - Comprehensive tests

## Core Features
- User authentication and authorization
- Task creation, listing, updating, and deletion
- Task completion status management
- User-specific task isolation
- Responsive UI for all device sizes

## Success Criteria
- Stable task management functionality
- Responsive and beautiful UI
- Proper authentication and data security
- Comprehensive API coverage