import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("⚙️ News Filters")

country_options = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

category_options = [
    "general",
    "business",
    "technology",
    "sports",
    "health",
    "science",
    "entertainment"
]

country = st.sidebar.selectbox(
    "🌍 Select Country",
    list(country_options.keys())
)

category = st.sidebar.selectbox(
    "📰 Select Category",
    category_options
)

keyword = st.sidebar.text_input(
    "🔍 Search Keyword",
    placeholder="AI, Tesla, Cricket..."
)

num_articles = st.sidebar.slider(
    "📄 Number of Articles",
    min_value=5,
    max_value=50,
    value=15
)

refresh = st.sidebar.button("🔄 Refresh News")

# -----------------------------
# Title
# -----------------------------
st.title("📰 Advanced News Headlines Dashboard")
st.markdown("Stay updated with the latest headlines around the world.")

# -----------------------------
# Fetch News Function
# -----------------------------
@st.cache_data(ttl=300)
def fetch_news(country_code, category, keyword, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "category": category,
        "pageSize": page_size
    }

    if keyword.strip():
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "status": "error",
            "message": f"API Error: {response.status_code}"
        }

# -----------------------------
# Get News
# -----------------------------
country_code = country_options[country]

data = fetch_news(
    country_code,
    category,
    keyword,
    num_articles
)

# -----------------------------
# Display News
# -----------------------------
if data.get("status") == "ok":

    articles = data.get("articles", [])

    st.success(f"Found {len(articles)} articles")

    for article in articles:

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if article.get("urlToImage"):
                    st.image(
                        article["urlToImage"],
                        use_container_width=True
                    )

            with col2:
                st.subheader(article.get("title", "No Title"))

                source = article.get("source", {}).get("name", "Unknown Source")

                published = article.get("publishedAt")

                if published:
                    try:
                        published = datetime.strptime(
                            published,
                            "%Y-%m-%dT%H:%M:%SZ"
                        ).strftime("%d %b %Y %I:%M %p")
                    except:
                        pass

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                st.write(
                    article.get(
                        "description",
                        "No description available."
                    )
                )

                st.link_button(
                    "🔗 Read Full Article",
                    article.get("url", "#")
                )

            st.divider()

elif data.get("status") == "error":
    st.error(data.get("message"))

else:
    st.warning("No news articles found.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "Built with Streamlit • Powered by NewsAPI"
)