import React, { useState } from 'react';
import EmptyState from './EmptyState';
import MessageBubble from './MessageBubble';
import CitationCard from './CitationCard';
import ChatInput from './ChatInput';

function ChatContainer() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    
    // Add user message
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    // Simulate API call and assistant response
    setTimeout(() => {
      const assistantMsg = {
        role: 'assistant',
        text: 'For investments in the SBI Large Cap Fund (formerly Bluechip), an exit load of 1% is payable if units are redeemed or switched out within 1 year from the date of allotment. No exit load is levied for redemptions after 1 year.',
        citationUrl: 'https://www.sbimf.com/sbimf-scheme-details/sbi-large-cap-fund-(formerly-known-as-sbi-bluechip-fund)-43',
        citationText: 'Source: SBI Large Cap Fund Details',
        lastUpdated: 'Oct 1, 2023'
      };
      setMessages(prev => [...prev, assistantMsg]);
      setIsLoading(false);
    }, 1500);
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
