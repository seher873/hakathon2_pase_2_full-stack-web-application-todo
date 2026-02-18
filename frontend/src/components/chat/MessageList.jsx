import React from 'react';
import ChatMessage from './ChatMessage';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages && messages.length > 0 ? (
        messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))
      ) : (
        <div className="empty-messages">
          <p>No messages yet. Start a conversation with the AI assistant!</p>
        </div>
      )}
    </div>
  );
};

export default MessageList;