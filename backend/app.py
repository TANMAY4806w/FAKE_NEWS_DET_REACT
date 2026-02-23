from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, joblib, warnings, numpy as np, re, os
from duckduckgo_search import DDGS
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from utils import fetch_web_articles, compute_similarity, combine_scores, extract_article_text

warnings.filterwarnings("ignore")

# -------------------------------------------------------
# ⚙️ Load ML Models
# -------------------------------------------------------
MODEL_PATH = "Model/logistic_regression_model.pkl"
TFIDF_PATH = "Model/tfidf_vectorizer.pkl"

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(TFIDF_PATH)
    print("✅ Model & TF-IDF Vectorizer Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading Model: {e}")
    raise e

# -------------------------------------------------------
# 🚀 Initialize Flask + CORS (env allowlist)
# -------------------------------------------------------
app = Flask(__name__)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins.strip() == "*":
    CORS(app)
else:
    origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
    CORS(app, resources={r"/api/*": {"origins": origins}})


# -------------------------------------------------------
# 🧼 Utility: Clean Input
# -------------------------------------------------------
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r"[^A-Za-z0-9\s.,!?']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -------------------------------------------------------
# 🧠 Pure Analysis Utility (no Flask request dependency)
# -------------------------------------------------------
def analyze_content(news_text: str):
    news_text = (news_text or "").strip()
    if not news_text:
        return {
            "suspicious_keywords": [],
            "trust_keywords": [],
            "sentiment": "Neutral",
            "red_flags": ["❌ No text provided."],
        }

    suspicious_words = ["shocking", "breaking", "viral", "amazing", "exclusive", "rumor"]
    trust_words = ["report", "official", "source", "confirmed", "data", "government", "research"]

    found_suspicious = [w for w in suspicious_words if re.search(rf"\b{w}\b", news_text, re.IGNORECASE)]
    found_trust = [w for w in trust_words if re.search(rf"\b{w}\b", news_text, re.IGNORECASE)]

    sentiment_score = TextBlob(news_text).sentiment.polarity
    if sentiment_score > 0.2:
        sentiment_label = "Positive"
    elif sentiment_score < -0.2:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    red_flags = []
    if len(found_suspicious) > 2:
        red_flags.append("🚨 Contains emotionally charged or exaggerated words.")
    if sentiment_label == "Negative":
        red_flags.append("⚠️ Negative or fear-based sentiment detected.")
    if len(news_text.split()) < 50:
        red_flags.append("🧾 Text too short — might lack credibility.")
    if not found_trust:
        red_flags.append("❌ No trustworthy keywords detected (like ‘official’, ‘report’).")

    return {
        "suspicious_keywords": found_suspicious,
        "trust_keywords": found_trust,
        "sentiment": sentiment_label,
        "red_flags": red_flags
    }


# -------------------------------------------------------
# 🔍 Hybrid Prediction (Text)
# -------------------------------------------------------
def predict_hybrid(news_text):
    news_text = clean_text(news_text)
    input_tfidf = vectorizer.transform([news_text])
    pred = model.predict(input_tfidf)[0]
    prob = model.predict_proba(input_tfidf)[0][1] * 100

    ml_label = "Fake" if pred == 1 else "Real"
    ml_confidence = round(prob if pred == 1 else 100 - prob, 2)

    ddg_res = fetch_web_articles(news_text)
    web_status = ddg_res["status"]
    articles = ddg_res["articles"]

    web_similarity = round(compute_similarity(news_text, articles), 2)

    # 🚨 Combine handles "0" similarity gracefully if it's unavailable, 
    # but let's pass down exactly what to weight if unavailable.
    # We already have thresholding inside combine_scores.
    combined = combine_scores(ml_label, ml_confidence, web_similarity)

    return {
        "ml_label": ml_label,
        "ml_confidence": ml_confidence,
        "web_similarity": web_similarity,
        "web_verification_status": web_status,
        "final_label": combined["final_label"],
        "combined_score": combined["combined_score"],
        "sources": [{"title": a["title"], "link": a["link"]} for a in articles],
    }


# -------------------------------------------------------
# 📊 Analyze Text (Keywords, Sentiment, Red Flags)
# -------------------------------------------------------
@app.route("/api/analyze_text", methods=["POST"])
def analyze_text():
    data = request.get_json()
    news_text = (data.get("news", "") if data else "").strip()
    if not news_text:
        return jsonify({"error": "No text provided"}), 400
    return jsonify(analyze_content(news_text))


# -------------------------------------------------------
# 🧠 Predict Text Route
# -------------------------------------------------------
@app.route("/api/predict_text", methods=["POST"])
def predict_text():
    data = request.get_json()
    news_text = data.get("news", "").strip()
    if not news_text:
        return jsonify({"error": "No text provided"}), 400

    result = predict_hybrid(news_text)
    result["analysis"] = analyze_content(news_text)
    return jsonify(result), 200


# -------------------------------------------------------
# 🌐 Predict URL Route
# -------------------------------------------------------
@app.route("/api/predict_url", methods=["POST"])
def predict_url():
    try:
        data = request.get_json()
        url = data.get("url", "").strip()
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # 1️⃣ Extract article
        article_data = extract_article_text(url)
        text = article_data.get("text", "").strip()
        if not text:
            error_msg = article_data.get("error", "Unable to extract content from URL. Site may have bot protection.")
            return jsonify({"error": error_msg}), 422

        # 2️⃣ Run Hybrid Prediction using existing function
        result = predict_hybrid(text)

        # 3️⃣ Add extra URL specific fields
        result["headline"] = article_data.get("title", "")
        result["news_text"] = text[:2000]

        # 4️⃣ Analyze
        result["analysis"] = analyze_content(text)

        return jsonify(result), 200

    except Exception as e:
        print("Error in /predict_url:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------
# 🏠 Health Check
# -------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Hybrid Fake News Detection API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
