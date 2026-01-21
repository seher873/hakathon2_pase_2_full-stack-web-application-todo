import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { pool, initializeDatabase } from './services/database';

// Load environment variables
dotenv.config();

const app = express();
const PORT = parseInt(process.env.API_PORT || '4000');

// Enhanced CORS configuration for frontend integration
const corsOptions = {
  origin: [
    process.env.BETER_AUTH_URL || 'http://localhost:3000',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:5173', // Vite default port
    'http://localhost:3002',
    'https://*.vercel.app', // Allow any vercel deployment
    'http://localhost:4000' // Our backend port
  ],
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Origin',
    'X-Requested-With',
    'Content-Type',
    'Accept',
    'Authorization',
    'Set-Cookie'
  ]
};

app.use(cors(corsOptions));
app.use(express.json());

// Additional middleware for handling cookies and headers
app.use((req, res, next) => {
  // Set security headers
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Origin', req.headers.origin as string || '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

  // intercept OPTIONS method
  if ('OPTIONS' === req.method) {
    res.sendStatus(200);
  } else {
    next();
  }
});

// No authentication middleware needed here - we'll handle it in the routes
// The authentication will be handled by individual route middleware

// Import routes
import authRoutes from './routes/auth';
import tasksRoutes from './routes/tasks';
import healthRoutes from './routes/health';
import { authenticateToken } from './middleware/auth';

// Health check routes
app.use('/api/health', healthRoutes);

// Alternative health check endpoint for compatibility
app.get('/api/status', async (req: Request, res: Response) => {
  try {
    // Test database connection
    await pool.query('SELECT 1');

    res.status(200).json({
      status: 'healthy',
      service: 'Hackathon Phase 2 Backend',
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      error: 'Database connection failed'
    });
  }
});

// API routes
app.use('/api/auth', authRoutes);

// Protected routes - require authentication
app.use('/api/tasks', authenticateToken, tasksRoutes);

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.status(200).json({
    message: 'Hackathon Phase 2 Backend API',
    docs: '/api/docs',
    version: '1.0.0',
  });
});


// Error handling middleware
app.use((err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// Start server after database initialization
async function startServer() {
  try {
    // Wait for database to be initialized
    console.log('Waiting for database initialization...');
    await initializeDatabase();
    console.log('Database initialized successfully!');

    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
      console.log(`Health check available at http://localhost:${PORT}/api/health`);
      console.log(`BetterAuth endpoints available at http://localhost:${PORT}/api/auth/*`);
      console.log(`Task endpoints available at http://localhost:${PORT}/api/tasks`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();

export default app;