from src.market_data import get_current_prices, get_historical_data
from src.news_manager import fetch_geopolitics_news
from src.sentiment_engine import aggregate_news_sentiment

print("--- Testing Market Data ---")
prices = get_current_prices()
print("Current Prices:", prices.keys())
for k, v in prices.items():
    print(f"{k}: {v['price']} (Change: {v['change_pct']}%)")

print("\n--- Testing Historical Data ---")
hist = get_historical_data("GC=F", period="5d")
print("Gold History Shape:", hist.shape)

print("\n--- Testing News & Sentiment ---")
news = fetch_geopolitics_news()
print(f"Fetched {len(news)} articles.")
if news:
    print(f"Sample: {news[0]['title']}")
    score, verdict = aggregate_news_sentiment(news)
    print(f"Sentiment Score: {score}, Verdict: {verdict}")
else:
    print("No news fetched.")
