import streamlit as st
import time
import pandas as pd
from src.market_data import get_current_prices, get_historical_data, TICKERS
from src.news_manager import fetch_geopolitics_news
from src.sentiment_engine import aggregate_news_sentiment
from src.ui_components import render_metric_card, plot_price_chart, render_sentiment_gauge

# Page Config
st.set_page_config(
    page_title="IIFT StockAnalysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #f0f2f6;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📈 StockAnalysis IIFT Dashboard")
    st.markdown("Live Market Data & Geopolitical Sentiment Analysis")

    # --- Sidebar Controls ---
    st.sidebar.header("Configuration")
    refresh_btn = st.sidebar.button("Refresh Data")
    
    # Auto-refresh using empty container trick if needed, but manual for now is safer for APIs.
    if refresh_btn:
        st.cache_data.clear()

    # --- Key Metrics Row ---
    st.subheader("Live Market Overview")
    
    # Fetch Data
    with st.spinner("Fetching Market Data..."):
        prices = get_current_prices()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        data = prices.get("Gold", {})
        render_metric_card("Gold (₹)", data.get("price_inr", 0), data.get("change_inr", 0), data.get("change_pct", 0))
    
    with col2:
        data = prices.get("Silver", {})
        render_metric_card("Silver (₹)", data.get("price_inr", 0), data.get("change_inr", 0), data.get("change_pct", 0))

    with col3:
        data = prices.get("Oil", {})
        render_metric_card("Crude Oil (₹)", data.get("price_inr", 0), data.get("change_inr", 0), data.get("change_pct", 0))

    with col4:
        data = prices.get("USD/INR", {})
        render_metric_card("USD/INR", data.get("price", 0), data.get("change_abs", 0), data.get("change_pct", 0))

    st.markdown("---")

    # --- Charts & Sentiment Section ---
    col_charts, col_sentiment = st.columns([2, 1])

    with col_charts:
        st.subheader("Price Trends")
        selected_ticker = st.selectbox("Select Asset to View", list(TICKERS.keys()))
        period = st.select_slider("Time Period", options=["5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"], value="1mo")
        
        with st.spinner(f"Loading chart for {selected_ticker}..."):
            ticker_symbol = TICKERS[selected_ticker]
            hist_df = get_historical_data(ticker_symbol, period=period)
            
            # Logic for INR conversion on the chart
            y_col = 'Close'
            currency_symbol = '$'
            
            if selected_ticker != "USD/INR" and not hist_df.empty:
                # Fetch USD/INR history for the same period
                fx_df = get_historical_data("INR=X", period=period)
                
                # Align the DataFrames on Index (Date)
                # We use an inner join to ensure we only have points where we have both data
                if not fx_df.empty:
                    combined = hist_df[['Close']].join(fx_df[['Close']], lsuffix='_Asset', rsuffix='_FX')
                    
                    # Calculate INR Price
                    combined['Close_INR'] = combined['Close_Asset'] * combined['Close_FX']
                    combined = combined.dropna()
                    
                    # Update parameters for plotting
                    hist_df = combined
                    y_col = 'Close_INR'
                    currency_symbol = '₹'
            elif selected_ticker == "USD/INR":
                 currency_symbol = '₹'

            plot_price_chart(hist_df, selected_ticker, y_col=y_col, currency_symbol=currency_symbol)

    with col_sentiment:
        st.subheader("Geopolitical Pulse")
        with st.spinner("Analyzing Global News..."):
            news = fetch_geopolitics_news()
            score, verdict = aggregate_news_sentiment(news)
        
        render_sentiment_gauge(score, verdict)
        
        st.markdown("#### Latest Headlines")
        with st.container(height=400):
            for item in news:
                st.markdown(f"**[{item['title']}]({item['link']})**")
                # Clean up summary: remove HTML tags if any (simple approach) or just show snippet
                summary = item['summary'].split('<')[0] 
                if summary:
                    st.caption(summary[:150] + "...")
                st.divider()

    st.sidebar.markdown("---")
    st.sidebar.info("Data Sources: Yahoo Finance (Prices), Google News RSS (Sentiment).")

if __name__ == "__main__":
    main()
