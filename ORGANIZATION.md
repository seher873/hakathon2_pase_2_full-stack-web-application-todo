# Project Organization Summary

## Main Project Structure
```
hakathon_2/
├── .claude/              # Claude-specific configurations
├── .qwen/                # Qwen-specific configurations  
├── .spec-kit/            # Spec kit configurations
├── .specify/             # Specification tools
├── .vscode/              # VSCode settings
├── phase2/               # Phase 2: Specification
│   ├── backend/          # FastAPI backend
│   ├── frontend/         # Next.js/React frontend
│   ├── specs/            # Feature specifications
│   ├── history/          # Prompt history records
│   ├── docs/             # Documentation
│   ├── tests/            # Test files
│   ├── prompts/          # AI prompt templates
│   ├── config/           # Configuration files
│   └── CONSTITUTION-PHASE2.md # Phase rules
├── phase3/               # Phase 3: Planning
│   ├── backend/          # Planned backend architecture
│   ├── frontend/         # Planned frontend architecture
│   ├── specs/            # Reference specifications
│   ├── history/          # Planning history records
│   ├── docs/             # Architecture documentation
│   ├── tests/            # Test architecture plans
│   ├── prompts/          # Planning prompt templates
│   ├── config/           # Configuration architecture
│   └── CONSTITUTION-PHASE3.md # Phase rules
├── phase4/               # Phase 4: Build/Implementation
│   ├── backend/          # Planned backend implementation
│   ├── frontend/         # Planned frontend implementation
│   ├── specs/            # Reference specifications
│   ├── history/          # Implementation history records
│   ├── docs/             # Implementation documentation
│   ├── tests/            # Implementation tests
│   ├── prompts/          # Implementation prompt templates
│   ├── config/           # Configuration files
│   └── CONSTITUTION-PHASE4.md # Phase rules
├── .gitignore            # Git ignore rules
├── build.sh              # Build script
├── CLAUDE.md             # Claude instructions
├── CONSTITUTION.md       # Root AI Constitution
├── netlify.toml          # Netlify configuration
├── QWEN.md               # Qwen instructions
└── README.md             # Main project documentation
```

## Key Organizational Improvements Made

1. **Phase Structure**: Each phase now has a consistent directory structure with dedicated spaces for backend, frontend, specs, history, docs, tests, prompts, and config.

2. **Documentation**: Created comprehensive README files for the main project and each phase explaining their purpose and structure.

3. **Asset Placement**: Moved documentation files to appropriate phase directories and relocated the frontend build artifacts (dist/) to phase2/frontend/dist/.

4. **Constitution Alignment**: The structure now aligns with the multi-phase approach defined in the ROOT AI CONSTITUTION.

## Phase Purposes

- **Phase 1**: Exploration (planned)
- **Phase 2**: Specification (active) - Defining WHAT to build
- **Phase 3**: Planning (planned) - Defining HOW to build
- **Phase 4**: Implementation (planned) - Building the system
- **Phase 5**: Validation (planned) - Validating and polishing

## Technology Stack

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: Next.js/React with TypeScript and Tailwind CSS
- **AI Components**: Spec-driven architecture with skill-based actions
- **Database**: SQLAlchemy models (to be implemented)

This organization follows the principles outlined in the AI Constitution with clear separation of concerns between phases and components.