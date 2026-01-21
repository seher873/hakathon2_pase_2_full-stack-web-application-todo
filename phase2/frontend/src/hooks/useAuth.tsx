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

import { createContext, useContext, useCallback, useEffect, useState, ReactNode } from "react";
import type { AuthState } from "@/types";
import {
  saveSession,
  clearSession,
  restoreSession,
  getToken,
  getUser,
} from "@/utils/storage";
import { signup as authSignup, login as authLogin } from "../lib/auth";

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

interface AuthContextType extends AuthState {
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider component to wrap the app.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const auth = useAuthProvider();

  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
}

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
function useAuthProvider() {
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
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
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
   * @throws Error if signup fails
   */
  const signup = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({
        ...prev,
        isLoading: true,
        error: undefined,
      }));

      try {
        const { token, user } = await authSignup(email, password);

        // Save session
        saveSession(token, {
          id: user.id,
          email: user.email,
        });

        setState({
          user: {
            id: user.id as any,
            email: user.email,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
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
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
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

/**
 * Custom hook to use the auth context.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
