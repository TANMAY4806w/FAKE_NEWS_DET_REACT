import os
import ipaddress
import socket
import numpy as np
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# optional: prefer newspaper3k when available (best extraction)
try:
    from newspaper import Article
    HAS_NEWSPAPER = True
except Exception:
    HAS_NEWSPAPER = False

# Enable Jina fallback by default; set USE_JINA_FALLBACK=0 to disable
USE_JINA_FALLBACK = os.getenv("USE_JINA_FALLBACK", "1") not in ("0", "false", "False")

# -------------------------------------------------------
# 🔍 Fetch Web Articles (DuckDuckGo)
# -------------------------------------------------------
@lru_cache(maxsize=100)
def fetch_web_articles(query, max_results=3):
    """
    Fetch brief text snippets and links from DuckDuckGo search results.
    Args:
        query (str): The news headline or sentence to search.
        max_results (int): Number of articles to fetch (default = 3)
    Returns:
        dict: {"status": "success"|"unavailable", "articles": [{title, body, link}, ...]}
    """
    results = []
    status = "success"
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="in-en", max_results=max_results):
                results.append({
                    "title": r.get("title", "No title"),
                    "body": r.get("body", "No content available"),
                    "link": r.get("href", "")
                })
    except Exception as e:
        print(f"[⚠️] DuckDuckGo fetch failed: {e}")
        status = "unavailable"
    return {"status": status, "articles": results}


# -------------------------------------------------------
# 🔎 Extract Article Text (robust, with fallbacks)
# -------------------------------------------------------
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
}

# Broaden headers to look more like a real browser
DEFAULT_HEADERS.update({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
})


