import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Get JWT token from wherever it's stored in your app (localStorage, context, etc.)
  const getToken = () => {
    return localStorage.getItem('access_token'); // Adjust based on your auth implementation
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { id: Date.now(), text: inputValue, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_BASE_URL}/api/chatbot/chat`,
        { message: inputValue },
        { 
          headers: { 
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
          }
        }
      );

      // Add bot response to chat
      const botMessage = {
        id: response.data.conversation_id,
        text: response.data.response,
        sender: 'bot',
        intent: response.data.intent,
        confidence: response.data.confidence,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now(),
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'system',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>AI Assistant</h2>
        <p>Ask me to manage your tasks!</p>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your AI assistant. You can ask me to:</p>
            <ul>
              <li>Create new tasks (e.g., "Create a task called 'Buy groceries'")</li>
              <li>List your tasks (e.g., "Show me my tasks")</li>
              <li>Delete tasks (e.g., "Delete my task 'Call mom'")</li>
              <li>Update tasks (e.g., "Mark 'Finish report' as complete")</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.sender}-message`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                {message.intent && (
                  <small className="intent-info">
                    Intent: {message.intent} (Confidence: {(message.confidence * 100).toFixed(1)}%)
                  </small>
                )}
              </div>
              <div className="message-timestamp">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;