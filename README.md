# StockAnalysis IIFT Dashboard

A real-time dashboard for IIFT Analysis, tracking key commodities and currency rates, augmented with geopolitical sentiment analysis.

## Features
- **Live Market Data**: Tracks Gold, Oil, Silver, and USD/INR using `yfinance`.
- **Geopolitical Sentiment**: Analyzes top news headlines (fetched via Google News) using `NLTK VADER` to assay the global geopolitical pulse.
- **Interactive Charts**: Historical price trends visualization with Plotly.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/mayur-sharma-ci/Stock_Analysis.git
    cd Stock_Analysis
    ```

2.  Install dependencies:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate  # Windows
    # source .venv/bin/activate # Mac/Linux
    
    pip install -r requirements.txt
    ```

3.  Download NLTK Data (if not auto-downloaded):
    ```bash
    python -c "import nltk; nltk.download('vader_lexicon')"
    ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Tech Stack
- **Frontend**: Streamlit
- **Data**: yfinance, feedparser (Google News RSS)
- **Analysis**: NLTK (Sentiment), Pandas
- **Visualization**: Plotly

## License
MIT
