/**
 * Authentication API functions for signup and login.
 */

import { BACKEND_URL } from '@/utils/config';

/**
 * Interface for signup request body.
 */
interface SignupRequest {
  email: string;
  password: string;
}

/**
 * Interface for login request body.
 */
interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Interface for user data.
 */
interface User {
  id: string;
  email: string;
  created_at?: string;
  updated_at?: string;
}

/**
 * Interface for authentication response.
 */
interface AuthResponse {
  token: string;
  user: User;
}

/**
 * Signup a new user.
 *
 * @param email - User email
 * @param password - User password
 * @returns Promise resolving to auth response
 */
export async function signup(
  email: string,
  password: string
): Promise<AuthResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || errorData.message || 'Signup failed');
    }

    const responseData = await response.json();
    // Extract the actual token and user data from the response structure
    const { token, user } = responseData.data;
    return { token, user };
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
}

/**
 * Login user.
 *
 * @param email - User email
 * @param password - User password
 * @returns Promise resolving to auth response
 */
export async function login(
  email: string,
  password: string
): Promise<AuthResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || errorData.message || 'Login failed');
    }

    const responseData = await response.json();
    // Extract the actual token and user data from the response structure
    const { token, user } = responseData.data;
    return { token, user };
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}