import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <section className="flex justify-center items-center mt-24 px-4 relative z-10 w-full animate-fadeIn">
      <div className="w-full max-w-3xl glass-panel p-10 text-center">
        {/* Gradient Title */}
        <h1 className="text-5xl md:text-6xl font-extrabold mb-6 text-gradient tracking-tight">
          Fake News Detector
        </h1>

        <p className="text-gray-300 text-lg mb-10 leading-relaxed font-light">
          Harness the power of <span className="text-primary font-semibold">AI</span> and
          <span className="text-secondary font-semibold"> Web Verification</span> to instantly evaluate
          the authenticity of news articles and online sources.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-6 mt-6">
          <Link to="/analyze" className="btn-primary text-lg flex items-center justify-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            Analyze Text or URL
          </Link>
          <Link to="/about" className="btn-secondary text-lg flex items-center justify-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            About Project
          </Link>
        </div>

        <div className="mt-12 bg-white/5 border border-white/10 p-6 rounded-xl shadow-inner backdrop-blur-sm">
          <p className="text-gray-400 text-sm md:text-base leading-relaxed">
            🚀 Built using <span className="font-semibold text-primary/90">Machine Learning</span> and
            <span className="font-semibold text-secondary/90"> Similarity Analysis</span> — this tool provides
            a <span className="text-white font-semibold">credibility score</span> to help you identify
            <span className="text-danger font-semibold"> fake</span> or
            <span className="text-accent font-semibold"> real</span> news instantly.
          </p>
        </div>
      </div>
    </section>

  );
}
