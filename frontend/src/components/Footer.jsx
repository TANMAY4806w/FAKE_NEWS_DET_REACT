import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer bg-transparent border-t border-white/10 mt-12 py-6">
      <div className="text-gray-400 tracking-wide text-sm">
        © {currentYear} <span className="font-semibold">Fake News Detector</span>. Built with ❤️ using AI.
      </div>
    </footer>
  );
}
