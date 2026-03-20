import { NextResponse } from 'next/server';

// PATCH /api/task/:id/complete - Update task completion status
export async function PATCH(request, { params }) {
  try {
    const taskId = params.id;
    const body = await request.json();
    const { completed } = body;

    // Transform frontend format to backend format
    const backendTask = {
      status: completed ? 'completed' : 'pending'
    };

    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/api/tasks/${taskId}`, {
      method: 'PATCH',
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
    console.error('Error updating task completion status:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to update task completion status',
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