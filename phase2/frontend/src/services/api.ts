/**
 * API client service for backend communication.
 *
 * Handles all HTTP requests to the FastAPI backend with:
 * - Automatic JWT token injection
 * - Request/response serialization
 * - Error handling
 * - Type safety with TypeScript
 */

import type {
  ApiError,
  ErrorResponse,
  SuccessResponse,
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
} from "@/types";
type UUID = string;
import { getAuthHeader } from "@/utils/storage";

// ============================================================================
// Constants
// ============================================================================

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

// ============================================================================
// Error Handling
// ============================================================================

/**
 * Transform API error response to ApiError type.
 *
 * @param response - Fetch Response object
 * @param data - Parsed response data
 * @returns ApiError object
 */
async function parseError(
  response: Response,
  data?: unknown
): Promise<ApiError> {
  if (data && typeof data === "object" && "code" in data && "message" in data) {
    const errorData = data as ErrorResponse;
    return {
      status: response.status,
      code: errorData.code,
      message: errorData.message,
      details: errorData.details,
    };
  }

  const statusMessages: Record<number, string> = {
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not found",
    409: "Conflict",
    422: "Validation error",
    500: "Server error",
  };

  return {
    status: response.status,
    code: `HTTP_${response.status}`,
    message: statusMessages[response.status] || "Unknown error",
    details: data as Record<string, unknown>,
  };
}

/**
 * Custom error class for API errors.
 */
export class ApiErrorException extends Error implements ApiError {
  status: number;
  code: string;
  details?: Record<string, unknown>;

  constructor(error: ApiError) {
    super(error.message);
    this.name = "ApiError";
    this.status = error.status;
    this.code = error.code;
    this.details = error.details;
  }
}

// ============================================================================
// Request/Response Helpers
// ============================================================================

/**
 * Prepare fetch options with JWT header injection.
 *
 * @param method - HTTP method
 * @param data - Request body data
 * @returns Fetch options object
 */
function prepareFetchOptions(
  method: string,
  data?: unknown
): RequestInit {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  // Inject JWT authorization header
  const authHeader = getAuthHeader();
  if (authHeader) {
    Object.assign(headers, authHeader);
  }

  const options: RequestInit = {
    method,
    headers,
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  return options;
}

/**
 * Build URL with query parameters.
 *
 * @param path - API path
 * @param params - Query parameters
 * @returns Full URL with query string
 */
function buildUrl(path: string, params?: Record<string, unknown>): string {
  // Add /api prefix to the path if it doesn't already start with /api
  const normalizedPath = path.startsWith('/api') ? path : `/api${path}`;
  const url = new URL(`${API_URL}${normalizedPath}`);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  return url.toString();
}

// ============================================================================
// Generic API Methods
// ============================================================================

/**
 * Make GET request to API.
 *
 * @param path - API endpoint path
 * @param params - Query parameters
 * @returns Parsed response data
 * @throws ApiErrorException if request fails
 */
export async function apiGet<T>(
  path: string,
  params?: Record<string, unknown>
): Promise<SuccessResponse<T>> {
  const url = buildUrl(path, params);

  try {
    const response = await fetch(url, prepareFetchOptions("GET"));

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new ApiErrorException(await parseError(response, data));
    }

    return response.json() as Promise<SuccessResponse<T>>;
  } catch (error) {
    if (error instanceof ApiErrorException) {
      throw error;
    }
    throw new ApiErrorException({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Network error",
      details: { error: String(error) },
    });
  }
}

/**
 * Make POST request to API.
 *
 * @param path - API endpoint path
 * @param data - Request body data
 * @returns Parsed response data
 * @throws ApiErrorException if request fails
 */
export async function apiPost<T>(
  path: string,
  data?: unknown
): Promise<SuccessResponse<T>> {
  const url = buildUrl(path);

  try {
    const response = await fetch(url, prepareFetchOptions("POST", data));

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiErrorException(await parseError(response, errorData));
    }

    return response.json() as Promise<SuccessResponse<T>>;
  } catch (error) {
    if (error instanceof ApiErrorException) {
      throw error;
    }
    throw new ApiErrorException({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Network error",
      details: { error: String(error) },
    });
  }
}

