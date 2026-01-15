You are defining the ROOT AI CONSTITUTION
for a Spec-Driven, multi-phase Todo Application.

This document is the SINGLE SOURCE OF TRUTH
that governs ALL phases of the project.

This constitution must NEVER be replaced.
It may only be EXTENDED as the system evolves.

==================================================
SECTION 1: CORE CONSTITUTIONAL PRINCIPLES
(APPLY TO ALL PHASES)
==================================================

1. Spec-Driven Development
- No implementation without specification
- Every phase must follow:
  Explore → Specify → Plan → Build → Validate

2. Safety & Determinism
- AI must behave predictably
- No hallucinated actions
- No undefined behavior

3. Least Privilege
- AI has NO direct database access
- All actions go through approved APIs

4. User Isolation
- Each user may only access their own data
- Cross-user access is strictly forbidden

5. Explainability & Observability
- Every AI decision must be explainable
- Every action must be traceable via logs

==================================================
SECTION 2: GLOBAL SYSTEM CONSTRAINTS
==================================================

- JWT authentication is mandatory
- user_id must come ONLY from auth context
- No hard-coded secrets
- No bypassing backend authorization
- No external tools unless explicitly specified
- No background autonomous execution

==================================================
SECTION 3: PHASE-1 — EXPLORE
==================================================

Purpose:
- Understand the problem space
- Explore ideas and assumptions

Rules:
- Experimental code allowed
- Prototypes are disposable
- No production guarantees required

Outputs:
- Problem understanding
- Initial ideas
- Risks and assumptions

==================================================
SECTION 4: PHASE-2 — SPECIFY
==================================================

Purpose:
- Define WHAT must be built

Rules:
- No production code
- Define boundaries, rules, and acceptance criteria

Outputs:
- Specifications
- AI Constitution extensions
- Skill definitions (if AI involved)
- Security rules

==================================================
SECTION 5: PHASE-3 — PLAN
==================================================

Purpose:
- Define HOW the system will be built

Rules:
- No feature changes
- Architecture decisions only

Outputs:
- Architecture plan
- Folder structure
- Data flow
- Agent orchestration design

==================================================
SECTION 6: PHASE-4 — BUILD / IMPLEMENT
==================================================

Purpose:
- Implement the planned system

Rules:
- Must strictly follow specifications and plans
- Backend APIs are authoritative
- Frontend communicates only via APIs

AI-Specific Rules (if applicable):
- AI may act ONLY via predefined SKILLS
- SKILLS map directly to existing backend APIs
- SUB-AGENTS may decide, not act
- No direct DB or model access by agents

Architecture:
User → Sub-Agents → Skills → Backend APIs → Database

==================================================
SECTION 7: PHASE-5 — VALIDATE & POLISH
==================================================

Purpose:
- Prove the system is correct, safe, and clear

Rules:
- NO new features allowed
- Focus on validation, logging, and documentation

Required:
- Validation of AI boundaries
- Logging of agent and skill execution
- User-friendly error handling
- Clear README and demo explanation

==================================================
SECTION 8: CHANGE MANAGEMENT
==================================================

- Core principles may NEVER be removed
- Each phase may only ADD constraints
- No phase may weaken security or safety rules

==================================================
SECTION 9: SUCCESS CRITERIA
==================================================

The system is complete when:
- All 5 phases follow this constitution
- AI behavior is controlled and deterministic
- User data is fully isolated
- System behavior is observable and explainable
- Documentation clearly reflects architecture

==================================================
END OF ROOT AI CONSTITUTION
==================================================