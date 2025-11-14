import streamlit as st
import requests


# ---------------------------------------------------------
# CONFIG — Your NewsAPI Key
# ---------------------------------------------------------
NEWS_API_KEY = "7b8d5e84d6974e7ca33d5c9d884ce31b"   # <-- YOUR KEY INSERTED


# ---------------------------------------------------------
# Fetch news using NewsAPI
# ---------------------------------------------------------
def fetch_news(query="Shankara", max_results=20, language="en"):
    """
    Fetch news from NewsAPI.org.
    query: any search term
    max_results: max articles to return (NewsAPI returns up to 100)
    language: en, hi, fr, etc.
    """

    query = (query or "").strip()
    language = (language or "en").strip()

    if not query:
        st.error("Please enter a search term.")
        return []

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": language,
        "pageSize": max_results,
        "apiKey": NEWS_API_KEY,
    }

    # Debug info
    st.caption(f"🔍 Query: **{query}**")
    st.caption(f"🌐 Language: **{language}**")
    st.caption(f"🔗 API Endpoint: `{url}`")

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ HTTP Error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network Error: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Unknown Error: {e}")
        return []

    # API error handling
    if data.get("status") != "ok":
        st.error(f"❌ API Error: {data.get('message', 'Unknown error')}")
        return []

    return data.get("articles", [])


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="News Search App",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Universal News Search App (Powered by NewsAPI)")
st.markdown(
    """
Search the latest news about **anything** — a person, company, topic, or event.  
This uses **NewsAPI**, which is fast, reliable, and fully JSON-based.
"""
)

# Sidebar inputs
with st.sidebar:
    st.header("Search Controls")

    query = st.text_input(
        "Search term",
        value="Shankara",
        placeholder="e.g. Aakash, Tesla, AI Jobs, Cricket, Qatar Airways...",
        help="You can search ANY topic."
    )

    max_results = st.slider(
        "Max results",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
    )

    language = st.selectbox(
        "Language",
        ["en", "hi", "fr", "de", "es", "it", "ru"],
        index=0,
        help="Choose the language of the news."
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
                language=language
            )

        if not articles:
            st.info("No news articles found. Try a more specific term.")
        else:
            st.success(f"Found {len(articles)} articles.")

            for i, a in enumerate(articles, start=1):
                title = a.get("title", "No Title")
                url = a.get("url")
                published = a.get("publishedAt", "")
                description = a.get("description", "")
                source = a.get("source", {}).get("name", "Unknown Source")

                st.markdown(f"### {i}. {title}")
                st.caption(f"📰 {source} | 🕒 {published}")

                if description:
                    st.write(description)

                if url:
                    st.markdown(f"[🔗 Read full article]({url})")

                st.markdown("---")

else:
    st.info("Enter a keyword and click **Search News** to begin.")
