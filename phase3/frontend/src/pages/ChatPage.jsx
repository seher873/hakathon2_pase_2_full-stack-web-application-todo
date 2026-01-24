import React from 'react';
import ChatInterface from '../components/ChatInterface';
import '../styles/ChatPage.css'; // We'll create this next

const ChatPage = () => {
  return (
    <div className="chat-page">
      <header className="chat-header">
        <h1>AI Task Manager</h1>
        <p>Chat with your AI assistant to manage tasks</p>
      </header>
      
      <main className="chat-main">
        <ChatInterface />
      </main>
    </div>
  );
};

export default ChatPage;