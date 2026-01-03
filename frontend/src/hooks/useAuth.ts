/**
 * Custom React hook for authentication state management.
 *
 * Provides:
 * - User authentication state
 * - Signup/login/logout functions
 * - Token management
 * - Session persistence
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import type { AuthState } from "@/types";
import {
  saveSession,
  clearSession,
  restoreSession,
  getToken,
  getUser,
} from "@/utils/storage";
import { signup as authSignup, login as authLogin } from "@/lib/auth";

/**
 * Initial auth state.
 */
const initialState: AuthState = {
  user: undefined,
  token: undefined,
  isAuthenticated: false,
  isLoading: true,
  error: undefined,
};

/**
 * Custom hook for authentication management.
 *
 * Usage:
 * ```tsx
 * const { user, isAuthenticated, signup, login, logout } = useAuth();
 *
 * if (isLoading) return <LoadingSpinner />;
 *
 * if (!isAuthenticated) {
 *   return <LoginPage onSignup={signup} />;
 * }
 *
 * return <Dashboard user={user} onLogout={logout} />;
 * ```
 *
 * @returns Authentication state and functions
 */
export function useAuth() {
  const [state, setState] = useState<AuthState>(initialState);

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const session = restoreSession();

        if (session) {
          setState({
            user: {
              id: session.user.id as any,
              email: session.user.email,
            },
            token: session.token,
            isAuthenticated: true,
            isLoading: false,
            error: undefined,
          });
        } else {
          setState({
            user: undefined,
            token: undefined,
            isAuthenticated: false,
            isLoading: false,
            error: undefined,
          });
        }
      } catch (error) {
        setState({
          user: undefined,
          token: undefined,
          isAuthenticated: false,
          isLoading: false,
          error: "Failed to restore session",
        });
      }
    };

    initializeAuth();
  }, []);

  /**
   * Handle user signup.
   *
   * @param email - User email
   * @param password - User password
   * @param passwordConfirm - Password confirmation
   * @throws Error if signup fails
   */
  const signup = useCallback(
    async (email: string, password: string, passwordConfirm: string) => {
      setState((prev) => ({
        ...prev,
        isLoading: true,
        error: undefined,
      }));

      try {
        const { token, user } = await authSignup(email, password, passwordConfirm);

        // Save session
        saveSession(token, {
          id: user.id,
          email: user.email,
        });

        setState({
          user: {
            id: user.id as any,
            email: user.email,
          },
          token,
          isAuthenticated: true,
          isLoading: false,
          error: undefined,
        });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Signup failed";
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    []
  );

  /**
   * Handle user login.
   *
   * @param email - User email
   * @param password - User password
   * @throws Error if login fails
   */
  const login = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({
        ...prev,
        isLoading: true,
        error: undefined,
      }));

      try {
        const { token, user } = await authLogin(email, password);

        // Save session
        saveSession(token, {
          id: user.id,
          email: user.email,
        });

        setState({
          user: {
            id: user.id as any,
            email: user.email,
          },
          token,
          isAuthenticated: true,
          isLoading: false,
          error: undefined,
        });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Login failed";
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    []
  );

  /**
   * Handle user logout.
   */
  const logout = useCallback(() => {
    clearSession();
    setState({
      user: undefined,
      token: undefined,
      isAuthenticated: false,
      isLoading: false,
      error: undefined,
    });
  }, []);

  /**
   * Clear error message.
   */
  const clearError = useCallback(() => {
    setState((prev) => ({
      ...prev,
      error: undefined,
    }));
  }, []);

  return {
    ...state,
    signup,
    login,
    logout,
    clearError,
  };
}
