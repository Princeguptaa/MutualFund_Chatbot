import React from 'react';

function Footer() {
  return (
    <footer className="glass-panel" style={{ backgroundColor: 'var(--surface-container-lowest)', borderTop: '1px solid var(--outline-variant)', marginTop: 'auto', paddingBottom: '100px' }}>
      <div className="flex justify-between items-center w-full max-w-7xl mx-auto flex-wrap" style={{ padding: 'var(--spacing-lg) var(--spacing-margin)', gap: 'var(--spacing-md)' }}>
        <div className="flex flex-col text-left" style={{ gap: 'var(--spacing-sm)' }}>
          <span className="headline-lg" style={{ color: 'var(--primary)', fontSize: '24px' }}>Fintech Advisor</span>
          <span className="body-md max-w-md" style={{ color: 'var(--secondary)' }}>Securities investments are subject to market risks. Read all scheme related documents carefully.</span>
        </div>
        <div className="flex justify-center flex-wrap" style={{ gap: 'var(--spacing-md)' }}>
          <a href="#" className="label-sm" style={{ color: 'var(--on-surface-variant)' }}>Privacy Policy</a>
          <a href="#" className="label-sm" style={{ color: 'var(--on-surface-variant)' }}>Terms of Service</a>
          <a href="#" className="label-sm" style={{ color: 'var(--on-surface-variant)' }}>FAQ</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
