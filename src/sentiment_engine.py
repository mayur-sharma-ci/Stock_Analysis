import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes sentiment of a text string.
    Returns a dict with 'pos', 'neg', 'neu', 'compound'.
    """
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)

def aggregate_news_sentiment(news_items):
    """
    Calculates average sentiment from a list of news items.
    """
    if not news_items:
        return 0.0, "Neutral"

    total_compound = 0
    
    for item in news_items:
        # Combine title and summary for analysis
        text = f"{item['title']} {item.get('summary', '')}"
        scores = analyze_sentiment(text)
        total_compound += scores['compound']
    
    avg_score = total_compound / len(news_items)
    
    if avg_score >= 0.05:
        verdict = "Positive"
    elif avg_score <= -0.05:
        verdict = "Negative"
    else:
        verdict = "Neutral"
        
    return avg_score, verdict
