import { getAccessToken } from './auth'; // Assuming there's an auth utility

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

class ChatService {
  constructor() {
    this.token = null;
  }

  // Initialize the service with authentication
  async initialize() {
    this.token = await getAccessToken();
  }

  // Get the current auth token
  getAuthHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Send a message to the chatbot API
  async sendMessage(message, userId) {
    try {
      // Ensure we have a valid token
      if (!this.token) {
        await this.initialize();
      }

      const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          message: message,
          user_id: userId || 'unknown'
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  // Stream a message to the chatbot API (for real-time responses)
  async streamMessage(message, userId) {
    try {
      // Ensure we have a valid token
      if (!this.token) {
        await this.initialize();
      }

      const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          message: message,
          user_id: userId || 'unknown'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process each complete line (SSE format)
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep the incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6); // Remove 'data: ' prefix
            if (dataStr.trim()) {
              try {
                const data = JSON.parse(dataStr);
                yield data;
              } catch (e) {
                console.error('Error parsing SSE data:', e);
              }
            }
          }
        }
      }

      // Process any remaining data in buffer
      if (buffer.trim()) {
        const dataStr = buffer.trim();
        if (dataStr.startsWith('data: ')) {
          const actualData = dataStr.slice(6);
          try {
            const data = JSON.parse(actualData);
            yield data;
          } catch (e) {
            console.error('Error parsing final SSE data:', e);
          }
        }
      }
    } catch (error) {
      console.error('Error streaming message:', error);
      throw error;
    }
  }

  // Get chat history (if implemented)
  async getChatHistory() {
    try {
      if (!this.token) {
        await this.initialize();
      }

      const response = await fetch(`${API_BASE_URL}/api/chat/history`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  }

  // Clear conversation context (if implemented)
  async clearConversation() {
    try {
      if (!this.token) {
        await this.initialize();
      }

      const response = await fetch(`${API_BASE_URL}/api/chat/clear`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error clearing conversation:', error);
      throw error;
    }
  }
}

// Create a singleton instance
const chatService = new ChatService();

// Export the instance and helper functions
export { chatService };

// Default export for backward compatibility
export default chatService;