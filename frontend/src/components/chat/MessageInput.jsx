import React, { useState } from 'react';

const MessageInput = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (message.trim() && !disabled) {
        onSendMessage(message);
        setMessage('');
      }
    }
  };

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <textarea
          className="message-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your task request here... (e.g., 'Add a task to submit report tomorrow')"
          disabled={disabled}
          rows={1}
        />
        <button
          type="submit"
          className="send-button"
          disabled={disabled || !message.trim()}
        >
          Send
        </button>
      </div>
      <div className="input-hints">
        <small>Press Enter to send, Shift+Enter for new line</small>
      </div>
    </form>
  );
};

export default MessageInput;