# 🧠 Hybrid Fake News Detection System

A modern web application that combines machine learning and web verification to detect fake news. Built with React, Flask, and scikit-learn.

## 🔎 What’s inside (quick)
- Backend: Flask API serving ML inference + web verification (DuckDuckGo + scraping) with SSRF guard
- Frontend: React (Vite) UI with smooth UX
- Production-ready bits: WSGI entrypoint (Gunicorn), CORS allowlist via env, safer URL handling

## ✨ Features

- **Hybrid Detection**: Combines ML predictions with web verification
- **Multiple Input Types**: Analyze both text content and URLs
- **Deep Analysis**: Sentiment analysis, keyword detection, and red flags
- **Rich UI**: Modern, responsive interface with animations
- **Real-time Processing**: Quick analysis with progress feedback

## ✅ Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Model files in `backend/Model/` (`logistic_regression_model.pkl`, `tfidf_vectorizer.pkl`)

## 🏗️ Project Structure

```
├── backend/                 # Flask Backend
│   ├── app.py              # Main Flask application
│   ├── utils.py            # Helper functions
│   ├── requirements.txt    # Python dependencies
│   ├── wsgi.py             # WSGI entrypoint (for Gunicorn)
│   └── Model/              # ML model files
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── utils/        # Frontend utilities
│   │   └── assets/       # Static assets
│   ├── package.json
│   └── vite.config.js
│
└── Model_training/        # ML Model Training
    └── Fake_news_model_training.ipynb
```

## 🔧 Environment Variables

Backend (Flask):
```
ALLOWED_ORIGINS="*"                               # CORS allowlist. Use '*' for dev; set comma-separated origins in prod.
USE_JINA_FALLBACK=1                               # Use Jina text proxy fallback when direct scraping fails (1 to enable, 0 to disable)
```

Frontend (Vite):
```
VITE_API_BASE=http://localhost:5000               # Backend API base URL
```

## 🚀 Quick Start

Below are two ways to run the project: the recommended (using a virtual environment) and a quick method that does not use a Python virtual environment.

### Recommended: Using a Python virtual environment (best practice)

PowerShell / Bash:

```powershell
# Create and activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\activate

cd backend
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Frontend (separate shell):

```powershell
cd frontend
npm install
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

---

### Production Run (Linux) with Gunicorn

Backend (WSGI with multiple workers):

```bash
cd backend
pip install -r requirements.txt
export ALLOWED_ORIGINS="https://your-frontend.com,https://admin.your-frontend.com"
gunicorn -w 2 -k gthread -t 60 -b 0.0.0.0:5000 wsgi:application
```

Notes:
- Set `ALLOWED_ORIGINS` to a comma-separated list of trusted origins, or `*` for development.
- Put Gunicorn behind Nginx for TLS and buffering in production.
- On Windows, prefer Docker or run via `python app.py` behind a reverse proxy. (Gunicorn is Linux-focused.)

Dockerfile example (backend):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /app
ENV ALLOWED_ORIGINS="*"
EXPOSE 5000
CMD ["gunicorn","-w","2","-k","gthread","-t","60","-b","0.0.0.0:5000","wsgi:application"]
```

### Configure CORS allowlist

- Backend reads `ALLOWED_ORIGINS` from environment:
  - `*` (default): allow all origins (use only for development)
  - Comma-separated origins to restrict in production, e.g. `https://your-frontend.com,https://admin.your-frontend.com`

### Quick: Run without a virtual environment (no venv)

If you prefer not to create or activate a Python virtual environment, you can install the required Python packages globally or for your user. Note: global installs may require administrator privileges and may change system packages. Using the `--user` flag installs packages for the current user without admin rights.

PowerShell (install packages globally for current user):

```powershell
cd backend
# Install dependencies for the current user to avoid needing admin rights
pip install --user -r requirements.txt

# Run the Flask server
python app.py
```

If you installed packages globally (not using --user) you might need to run PowerShell as Administrator.

Frontend (same as above):

```powershell
cd frontend
npm install
npm run dev
```

If the frontend needs to talk to a backend running on a different host/port, set the Vite API base before starting the dev server (PowerShell):

```powershell
$env:VITE_API_BASE = 'http://localhost:5000'; npm run dev
```

Or create a `frontend/.env` file with:

```
VITE_API_BASE=http://localhost:5000
```

Notes:
- Running without a virtual environment may affect system Python packages. Prefer `--user` installs if you can't use a venv.
- CORS is enabled in the backend so the frontend dev server should be able to call the API at the default port.

## 🛠️ Tech Stack

### Backend
- Flask (Python web framework)
- scikit-learn (Machine Learning)
- newspaper3k (Article extraction)
- BeautifulSoup4 (Web scraping)
- TextBlob (Text analysis)
- DuckDuckGo Search (`duckduckgo_search`)
- Gunicorn (WSGI, Linux)

### Frontend
- React (UI library)
- Vite (Build tool)
- Native Fetch for HTTP
- Modern CSS with animations

## 📝 API Endpoints

### `/api/predict_text`
- **Method**: POST
- **Input**: `{ "news": "text content" }`
- **Returns**: Prediction results with confidence scores and analysis
- **Success Example**:
```json
{
  "ml_label": "Real",
  "ml_confidence": 87.12,
  "web_similarity": 62.4,
  "combined_score": 76.1,
  "final_label": "Real",
  "sources": [{ "title": "Example", "link": "https://example.com" }],
  "analysis": {
    "sentiment": "Neutral",
    "suspicious_keywords": [],
    "trust_keywords": ["report"],
    "red_flags": []
  }
}
```
- **Error Example**: `{"error":"No text provided"}` (HTTP 400)

### `/api/predict_url`
- **Method**: POST
- **Input**: `{ "url": "article url" }`
- **Returns**: Extracted content and prediction results
- **Error Example**: `{"error":"Unable to extract content from URL"}` (HTTP 422)

### `/api/analyze_text`
- **Method**: POST
- **Input**: `{ "news": "text content" }`
- **Returns**: Deep analysis results (sentiment, keywords, red flags)

## 🔐 Security & Safety Notes
- SSRF guard: URLs are validated and resolved to block private/loopback/link-local IPs before fetching.
- CORS: In production, set `ALLOWED_ORIGINS` to your trusted origins (do not leave `*`). 
- Timeouts: Network calls use timeouts; scraping may still be slow on some hosts—deploy behind a proxy with sensible read timeouts.
- Respect robots/legal constraints and consider whitelisting sources in regulated environments.

## 🎨 UI Components

- **NewsInput**: Main component for text/URL input
- **Results Display**: Shows prediction results with animations
- **Analysis Card**: Displays detailed content analysis
- **Loading States**: Animated loading indicators
- **Error Handling**: Clear error messages with recovery options

## 🔧 Environment Variables

See the consolidated Environment Variables section above.

## 📚 Dependencies

Backend:
```
flask
flask-cors
scikit-learn
newspaper3k
beautifulsoup4
requests
textblob
numpy
duckduckgo-search
sentence-transformers
gunicorn
```

Frontend:
```
react
react-dom
@vitejs/plugin-react
vite
```

## 🌟 Future Improvements

1. Add user authentication
2. Implement result caching
3. Add more ML models
4. Expand web verification sources
5. Add social sharing features
6. Implement browser extension
7. Add rate limiting and request quotas
8. Async/queued web verification for scale

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.