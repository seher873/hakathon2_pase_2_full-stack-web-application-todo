// src/utils/chatApi.js
import axios from 'axios';

const CHATBOT_API_BASE_URL = process.env.REACT_APP_BACKEND_BASE_URL + '/api/chatbot';

class ChatApi {
  constructor() {
    this.token = null;
  }

  setToken(token) {
    this.token = token;
  }

  async sendMessage(message, conversationId = null) {
    try {
      const response = await axios.post(
        `${CHATBOT_API_BASE_URL}/chat`,
        { 
          message,
          conversation_id: conversationId 
        },
        { 
          headers: { 
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('Error sending message to chatbot:', error);
      throw error;
    }
  }

  async getChatHealth() {
    try {
      const response = await axios.get(`${CHATBOT_API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      console.error('Error checking chatbot health:', error);
      throw error;
    }
  }
}

export default new ChatApi();