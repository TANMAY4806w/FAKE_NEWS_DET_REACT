# 🧠 Hybrid Fake News Detection System  
### Developed by: **Tanmay Patil**  
### Platform: Google Colab + MERN-like Stack (React + Flask)  
### Tech Stack: Python, Pandas, Scikit-learn, TensorFlow, Transformers, PyTorch, Matplotlib, Flask, React, Vite, TailwindCSS  

---

## 📰 Overview
The **Hybrid Fake News Detection System** combines **Machine Learning (ML)**, **Natural Language Processing (NLP)**, and **Web Verification** to identify fake or misleading news.  
It uses a **Logistic Regression model** trained with **TF-IDF features** and cross-verifies claims via **semantic similarity (SBERT)** and **real-time web sources**.

---

# 🧩 1️⃣ Project Architecture
FAKE_NEWS_DET_REACT/
│
├── backend/ # Flask Backend (Hybrid API)
│ ├── app.py # Main Flask app (ML + Web Verification)
│ ├── utils.py # Text extraction, DuckDuckGo search, SBERT similarity
│ ├── requirements.txt # Python dependencies
│ └── Model/ # Trained model (.pkl files)
│
├── frontend/ # React Frontend (Vite + TailwindCSS)
│ ├── src/
│ ├── package.json
│ └── vite.config.js
│
└── Model_training/ # Model training & evaluation (Google Colab)
└── Fake_news_model_training.ipynb

markdown
Copy code

---

# 🧠 2️⃣ Dataset Details
- **Source:** [Fake and Real News Dataset (Kaggle)](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)  
- **License:** CC-BY-NC-SA-4.0  
- **Total Records:** 44,898 → **39,103 after cleaning**  
- **Labels:**
  - `1` → Fake News  
  - `0` → Real News  

| File | Description |
|------|--------------|
| `Fake.csv` | Contains fake news articles |
| `True.csv` | Contains real news articles |

---

# 🧹 3️⃣ Data Preprocessing
Performed using **Pandas**, **NLTK**, and **WordNetLemmatizer**.

✅ Steps:
1. Combined `Fake.csv` + `True.csv`
2. Removed duplicates and null values (≈ 5,800)
3. Text cleaning:
   - Lowercasing  
   - Removing punctuation, stopwords  
   - Lemmatization  
4. Merged `title` + `text` → one content column

✅ Final Clean Dataset → **39,103 records**

---

# ⚙️ 4️⃣ Feature Engineering
- **TF-IDF Vectorization** with 10,000 features  
- **Train-Test Split:**
  - Train: 31,282 samples (80%)  
  - Test: 7,821 samples (20%)

Result shapes:
Train: (31282, 10000)
Test: (7821, 10000)

yaml
Copy code

---

# 🤖 5️⃣ Model Training & Evaluation

### **Phase A — Classical ML (TF-IDF Models)**

| Model | Accuracy | Precision | Recall | F1-Score |
|--------|-----------|------------|----------|-----------|
| Logistic Regression | 0.9839 | 0.9901 | 0.9746 | 0.9823 |
| Naive Bayes | 0.9356 | 0.9292 | 0.9302 | 0.9297 |
| SVM (LinearSVC) | 0.9919 | 0.9955 | 0.9869 | 0.9912 |
| Random Forest | **0.9951** | **0.9966** | **0.9927** | **0.9947** |

✅ **Best Realistic Performer:** Logistic Regression  
✅ **Best Accuracy:** Random Forest  

---

### **Phase B — Deep Learning Models**

| Model | Embedding | Accuracy | Notes |
|--------|------------|-----------|--------|
| BiLSTM | Learned from scratch | 0.9987 | Overfit on training |
| BiLSTM + GloVe | Pre-trained embeddings | 0.9983 | Better generalization |

⚠️ Both overfitted short-text inputs → predicted most as *Fake*.

---

### **Phase C — Transformer (BERT)**
| Model | Accuracy | Notes |
|--------|-----------|--------|
| BERT (fine-tuned) | 0.9954 | Excellent context awareness but biased toward Fake on short claims |

⚠️ **Problem:** Deep models misclassified short factual headlines due to context limitation.

---

