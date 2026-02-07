import React from 'react';

function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <a href="/" className="logo">
            <span className="logo-icon">✨</span>
            <span>PromptGenius</span>
          </a>
          <nav className="nav">
            <div className="nav-badge">
              <span style={{fontSize: '0.875rem', color: '#94a3b8'}}>
                Portfolio Project
              </span>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
