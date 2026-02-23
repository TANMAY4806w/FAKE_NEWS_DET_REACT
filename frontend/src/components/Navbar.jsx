import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();

  // Helper for active link styling
  const isActive = (path) =>
    location.pathname === path
      ? 'text-white font-semibold underline underline-offset-4'
      : 'text-blue-100 hover:text-white transition-colors duration-200';

  return (
    <header className="glass-navbar">
      <div className="max-w-6xl mx-auto flex items-center justify-between py-3 px-6">
        {/* Logo */}
        <Link to="/" className="text-white text-2xl font-bold flex items-center gap-1">
          FakeNews<span role="img" aria-label="search">🔍</span>
        </Link>

        {/* Nav Links */}
        <nav className="flex gap-6">
          <Link to="/" className={isActive('/')}>Home</Link>
          <Link to="/analyze" className={isActive('/analyze')}>Analyze</Link>
          <Link to="/about" className={isActive('/about')}>About</Link>
        </nav>
      </div>
    </header>
  );
}