/**
 * Make PUT request to API.
 *
 * @param path - API endpoint path
 * @param data - Request body data
 * @returns Parsed response data
 * @throws ApiErrorException if request fails
 */
export async function apiPut<T>(
  path: string,
  data?: unknown
): Promise<SuccessResponse<T>> {
  const url = buildUrl(path);

  try {
    const response = await fetch(url, prepareFetchOptions("PUT", data));

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiErrorException(await parseError(response, errorData));
    }

    return response.json() as Promise<SuccessResponse<T>>;
  } catch (error) {
    if (error instanceof ApiErrorException) {
      throw error;
    }
    throw new ApiErrorException({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Network error",
      details: { error: String(error) },
    });
  }
}

/**
 * Make DELETE request to API.
 *
 * @param path - API endpoint path
 * @returns Parsed response data
 * @throws ApiErrorException if request fails
 */
export async function apiDelete(path: string): Promise<void> {
  const url = buildUrl(path);

  try {
    const response = await fetch(url, prepareFetchOptions("DELETE"));

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiErrorException(await parseError(response, errorData));
    }
  } catch (error) {
    if (error instanceof ApiErrorException) {
      throw error;
    }
    throw new ApiErrorException({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Network error",
      details: { error: String(error) },
    });
  }
}

/**
 * Make PATCH request to API.
 *
 * @param path - API endpoint path
 * @param data - Request body data
 * @returns Parsed response data
 * @throws ApiErrorException if request fails
 */
export async function apiPatch<T>(
  path: string,
  data?: unknown
): Promise<SuccessResponse<T>> {
  const url = buildUrl(path);

  try {
    const response = await fetch(url, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...(getAuthHeader() || {}),
      },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiErrorException(await parseError(response, errorData));
    }

    return response.json() as Promise<SuccessResponse<T>>;
  } catch (error) {
    if (error instanceof ApiErrorException) {
      throw error;
    }
    throw new ApiErrorException({
      status: 0,
      code: "NETWORK_ERROR",
      message: "Network error",
      details: { error: String(error) },
    });
  }
}

// ============================================================================
// Health Check
// ============================================================================

/**
 * Check API health status.
 *
 * @returns Health status response
 */
export async function checkHealth(): Promise<SuccessResponse<unknown>> {
  return apiGet("/health");
}

// ============================================================================
// Task Operations
// ============================================================================

/**
 * List all tasks for authenticated user.
 *
 * @returns List of tasks
 */
export async function listTasks(): Promise<SuccessResponse<Task[]>> {
  return apiGet<Task[]>(`/tasks`);
}

/**
 * Get single task details.
 *
 * @param taskId - Task ID
 * @returns Task details
 */
export async function getTask(
  taskId: UUID
): Promise<SuccessResponse<Task>> {
  return apiGet<Task>(`/tasks/${taskId}`);
}

/**
 * Create new task.
 *
 * @param data - Task creation data
 * @returns Created task
 */
export async function createTask(
  data: CreateTaskRequest
): Promise<SuccessResponse<Task>> {
  return apiPost<Task>(`/tasks`, data);
}

/**
 * Update existing task.
 *
 * @param taskId - Task ID
 * @param data - Task update data
 * @returns Updated task
 */
export async function updateTask(
  taskId: UUID,
  data: UpdateTaskRequest
): Promise<SuccessResponse<Task>> {
  return apiPut<Task>(`/tasks/${taskId}`, data);
}

/**
 * Delete task.
 *
 * @param taskId - Task ID
 */
export async function deleteTask(
  taskId: UUID
): Promise<void> {
  return apiDelete(`/tasks/${taskId}`);
}

/**
 * Mark task as complete or incomplete.
 *
 * @param taskId - Task ID
 * @param completed - Completion status
 * @returns Updated task
 */
export async function markTaskComplete(
  taskId: UUID,
  completed: boolean
): Promise<SuccessResponse<Task>> {
  return apiPatch<Task>(`/tasks/${taskId}/complete`, {
    completed,
  });
}
