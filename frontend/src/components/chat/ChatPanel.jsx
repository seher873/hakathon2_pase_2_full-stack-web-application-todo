import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import { chatService } from '../../utils/chatService';
import './ChatPanel.css';

const ChatPanel = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Load any initial messages or conversation history
  useEffect(() => {
    // Add welcome message
    setMessages([
      {
        id: 'welcome',
        type: 'system',
        content: 'Hello! I\'m your AI assistant. You can ask me to create, update, or manage your tasks. Try saying "Add a task to buy groceries"',
        timestamp: new Date()
      }
    ]);
  }, []);

  // Scroll to bottom of messages when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send message to backend
      const response = await chatService.sendMessage(messageText, user?.id);

      // Add AI response to the chat
      const aiMessage = {
        id: `ai-${Date.now()}`,
        type: 'ai',
        content: response.response,
        timestamp: new Date(),
        data: response.data
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Handle different types of errors
      if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        // Add authentication error message to the chat
        const authErrorMessage = {
          id: `auth-error-${Date.now()}`,
          type: 'system',
          content: 'Authentication failed. Please log in again to continue using the chat.',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, authErrorMessage]);
        setError('Authentication error');
      } else {
        // Add general error message to the chat
        const errorMessage = {
          id: `error-${Date.now()}`,
          type: 'system',
          content: 'Sorry, I encountered an error processing your request. Please try again.',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h3>AI Task Assistant</h3>
      </div>

      <div className="chat-messages-container">
        <MessageList messages={messages} />
        {isLoading && <TypingIndicator />}
        {error && (
          <div className="error-indicator">
            Error: {error}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};

export default ChatPanel;