import React from 'react';

function MessageBubble({ text }) {
  return (
    <div className="flex justify-end w-full" style={{ marginBottom: 'var(--spacing-md)' }}>
      <div className="custom-shadow body-md" style={{ 
        backgroundColor: 'var(--primary)', 
        color: 'var(--on-primary)', 
        padding: 'var(--spacing-md) var(--spacing-lg)', 
        borderRadius: 'var(--rounded-lg)', 
        borderBottomRightRadius: '0', 
        maxWidth: '85%' 
      }}>
        {text}
      </div>
    </div>
  );
}

export default MessageBubble;
