import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import ChatContainer from './components/Chat/ChatContainer';

function App() {
  return (
    <div className="flex flex-col flex-grow">
      <Header />
      <main className="flex-grow flex flex-col max-w-4xl w-full mx-auto" style={{ padding: 'var(--spacing-lg) var(--spacing-md) 100px', position: 'relative' }}>
        {/* Header Title Area */}
        <div className="flex flex-col items-center justify-center text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
          <h1 className="headline-lg" style={{ color: 'var(--primary)', marginBottom: 'var(--spacing-sm)' }}>
            GrowwAI Assistant
          </h1>
          <span className="inline-flex items-center label-md" style={{ gap: 'var(--spacing-xs)', padding: 'var(--spacing-sm) var(--spacing-md)', backgroundColor: 'var(--surface-container-low)', border: '1px solid var(--outline-variant)', borderRadius: 'var(--rounded-full)', color: 'var(--on-surface-variant)' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '16px' }}>info</span>
            Facts-only. No investment advice.
          </span>
        </div>
        
        {/* Chat Area */}
        <ChatContainer />
      </main>
      <Footer />
    </div>
  );
}

export default App;
