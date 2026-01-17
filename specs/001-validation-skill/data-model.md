# Data Model: Phase-2 Backend

## Overview
The data model consists of two primary entities: Users and Tasks, with a relationship where each task belongs to a user. The system uses PostgreSQL as the primary data store with Neon hosting for serverless capabilities.

## Entity: User

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address for login |
| password | VARCHAR(255) | NOT NULL | BCrypt hashed password |
| name | VARCHAR(255) | NULL | Optional user display name |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record update timestamp |

### Relationships
- **One-to-Many**: User has many Tasks (via user_id foreign key)

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must be provided and stored as a hash
- Email and password required for registration

### State Transitions
- User account created on registration
- User data updated when profile information is modified

## Entity: Task

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing unique identifier |
| user_id | INTEGER | FOREIGN KEY references users(id), NOT NULL | Reference to owning user |
| title | VARCHAR(255) | NOT NULL | Task title or subject |
| description | TEXT | NULL | Detailed task description |
| status | VARCHAR(50) | DEFAULT 'todo' | Task status (todo, in-progress, done) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record update timestamp |

### Relationships
- **Many-to-One**: Task belongs to one User (via user_id foreign key)

### Validation Rules
- Title is required for all tasks
- Status must be one of: 'todo', 'in-progress', 'done'
- Task can only be accessed/modified by the owning user
- User_id must reference an existing user

### State Transitions
- Task created with status 'todo' by default
- Task status updated through PUT requests
- Task deleted permanently on DELETE request

## Database Schema SQL

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'todo',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at columns
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
  BEFORE UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Indexes
- Primary key indexes on id fields (automatically created)
- Foreign key index on tasks.user_id (for JOIN operations)
- Potential future indexes on status field if needed for queries

## Data Integrity
- Foreign key constraint ensures tasks reference valid users
- Cascade delete removes tasks when user is deleted
- Unique constraint on email prevents duplicate accounts
- NOT NULL constraints ensure required fields are populated

## Security Considerations
- No direct access to passwords (stored as hashes)
- Row-level security via user_id foreign key (users can only access their own tasks)
- Parameterized queries prevent SQL injection
- Proper authentication required for all data access operations