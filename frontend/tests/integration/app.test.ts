/**
 * Frontend integration tests for the Todo application.
 * 
 * Tests the main user flows and component interactions.
 */

// Mock localStorage for testing
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
    get length() {
      return Object.keys(store).length;
    },
    key: (index: number) => Object.keys(store)[index] || null,
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock fetch API
global.fetch = jest.fn();

describe('Todo App Integration Tests', () => {
  beforeEach(() => {
    // Reset mocks before each test
    (global.fetch as jest.MockedFunction<typeof fetch>).mockClear();
    localStorage.clear();
  });

  describe('Authentication Flow', () => {
    it('should allow user to sign up successfully', async () => {
      // Mock successful signup response
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'success',
          data: {
            token: 'mock-jwt-token',
            user: {
              id: 'test-user-id',
              email: 'test@example.com',
              created_at: '2026-01-03T12:00:00Z',
            },
          },
          timestamp: '2026-01-03T12:00:00Z',
        }),
      } as Response);

      // Import and test auth functions
      const { signup } = await import('../src/lib/auth');
      
      const result = await signup('test@example.com', 'password123', 'password123');
      
      expect(result).toBeDefined();
      expect(result.token).toBe('mock-jwt-token');
      expect(localStorage.getItem('hackathon_todo_auth_token')).toBe('mock-jwt-token');
    });

    it('should allow user to log in successfully', async () => {
      // Mock successful login response
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'success',
          data: {
            token: 'mock-jwt-token',
            user: {
              id: 'test-user-id',
              email: 'test@example.com',
              created_at: '2026-01-03T12:00:00Z',
            },
          },
          timestamp: '2026-01-03T12:00:00Z',
        }),
      } as Response);

      // Import and test auth functions
      const { login } = await import('../src/lib/auth');
      
      const result = await login('test@example.com', 'password123');
      
      expect(result).toBeDefined();
      expect(result.token).toBe('mock-jwt-token');
      expect(localStorage.getItem('hackathon_todo_auth_token')).toBe('mock-jwt-token');
    });
  });

  describe('Task Management Flow', () => {
    it('should allow authenticated user to create a task', async () => {
      // Mock successful task creation response
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'success',
          data: {
            id: 'test-task-id',
            title: 'Test Task',
            description: 'Test Description',
            completed: false,
            user_id: 'test-user-id',
            created_at: '2026-01-03T12:00:00Z',
            updated_at: '2026-01-03T12:00:00Z',
          },
          timestamp: '2026-01-03T12:00:00Z',
        }),
      } as Response);

      // Set up mock auth token
      localStorage.setItem('hackathon_todo_auth_token', 'mock-jwt-token');

      // Import and test task creation
      const { createTask } = await import('../src/services/api');
      
      const result = await createTask('test-user-id', {
        title: 'Test Task',
        description: 'Test Description',
      });
      
      expect(result).toBeDefined();
      expect(result.data?.id).toBe('test-task-id');
      expect(result.data?.title).toBe('Test Task');
    });

    it('should allow authenticated user to update a task', async () => {
      // Mock successful task update response
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'success',
          data: {
            id: 'test-task-id',
            title: 'Updated Task',
            description: 'Updated Description',
            completed: true,
            user_id: 'test-user-id',
            created_at: '2026-01-03T12:00:00Z',
            updated_at: '2026-01-03T12:00:01Z',
          },
          timestamp: '2026-01-03T12:00:01Z',
        }),
      } as Response);

      // Set up mock auth token
      localStorage.setItem('hackathon_todo_auth_token', 'mock-jwt-token');

      // Import and test task update
      const { updateTask } = await import('../src/services/api');
      
      const result = await updateTask('test-user-id', 'test-task-id', {
        title: 'Updated Task',
        description: 'Updated Description',
        completed: true,
      });
      
      expect(result).toBeDefined();
      expect(result.data?.id).toBe('test-task-id');
      expect(result.data?.title).toBe('Updated Task');
      expect(result.data?.completed).toBe(true);
    });

    it('should allow authenticated user to delete a task', async () => {
      // Mock successful task deletion response
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValueOnce({
        ok: true,
        status: 204,
      } as Response);

      // Set up mock auth token
      localStorage.setItem('hackathon_todo_auth_token', 'mock-jwt-token');

      // Import and test task deletion
      const { deleteTask } = await import('../src/services/api');
      
      await expect(deleteTask('test-user-id', 'test-task-id')).resolves.not.toThrow();
    });
  });

  describe('Storage Utilities', () => {
    it('should properly store and retrieve auth data', async () => {
      const { saveSession, restoreSession, clearSession } = await import('../src/utils/storage');
      
      // Save session
      saveSession('test-token', {
        id: 'test-user-id',
        email: 'test@example.com',
      });
      
      // Restore session
      const session = restoreSession();
      
      expect(session).toEqual({
        token: 'test-token',
        user: {
          id: 'test-user-id',
          email: 'test@example.com',
        },
      });
      
      // Clear session
      clearSession();
      
      // Verify cleared
      expect(restoreSession()).toBeNull();
    });
  });
});