import express, { Request, Response, Router } from 'express';
import { pool } from '../../services/database';

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

// All routes are protected by the server-level authenticateToken middleware
// which will be applied in server.ts to all /api/ai routes

// Mock AI processing endpoint
router.post('/process', async (req: Request, res: Response) => {
  try {
    // @ts-ignore - User is attached by server-level authenticateToken middleware
    const userId = req.user.id;
    const { input } = req.body;

    if (!input) {
      return res.status(400).json({
        error: 'Input is required',
        message: 'No command provided to process'
      });
    }

    // Log the received command for debugging
    console.log(`Processing AI command for user ${userId}:`, input);

    // Simple mock AI processing - in a real implementation, this would connect to an AI service
    let responseMessage = '';
    let tasksToCreate: any[] = [];

    // Simple parsing of the command to determine intent
    const lowerInput = input.toLowerCase();

    if (lowerInput.includes('add') || lowerInput.includes('create') || lowerInput.includes('new')) {
      // Extract potential task information from the command
      const titleMatch = input.match(/(?:add|create|new)\s+(.+?)(?:\.|$)/i);
      let title = titleMatch ? titleMatch[1].trim() : 'New task from AI';
      
      // If title is too generic, use the whole input
      if (title.toLowerCase().includes('task')) {
        title = input.substring(0, 50) + (input.length > 50 ? '...' : '');
      }

      tasksToCreate.push({
        title,
        description: `Created from AI command: "${input}"`,
        status: 'todo'
      });

      responseMessage = `I've created the task: "${title}"`;
    } else if (lowerInput.includes('list') || lowerInput.includes('show') || lowerInput.includes('view')) {
      // Return user's tasks
      const result = await pool.query(
        'SELECT *, CASE WHEN status = \'completed\' THEN true ELSE false END as completed FROM tasks WHERE user_id = $1 ORDER BY created_at DESC LIMIT 10',
        [userId]
      );

      const tasks = result.rows.map(task => ({
        ...task,
        completed: task.status === 'completed'
      }));

      responseMessage = `You have ${tasks.length} tasks. ${tasks.length > 0 ? 'Here are your most recent tasks:' : 'You have no tasks.'}`;
      
      return res.status(200).json({
        data: {
          message: responseMessage,
          tasks
        },
        message: 'Tasks retrieved successfully'
      });
    } else {
      // Default response for unrecognized commands
      responseMessage = `I understood your command: "${input}". You can ask me to create tasks or list your existing tasks.`;
    }

    // Create any tasks that were identified
    for (const taskData of tasksToCreate) {
      await pool.query(
        'INSERT INTO tasks (user_id, title, description, status) VALUES ($1, $2, $3, $4)',
        [userId, taskData.title, taskData.description, taskData.status]
      );
    }

    res.status(200).json({
      data: {
        message: responseMessage,
        tasksCreated: tasksToCreate.length,
        tasks: tasksToCreate
      },
      message: 'AI command processed successfully'
    });
    return; // Explicit return to satisfy TS compiler
  } catch (error: any) {
    console.error('AI process error:', error);
    res.status(500).json({
      error: 'Failed to process AI command',
      message: error.message
    });
    return; // Explicit return to satisfy TS compiler
  }
});

// Health check for AI service
router.get('/health', (_req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    service: 'AI Processing Service',
    timestamp: new Date().toISOString()
  });
});

export default router;