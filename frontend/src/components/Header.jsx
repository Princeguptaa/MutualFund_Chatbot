import React from 'react';

function Header() {
  return (
    <header className="sticky top-0 z-50 glass-panel" style={{ borderBottom: '1px solid var(--outline-variant)' }}>
      <div className="flex justify-between items-center w-full max-w-7xl mx-auto" style={{ padding: 'var(--spacing-md) var(--spacing-margin)' }}>
        <div className="flex items-center" style={{ gap: 'var(--spacing-sm)' }}>
          <span className="material-symbols-outlined" style={{ color: 'var(--primary)', fontVariationSettings: "'FILL' 1" }}>assured_workload</span>
          <span className="headline-md tracking-tight" style={{ color: 'var(--primary)' }}>GrowwAI</span>
        </div>
        <div className="flex items-center" style={{ gap: 'var(--spacing-md)' }}>
          <button style={{ color: 'var(--primary)', padding: 'var(--spacing-sm)', borderRadius: 'var(--rounded-full)', display: 'flex', alignItems: 'center', justifyContent: 'center' }} title="Info">
            <span className="material-symbols-outlined">info</span>
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
