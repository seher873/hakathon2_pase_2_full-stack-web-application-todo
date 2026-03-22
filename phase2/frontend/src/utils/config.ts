/**
 * Configuration constants for the application.
 */

// Backend API URL - Uses NEXT_PUBLIC_API_BASE_URL from environment
// For production: Hugging Face Space backend
// For development: localhost
export const BACKEND_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://sehrkhan873-hakathon-2.hf.space';