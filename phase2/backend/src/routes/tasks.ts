import express, { Request, Response, Router } from 'express';
import { pool } from '../services/database';

// Extend the Express Request type to include user
declare global {
  namespace Express {
    interface Request {
      user?: any;
    }
  }
}

// Need to export something to make this file a module
export {};

const router: Router = express.Router();

// Middleware to protect routes - check if user is authenticated
const authenticateUser = async (req: Request, res: Response, next: any) => {
  // @ts-ignore - BetterAuth adds session info to req.auth when using the middleware
  const session = req.auth?.session;

  if (!session) {
    return res.status(401).json({
      error: 'Unauthorized: No active session'
    });
  }

  // @ts-ignore - Access user data from BetterAuth
  req.user = req.auth.user;
  next();
  return; // Explicit return to satisfy TS compiler
};

// Get all tasks for authenticated user
router.get('/', authenticateUser, async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by authenticateUser middleware
    const userId = req.user.id;

    const result = await pool.query(
      'SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
      [userId]
    );

    res.status(200).json({
      data: result.rows,
      message: 'Tasks retrieved successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Get tasks error:', error);
    res.status(500).json({
      error: 'Failed to retrieve tasks',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Create a new task for authenticated user
router.post('/', authenticateUser, async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by authenticateUser middleware
    const userId = req.user.id;
    const { title, description, status } = req.body;

    if (!title) {
      return res.status(400).json({
        error: 'Title is required'
      });
    }

    const result = await pool.query(
      'INSERT INTO tasks (user_id, title, description, status) VALUES ($1, $2, $3, $4) RETURNING *',
      [userId, title, description || '', status || 'todo']
    );

    res.status(201).json({
      data: result.rows[0],
      message: 'Task created successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Create task error:', error);
    res.status(500).json({
      error: 'Failed to create task',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Update a task for authenticated user
router.put('/:id', authenticateUser, async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by authenticateUser middleware
    const userId = req.user.id;
    const taskId = req.params.id;
    const { title, description, status } = req.body;

    // Check if the task belongs to the user
    const existingTask = await pool.query(
      'SELECT * FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    if (existingTask.rows.length === 0) {
      return res.status(404).json({
        error: 'Task not found or does not belong to user'
      });
    }

    const result = await pool.query(
      'UPDATE tasks SET title = $1, description = $2, status = $3 WHERE id = $4 AND user_id = $5 RETURNING *',
      [title, description, status, taskId, userId]
    );

    res.status(200).json({
      data: result.rows[0],
      message: 'Task updated successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Update task error:', error);
    res.status(500).json({
      error: 'Failed to update task',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Delete a task for authenticated user
router.delete('/:id', authenticateUser, async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by authenticateUser middleware
    const userId = req.user.id;
    const taskId = req.params.id;

    const result = await pool.query(
      'DELETE FROM tasks WHERE id = $1 AND user_id = $2 RETURNING *',
      [taskId, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        error: 'Task not found or does not belong to user'
      });
    }

    res.status(200).json({
      message: 'Task deleted successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Delete task error:', error);
    res.status(500).json({
      error: 'Failed to delete task',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Get a specific task for authenticated user
router.get('/:id', authenticateUser, async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by authenticateUser middleware
    const userId = req.user.id;
    const taskId = req.params.id;

    const result = await pool.query(
      'SELECT * FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        error: 'Task not found or does not belong to user'
      });
    }

    res.status(200).json({
      data: result.rows[0],
      message: 'Task retrieved successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Get task error:', error);
    res.status(500).json({
      error: 'Failed to retrieve task',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

export default router;