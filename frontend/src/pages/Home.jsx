import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <section className="flex justify-center items-center mt-24 px-4">
  <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8 text-center">
    {/* Gradient Title */}
    <h1 className="text-4xl md:text-5xl font-extrabold mb-4 bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text">
      Fake News Detector
    </h1>

    <p className="text-gray-600 text-lg mb-8">
      Harness the power of <span className="text-primary font-medium">AI</span> and 
      <span className="text-secondary font-medium"> web verification</span> to instantly evaluate 
      the authenticity of news articles and online sources.
    </p>

    <div className="flex flex-col sm:flex-row justify-center gap-4 mt-6">
      <Link to="/analyze" className="btn-primary text-lg px-8 py-3 shadow-sm hover:shadow-md transition-all duration-300">
        🔍 Analyze Text or URL
      </Link>
      <Link to="/about" className="btn-secondary text-lg px-8 py-3">
        ℹ️ About the Project
      </Link>
    </div>

    <div className="mt-10 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-100 p-5 rounded-xl shadow-sm">
      <p className="text-gray-700">
        🚀 Built using <span className="font-semibold text-primary">Machine Learning</span> and 
        <span className="font-semibold text-secondary"> Web Similarity Analysis</span> — this tool provides 
        a <span className="text-accent font-semibold">credibility score</span> to help you identify 
        <span className="text-red-600 font-semibold"> fake</span> or 
        <span className="text-green-600 font-semibold"> real</span> news instantly.
      </p>
    </div>
  </div>
</section>

  );
}
