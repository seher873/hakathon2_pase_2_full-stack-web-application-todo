/**
 * localStorage utilities for managing JWT tokens and user state.
 *
 * Provides type-safe access to browser localStorage with
 * automatic serialization/deserialization of JSON data.
 */

// ============================================================================
// Constants
// ============================================================================

const TOKEN_KEY = "auth_token";
const USER_KEY = "auth_user";
const STORAGE_PREFIX = "hackathon_todo_";

// ============================================================================
// Token Management
// ============================================================================

/**
 * Store JWT token in localStorage.
 *
 * @param token - JWT token string
 */
export function setToken(token: string): void {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}${TOKEN_KEY}`, token);
  } catch (error) {
    console.error("Failed to store token:", error);
  }
}

/**
 * Retrieve JWT token from localStorage.
 *
 * @returns JWT token string or null if not found
 */
export function getToken(): string | null {
  try {
    return localStorage.getItem(`${STORAGE_PREFIX}${TOKEN_KEY}`);
  } catch (error) {
    console.error("Failed to retrieve token:", error);
    return null;
  }
}

/**
 * Check if valid JWT token exists in localStorage.
 *
 * @returns true if token exists and is not empty
 */
export function hasToken(): boolean {
  const token = getToken();
  return Boolean(token && token.trim().length > 0);
}

/**
 * Clear JWT token from localStorage.
 */
export function clearToken(): void {
  try {
    localStorage.removeItem(`${STORAGE_PREFIX}${TOKEN_KEY}`);
  } catch (error) {
    console.error("Failed to clear token:", error);
  }
}

// ============================================================================
// Authorization Header
// ============================================================================

/**
 * Get Authorization header for API requests.
 *
 * @returns Authorization header object or null if no token
 */
export function getAuthHeader(): { Authorization: string } | null {
  const token = getToken();
  if (!token) {
    return null;
  }
  return {
    Authorization: `Bearer ${token}`,
  };
}

/**
 * Inject JWT token into request headers.
 *
 * @param headers - Existing headers object
 * @returns Headers with Authorization header injected
 */
export function injectAuthHeader(
  headers: Record<string, string> = {}
): Record<string, string> {
  const authHeader = getAuthHeader();
  if (authHeader) {
    return {
      ...headers,
      ...authHeader,
    };
  }
  return headers;
}

// ============================================================================
// User Data Management
// ============================================================================

/**
 * User data structure stored in localStorage.
 */
interface StoredUser {
  id: string;
  email: string;
}

/**
 * Store user data in localStorage.
 *
 * @param user - User object to store
 */
export function setUser(user: StoredUser): void {
  try {
    localStorage.setItem(
      `${STORAGE_PREFIX}${USER_KEY}`,
      JSON.stringify(user)
    );
  } catch (error) {
    console.error("Failed to store user:", error);
  }
}

/**
 * Retrieve user data from localStorage.
 *
 * @returns User object or null if not found
 */
export function getUser(): StoredUser | null {
  try {
    const userData = localStorage.getItem(`${STORAGE_PREFIX}${USER_KEY}`);
    if (!userData) {
      return null;
    }
    return JSON.parse(userData) as StoredUser;
  } catch (error) {
    console.error("Failed to retrieve user:", error);
    return null;
  }
}

/**
 * Clear user data from localStorage.
 */
export function clearUser(): void {
  try {
    localStorage.removeItem(`${STORAGE_PREFIX}${USER_KEY}`);
  } catch (error) {
    console.error("Failed to clear user:", error);
  }
}

// ============================================================================
// Session Management
// ============================================================================

/**
 * Save complete session (token + user) to localStorage.
 *
 * @param token - JWT token
 * @param user - User object
 */
export function saveSession(token: string, user: StoredUser): void {
  setToken(token);
  setUser(user);
}

/**
 * Load session from localStorage.
 *
 * @returns Object with token and user, or null if session not found
 */
export function loadSession(): { token: string; user: StoredUser } | null {
  const token = getToken();
  const user = getUser();

  if (!token || !user) {
    return null;
  }

  return { token, user };
}

/**
 * Clear entire session from localStorage.
 */
export function clearSession(): void {
  clearToken();
  clearUser();
}

/**
 * Check if valid session exists.
 *
 * @returns true if both token and user exist
 */
export function hasSession(): boolean {
  return hasToken() && Boolean(getUser());
}

// ============================================================================
// Session Persistence
// ============================================================================

/**
 * Initialize session on app startup.
 * Checks if session exists in localStorage.
 *
 * @returns Existing session or null if not found
 */
export function initializeSession(): { token: string; user: StoredUser } | null {
  try {
    return loadSession();
  } catch (error) {
    console.error("Failed to initialize session:", error);
    clearSession();
    return null;
  }
}

/**
 * Restore session on page reload/refresh.
 * Validates that stored token and user are still valid.
 *
 * @returns Session if valid, null otherwise
 */
export function restoreSession(): { token: string; user: StoredUser } | null {
  try {
    const session = loadSession();

    if (!session) {
      return null;
    }

    // Basic validation
    if (!session.token || !session.user || !session.user.id || !session.user.email) {
      clearSession();
      return null;
    }

    return session;
  } catch (error) {
    console.error("Failed to restore session:", error);
    clearSession();
    return null;
  }
}

// ============================================================================
// Debug Utilities (Development Only)
// ============================================================================

/**
 * Get all stored auth data (development only).
 *
 * @returns Object with all stored auth data
 */
export function getAllAuthData(): Record<string, unknown> {
  const result: Record<string, unknown> = {};

  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(STORAGE_PREFIX)) {
        const value = localStorage.getItem(key);
        result[key] = value;
      }
    }
  } catch (error) {
    console.error("Failed to get all auth data:", error);
  }

  return result;
}

/**
 * Clear all auth data (use with caution).
 */
export function clearAllAuthData(): void {
  try {
    const keysToRemove: string[] = [];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(STORAGE_PREFIX)) {
        keysToRemove.push(key);
      }
    }

    keysToRemove.forEach((key) => localStorage.removeItem(key));
  } catch (error) {
    console.error("Failed to clear all auth data:", error);
  }
}
