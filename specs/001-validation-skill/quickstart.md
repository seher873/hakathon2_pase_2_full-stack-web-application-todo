# Quickstart Guide: Phase-2 Backend

## Prerequisites
- Node.js (v18.0 or higher)
- npm or yarn package manager
- PostgreSQL access (Neon database connection)
- Environment variables configured

## Setup Instructions

### 1. Clone and Navigate
```bash
cd /path/to/project/phase-2/backend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
Copy and configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your specific values:
```env
BETER_AUTH_SECRET=your_secret_key_here
DATABASE_URL=postgresql://username:password@host:port/database
BETER_AUTH_URL=http://localhost:3000
PORT=4000
JWT_SECRET=your_jwt_secret
```

### 4. Database Initialization
Initialize the database with required tables:

```bash
npx ts-node src/init-db.ts
```

This creates the `users` and `tasks` tables with proper relationships and triggers.

### 5. Build the Application
Compile TypeScript to JavaScript:

```bash
npm run build
```

### 6. Run the Server
Start the backend server:

```bash
npm start
```

Or run in development mode with auto-reload:

```bash
npm run dev:ts-node
```

The server will start on the configured PORT (default: 4000).

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Authenticate and get token
- `POST /api/auth/logout` - Logout (client-side token invalidation)
- `GET /api/auth/me` - Get authenticated user info

### Tasks Management
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `GET /api/tasks/:id` - Get specific task

### Health Checks
- `GET /api/health/ping` - Simple health check
- `GET /api/health/status` - Detailed status
- `GET /api/status` - Alternative status endpoint

## Testing the API

### Register a New User
```bash
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

### Login to Get Token
```bash
curl -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

### Access Protected Resources
```bash
curl -X GET http://localhost:4000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Create a Task
```bash
curl -X POST http://localhost:4000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{"title":"Sample Task", "description":"This is a sample task"}'
```

## Development

### Running in Development Mode
```bash
npm run dev:ts-node
```

This enables auto-reloading when code changes.

### Building for Production
```bash
npm run build
```

### Environment Variables Explained
- `BETER_AUTH_SECRET`: Secret key for authentication (also used for JWT)
- `DATABASE_URL`: PostgreSQL connection string (Neon database)
- `BETER_AUTH_URL`: Base URL for the application
- `PORT`: Port number for the server
- `JWT_SECRET`: Secret for JWT token signing (separate from auth secret)
- `NODE_ENV`: Environment mode (development/production)

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Verify `DATABASE_URL` is correct and database is accessible
2. **Authentication Failures**: Check that JWT_SECRET matches between token generation and verification
3. **Port Already in Use**: Change the PORT environment variable
4. **Missing Tables**: Run the init-db script again

### Checking Server Status
```bash
curl http://localhost:4000/api/health/ping
```

### Viewing Logs
The server outputs status information when started. Check for any error messages during startup.

## Next Steps
1. Integrate with frontend application
2. Add additional API endpoints as needed
3. Implement comprehensive test suite
4. Deploy to production environment