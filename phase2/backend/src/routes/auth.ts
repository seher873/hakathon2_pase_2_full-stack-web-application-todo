import express, { Request, Response, Router } from 'express';
import { pool } from '../services/database';
import { hashPassword, verifyPassword, generateToken } from '../middleware/auth';

const router: Router = express.Router();

// Register endpoint
router.post('/register', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        error: 'Email and password are required'
      });
    }

    // Check if user already exists
    const existingUser = await pool.query('SELECT id FROM users WHERE email = $1', [email]);

    if (existingUser.rows.length > 0) {
      return res.status(409).json({
        error: 'User with this email already exists'
      });
    }

    // Hash the password
    const hashedPassword = await hashPassword(password);

    // Create the user
    const result = await pool.query(
      'INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email, created_at',
      [email, hashedPassword]
    );

    const user = result.rows[0];
    const token = generateToken(user.id, user.email);

    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user.id,
        email: user.email,
        createdAt: user.created_at
      },
      token
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Registration error:', error);
    res.status(500).json({
      error: 'Registration failed',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Login endpoint
router.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        error: 'Email and password are required'
      });
    }

    // Find the user
    const result = await pool.query('SELECT id, email, password FROM users WHERE email = $1', [email]);

    if (result.rows.length === 0) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }

    const user = result.rows[0];
    const isValidPassword = await verifyPassword(password, user.password);

    if (!isValidPassword) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }

    // Generate token
    const token = generateToken(user.id, user.email);

    res.status(200).json({
      message: 'Login successful',
      user: {
        id: user.id,
        email: user.email
      },
      token
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Login error:', error);
    res.status(500).json({
      error: 'Login failed',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Logout endpoint (client-side operation - just invalidate token)
router.post('/logout', (req: Request, res: Response) => {
  res.status(200).json({
    message: 'Logged out successfully'
  });
});

// Get authenticated user info
router.get('/me', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User will be attached by authentication middleware
    const user = req.user;

    if (!user) {
      return res.status(401).json({
        error: 'Unauthorized: No active session'
      });
    }

    res.status(200).json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name || null,
        createdAt: user.created_at,
        updatedAt: user.updated_at
      }
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Get user info error:', error);
    res.status(500).json({
      error: 'Failed to get user information',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

export default router;