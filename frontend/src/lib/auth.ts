/**
 * Better Auth client configuration and setup.
 *
 * Initializes Better Auth for user signup and login.
 * Better Auth handles OAuth and password management.
 * JWT tokens are stored in localStorage for API requests.
 */

// Note: Better Auth full integration depends on backend setup
// For Phase II MVP, we'll use a simplified auth flow

/**
 * Initialize authentication state on app startup.
 * Checks localStorage for existing JWT token and user data.
 *
 * @returns Authentication state with user and token if exists
 */
export async function initializeAuth(): Promise<{
  user?: { id: string; email: string };
  token?: string;
  isAuthenticated: boolean;
} | null> {
  try {
    // Check localStorage for existing session
    const token = localStorage.getItem("auth_token");
    const userStr = localStorage.getItem("auth_user");

    if (token && userStr) {
      const user = JSON.parse(userStr);
      return {
        user,
        token,
        isAuthenticated: true,
      };
    }

    return {
      isAuthenticated: false,
    };
  } catch (error) {
    console.error("Failed to initialize auth:", error);
    return {
      isAuthenticated: false,
    };
  }
}

/**
 * Handle user signup via backend signup endpoint.
 *
 * @param email - User email
 * @param password - User password
 * @param passwordConfirm - Password confirmation
 * @returns Auth response with token and user
 * @throws Error if signup fails
 */
export async function signup(
  email: string,
  password: string,
  passwordConfirm: string
): Promise<{
  token: string;
  user: { id: string; email: string };
}> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/auth/signup`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        password_confirm: passwordConfirm,
      }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.message || `Signup failed with status ${response.status}`
    );
  }

  const data = await response.json();
  return {
    token: data.data.token,
    user: {
      id: data.data.user.id,
      email: data.data.user.email,
    },
  };
}

/**
 * Handle user login via backend login endpoint.
 *
 * @param email - User email
 * @param password - User password
 * @returns Auth response with token and user
 * @throws Error if login fails
 */
export async function login(
  email: string,
  password: string
): Promise<{
  token: string;
  user: { id: string; email: string };
}> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.message || `Login failed with status ${response.status}`
    );
  }

  const data = await response.json();
  return {
    token: data.data.token,
    user: {
      id: data.data.user.id,
      email: data.data.user.email,
    },
  };
}

/**
 * Validate email format.
 *
 * @param email - Email to validate
 * @returns true if valid email
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate password strength.
 *
 * Requirements:
 * - Minimum 8 characters
 * - Maximum 128 characters
 *
 * @param password - Password to validate
 * @returns true if valid password
 */
export function validatePassword(password: string): boolean {
  return password.length >= 8 && password.length <= 128;
}

/**
 * Get error message for validation failure.
 *
 * @param field - Field name that failed validation
 * @param value - Value that failed
 * @returns Human-readable error message
 */
export function getValidationErrorMessage(
  field: string,
  value: unknown
): string {
  switch (field) {
    case "email":
      return "Please enter a valid email address";
    case "password":
      return "Password must be at least 8 characters";
    case "passwordConfirm":
      return "Passwords do not match";
    default:
      return "Validation failed";
  }
}
