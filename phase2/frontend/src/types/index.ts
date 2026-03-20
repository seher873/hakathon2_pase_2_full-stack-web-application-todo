

/**
 * Shared TypeScript types and interfaces.
 *
 * Defines types for:
 * - API request/response formats
 * - Domain models (Task, User)
 * - Authentication state
 * - Component props
 */

import { UUID } from "crypto";

// ============================================================================
// Domain Models
// ============================================================================

/**
 * Task priority levels.
 */
export type TaskPriority = "low" | "medium" | "high";

/**
 * User entity (created by Better Auth).
 * Note: Better Auth manages user creation and authentication,
 * backend only stores user reference via user_id in JWT.
 */
export interface User {
  id: UUID;
  email: string;
  created_at: string;
  updated_at: string;
}

/**
 * Task entity - represents a todo item.
 * Each task belongs to a single user (via user_id).
 */
export interface Task {
  id: UUID;
  user_id: UUID;
  title: string;
  description?: string;
  completed: boolean;
  url?: string; // Optional URL field for running links
  priority: TaskPriority; // Task priority level
  tags?: string; // Comma-separated tags string
  due_date?: string; // Optional due date (ISO string)
  created_at: string;
  updated_at: string;
}

// ============================================================================
// API Request/Response Types
// ============================================================================

/**
 * Task creation request payload.
 */
export interface CreateTaskRequest {
  title: string;
  description?: string;
  url?: string; // Optional URL field for running links
  priority?: TaskPriority; // Optional priority (defaults to medium)
  tags?: string; // Comma-separated tags string
  due_date?: string; // Optional due date (ISO string)
}

/**
 * Task update request payload.
 */
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  url?: string; // Optional URL field for running links
  priority?: TaskPriority;
  tags?: string; // Comma-separated tags string
  due_date?: string;
}

/**
 * Mark task complete request payload.
 */
export interface MarkCompleteRequest {
  completed: boolean;
}

/**
 * Paginated task list response.
 */
export interface TaskListResponse {
  status: "success";
  data: Task[];
  total?: number;
  skip?: number;
  limit?: number;
  timestamp: string;
}

/**
 * Single task response.
 */
export interface TaskResponse {
  status: "success";
  data: Task;
  timestamp: string;
}

/**
 * Generic success response wrapper.
 */
export interface SuccessResponse<T> {
  status: "success";
  data: T;
  timestamp: string;
}

/**
 * Generic error response.
 */
export interface ErrorResponse {
  status: "error";
  code: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}

/**
 * Validation error details.
 */
export interface ValidationErrorDetails {
  [field: string]: string;
}

/**
 * Validation error response.
 */
export interface ValidationErrorResponse extends ErrorResponse {
  code: "VALIDATION_ERROR";
  details: ValidationErrorDetails;
}

// ============================================================================
// Authentication
// ============================================================================

/**
 * Authentication state in localStorage.
 */
export interface AuthState {
  user?: User;
  token?: string;
  isAuthenticated: boolean;
  isLoading: boolean;
  error?: string;
}

/**
 * User login credentials.
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * User signup credentials.
 */
export interface SignupCredentials {
  email: string;
  password: string;
  confirmPassword?: string;
}

/**
 * Authentication response from backend.
 */
export interface AuthResponse {
  status: "success";
  data: {
    token: string;
    user: User;
  };
  timestamp: string;
}

// ============================================================================
// UI State
// ============================================================================

/**
 * Task filter options.
 */
export type TaskFilter = "all" | "pending" | "completed";

/**
 * Task sort options.
 */
export type TaskSortBy = "created_at" | "title" | "priority" | "due_date";
export type TaskSortOrder = "asc" | "desc";

/**
 * Form state for task creation/editing.
 */
export interface TaskFormState {
  title: string;
  description: string;
  priority: TaskPriority;
  tags: string[];
  due_date?: string;
  isSubmitting: boolean;
  error?: string;
}

/**
 * Task list view state.
 */
export interface TaskListState {
  tasks: Task[];
  isLoading: boolean;
  error?: string;
  filter: TaskFilter;
  searchQuery: string;
  sortBy: TaskSortBy;
  sortOrder: TaskSortOrder;
  total: number;
}

/**
 * API error details for user display.
 */
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  status: number;
}

// ============================================================================
// Component Props
// ============================================================================

/**
 * Props for TaskForm component.
 */
export interface TaskFormProps {
  onSubmit: (data: CreateTaskRequest) => Promise<void>;
  isLoading?: boolean;
  error?: string;
  initialTitle?: string;
  initialDescription?: string;
}

/**
 * Props for TaskList component.
 */
export interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  error?: string;
  onDelete: (taskId: UUID) => Promise<void>;
  onToggleComplete: (taskId: UUID, completed: boolean) => Promise<void>;
  onEdit: (task: Task) => void;
  filter?: TaskFilter;
  searchQuery?: string;
  onFilterChange?: (filter: TaskFilter) => void;
  onSearchChange?: (searchQuery: string) => void;
}

/**
 * Props for TaskItem component.
 */
export interface TaskItemProps {
  task: Task;
  onDelete: () => Promise<void>;
  onToggleComplete: (completed: boolean) => Promise<void>;
  onEdit: () => void;
  isLoading?: boolean;
}

/**
 * Props for Header component.
 */
export interface HeaderProps {
  userEmail?: string;
  onLogout: () => void;
  isLoading?: boolean;
}

/**
 * Props for protected route component.
 */
export interface ProtectedRouteProps {
  children: React.ReactNode;
}

// ============================================================================
// API Client Configuration
// ============================================================================

/**
 * HTTP method types.
 */
export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

/**
 * API request configuration.
 */
export interface ApiRequestConfig {
  method: HttpMethod;
  url: string;
  data?: unknown;
  headers?: Record<string, string>;
  params?: Record<string, unknown>;
}

/**
 * API response wrapper.
 */
export interface ApiResponse<T> {
  status: "success" | "error";
  data?: T;
  code?: string;
  message?: string;
  details?: unknown;
  timestamp: string;
}
