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
    if (!label) return 'bg-gray-50 border-gray-200'
    if (label.toLowerCase().includes('real')) return 'bg-green-50 border-green-300'
    if (label.toLowerCase().includes('fake')) return 'bg-red-50 border-red-300'
    return 'bg-blue-50 border-blue-300'
  }

  async function runAnalysis() {
    try {
      setLoading(true)
      setError(null)
      setResult(null)
      const res = mode === 'text' ? await predictText(text) : await predictUrl(url)
      setResult(res)
    } catch (err) {
      setError(err.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="container mt-20 fade-in">
      <div className="card">
        <h1 className="text-3xl font-bold text-center mb-6 bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text">
          Analyze News Credibility
        </h1>

        {/* ===== Mode Toggle ===== */}
        <div className="flex justify-center gap-4 mb-6">
          <button
            onClick={() => setMode('text')}
            className={`px-4 py-2 rounded-md ${mode === 'text' ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Analyze Text
          </button>
          <button
            onClick={() => setMode('url')}
            className={`px-4 py-2 rounded-md ${mode === 'url' ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Analyze URL
          </button>
        </div>

        {/* ===== TEXT MODE ===== */}
        {mode === 'text' && (
          <div>
            <label className="block mb-2 font-medium text-primary">📝 Paste Article Text</label>
            <textarea
              value={text}
              onChange={e => setText(e.target.value)}
              rows={6}
              className="w-full border rounded p-2 mb-3"
              placeholder="Paste article text here..."
            />
          </div>
        )}

        {/* ===== URL MODE ===== */}
        {mode === 'url' && (
          <div>
            <label className="block mb-2 font-medium text-primary">🌐 Enter Article URL</label>
            <input
              value={url}
              onChange={e => setUrl(e.target.value)}
              className="w-full border rounded p-2 mb-3"
              placeholder="https://example.com/article"
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

        {/* ===== Results ===== */}
        {result && (
          <div className={`p-6 rounded-xl border ${getResultColor(result.final_label)} shadow-sm`}>
            <h3 className="text-2xl font-semibold mb-3">
              ⚖️ Result: {result.final_label || result.ml_label}
            </h3>
            <p><strong>ML Model Prediction:</strong> {result.ml_label} ({result.ml_confidence}% confidence)</p>
            <p><strong>Web Similarity:</strong> {result.web_similarity}%</p>
            <p><strong>Combined Score:</strong> {result.combined_score}%</p>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1 mb-4">
              <div
                className={`h-2 rounded-full ${result.final_label === 'Fake' ? 'bg-red-500' : 'bg-green-500'}`}
                style={{ width: `${Math.min(result.combined_score, 100)}%` }}
              />
            </div>

            {/* ===== Headline + Article Preview ===== */}
            {result.headline && <h4 className="text-lg font-semibold text-primary mb-2">📰 {result.headline}</h4>}
            {result.news_text && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-3">
                <p className="text-gray-700 mb-2">
                  {showFull ? result.news_text : result.news_text.slice(0, 350) + (result.news_text.length > 350 ? "..." : "")}
                </p>
                {result.news_text.length > 350 && (
                  <button onClick={() => setShowFull(!showFull)} className="text-blue-600 text-sm hover:underline">
                    {showFull ? "Hide Full Article ▲" : "Read More ▼"}
                  </button>
                )}
              </div>
            )}

            {/* ===== Referenced Sources ===== */}
            {result.sources && result.sources.length > 0 && (
              <div>
                <h4 className="text-primary font-medium mb-1">🔗 Referenced Sources:</h4>
                <ul className="list-disc ml-5 space-y-1">
                  {result.sources.map((s, i) => (
                    <li key={i}>
                      <a href={s.link} target="_blank" rel="noreferrer" className="text-secondary hover:text-primary">
                        {s.title || s.link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* ===== Optional Analysis Insights ===== */}
            {result.analysis && (
              <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-100 rounded-lg">
                <h4 className="text-primary font-semibold mb-2">🧠 Analysis Insights</h4>
                <p><strong>Sentiment:</strong> {result.analysis.sentiment}</p>
                {result.analysis.red_flags?.length > 0 && (
                  <ul className="list-disc ml-5 text-sm text-red-600">
                    {result.analysis.red_flags.map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  )
}
