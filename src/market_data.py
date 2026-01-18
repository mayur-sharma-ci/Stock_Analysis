import yfinance as yf
import pandas as pd

TICKERS = {
    "Gold": "GC=F",
    "Oil": "CL=F",
    "Silver": "SI=F",
    "USD/INR": "INR=X"
}

def get_current_prices():
    """
    Fetches the latest price and today's change for all defined tickers.
    """
    data = {}
    for name, ticker in TICKERS.items():
        try:
            ticker_obj = yf.Ticker(ticker)
            # Fetch recent history (1 day with 1m interval if possible, else 5d)
            # 'fast_info' is often faster for current price
            info = ticker_obj.fast_info
            
            # Fallback to history if fast_info is not returning expected values
            # (Sometimes fast_info keys differ by version)
            try:
                current_price = info.last_price
                prev_close = info.previous_close
            except:
                hist = ticker_obj.history(period="5d")
                if len(hist) > 0:
                    current_price = hist["Close"].iloc[-1]
                    prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else current_price
                else:
                    current_price = 0.0
                    prev_close = 0.0

            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0.0

            data[name] = {
                "price": current_price,
                "change_abs": change,
                "change_pct": change_percent
            }
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            data[name] = {"price": 0.0, "change_abs": 0.0, "change_pct": 0.0}
    
    # Calculate INR prices
    usd_inr = data.get("USD/INR", {}).get("price", 80.0) # Fallback to 80 if fails
    
    for name in ["Gold", "Oil", "Silver"]:
        if name in data:
            usd_price = data[name]["price"]
            usd_change = data[name]["change_abs"]
            
            # Conversion
            data[name]["price_inr"] = usd_price * usd_inr
            data[name]["change_inr"] = usd_change * usd_inr
            
    return data

def get_historical_data(ticker_symbol, period="1mo", interval="1d"):
    """
    Fetches historical data for a specific ticker.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period=period, interval=interval)
        return history
    except Exception as e:
        print(f"Error fetching history for {ticker_symbol}: {e}")
        return pd.DataFrame()
