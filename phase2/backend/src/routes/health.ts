import express, { Request, Response, Router } from 'express';
import { pool } from '../services/database';

const router: Router = express.Router();

// Root health check endpoint
router.get('/', async (req: Request, res: Response) => {
  try {
    // Test database connection
    await pool.query('SELECT 1');

    res.status(200).json({
      status: 'healthy',
      service: 'Hackathon Phase 2 Backend',
      version: '1.0.0',
      timestamp: new Date().toISOString()
    });
  } catch (error: any) {
    console.error('Health check error:', error);
    res.status(500).json({
      status: 'unhealthy',
      service: 'Hackathon Phase 2 Backend',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Detailed health check with database connectivity
router.get('/status', async (req: Request, res: Response) => {
  try {
    // Test database connection
    await pool.query('SELECT 1');

    res.status(200).json({
      status: 'healthy',
      service: 'Hackathon Phase 2 Backend',
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      timestamp: new Date().toISOString(),
      database: {
        status: 'connected',
        name: process.env.DATABASE_URL ? 'PostgreSQL (Neon)' : 'unknown'
      },
      uptime: process.uptime(),
      memory: process.memoryUsage()
    });
  } catch (error: any) {
    console.error('Health check error:', error);
    res.status(500).json({
      status: 'unhealthy',
      service: 'Hackathon Phase 2 Backend',
      version: '1.0.0',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Simple ping endpoint
router.get('/ping', (req: Request, res: Response) => {
  res.status(200).json({
    message: 'Pong!',
    timestamp: new Date().toISOString()
  });
});

export default router;