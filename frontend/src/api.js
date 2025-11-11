const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

export async function predictText(newsText) {
  const res = await fetch(`${API_BASE}/api/predict_text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ news: newsText }),
  });
  if (!res.ok) {
    let message = 'Request failed';
    try {
      const err = await res.json();
      message = err?.error || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}

export async function predictUrl(url) {
  const res = await fetch(`${API_BASE}/api/predict_url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    let message = 'Request failed';
    try {
      const err = await res.json();
      message = err?.error || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}
