import feedparser
from urllib.parse import quote
import streamlit as st
import requests


# ---------------------------------------------------------
# Fetch news using Google News RSS
# ---------------------------------------------------------
def fetch_news(query="Shankara", max_results=20, region="IN"):
    """
    Fetch news from Google News RSS for any query.
    query: search term (any text)
    max_results: number of articles to return
    region: country code (IN, US, GB, etc.)
    """

    query = (query or "").strip()
    region = (region or "").strip().upper() or "IN"

    # Improve search for single-word queries
    if len(query.split()) == 1:
        search_term = f"{query} news"
    else:
        search_term = query

    # Encode properly for Google News
    q = quote(search_term)

    # Google News RSS URL
    url = f"https://news.google.com/rss/search?q={q}&hl=en-{region}&gl={region}&ceid={region}:en"

    # Show what is being searched (useful for debugging)
    st.caption(f"🔍 Search term used: **{search_term}**")
    st.caption(f"🔗 RSS URL: `{url}`")

    # --- Fetch and clean response manually to avoid XML token issues ---
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        st.error(f"❌ Error fetching RSS: {e}")
        return []

    # Decode, ignoring invalid characters that break XML parsing
    content = resp.content.decode("utf-8", errors="ignore")

    # Parse RSS feed
    feed = feedparser.parse(content)

    # Only warn if parser is unhappy *and* there are no entries
    if getattr(feed, "bozo", 0) and not getattr(feed, "entries", []):
        st.warning(f"⚠️ RSS parsing warning: {getattr(feed, 'bozo_exception', 'Unknown error')}")

    articles = []
    for entry in feed.entries[:max_results]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get(
