import React from 'react';

function EmptyState({ onSuggestionClick }) {
  const suggestions = [
    "What is the exit load for SBI Small Cap Fund?",
    "What is the riskometer for SBI Flexicap?",
    "What is the lock-in for ELSS Tax Saver?"
  ];

  return (
    <div className="flex flex-col items-center text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
      <div className="custom-shadow" style={{ width: '64px', height: '64px', borderRadius: 'var(--rounded-full)', backgroundColor: 'var(--primary-container)', color: 'var(--on-primary-container)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 'var(--spacing-md)' }}>
        <span className="material-symbols-outlined" style={{ fontSize: '32px', fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
      </div>
      <p className="body-lg max-w-lg" style={{ color: 'var(--on-surface)', marginBottom: 'var(--spacing-lg)' }}>
        Hello! I can help you with factual information about mutual fund schemes.
      </p>
      <div className="flex flex-wrap justify-center max-w-2xl" style={{ gap: 'var(--spacing-sm)' }}>
        {suggestions.map((s, i) => (
          <button 
            key={i} 
            onClick={() => onSuggestionClick(s)}
            className="label-md"
            style={{ 
              padding: 'var(--spacing-sm) var(--spacing-md)', 
              borderRadius: 'var(--rounded-full)', 
              border: '1px solid var(--primary)', 
              color: 'var(--primary)', 
              backgroundColor: 'transparent',
              cursor: 'pointer',
              transition: 'background-color 0.2s, color 0.2s'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--primary)';
              e.currentTarget.style.color = 'var(--on-primary)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
              e.currentTarget.style.color = 'var(--primary)';
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

export default EmptyState;
