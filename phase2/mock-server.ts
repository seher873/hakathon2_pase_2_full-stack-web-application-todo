import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = parseInt(process.env.PORT || '4000');

// Enable CORS for frontend integration
app.use(cors());
app.use(express.json());

// Simple in-memory storage for tasks and users
let users: any[] = [
  { id: '1', email: 'test@example.com', name: 'Test User', created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
];

let tasks: any[] = [];

// Health check endpoint
app.get('/api/health', (req: Request, res: Response) => {
  res.status(200).json({ status: 'ok', message: 'Mock server running' });
});

// Alternative health check endpoint
app.get('/api/status', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    service: 'Mock Backend for Testing',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString()
  });
});

// Mock authentication middleware
const authenticateToken = (req: Request, res: Response, next: any) => {
  // For testing purposes, we'll allow all requests and attach a mock user
  (req as any).user = users[0];
  next();
};

// Get all tasks for authenticated user
app.get('/api/tasks', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;

  // Filter tasks by user
  let userTasks = tasks.filter(task => task.user_id === userId);

  // Apply filters if provided
  const completedParam = req.query.completed;
  if (completedParam !== undefined) {
    const completed = completedParam === 'true';
    userTasks = userTasks.filter(task => task.completed === completed);
  }

  res.status(200).json({
    data: userTasks,
    message: 'Tasks retrieved successfully'
  });
});

// Create a new task for authenticated user
app.post('/api/tasks', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const { title, description } = req.body;

  if (!title) {
    return res.status(400).json({
      error: 'Title is required'
    });
  }

  const newTask = {
    id: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
    user_id: userId,
    title,
    description: description || '',
    completed: false, // New tasks are not completed by default
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  tasks.push(newTask);

  res.status(201).json({
    data: newTask,
    message: 'Task created successfully'
  });
});

// Update a task for authenticated user
app.put('/api/tasks/:id', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const taskId = req.params.id;
  const { title, description } = req.body;

  const taskIndex = tasks.findIndex(task => task.id === taskId && task.user_id === userId);

  if (taskIndex === -1) {
    return res.status(404).json({
      error: 'Task not found or does not belong to user'
    });
  }

  tasks[taskIndex] = {
    ...tasks[taskIndex],
    title: title || tasks[taskIndex].title,
    description: description || tasks[taskIndex].description,
    updated_at: new Date().toISOString()
  };

  res.status(200).json({
    data: tasks[taskIndex],
    message: 'Task updated successfully'
  });
});

// Toggle task completion status
app.patch('/api/tasks/:id/complete', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const taskId = req.params.id;
  const { completed } = req.body;

  if (typeof completed !== 'boolean') {
    return res.status(400).json({
      error: 'Completed field is required and must be a boolean'
    });
  }

  const taskIndex = tasks.findIndex(task => task.id === taskId && task.user_id === userId);

  if (taskIndex === -1) {
    return res.status(404).json({
      error: 'Task not found or does not belong to user'
    });
  }

  tasks[taskIndex] = {
    ...tasks[taskIndex],
    completed,
    updated_at: new Date().toISOString()
  };

  res.status(200).json({
    data: tasks[taskIndex],
    message: 'Task updated successfully'
  });
});

// Delete a task for authenticated user
app.delete('/api/tasks/:id', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const taskId = req.params.id;

  const taskIndex = tasks.findIndex(task => task.id === taskId && task.user_id === userId);

  if (taskIndex === -1) {
    return res.status(404).json({
      error: 'Task not found or does not belong to user'
    });
  }

  tasks.splice(taskIndex, 1);

  res.status(200).json({
    message: 'Task deleted successfully'
  });
});

// Get a specific task for authenticated user
app.get('/api/tasks/:id', authenticateToken, (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const taskId = req.params.id;

  const task = tasks.find(task => task.id === taskId && task.user_id === userId);

  if (!task) {
    return res.status(404).json({
      error: 'Task not found or does not belong to user'
    });
  }

  res.status(200).json({
    data: task,
    message: 'Task retrieved successfully'
  });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.status(200).json({
    message: 'Mock Backend API for Testing',
    docs: '/api/docs',
    version: '1.0.0',
  });
});

app.listen(PORT, () => {
  console.log(`Mock server is running on port ${PORT}`);
  console.log(`Health check available at http://localhost:${PORT}/api/health`);
  console.log(`Task endpoints available at http://localhost:${PORT}/api/tasks`);
});