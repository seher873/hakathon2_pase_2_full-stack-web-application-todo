/**
 * Task context and hook for managing task state.
 * 
 * Provides centralized task management functionality
 * including CRUD operations, filtering, and loading states.
 */

import { createContext, useContext, useReducer, useEffect } from 'react';
import { Task, TaskFilter, TaskListState, CreateTaskRequest, UpdateTaskRequest, TaskListResponse } from '../types';
import { apiGet, apiPost, apiPut, apiDelete, apiPatch } from '../services/api';
import { useAuth } from './useAuth';

// ============================================================================
// Action Types
// ============================================================================

const TASK_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  SET_TASKS: 'SET_TASKS',
  ADD_TASK: 'ADD_TASK',
  UPDATE_TASK: 'UPDATE_TASK',
  DELETE_TASK: 'DELETE_TASK',
  SET_FILTER: 'SET_FILTER',
  SET_SEARCH_QUERY: 'SET_SEARCH_QUERY',
  CLEAR_ERROR: 'CLEAR_ERROR',
} as const;

// ============================================================================
// Action Interfaces
// ============================================================================

interface SetLoadingAction {
  type: typeof TASK_ACTIONS.SET_LOADING;
  payload: boolean;
}

interface SetErrorAction {
  type: typeof TASK_ACTIONS.SET_ERROR;
  payload: string;
}

interface SetTasksAction {
  type: typeof TASK_ACTIONS.SET_TASKS;
  payload: { tasks: Task[]; total: number };
}

interface AddTaskAction {
  type: typeof TASK_ACTIONS.ADD_TASK;
  payload: Task;
}

interface UpdateTaskAction {
  type: typeof TASK_ACTIONS.UPDATE_TASK;
  payload: Task;
}

interface DeleteTaskAction {
  type: typeof TASK_ACTIONS.DELETE_TASK;
  payload: string; // task id
}

interface SetFilterAction {
  type: typeof TASK_ACTIONS.SET_FILTER;
  payload: TaskFilter;
}

interface SetSearchQueryAction {
  type: typeof TASK_ACTIONS.SET_SEARCH_QUERY;
  payload: string;
}

interface ClearErrorAction {
  type: typeof TASK_ACTIONS.CLEAR_ERROR;
}

type TaskAction =
  | SetLoadingAction
  | SetErrorAction
  | SetTasksAction
  | AddTaskAction
  | UpdateTaskAction
  | DeleteTaskAction
  | SetFilterAction
  | SetSearchQueryAction
  | ClearErrorAction;

// ============================================================================
// Initial State
// ============================================================================

const initialState: TaskListState = {
  tasks: [],
  isLoading: false,
  error: undefined,
  filter: 'all',
  searchQuery: '',
  total: 0,
};

// ============================================================================
// Reducer
// ============================================================================

const taskReducer = (state: TaskListState, action: TaskAction): TaskListState => {
  switch (action.type) {
    case TASK_ACTIONS.SET_LOADING:
      return { ...state, isLoading: action.payload };

    case TASK_ACTIONS.SET_ERROR:
      return { ...state, error: action.payload, isLoading: false };

    case TASK_ACTIONS.SET_TASKS:
      return {
        ...state,
        tasks: action.payload.tasks,
        total: action.payload.total,
        isLoading: false,
        error: undefined,
      };

    case TASK_ACTIONS.ADD_TASK:
      return {
        ...state,
        tasks: [action.payload, ...state.tasks],
        total: state.total + 1,
      };

    case TASK_ACTIONS.UPDATE_TASK:
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
      };

    case TASK_ACTIONS.DELETE_TASK:
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
        total: state.total - 1,
      };

    case TASK_ACTIONS.SET_FILTER:
      return { ...state, filter: action.payload };

    case TASK_ACTIONS.SET_SEARCH_QUERY:
      return { ...state, searchQuery: action.payload };

    case TASK_ACTIONS.CLEAR_ERROR:
      return { ...state, error: undefined };

    default:
      return state;
  }
};

// ============================================================================
// Context
// ============================================================================

interface TaskContextType extends TaskListState {
  createTask: (taskData: CreateTaskRequest) => Promise<void>;
  updateTask: (taskId: string, taskData: UpdateTaskRequest) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
  toggleTaskComplete: (taskId: string, completed: boolean) => Promise<void>;
  setFilter: (filter: TaskFilter) => void;
  setSearchQuery: (searchQuery: string) => void;
  refreshTasks: () => Promise<void>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

// ============================================================================
// Provider Component
// ============================================================================

interface TaskProviderProps {
  children: React.ReactNode;
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  const { user } = useAuth();

