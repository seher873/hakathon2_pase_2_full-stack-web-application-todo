import { NextResponse } from 'next/server';

// GET /api/task - Retrieve all tasks
export async function GET(request) {
  try {
    // TODO: Implement actual task retrieval logic
    // This is a placeholder implementation
    
    const tasks = [
      {
        id: 1,
        title: "Sample Task",
        description: "This is a sample task",
        completed: false,
        createdAt: new Date().toISOString()
      },
      {
        id: 2,
        title: "Another Sample Task",
        description: "This is another sample task",
        completed: true,
        createdAt: new Date().toISOString()
      }
    ];

    return NextResponse.json({ 
      success: true, 
      data: tasks,
      message: "Tasks retrieved successfully"
    });
  } catch (error) {
    console.error('Error retrieving tasks:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to retrieve tasks',
      message: error.message 
    }, { status: 500 });
  }
}

// POST /api/task - Create a new task
export async function POST(request) {
  try {
    // TODO: Implement actual task creation logic
    // This is a placeholder implementation
    
    const body = await request.json();
    
    const newTask = {
      id: Date.now(), // In a real app, use a proper ID generator
      ...body,
      completed: false,
      createdAt: new Date().toISOString()
    };

    return NextResponse.json({ 
      success: true, 
      data: newTask,
      message: "Task created successfully"
    }, { status: 201 });
  } catch (error) {
    console.error('Error creating task:', error);
    return NextResponse.json({ 
      success: false, 
      error: 'Failed to create task',
      message: error.message 
    }, { status: 500 });
  }
}