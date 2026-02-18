import React from 'react';
import { format } from 'date-fns';
import { formatMessageContent } from '../../utils/messageFormatter';

const ChatMessage = ({ message }) => {
  const formatTimestamp = (timestamp) => {
    return format(new Date(timestamp), 'HH:mm');
  };

  const renderContent = (content, type, data) => {
    if (type === 'ai' && data) {
      // Format the content using the message formatter
      const formattedContent = formatMessageContent(content, type, data);

      return (
        <div className="message-content">
          {formattedContent.split('\n').map((line, index) => (
            <p key={index} className={line.startsWith('• ') || line.match(/^\d+\./) ? 'task-item' : ''}>
              {line}
            </p>
          ))}
        </div>
      );
    }

    return (
      <div className="message-content">
        {content.split('\n').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
    );
  };

  const getMessageClass = () => {
    switch (message.type) {
      case 'user':
        return 'user-message';
      case 'ai':
        return 'ai-message';
      case 'system':
        return 'system-message';
      default:
        return 'default-message';
    }
  };

  return (
    <div className={`chat-message ${getMessageClass()}`}>
      <div className="message-wrapper">
        {renderContent(message.content, message.type, message.data)}
        <div className="message-timestamp">
          {formatTimestamp(message.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;