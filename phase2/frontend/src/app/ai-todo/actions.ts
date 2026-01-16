'use server';

import { revalidatePath } from 'next/server';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

/**
 * Process an AI command from the user
 * @param command The natural language command from the user
 * @returns The result of processing the command
 */
export async function processAICommand(command: string) {
  try {
    // Get the JWT token from cookies
    const token = cookies().get('token')?.value;

    if (!token) {
      return {
        success: false,
        message: 'User not authenticated. Please log in first.',
      };
    }

    // Call the backend AI skills API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        input: command,
      }),
    });

    if (response.status === 401) {
      // Token expired or invalid, redirect to login
      cookies().delete('token');
      redirect('/login');
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to process AI command');
    }

    const result = await response.json();

    // Revalidate the tasks page to show updated tasks
    revalidatePath('/dashboard');

    return {
      success: true,
      data: result.data,
      message: result.data?.message || 'Command processed successfully',
    };
  } catch (error) {
    console.error('Error processing AI command:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'An error occurred processing your request',
    };
  }
}

/**
 * Alternative function to create a task directly
 * @param title The title of the task
 * @param description The description of the task
 * @returns The result of creating the task
 */
export async function createTaskWithAI(title: string, description?: string) {
  try {
    // Get the JWT token from cookies
    const token = cookies().get('token')?.value;

    if (!token) {
      return {
        success: false,
        message: 'User not authenticated. Please log in first.',
      };
    }

    // Get user ID from the token (decode JWT to get user ID)
    // For now, we'll use a separate API call to get user profile
    const userIdResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (userIdResponse.status === 401) {
      // Token expired or invalid, redirect to login
      cookies().delete('token');
      redirect('/login');
    }

    if (!userIdResponse.ok) {
      throw new Error('Failed to get user profile');
    }

    const userData = await userIdResponse.json();
    const userId = userData.data?.id;

    if (!userId) {
      throw new Error('User ID not found');
    }

    // Create the task
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        title,
        description: description || '',
      }),
    });

    if (response.status === 401) {
      // Token expired or invalid, redirect to login
      cookies().delete('token');
      redirect('/login');
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create task');
    }

    const result = await response.json();

    // Revalidate the tasks page to show the new task
    revalidatePath('/dashboard');

    return {
      success: true,
      data: result.data,
      message: 'Task created successfully!',
    };
  } catch (error) {
    console.error('Error creating task with AI:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'An error occurred creating the task',
    };
  }
}