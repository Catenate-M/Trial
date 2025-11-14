import feedparser
from urllib.parse import quote
import streamlit as st


def fetch_news(query="Shankara", max_results=20, region="IN"):
    """
    Fetch news from Google News RSS for a given query.

    query: search term, e.g. 'Shankara'
    max_results: how many articles to show
    region: country code, e.g. 'IN', 'US', 'GB'
    """
    q = quote(query)

    # Google News RSS URL
    url = f"https://news.google.com/rss/search?q={q}&hl=en-{region}&gl={region}&ceid={region}:en"

    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_results]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        })
    return articles


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Shankara News Finder",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Shankara News Finder")
st.markdown(
    """
Search the latest news about **Shankara** (or anything else) using Google News RSS.  
No API keys, no paid services.
"""
)

with st.sidebar:
    st.header("Search Settings")

    query = st.text_input(
        "Search term",
        value="Shankara",
        help="Example: 'Shankara', 'Adi Shankaracharya', 'Shankara building products'"
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
        help="Examples: IN, US, GB, AU..."
    )

    search_button = st.button("Search News")


if search_button:
    if not query.strip():
        st.warning("Please enter a search term.")
    else:
        with st.spinner("Fetching news..."):
            articles = fetch_news(query=query.strip(), max_results=max_results, region=region.strip() or "IN")

        if not articles:
            st.info("No news articles found.")
        else:
            st.success(f"Found {len(articles)} articles.")
            for i, a in enumerate(articles, start=1):
                title = a["title"]
                link = a["link"]
                published = a["published"]
                summary = a["summary"]

                st.markdown(f"### {i}. {title}")
                if published:
                    st.caption(published)
                if summary:
                    st.write(summary, unsafe_allow_html=True)
                st.markdown(f"[Read full article]({link})")
                st.markdown("---")
else:
    st.info("Set your search in the sidebar and click **Search News**.")