  // Fetch tasks when user logs in
  useEffect(() => {
    if (user) {
      refreshTasks();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  // Refresh tasks when filter or search query changes (only if user is authenticated)
  useEffect(() => {
    if (user) {
      refreshTasks();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.filter, state.searchQuery]);

  // ============================================================================
  // Helper Functions
  // ============================================================================

  const refreshTasks = async (): Promise<void> => {
    if (!user) return;

    try {
      dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: true });

      // Fetch tasks from API
      const response = await apiGet<TaskListResponse>(`/tasks`);

      if (response && response.data) {
        // Ensure response.data.data is an array before processing
        let tasksArray = Array.isArray(response.data.data) ? response.data.data : [];
        
        // Filter tasks client-side based on the state filter
        let filteredTasks = tasksArray;

        switch (state.filter) {
          case 'completed':
            filteredTasks = tasksArray.filter(task => task.completed);
            break;
          case 'pending':
            filteredTasks = tasksArray.filter(task => !task.completed);
            break;
          default:
            filteredTasks = tasksArray;
        }

        // Apply search query if present
        if (state.searchQuery.trim()) {
          const searchTerm = state.searchQuery.trim().toLowerCase();
          filteredTasks = filteredTasks.filter(task =>
            task.title?.toLowerCase().includes(searchTerm) ||
            (task.description && task.description.toLowerCase().includes(searchTerm))
          );
        }

        dispatch({
          type: TASK_ACTIONS.SET_TASKS,
          payload: {
            tasks: filteredTasks,
            total: response.data.total ?? tasksArray.length,
          },
        });
      } else {
        // If data is missing for some reason, at least stop loading
        dispatch({ 
          type: TASK_ACTIONS.SET_TASKS,
          payload: {
            tasks: [],
            total: 0,
          },
        });
      }
    } catch (error: any) {
      // Don't show error if it's a 403 (user not authenticated)
      if (error.message && !error.message.includes('403') && !error.message.includes('Forbidden')) {
        const errorMessage = error.message || 'Failed to fetch tasks';
        dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: errorMessage });
      } else {
        // Silently fail for auth errors - user will be redirected to login
        dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: false });
      }
    }
  };

  // ============================================================================
  // Public Methods
  // ============================================================================

  const createTask = async (taskData: CreateTaskRequest): Promise<void> => {
    if (!user) return;

    try {
      dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: true });

      const response = await apiPost<Task>(`/tasks`, taskData);

      if (response.status === 'success' && response.data) {
        dispatch({ type: TASK_ACTIONS.ADD_TASK, payload: response.data });
        dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to create task';
      dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: errorMessage });
    }
  };

  const updateTask = async (
    taskId: string,
    taskData: UpdateTaskRequest
  ): Promise<void> => {
    if (!user) return;

    try {
      dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: true });

      const response = await apiPut<Task>(
        `/tasks/${taskId}`,
        taskData
      );

      if (response.status === 'success' && response.data) {
        dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: response.data });
        dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to update task';
      dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: errorMessage });
    }
  };

  const deleteTask = async (taskId: string): Promise<void> => {
    if (!user) return;

    try {
      // Log the task ID for debugging
      console.log('Attempting to delete task with ID:', taskId);

      dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: true });

      // Ensure the task ID is properly formatted
      const cleanTaskId = String(taskId).split(':')[0]; // Take only the part before any colon
      console.log('Cleaned task ID:', cleanTaskId);

      await apiDelete(`/tasks/${cleanTaskId}`);

      dispatch({ type: TASK_ACTIONS.DELETE_TASK, payload: cleanTaskId });
      dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to delete task';
      dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: errorMessage });
    }
  };

  const toggleTaskComplete = async (
    taskId: string,
    completed: boolean
  ): Promise<void> => {
    if (!user) return;

    try {
      dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: true });

      const response = await apiPatch<Task>(
        `/tasks/${taskId}/complete`,
        { completed }
      );

      if (response.status === 'success' && response.data) {
        dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: response.data });
        dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to update task status';
      dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: errorMessage });
    }
  };

  const setFilter = (filter: TaskFilter): void => {
    dispatch({ type: TASK_ACTIONS.SET_FILTER, payload: filter });
  };

  // ============================================================================
  // Context Value
  // ============================================================================

  const contextValue: TaskContextType = {
    ...state,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskComplete,
    setFilter,
    setSearchQuery: (searchQuery: string): void => {
      dispatch({ type: TASK_ACTIONS.SET_SEARCH_QUERY, payload: searchQuery });
    },
    refreshTasks,
  };

  return (
    <TaskContext.Provider value={contextValue}>
      {children}
    </TaskContext.Provider>
  );
};

// ============================================================================
// Hook
// ============================================================================

export const useTasks = (): TaskContextType => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTasks must be used within a TaskProvider');
  }
  return context;
};