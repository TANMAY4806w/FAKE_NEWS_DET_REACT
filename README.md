# 🧠 Hybrid Fake News Detection System

A modern web application that combines machine learning and web verification to detect fake news. Built with React, Flask, and scikit-learn.
> A modern, production-ready web application that combines machine learning and web verification to detect fake news with 98%+ accuracy.

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## � System Overview

| Component | Technology | Features |
|-----------|-----------|----------|
| **Backend API** | Flask + scikit-learn | ML inference, web verification, DuckDuckGo integration |
| **Frontend** | React + Vite | Responsive UI, real-time feedback, smooth animations |
| **ML Models** | LR + BERT | 99%+ accuracy hybrid detection |
| **Deployment** | Gunicorn + Docker | Production-ready, CORS allowlist, env-config |

## 🔎 What's Inside
- **Backend**: Flask API with ML inference + web verification (DuckDuckGo + scraping) with SSRF protection
- **Frontend**: React (Vite) with smooth UX and responsive design
- **Production**: WSGI entrypoint (Gunicorn), CORS allowlist via environment variables
## ✨ Features

- **Hybrid AI Detection**: Combines Machine Learning predictions with real-time web verification.
- **Premium Interface**: A stunning, modern dark-themed UI featuring glassmorphism elements, neon glows, and fluid `framer-motion` micro-animations.
- **Extreme Performance**: Uses `functools.lru_cache` on the backend to cache external API responses, yielding instant results for repeated queries.
- **Intelligent Semantic Search**: Encodes the core claims of articles using **TF-IDF Vectorization** and **Cosine Similarity** to detect factual overlap with DuckDuckGo search snippets, optimized specifically for low-memory deployment environments.
- **Multiple Input Types**: Seamlessly analyze both raw text content and article URLs, protected by strong SSRF guards.
- **Deep NLP Analysis**: Provides sentiment analysis, suspicious keyword detection, and structural red flags.

## 📊 Dataset Information

The model is trained on the **Fake and Real News Dataset** from Kaggle.

- **Source**: [Fake and Real News Dataset (Kaggle)](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- **License**: CC-BY-NC-SA-4.0  
- **Total Records**: 44,898 (after cleaning: 39,103)  
- **Dataset Files**:
  - `Fake.csv` - Contains fake news articles
  - `True.csv` - Contains real news articles

### Data Classes:
- `1` → Fake News
- `0` → Real News

### Data Preprocessing:
✅ Steps performed during model training:
1. Combined both `Fake.csv` and `True.csv` into one DataFrame
2. Removed duplicates and null records (5,795 duplicates removed)
3. Cleaned text using:
   - Lowercasing
   - Removing punctuation, stopwords
   - Lemmatization using WordNetLemmatizer
4. Merged `title` and `text` into a single content column for better context
5. Split data: **Train** (31,282 samples - 80%), **Test** (7,821 samples - 20%)
6. Text vectorized using **TF-IDF** (10,000 max features)

### Model Performance:
- **Random Forest (Best Performer)**: 99.51% Accuracy
- **Logistic Regression**: 98.39% Accuracy
- **SVM (LinearSVC)**: 99.19% Accuracy
- **BERT (Transformer)**: 99.54% Accuracy

For detailed model training info, see `Model_traing/Fake_news_model_training.ipynb`

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
- React 18 (UI library)
- Vite (Next-generation Build tool)
- Tailwind CSS (Utility-first styling & Neon Glassmorphism design system)
- Framer Motion (Fluid layout animations and page transitions)
- Native Fetch for HTTP

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

## 🎨 UI & Design System

- **Premium Dark Aesthetics**: Deep space backgrounds with floating ambient gradient orbs.
- **Glassmorphism Components**: Frosted glass dashboard panels (`backdrop-blur-xl`) with translucent borders.
- **Dynamic Neon Results**: Glowing progress bars and verdict text (Neon Green for Real, Neon Red for Fake).
- **Animated Page Transitions**: Seamless morphing and fading between Home, Analyze, and About pages.
- **Typography**: Powered by the modern `Outfit` Google Font for a crisp tech-forward presentation.

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

---

## 📈 Performance Metrics

- **Average Response Time**: ~2-3 seconds
- **Model Inference Speed**: <100ms  
- **Supported Content**: Up to 50KB text
- **Concurrent Users**: 10+ simultaneous (deployment dependent)
- **Test Accuracy**: 98-99%

---

## 🐛 Troubleshooting Guide

### Backend Issues

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | Change port in `app.py` or kill process: `netstat -ano \| findstr :5000` |
| Model files not found | Ensure `.pkl` files exist in `backend/Model/` directory |
| CORS errors in frontend | Check `ALLOWED_ORIGINS` env variable matches frontend URL |
| Slow web scraping | Disable Jina fallback: `USE_JINA_FALLBACK=0` or increase timeout |
| Import errors | Run `pip install -r requirements.txt` in virtual environment |

### Frontend Issues

| Issue | Solution |
|-------|----------|
| API connection failed | Verify backend running: `http://localhost:5000` |
| Module not found | Run `npm install` in frontend directory |
| Port 5173 in use | Vite will auto-increment to next available port |
| Blank page on load | Check browser console for errors, verify API endpoints |

---

## 🔄 Future Enhancements

- [ ] User authentication & result history
- [ ] Advanced caching mechanisms
- [ ] Additional ML models (ensemble, XGBoost)
- [ ] Expand web verification sources
- [ ] Browser extension
- [ ] Rate limiting & request quotas
- [ ] Celery task queue for async processing
- [ ] PostgreSQL database integration
- [ ] Analytics dashboard
- [ ] Multi-language support

---

## 👨‍💻 Author

**Developed by**: Tanmay Patil

---

**Made with ❤️ and Machine Learning** 🚀
