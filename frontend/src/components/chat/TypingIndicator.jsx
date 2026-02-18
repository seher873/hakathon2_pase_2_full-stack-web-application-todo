import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="typing-indicator">
      <div className="typing-dots">
        <div className="dot"></div>
        <div className="dot"></div>
        <div className="dot"></div>
      </div>
      <span>AI is thinking...</span>
    </div>
  );
};

export default TypingIndicator;