def _is_ip_private_or_disallowed(ip_str: str) -> bool:
    """
    Return True if the IP is private, loopback, link-local, multicast, reserved, or unspecified.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )
    except Exception:
        return True


def is_url_allowed(url: str) -> bool:
    """
    Basic SSRF guard:
    - Require http/https scheme
    - Resolve hostname and disallow private/loopback/link-local/reserved IPs
    - Disallow empty/invalid hosts
    """
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.hostname:
            return False

        # Resolve A/AAAA records and verify all results are public
        try:
            addrinfos = socket.getaddrinfo(parsed.hostname, None)
        except Exception:
            return False

        for ai in addrinfos:
            sockaddr = ai[4]
            if not sockaddr:
                return False
            ip = sockaddr[0]
            if _is_ip_private_or_disallowed(ip):
                return False

        return True
    except Exception:
        return False


@lru_cache(maxsize=100)
def extract_article_text(url, timeout=10):
    """
    Try multiple strategies to extract article title and text from a URL.
    Returns: dict {"title": str, "text": str}
    """
    # SSRF guard: strictly abort if check fails
    if not is_url_allowed(url):
        print(f"[⚠️] SSRF blocked: {url}")
        return {"title": "", "text": ""}

        # 1) Try newspaper3k if available (often the best).
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    if HAS_NEWSPAPER:
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            art = Article(url)
            art.set_html(resp.text)
            art.parse()
            title = (art.title or "").strip()
            text = (art.text or "").strip()
            if text:
                return {"title": title, "text": text}
        except Exception as e:
            # specifically check for anti-bot
            if "403" in str(e) or "401" in str(e):
                pass # let it fall through to Jina
            pass

    # 2) requests + BeautifulSoup fallback
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title = ""
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title.get("content").strip()
        elif soup.title and soup.title.string:
            title = soup.title.string.strip()

        text = ""
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = [p.get_text(strip=True) for p in article_tag.find_all("p")]
            text = "\n\n".join([p for p in paragraphs if p])
        else:
            ps = soup.find_all("p")
            if ps:
                paragraphs = [p.get_text(strip=True) for p in ps[:12]]
                text = "\n\n".join([p for p in paragraphs if p])

        if text:
            return {"title": title or "", "text": text}
            
    except requests.exceptions.HTTPError as he:
        # If it's a 403 Forbidden, the site is explicitly blocking us
        if he.response.status_code in (403, 401, 404, 520, 503):
            return {"title": "", "text": "", "error": f"The website blocked automated access (Status {he.response.status_code}). Please paste the article text directly instead."}
    except Exception as e:
        pass

    # 3) If direct requests failed, attempt Jina Proxy
    if USE_JINA_FALLBACK:
        try:
            cleaned_url = url.replace('https://', '').replace('http://', '')
            jina_url = f"https://r.jina.ai/http://{cleaned_url}"
            jr = session.get(jina_url, timeout=8)
            if jr.status_code == 200 and jr.text.strip():
                body = jr.text.strip()
                if "SecurityCompromiseError" not in body and len(body) > 100:
                    first_line = body.splitlines()[0].strip()
                    return {"title": first_line or "", "text": body}
        except Exception:
            pass

    return {"title": "", "text": "", "error": "This website has strong anti-bot protection and blocked extraction. Please copy and paste the article text manually."}


# -------------------------------------------------------
# 🧠 Compute Semantic Similarity (TF-IDF)
# -------------------------------------------------------
def compute_similarity(news_text, articles):
    """
    Compute cosine similarity between input news and fetched web article snippets using TF-IDF.
    Args:
        news_text (str): Input claim text.
        articles (list): List of dicts with "body" keys.
    Returns:
        float: Average similarity score in percentage.
    """
    if not articles or not news_text.strip():
        return 0.0
    
    valid_articles = [a for a in articles if a.get("body", "").strip()]
    if not valid_articles:
        return 0.0
        
    try:
        # Extract first ~3 sentences for tighter comparison instead of full article
        sentences = [s.strip() for s in news_text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        claim_text = '. '.join(sentences[:3]) + '.' if sentences else news_text
        
        # Combine the claim and all article snippets into a single list for TF-IDF vectorization
        documents = [claim_text] + [a["body"] for a in valid_articles]
        
        # Initialize the vectorizer and fit_transform the documents
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # The first row is the claim vector, the rest are article vectors
        claim_vector = tfidf_matrix[0:1]
        article_vectors = tfidf_matrix[1:]
        
        # Calculate cosine similarities
        sims = cosine_similarity(claim_vector, article_vectors)[0]
        
        # Average similarity across all retrieved articles snippet bodies
        avg_sim = float(np.mean(sims)) * 100
        return avg_sim
    except Exception as e:
        print(f"[⚠️] Similarity computation failed: {e}")
        return 0.0


# -------------------------------------------------------
# 🧩 Hybrid Combination Logic
# -------------------------------------------------------
def combine_scores(ml_label, ml_confidence, web_similarity, ml_weight=0.6, web_weight=0.4):
    """
    Combine ML confidence and Web Similarity for hybrid verdict.
    Args:
        ml_label (str): "Real" or "Fake" from ML model
        ml_confidence (float): Model’s confidence in its prediction (0–100)
        web_similarity (float): Average factual similarity score (0–100)
        ml_weight (float): Weight for ML prediction (default = 0.6)
        web_weight (float): Weight for web verification (default = 0.4)
    Returns:
        dict: {combined_score, final_label}
    """
    # Define threshold for "inconclusive" web verification
    WEB_VERIFICATION_THRESHOLD = 20  # Below this, web verification is unreliable

    if web_similarity < WEB_VERIFICATION_THRESHOLD:
        ml_weight_adjusted = 0.8
        web_weight_adjusted = 0.2
    else:
        ml_weight_adjusted = ml_weight
        web_weight_adjusted = web_weight

    # Convert to unified scale (100 = Real, 0 = Fake)
    ml_score = ml_confidence if ml_label == "Real" else (100 - ml_confidence)

    combined = (ml_score * ml_weight_adjusted) + (web_similarity * web_weight_adjusted)
    label = "Real" if combined >= 50 else "Fake"
    
    return {
        "combined_score": round(combined, 2), 
        "final_label": label,
        "ml_score": round(ml_score, 2),
        "web_verification_reliable": web_similarity >= WEB_VERIFICATION_THRESHOLD
    }
