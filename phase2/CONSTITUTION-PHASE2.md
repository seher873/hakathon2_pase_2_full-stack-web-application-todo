# Phase 2 Constitution
## Core Task Management Application

### Purpose
The core application providing essential task management functionality with a beautiful, responsive UI.

### Structure
```
phase2/
├── frontend/          # React/Next.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Button.tsx
│   │   ├── pages/
│   │   ├── styles/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── backend/
│   ├── main.py          # FastAPI application entry point
│   ├── api/
│   │   ├── tasks.py     # Task-related endpoints
│   │   ├── auth.py      # Authentication endpoints
│   │   └── users.py     # User-related endpoints
│   ├── models/
│   │   ├── task.py      # Task data model
│   │   ├── user.py      # User data model
│   │   └── base.py      # Base model
│   ├── auth/
│   │   └── security.py  # Authentication logic
│   ├── db/
│   │   └── database.py  # Database connection and session management
│   ├── services/
│   │   └── task_service.py  # Business logic for tasks
│   ├── requirements.txt
│   └── tests/
└── README.md
```

### Rules and Guidelines
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

### Core Features
- User authentication and authorization
- Task creation, listing, updating, and deletion
- Task completion status management
- User-specific task isolation
- Responsive UI for all device sizes

### Success Criteria
- Stable task management functionality
- Responsive and beautiful UI
- Proper authentication and data security
- Comprehensive API coverage