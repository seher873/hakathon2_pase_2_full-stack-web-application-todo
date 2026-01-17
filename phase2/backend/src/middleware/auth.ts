import { Request, Response, NextFunction } from 'express';
import { pool } from '../services/database';
import * as bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

// Extend the Express Request type to include user
declare global {
  namespace Express {
    interface Request {
      user?: any;
    }
  }
}

export const generateToken = (userId: string, email: string): string => {
  const secret = process.env.JWT_SECRET || 'fallback_secret_key_for_dev';
  const expiresIn = process.env.JWT_EXPIRES_IN || '24h';

  return jwt.sign(
    { userId, email },
    secret,
    { expiresIn: expiresIn as any }
  );
};

export const hashPassword = async (password: string): Promise<string> => {
  const saltRounds = parseInt(process.env.SALT_ROUNDS || '10');
  return await bcrypt.hash(password, saltRounds);
};

export const verifyPassword = async (password: string, hashedPassword: string): Promise<boolean> => {
  return await bcrypt.compare(password, hashedPassword);
};

export const authenticateToken = async (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  const secret = process.env.JWT_SECRET || 'fallback_secret_key_for_dev';

  try {
    const decoded: any = jwt.verify(token, secret);

    // Verify the user still exists in the database
    const result = await pool.query('SELECT id, email, name, created_at, updated_at FROM users WHERE id = $1', [decoded.userId]);

    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid token - user not found' });
    }

    req.user = result.rows[0];
    next();
    return; // Explicit return to satisfy TS compiler
  } catch (error) {
    console.error('Token verification error:', error);
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
};

export {};