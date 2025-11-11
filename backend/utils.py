import os
import ipaddress
import socket
import numpy as np
import requests
from duckduckgo_search import DDGS
from sentence_transformers import SentenceTransformer, util
from bs4 import BeautifulSoup

# optional: prefer newspaper3k when available (best extraction)
try:
    from newspaper import Article
    HAS_NEWSPAPER = True
except Exception:
    HAS_NEWSPAPER = False

# Load SBERT model only once globally (avoid reloading every time)
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Enable Jina fallback by default; set USE_JINA_FALLBACK=0 to disable
USE_JINA_FALLBACK = os.getenv("USE_JINA_FALLBACK", "1") not in ("0", "false", "False")

# -------------------------------------------------------
# 🔍 Fetch Web Articles (DuckDuckGo)
# -------------------------------------------------------
def fetch_web_articles(query, max_results=3):
    """
    Fetch brief text snippets and links from DuckDuckGo search results.
    Args:
        query (str): The news headline or sentence to search.
        max_results (int): Number of articles to fetch (default = 3)
    Returns:
        list[dict]: [{title, body, link}, ...]
    """
    results = []
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
    return results


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


def extract_article_text(url, timeout=10):
    """
    Try multiple strategies to extract article title and text from a URL.
    Returns: dict {"title": str, "text": str}
    """
    # SSRF guard
    if not is_url_allowed(url):
        return {"title": "", "text": ""}

    # 1) Try newspaper3k if available (often the best).
    # Use a requests Session to fetch HTML and then feed it to newspaper to allow
    # custom headers (helps avoid 401/403 on some sites).
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    if HAS_NEWSPAPER:
        try:
            # fetch HTML using session so we can control headers
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            art = Article(url)
            art.set_html(resp.text)
            art.parse()
            title = (art.title or "").strip()
            text = (art.text or "").strip()
            if text:
                return {"title": title, "text": text}
        except Exception:
            # fall through to requests + bs4
            pass

    # 2) requests + BeautifulSoup fallback
    try:
        # Limit redirects implicitly via requests (default 30). Enforce timeout.
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Title: prefer <meta property="og:title"> or <title>
        title = ""
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title.get("content").strip()
        elif soup.title and soup.title.string:
            title = soup.title.string.strip()

        # Text: prefer <article> tag, else aggregate paragraphs
        text = ""
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = [p.get_text(strip=True) for p in article_tag.find_all("p")]
            text = "\n\n".join([p for p in paragraphs if p])
        else:
            ps = soup.find_all("p")
            if ps:
                # take several leading paragraphs as a fallback
                paragraphs = [p.get_text(strip=True) for p in ps[:12]]
                text = "\n\n".join([p for p in paragraphs if p])

        result = {"title": title or "", "text": text or ""}
        if result["text"]:
            return result

        # If the site blocks direct scraping (401/403) or returned empty text,
        # attempt a lightweight text-extraction proxy as a final fallback.
        # Jina's text extraction proxy (r.jina.ai) often returns cleaned article text.
        try:
            cleaned_url = url.replace('https://', '').replace('http://', '')
            jina_url = f"https://r.jina.ai/http://{cleaned_url}"
            jr = session.get(jina_url, timeout=8)
            if jr.status_code == 200 and jr.text.strip():
                # Jina returns plaintext; first line is often the title
                body = jr.text.strip()
                first_line = body.splitlines()[0].strip()
                return {"title": first_line or title or "", "text": body}
        except Exception:
            pass

        return result
    except Exception as e:
        # If the direct fetch fails (401/403 or other), try the Jina proxy as a fallback
        print(f"[⚠️] extract_article_text failed for {url}: {e}")
        if USE_JINA_FALLBACK:
            try:
                cleaned_url = url.replace('https://', '').replace('http://', '')
                jina_url = f"https://r.jina.ai/http://{cleaned_url}"
                jr = session.get(jina_url, timeout=8)
                if jr.status_code == 200 and jr.text.strip():
                    body = jr.text.strip()
                    first_line = body.splitlines()[0].strip()
                    return {"title": first_line or "", "text": body}
            except Exception:
                pass

        return {"title": "", "text": ""}


# -------------------------------------------------------
# 🧠 Compute Semantic Similarity (SBERT)
# -------------------------------------------------------
def compute_similarity(news_text, articles):
    """
    Compute cosine similarity between input news and fetched web article snippets.
    Args:
        news_text (str): Input claim text.
        articles (list): List of dicts with "body" keys.
    Returns:
        float: Average similarity score in percentage.
    """
    if not articles:
        return 0.0
    try:
        claim_emb = sbert_model.encode(news_text, convert_to_tensor=True)
        article_embs = sbert_model.encode(
            [a["body"] for a in articles], convert_to_tensor=True
        )
        sims = util.cos_sim(claim_emb, article_embs)
        avg_sim = float(np.mean(sims.cpu().numpy())) * 100
        return avg_sim
    except Exception as e:
        print(f"[⚠️] Similarity computation failed: {e}")
        return 0.0


# -------------------------------------------------------
# 🧩 Hybrid Combination Logic
# -------------------------------------------------------
def combine_scores(ml_confidence, web_similarity, ml_weight=0.6, web_weight=0.4):
    """
    Combine ML confidence and Web Similarity for hybrid verdict.
    Args:
        ml_confidence (float): Model’s confidence in its prediction (0–100)
        web_similarity (float): Average factual similarity score (0–100)
        ml_weight (float): Weight for ML prediction (default = 0.6)
        web_weight (float): Weight for web verification (default = 0.4)
    Returns:
        dict: {combined_score, final_label}
    """
    combined = (ml_confidence * ml_weight) + (web_similarity * web_weight)
    label = "Real" if combined >= 50 else "Fake"
    return {"combined_score": round(combined, 2), "final_label": label}
