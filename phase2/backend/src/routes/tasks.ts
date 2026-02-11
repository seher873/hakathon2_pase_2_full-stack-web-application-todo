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
export { };

const router: Router = express.Router();

// All routes are protected by the server-level authenticateToken middleware
// which is applied in server.ts to all /api/tasks routes

// Get all tasks for authenticated user
router.get('/', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;

    const result = await pool.query(
      'SELECT *, CASE WHEN status = \'completed\' THEN true ELSE false END as completed FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
      [userId]
    );

    // Format the response to match frontend expectations
    const formattedTasks = result.rows.map(task => ({
      ...task,
      completed: task.status === 'completed'
    }));

    res.status(200).json({
      data: formattedTasks,
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
router.post('/', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const { title, description, url, status, completed } = req.body;

    console.log('Creating task for user:', userId);
    console.log('Task data:', { title, description, url, status, completed });

    if (!title) {
      return res.status(400).json({
        error: 'Title is required'
      });
    }

    // Map completed field to status if provided
    let taskStatus = status || 'todo';
    if (typeof completed === 'boolean') {
      taskStatus = completed ? 'completed' : 'todo';
    }

    console.log('Executing INSERT query...');
    const result = await pool.query(
      'INSERT INTO tasks (user_id, title, description, url, status) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [userId, title, description || '', url || null, taskStatus]
    );

    console.log('Task created successfully:', result.rows[0]);

    res.status(201).json({
      data: result.rows[0],
      message: 'Task created successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Create task error:', error);
    console.error('Error stack:', error.stack);
    res.status(500).json({
      error: 'Failed to create task',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Update a task for authenticated user
router.put('/:id', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const taskId = req.params.id;
    const { title, description, url, status, completed } = req.body;

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

    // Map completed field to status if provided
    let taskStatus = status;
    if (typeof completed === 'boolean') {
      taskStatus = completed ? 'completed' : 'todo';
    }

    // Prepare the fields to update
    const updateFields = [];
    const params = [];
    let paramIndex = 1;

    if (title !== undefined) {
      updateFields.push(`title = $${paramIndex}`);
      params.push(title);
      paramIndex++;
    }

    if (description !== undefined) {
      updateFields.push(`description = $${paramIndex}`);
      params.push(description);
      paramIndex++;
    }

    if (url !== undefined) {
      updateFields.push(`url = $${paramIndex}`);
      params.push(url);
      paramIndex++;
    }

    if (taskStatus !== undefined) {
      updateFields.push(`status = $${paramIndex}`);
      params.push(taskStatus);
      paramIndex++;
    }

    // Add the WHERE clause parameters
    params.push(taskId, userId);

    if (updateFields.length === 0) {
      return res.status(400).json({
        error: 'At least one field must be provided for update'
      });
    }

    const query = `UPDATE tasks SET ${updateFields.join(', ')} WHERE id = $${paramIndex} AND user_id = $${paramIndex + 1} RETURNING *`;
    const result = await pool.query(query, params);

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

// Toggle task completion status
router.patch('/:id/complete', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const taskId = req.params.id;
    const { completed } = req.body;

    if (typeof completed !== 'boolean') {
      return res.status(400).json({
        error: 'Completed field is required and must be a boolean'
      });
    }

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

    const newStatus = completed ? 'completed' : 'todo';

    const result = await pool.query(
      'UPDATE tasks SET status = $1 WHERE id = $2 AND user_id = $3 RETURNING *',
      [newStatus, taskId, userId]
    );

    // Format the response to match frontend expectations
    const task = {
      ...result.rows[0],
      completed: result.rows[0].status === 'completed'
    };

    res.status(200).json({
      data: task,
      message: 'Task updated successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('Toggle task completion error:', error);
    res.status(500).json({
      error: 'Failed to update task completion status',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Delete a task for authenticated user
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const taskId = parseInt(req.params.id, 10); // Ensure taskId is a number

    // First, check if the task exists and belongs to the user
    const existingTask = await pool.query(
      'SELECT id FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    if (existingTask.rows.length === 0) {
      return res.status(404).json({
        error: 'Task not found or does not belong to user'
      });
    }

    // Perform the deletion
    await pool.query(
      'DELETE FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

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
router.get('/:id', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const taskId = req.params.id;

    const result = await pool.query(
      'SELECT *, CASE WHEN status = \'completed\' THEN true ELSE false END as completed FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        error: 'Task not found or does not belong to user'
      });
    }

    // Format the response to match frontend expectations
    const task = {
      ...result.rows[0],
      completed: result.rows[0].status === 'completed'
    };

    res.status(200).json({
      data: task,
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