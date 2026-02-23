import React, { useState } from 'react'
import { predictText, predictUrl } from '../api'

export default function Analyze() {
  const [text, setText] = useState('')
  const [url, setUrl] = useState('')
  const [mode, setMode] = useState('text')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [showFull, setShowFull] = useState(false)

  const getResultColor = (label) => {
    if (!label) return 'border-white/10 bg-white/5'
    if (label.toLowerCase().includes('real')) return 'glow-real bg-[#0B1A14]/80'
    if (label.toLowerCase().includes('fake')) return 'glow-fake bg-[#1A0B0B]/80'
    return 'border-primary/50 shadow-glowBlue bg-[#0B1220]/80'
  }

  async function runAnalysis() {
    try {
      setLoading(true)
      setError(null)
      setResult(null)
      const res = mode === 'text' ? await predictText(text) : await predictUrl(url)

      // Safety check: if backend fails or doesn't return the expected format
      if (!res || res.error) {
        throw new Error(res?.error || 'Analysis failed. The server returned an invalid response.')
      }

      setResult(res)
    } catch (err) {
      setError(err.message || 'Error connecting to the analysis server. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="container mt-20 fade-in">
      <div className="glass-panel p-8 md:p-12 relative z-10 w-full max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-extrabold text-center mb-10 text-gradient tracking-tight drop-shadow-sm">
          Analyze News Credibility
        </h1>

        {/* ===== Mode Toggle ===== */}
        <div className="flex justify-center gap-4 mb-8">
          <button
            onClick={() => setMode('text')}
            className={`px-6 py-2.5 rounded-xl font-medium transition-all duration-300 ${mode === 'text' ? 'bg-primary text-white shadow-glowBlue' : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'}`}
          >
            Analyze Text
          </button>
          <button
            onClick={() => setMode('url')}
            className={`px-6 py-2.5 rounded-xl font-medium transition-all duration-300 ${mode === 'url' ? 'bg-primary text-white shadow-glowBlue' : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'}`}
          >
            Analyze URL
          </button>
        </div>

        {/* ===== TEXT MODE ===== */}
        {mode === 'text' && (
          <div className="animate-fadeIn">
            <label className="block mb-3 font-semibold text-primary/90 text-lg">📝 Paste Article Text</label>
            <textarea
              value={text}
              onChange={e => setText(e.target.value)}
              rows={6}
              className="mb-4"
              placeholder="Paste the suspicious article text here..."
            />
          </div>
        )}

        {/* ===== URL MODE ===== */}
        {mode === 'url' && (
          <div className="animate-fadeIn">
            <label className="block mb-3 font-semibold text-primary/90 text-lg">🌐 Enter Article URL</label>
            <input
              value={url}
              onChange={e => setUrl(e.target.value)}
              className="mb-4"
              placeholder="https://example.com/breaking-news"
            />
          </div>
        )}

        <div className="flex gap-3 mb-6">
          <button
            onClick={runAnalysis}
            disabled={loading || (!text && !url)}
            className={`btn-primary ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >
            {loading ? 'Analyzing...' : 'Run Analysis'}
          </button>
          <button onClick={() => { setText(''); setUrl(''); setResult(null); }} className="btn-secondary">Clear</button>
        </div>

        {/* ===== Error ===== */}
        {error && <div className="text-red-600 font-medium">{error}</div>}

        {/* ===== Results Dashboard ===== */}
        {result && (
          <div className={`p-8 mt-4 rounded-2xl border backdrop-blur-md transition-all duration-500 animate-fadeIn ${getResultColor(result.final_label)}`}>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
              <h3 className="text-3xl font-bold text-white flex items-center gap-3">
                <span className="text-2xl">⚖️</span>
                Verdict: <span className={result.final_label === 'Fake' ? 'text-danger' : 'text-accent'}>{result.final_label || result.ml_label}</span>
              </h3>
              <div className="text-right mt-2 md:mt-0">
                <p className="text-gray-300"><span className="text-primary font-semibold">ML Confidence:</span> {result.ml_confidence}%</p>
                <p className="text-gray-300"><span className="text-secondary font-semibold">Web Match:</span> {result.web_similarity}%</p>
              </div>
            </div>

            {/* Neon Progress Bar */}
            <div className="w-full bg-[#0B0F19] rounded-full h-3 mb-6 border border-white/5 overflow-hidden">
              <div
                className={`h-3 rounded-full transition-all duration-1000 ease-out ${result.final_label === 'Fake' ? 'bg-danger shadow-[0_0_10px_rgba(239,68,68,0.8)]' : 'bg-accent shadow-[0_0_10px_rgba(16,185,129,0.8)]'}`}
                style={{ width: `${Math.min(result.combined_score, 100)}%` }}
              />
            </div>
            <p className="text-center font-bold text-xl mb-6 text-white tracking-wide">
              Final Authenticity Score: {result.combined_score}%
            </p>

            {/* ===== Headline + Article Preview ===== */}
            {result.headline && <h4 className="text-xl font-bold text-white mb-3 tracking-wide">📰 {result.headline}</h4>}
            {result.news_text && (
              <div className="bg-[#0B0F19]/50 border border-white/5 rounded-xl p-4 mb-6 shadow-inner">
                <p className="text-gray-300 leading-relaxed mb-2 font-light">
                  {showFull ? result.news_text : result.news_text.slice(0, 350) + (result.news_text.length > 350 ? "..." : "")}
                </p>
                {result.news_text.length > 350 && (
                  <button onClick={() => setShowFull(!showFull)} className="text-primary font-medium hover:text-blue-400 transition-colors">
                    {showFull ? "Collapse snippet ▲" : "Expand snippet ▼"}
                  </button>
                )}
              </div>
            )}

            <div className="grid md:grid-cols-2 gap-6">
              {/* ===== Referenced Sources ===== */}
              {result.sources && result.sources.length > 0 && (
                <div className="bg-[#0B0F19]/30 border border-white/5 p-5 rounded-xl">
                  <h4 className="text-secondary font-semibold mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                    Web Sources Mapped
                  </h4>
                  <ul className="space-y-2">
                    {result.sources.map((s, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="text-primary mt-0.5">•</span>
                        <a href={s.link} target="_blank" rel="noreferrer" className="text-gray-300 hover:text-white transition-colors truncate block">
                          {s.title || s.link}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* ===== Analysis Insights ===== */}
              {result.analysis && (
                <div className="bg-[#0B0F19]/30 border border-white/5 p-5 rounded-xl">
                  <h4 className="text-primary font-semibold mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" /></svg>
                    NLP Insights
                  </h4>
                  <p className="text-gray-300 text-sm mb-2"><strong className="text-white">Emotional Sentiment:</strong> {result.analysis.sentiment}</p>
                  {result.analysis.red_flags?.length > 0 && (
                    <ul className="space-y-1 mt-2">
                      {result.analysis.red_flags.map((r, i) => (
                        <li key={i} className="text-danger text-sm flex items-start gap-2">
                          <span className="mt-0.5">⚠️</span> <span>{r.replace(/^[🚨⚠️🧾❌]\s*/, '')}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
