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
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        })
    return articles


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="News Search App",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Universal News Search App")
st.markdown(
    """
Search the latest news about **anything** — a person, company, topic, or event.  
This uses free **Google News RSS**, so no API key is needed.
"""
)

# Sidebar inputs
with st.sidebar:
    st.header("Search Controls")

    query = st.text_input(
        "Search term",
        value="Shankara",
        placeholder="e.g. Aakash, Tesla, AI Jobs, Cricket, Qatar Airways...",
        help="You can search for ANY topic."
    )

    max_results = st.number_input(
        "Max results",
        min_value=5,
        max_value=50,
        value=20,
        step=1,
    )

    region = st.text_input(
        "Region (country code)",
        value="IN",
        help="Examples: IN, US, GB, AU, CA"
    )

    search_button = st.button("Search News")


# Main output area
if search_button:
    if not query.strip():
        st.warning("⚠️ Please enter a search term.")
    else:
        with st.spinner("Fetching the latest news..."):
            articles = fetch_news(
                query=query.strip(),
                max_results=max_results,
                region=region.strip() or "IN"
            )

        # Show results
        if not articles:
            st.info("No news articles found. Try a more specific term (e.g. 'Aakash Institute').")
        else:
            st.success(f"Found {len(articles)} articles.")
            for i, a in enumerate(articles, start=1):
                title = a["title"]
                link = a["link"]
                published = a["published"]
                summary = a["summary"]

                st.markdown(f"### {i}. {title}")
                if published:
                    st.caption(f"🕒 {published}")
                if summary:
                    st.write(summary, unsafe_allow_html=True)

                st.markdown(f"[🔗 Read full article]({link})")
                st.markdown("---")

else:
    st.info("Enter a keyword and press **Search News** to get started.")
