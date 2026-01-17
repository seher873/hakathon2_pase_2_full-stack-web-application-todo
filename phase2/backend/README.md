# Phase 2 Backend - Hackathon Project

A fully functional backend for the hackathon project built with Node.js, TypeScript, Express, and BetterAuth.

## Tech Stack

- **Node.js** - JavaScript runtime
- **TypeScript** - Type-safe JavaScript
- **Express** - Web framework
- **BetterAuth** - Authentication system
- **PostgreSQL (Neon)** - Database
- **dotenv** - Environment variable management

## Features

- User authentication (register, login, logout)
- User profile management
- Task management (CRUD operations)
- Secure API endpoints
- PostgreSQL integration with Neon
- CORS configured for frontend integration

## Environment Variables

The following environment variables are required:

```env
BETER_AUTH_SECRET=94200af03c0f5f31f2b57aee49b6aa0e0afd21d843b92cb2bfacbd758223433d
DATABASE_URL=postgresql://neondb_owner:npg_Qarw4Wg5xSJe@ep-bitter-sea-a7z4sres-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETER_AUTH_URL=http://localhost:3000
PORT=4000
NODE_ENV=development
```

## API Endpoints

### Authentication
- `POST /api/auth/sign-up` - Register new user
- `POST /api/auth/sign-in` - Login user
- `POST /api/auth/sign-out` - Logout user
- `GET /api/auth/me` - Get authenticated user info

### Tasks
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `GET /api/tasks/:id` - Get specific task

### Health Check
- `GET /api/health` - Health check
- `GET /api/status` - System status
- `GET /api/health/ping` - Ping endpoint

## Installation

1. Clone the repository
2. Install dependencies: `npm install`
3. Set up environment variables
4. Build the project: `npm run build`
5. Start the server: `npm start`

## Development

To run in development mode with auto-reload:

```bash
npm run dev:ts-node
```

## Database

The application connects to a PostgreSQL database hosted on Neon. The connection is managed through a connection pool with appropriate settings for serverless environments.