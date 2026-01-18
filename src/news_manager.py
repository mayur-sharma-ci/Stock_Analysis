import feedparser
import time

# Google News RSS URL with query parameters
# "hl=en-IN&gl=IN&ceid=IN:en" ensures India-centric English news
RSS_URL_TEMPLATE = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

KEYWORDS = [
    "Geopolitics",
    "Trade War",
    "Crude Oil Prices",
    "Gold Prices",
    "USD INR Exchange Rate",
    "Middle East Conflict",
    "US Federal Reserve",
    "OPEC",
    "Russia Ukraine"
]

import urllib.parse

def fetch_geopolitics_news():
    """
    Fetches news articles related to geopolitical terms from Google News RSS.
    Returns a list of dictionaries with 'title', 'link', 'published', 'summary'.
    """
    all_news = []
    
    # Join keywords with OR
    raw_query = " OR ".join([f'"{k}"' for k in KEYWORDS])
    # URL Encode the query part
    encoded_query = urllib.parse.quote(raw_query)
    
    rss_url = RSS_URL_TEMPLATE.format(query=encoded_query)
    
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:20]: # Limit to top 20
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else "Unknown",
                "summary": entry.summary if "summary" in entry else ""
            })
    except Exception as e:
        print(f"Error fetching news: {e}")
        
    return all_news
