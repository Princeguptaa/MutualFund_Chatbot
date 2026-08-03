import React, { useRef, useEffect } from 'react';

function ChatInput({ input, setInput, onSubmit, disabled }) {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !disabled) {
        onSubmit();
      }
    }
  };

  return (
    <div className="fixed bottom-0 w-full z-40" style={{ backgroundColor: 'var(--surface-container-lowest)', borderTop: '1px solid var(--outline-variant)', padding: 'var(--spacing-md) var(--spacing-margin)', boxShadow: '0 -4px 6px -1px rgba(30,58,138,0.05)', left: 0 }}>
      <div className="flex flex-col max-w-4xl mx-auto w-full">
        <label htmlFor="chat-input" className="sr-only label-md" style={{ color: 'var(--on-surface)', marginBottom: 'var(--spacing-xs)' }}>Ask a question</label>
        <div className="relative flex items-end w-full">
          <textarea
            id="chat-input"
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Ask about a fund..."
            rows={1}
            className="w-full body-md custom-shadow"
            style={{ 
              backgroundColor: 'var(--surface)', 
              border: '1px solid var(--outline-variant)', 
              borderRadius: 'var(--rounded-lg)', 
              padding: 'var(--spacing-md)', 
              paddingRight: '64px', 
              resize: 'none', 
              color: 'var(--on-surface)', 
              minHeight: '56px', 
              maxHeight: '120px',
              fontFamily: 'inherit',
              outline: 'none'
            }}
          />
          <button 
            onClick={onSubmit}
            disabled={!input.trim() || disabled}
            className="absolute"
            style={{ 
              right: 'var(--spacing-sm)', 
              bottom: 'var(--spacing-sm)', 
              padding: 'var(--spacing-sm)', 
              backgroundColor: 'var(--primary)', 
              color: 'var(--on-primary)', 
              borderRadius: 'var(--rounded-md)', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              opacity: (!input.trim() || disabled) ? 0.5 : 1,
              cursor: (!input.trim() || disabled) ? 'not-allowed' : 'pointer'
            }}>
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
          </button>
        </div>
        <div className="text-center" style={{ marginTop: 'var(--spacing-xs)' }}>
          <span className="label-sm" style={{ color: 'var(--on-surface-variant)' }}>Press Enter to send. Responses are generated based on available documentation.</span>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;
