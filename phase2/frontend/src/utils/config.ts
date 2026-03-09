/**
 * Configuration constants for the application.
 */

// Backend API URL - Uses NEXT_PUBLIC_API_BASE_URL from environment
export const BACKEND_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';