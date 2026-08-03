import React, { useState } from 'react';
import EmptyState from './EmptyState';
import MessageBubble from './MessageBubble';
import CitationCard from './CitationCard';
import ChatInput from './ChatInput';

function ChatContainer() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user message
    const currentInput = input;
    const userMsg = { role: 'user', text: currentInput };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${apiUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: currentInput, stream: false })
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      
      const assistantMsg = {
        role: 'assistant',
        text: data.response || 'Sorry, no response was generated.',
        citationUrl: data.citation_url || '',
        citationText: data.citation_url ? 'View Source Document' : '',
        lastUpdated: data.last_updated && data.last_updated !== 'Unknown' ? data.last_updated : ''
      };
      
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      console.error("Failed to fetch response:", error);
      const errorMsg = {
        role: 'assistant',
        text: `An error occurred while fetching the response: ${error.message}`
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
    // Ideally we would trigger send right away, but setting input is fine for the demo
  };

  return (
    <>
      <div className="flex flex-col flex-grow" style={{ gap: 'var(--spacing-lg)', paddingBottom: 'var(--spacing-xl)' }}>
        {messages.length === 0 ? (
          <EmptyState onSuggestionClick={handleSuggestionClick} />
        ) : (
          <hr style={{ border: 'none', borderTop: '1px solid var(--outline-variant)', width: '100%', margin: '16px 0' }} />
        )}

        {messages.map((msg, index) => (
          msg.role === 'user' ? (
            <MessageBubble key={index} text={msg.text} />
          ) : (
            <CitationCard 
              key={index} 
              text={msg.text} 
              citationUrl={msg.citationUrl} 
              citationText={msg.citationText}
              lastUpdated={msg.lastUpdated}
            />
          )
        ))}

        {isLoading && (
          <div className="flex justify-start w-full" style={{ marginBottom: 'var(--spacing-md)' }}>
            <div className="flex flex-col w-full max-w-[90%]" style={{ gap: 'var(--spacing-sm)' }}>
              <div className="flex items-center" style={{ gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-xs)' }}>
                <div className="skeleton" style={{ width: '32px', height: '32px', borderRadius: 'var(--rounded-full)', border: '1px solid var(--outline-variant)' }}></div>
                <div className="skeleton" style={{ height: '16px', width: '96px', borderRadius: 'var(--rounded-sm)' }}></div>
              </div>
              <div className="custom-shadow" style={{ backgroundColor: 'var(--surface-container-lowest)', border: '1px solid var(--outline-variant)', padding: 'var(--spacing-md) var(--spacing-lg)', borderRadius: 'var(--rounded-lg)', borderBottomLeftRadius: '0' }}>
                <div className="skeleton" style={{ height: '16px', width: '75%', borderRadius: 'var(--rounded-sm)', marginBottom: 'var(--spacing-sm)' }}></div>
                <div className="skeleton" style={{ height: '16px', width: '100%', borderRadius: 'var(--rounded-sm)', marginBottom: 'var(--spacing-sm)' }}></div>
                <div className="skeleton" style={{ height: '16px', width: '83%', borderRadius: 'var(--rounded-sm)' }}></div>
                <div className="skeleton" style={{ marginTop: 'var(--spacing-md)', height: '48px', width: '256px', borderRadius: 'var(--rounded-md)' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <ChatInput input={input} setInput={setInput} onSubmit={handleSend} disabled={isLoading} />
    </>
  );
}

export default ChatContainer;
