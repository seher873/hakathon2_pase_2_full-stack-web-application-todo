import { NextResponse } from 'next/server';

// GET /api/task/:id - Retrieve a specific task
export async function GET(request, { params }) {
  try {
    const taskId = params.id;
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks/${taskId}`, {
      headers: {
        'Content-Type': 'application/json',
        // Add authorization header if needed
        ...getAuthHeaders()
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json({
          success: false,
          error: 'Task not found',
          message: `Task with ID ${taskId} does not exist`
        }, { status: 404 });
      }
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();

    // Transform backend response to frontend format
    const task = {
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
      data: task,
      message: "Task retrieved successfully"
    });
  } catch (error) {
    console.error('Error retrieving task:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to retrieve task',
      message: error.message
    }, { status: 500 });
  }
}

// PUT /api/task/:id - Update a specific task
export async function PUT(request, { params }) {
  try {
    const taskId = params.id;
    const body = await request.json();

    // Transform frontend format to backend format
    const backendTask = {
      title: body.title,
      description: body.description,
      due_date: body.due_date || body.dueDate,
      status: body.completed ? 'completed' : 'pending'
    };

    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks/${taskId}`, {
      method: 'PUT',
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
    const updatedTask = {
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
      data: updatedTask,
      message: "Task updated successfully"
    });
  } catch (error) {
    console.error('Error updating task:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to update task',
      message: error.message
    }, { status: 500 });
  }
}

// DELETE /api/task/:id - Delete a specific task
export async function DELETE(request, { params }) {
  try {
    const taskId = params.id;
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks/${taskId}`, {
      method: 'DELETE',
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

    return NextResponse.json({
      success: true,
      message: result.message || `Task with ID ${taskId} deleted successfully`
    });
  } catch (error) {
    console.error('Error deleting task:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to delete task',
      message: error.message
    }, { status: 500 });
  }
}

// Helper function to get auth headers
function getAuthHeaders() {
  // In a real app, you'd get this from cookies or headers
  const token = process.env.API_TOKEN; // In production, get from request headers/cookies
  if (token) {
    return {
      'Authorization': `Bearer ${token}`
    };
  }
  return {};
}