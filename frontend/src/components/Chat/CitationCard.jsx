import React from 'react';

function CitationCard({ text, citationUrl, citationText, lastUpdated }) {
  return (
    <div className="flex justify-start w-full" style={{ marginBottom: 'var(--spacing-md)' }}>
      <div className="flex flex-col max-w-[90%]" style={{ gap: 'var(--spacing-sm)' }}>
        {/* Avatar / Name */}
        <div className="flex items-center" style={{ gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-xs)' }}>
          <div style={{ width: '32px', height: '32px', borderRadius: 'var(--rounded-full)', backgroundColor: 'var(--surface-container-high)', border: '1px solid var(--outline-variant)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span className="material-symbols-outlined" style={{ color: 'var(--on-surface-variant)', fontSize: '18px' }}>smart_toy</span>
          </div>
          <span className="label-sm uppercase tracking-wider" style={{ color: 'var(--on-surface-variant)' }}>Assistant</span>
        </div>
        
        {/* Message Body */}
        <div className="custom-shadow body-md relative" style={{ 
          backgroundColor: 'var(--surface-container-lowest)', 
          border: '1px solid var(--outline-variant)', 
          color: 'var(--on-surface)', 
          padding: 'var(--spacing-md) var(--spacing-lg)', 
          borderRadius: 'var(--rounded-lg)', 
          borderBottomLeftRadius: '0',
          overflow: 'hidden'
        }}>
          {/* Left Accent */}
          <div className="absolute top-0 bottom-0 left-0" style={{ width: '4px', backgroundColor: 'var(--secondary)' }}></div>
          
          <p style={{ marginBottom: 'var(--spacing-md)' }}>{text}</p>
          
          {/* Citation Link */}
          {citationUrl && (
            <a href={citationUrl} target="_blank" rel="noreferrer" className="inline-flex items-center label-sm" style={{ 
              gap: 'var(--spacing-xs)', 
              padding: 'var(--spacing-sm) var(--spacing-md)', 
              backgroundColor: 'var(--surface-container)', 
              border: '1px solid var(--outline-variant)', 
              borderRadius: 'var(--rounded-md)', 
              color: 'var(--on-surface)',
              textDecoration: 'none'
            }}>
              <span className="material-symbols-outlined" style={{ color: 'var(--secondary)', fontSize: '16px' }}>link</span>
              <span className="truncate">{citationText || `Source: ${citationUrl}`}</span>
              <span className="material-symbols-outlined" style={{ color: 'var(--on-surface-variant)', fontSize: '14px', marginLeft: 'auto' }}>open_in_new</span>
            </a>
          )}
          
          {/* Footer Info */}
          <div className="flex justify-between items-center" style={{ marginTop: 'var(--spacing-md)', paddingTop: 'var(--spacing-sm)', borderTop: '1px solid var(--surface-variant)' }}>
            <span className="label-sm italic" style={{ color: 'var(--on-surface-variant)' }}>
              Last updated from sources: {lastUpdated || 'Unknown'}
            </span>
            <div className="flex" style={{ gap: 'var(--spacing-sm)' }}>
              <button style={{ padding: 'var(--spacing-xs)', color: 'var(--on-surface-variant)', borderRadius: 'var(--rounded-full)', display: 'flex' }} title="Helpful">
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>thumb_up</span>
              </button>
              <button style={{ padding: 'var(--spacing-xs)', color: 'var(--on-surface-variant)', borderRadius: 'var(--rounded-full)', display: 'flex' }} title="Not helpful">
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>thumb_down</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CitationCard;
