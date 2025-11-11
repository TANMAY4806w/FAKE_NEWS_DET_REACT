import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-primary to-secondary text-white text-center py-4 mt-12 shadow-inner">
      <div className="text-sm tracking-wide">
        © {currentYear} <span className="font-semibold">Fake News Detector</span>. Built with ❤️ using AI.
      </div>
    </footer>
  );
}
