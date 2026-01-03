# Phase 0: Research & Findings

**Feature**: Phase II Full-Stack Todo Web Application
**Date**: 2026-01-03
**Status**: Complete

---

## Research Tasks & Findings

### 1. Better Auth Integration Pattern

**Question**: How to integrate Better Auth SDK in Next.js App Router for user management?

**Decision**: Use Better Auth's official Next.js integration

**Rationale**:
- Better Auth provides pre-built Next.js middleware and hooks
- Automatic OAuth2 handling reduces custom code
- Works seamlessly with App Router
- User management handled server-side

**Implementation Approach**:
- Install `@better-auth/next` and `@better-auth/core`
- Initialize Better Auth in `src/lib/auth.ts`
- Create API route: `src/app/api/auth/[...auth]/route.ts`
- Use `useSession` hook in client components
- JWT token available in session after login

**Alternatives Considered**:
- Auth0: More complex, expensive for Phase II scope
- NextAuth.js: Different architecture, requires more configuration
- Manual OAuth: Not recommended, security risks

---

### 2. JWT Verification in FastAPI

**Question**: Best practices for JWT middleware in FastAPI with user context extraction?

**Decision**: Use PyJWT with FastAPI dependency injection

**Rationale**:
- FastAPI has native dependency injection support
- PyJWT is lightweight and battle-tested
- Middleware can extract JWT and pass user_id to routes
- Type-safe with Pydantic models

**Implementation Approach**:
```python
# Create JWT dependency
async def get_current_user(token: str = Header(...)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    user_id = payload.get("sub")
    return user_id

# Use in route
@app.get("/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id is automatically verified and extracted
```

**Error Handling**:
- 401 for missing token
- 401 for invalid signature
- 401 for expired token
- 403 for user_id mismatch in route parameters

**Alternatives Considered**:
- Python-jose: More features, overkill for simple JWT
- Custom token parsing: Security risks
- OAuth2 library: Unnecessary complexity

---

### 3. Neon Connection Pooling

**Question**: Optimal connection string configuration for serverless PostgreSQL?

**Decision**: Use Neon connection pooling with pgBouncer

**Rationale**:
- Serverless functions create/destroy connections rapidly
- pgBouncer pools connections to avoid connection limits
- Neon provides built-in pooling configuration
- Cost-effective for variable loads

**Implementation Approach**:
```
# Standard connection string
postgresql://user:password@neon.tech/dbname

# With pooling enabled
postgresql://user:password@neon-pooled.tech/dbname?sslmode=require
```

**Configuration**:
- Set `pool_size=5` in SQLAlchemy
- Use `NullPool` for serverless to avoid stale connections
- Connection timeout: 30 seconds
- Idle timeout: 300 seconds

**Monitoring**:
- Watch active connections in Neon dashboard
- Set alerts for connection limit exceeded
- Monitor query performance with pg_stat_statements

**Alternatives Considered**:
- AWS RDS Proxy: Regional, not available everywhere
- Manual connection management: Error-prone
- No pooling: Connection limits exceeded quickly

---

### 4. SQLModel Type Safety

**Question**: Patterns for SQLModel schema with Pydantic validation?

**Decision**: Separate table and schema models

**Rationale**:
- Clean separation: database models vs. API schemas
- Type safety for all operations
- Pydantic validation on input/output
- Easy to evolve API without DB changes

**Implementation Approach**:

```python
# Database model (table)
class TaskTable(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Schema for API (Pydantic)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Validation Benefits**:
- Input validation on create/update
- Output serialization on responses
- Type hints for IDE autocomplete
- Runtime validation with clear error messages

**Alternatives Considered**:
- Tortoise ORM: No Pydantic integration
- Django ORM: Not suitable for FastAPI
- Raw SQLAlchemy: No automatic validation

---

### 5. CORS Configuration

**Question**: Vercel frontend to Cloud Run backend CORS setup?

**Decision**: Configure CORS middleware in FastAPI

**Rationale**:
- Vercel URLs are dynamic with unique subdomains
- Browser security requires explicit CORS headers
- FastAPI has built-in CORS support
- Environment-based configuration for flexibility

**Implementation Approach**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.vercel.app",
        "http://localhost:3000",  # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],  # For pagination
)
```

**Environment Configuration**:
```
# .env
ALLOWED_ORIGINS=https://your-domain.vercel.app,http://localhost:3000
```

**Security Considerations**:
- Never use `allow_origins=["*"]` with credentials
- Be specific about allowed origins
- Review CORS headers in production

**Alternatives Considered**:
- Cloud Run CORS settings: Limited control
- Manual header middleware: Duplicates logic
- No CORS: Requests fail in browser

---

## Architectural Decisions Summary

| Topic | Decision | Confidence | ADR Required |
|-------|----------|------------|--------------|
| Frontend Auth | Better Auth + JWT | 95% | No |
| Backend JWT | PyJWT in FastAPI middleware | 95% | No |
| Database Pooling | Neon pgBouncer | 90% | No |
| Type Safety | SQLModel + Pydantic | 95% | No |
| CORS Strategy | FastAPI middleware + environment config | 95% | No |
| API Response Format | Standard JSON with status field | 90% | Yes (ADR-004) |
| Error Handling | Consistent error schema | 90% | Yes (ADR-005) |
| Data Isolation | User ID from JWT | 95% | Yes (ADR-001) |

---

## Resolved Clarifications

✅ All NEEDS CLARIFICATION items from spec have been addressed:
- Authentication method: JWT with Better Auth
- Database choice: Neon PostgreSQL
- ORM choice: SQLModel
- API style: RESTful JSON
- Type safety approach: Separate models + Pydantic validation

---

## Dependencies & Constraints Validated

✅ **Frontend Dependencies**:
- Next.js 16+ available on npm
- Better Auth has Next.js integration
- Tailwind CSS 3+ available
- TypeScript 5+ supported

✅ **Backend Dependencies**:
- FastAPI 0.100+ stable and production-ready
- SQLModel actively maintained
- PyJWT widely used for JWT handling
- Pydantic v2 for validation

✅ **Database & Deployment**:
- Neon PostgreSQL fully serverless
- Connection pooling available
- Vercel native support for both frontend and backend
- Environment-based configuration supported

---

## Next Steps

1. ✅ Research complete - all decisions made
2. ⏭️ Create data-model.md with detailed schema
3. ⏭️ Generate API contracts in OpenAPI format
4. ⏭️ Create quickstart.md for developers
5. ⏭️ Generate tasks.md with implementation breakdown

---

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-03 | Initial research findings |