# 📊 6️⃣ Comparative Analysis (ML Phase)
| Model | Behavior | Comment |
|--------|-----------|----------|
| Naive Bayes | Moderate | Good for small data |
| SVM | Too strict | Overflags Fake |
| Random Forest | Overfits easily | High variance |
| Logistic Regression | **Balanced, Explainable** | ✅ Final Choice |

---

# 💡 7️⃣ Hybrid Model Design (ML + Web Verification)

### 🧠 **Architecture**
| Layer | Function | Description |
|--------|-----------|--------------|
| **ML Layer** | Logistic Regression (TF-IDF) | Linguistic probability |
| **Web Layer** | DuckDuckGo + Wikipedia + Jina | Real-time factual check |
| **Similarity Layer** | SBERT (Sentence Transformers) | Semantic similarity |
| **Decision Layer** | Combine ML + Web Scores | Weighted hybrid confidence |

### **Example Output**
> 📰 *Claim:* “NASA confirms water on Mars.”  
> 🔹 ML Prediction: 68% Real  
> 🔹 Web Verification: 3 verified sources found  
> ✅ **Final Verdict: REAL (High Confidence)**  

---

# 🧩 8️⃣ Backend (Flask API)

### ⚙️ Endpoints
| Route | Method | Description |
|--------|---------|--------------|
| `/api/predict_text` | POST | Analyze news text |
| `/api/predict_url` | POST | Extract + analyze from URL |
| `/api/analyze_text` | POST | Sentiment, keywords, and red flags |

### ⚙️ Example Output (Hybrid)
```json
{
  "final_label": "Fake",
  "ml_label": "Fake",
  "ml_confidence": 87.3,
  "web_similarity": 42.1,
  "combined_score": 68.2,
  "sources": [
    {"title": "BBC News Article", "link": "https://bbc.com/news/..."}
  ]
}
💻 9️⃣ Frontend (React + Tailwind)
Built using Vite + React + TailwindCSS

Responsive, modern design

Includes dynamic result cards, sentiment highlights, and animated transitions

Commands:

bash
Copy code
cd frontend
npm install
npm run dev
Frontend → http://localhost:5173
Backend → http://localhost:5000

☁️ 10️⃣ Deployment
🌩️ Frontend — Cloudflare Pages
Root: frontend

Build command: npm run build

Output: dist

Add env: VITE_API_BASE=https://your-backend.onrender.com

⚙️ Backend — Render
bash
Copy code
gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app
Set environment variables:

ini
Copy code
ALLOWED_ORIGINS=*
USE_JINA_FALLBACK=1
🔐 Security & Reliability
✅ SSRF-safe URL validation

✅ Configurable CORS (via ALLOWED_ORIGINS)

✅ Timeout-controlled scraping

✅ Fallback via Jina proxy

📈 11️⃣ Key Results Summary
Model	Accuracy	Real-world Reliability	Notes
Logistic Regression	98.39%	✅ Balanced & Explainable	Best for production
Random Forest	99.5%	⚠️ Overfit risk	Not stable
BiLSTM + GloVe	99.8%	⚠️ Overfitted	
BERT	99.5%	⚠️ Bias toward Fake	

✅ Final Deployed Model: Logistic Regression + TF-IDF + SBERT Hybrid

🔮 12️⃣ Future Improvements
 Add multilingual dataset support

 Integrate DeBERTa-MNLI for stance detection

 Introduce caching for faster web verification

 Add user login + history dashboard

 Deploy a browser extension version

📄 License
MIT License – Free for academic and commercial use.
Developed with ❤️ by Tanmay Patil.

🧠 This project demonstrates how combining Machine Learning, NLP, and real-time Web Verification can create explainable and reliable fake news detection systems.

yaml
Copy code

---

## 🧠 Summary of What’s New
- Merged your **Colab training report** and **deployment guide**
- Added **architecture diagrams**, **endpoint summaries**, and **example outputs**
- Structured sections for dataset, models, backend, frontend, and deployment
- Uses emojis + code formatting for readability  
- Professional enough for GitHub, portfolio, or academic submission  

---

Would you like me to create a **shorter “research-paper style abstract version”** of this README (just 1 page, suitable for your report PDF or submission)?
