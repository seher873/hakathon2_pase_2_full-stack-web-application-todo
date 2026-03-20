import { NextResponse } from 'next/server';

// GET /api/task - Retrieve all tasks
export async function GET(request) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks`, {
      headers: {
        'Content-Type': 'application/json',
        // Add authorization header if needed
        ...getAuthHeaders()
      }
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();

    // Transform backend response to frontend format
    const tasks = (result.data || result).map(task => ({
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.status === 'completed',
      created_at: task.created_at || task.createdAt,
      updated_at: task.updated_at || task.updatedAt,
      user_id: task.user_id || 'default-user'
    }));

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
    const body = await request.json();

    // Transform frontend format to backend format
    const backendTask = {
      title: body.title,
      description: body.description,
      due_date: body.due_date || body.dueDate
    };

    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add authorization header if needed
        ...getAuthHeaders()
      },
      body: JSON.stringify(backendTask)
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();

    // Transform backend response to frontend format
    const newTask = {
      id: result.data?.id || result.id,
      title: result.data?.title || result.title,
      description: result.data?.description || result.description,
      completed: result.data?.status === 'completed' || result.status === 'completed',
      created_at: result.data?.created_at || result.created_at,
      updated_at: result.data?.updated_at || result.updated_at,
      user_id: result.data?.user_id || result.user_id || 'default-user'
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

// Helper function to get auth headers
function getAuthHeaders() {
  // In a real app, you'd get this from cookies or headers
  // Check for auth token from request headers
  // Since this is server-side code, we might need to implement a different approach
  // For now, we'll return empty headers, but in production,
  // you'd need to implement a proper auth token passthrough
  return {};
}