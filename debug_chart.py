from src.market_data import get_historical_data
import pandas as pd

def test_data_join(ticker_name="Gold", ticker_symbol="GC=F"):
    print(f"--- Testing {ticker_name} ---")
    
    # 1. Fetch Asset Data
    period = "1mo"
    hist_df = get_historical_data(ticker_symbol, period=period)
    print(f"Asset Data Shape: {hist_df.shape}")
    if not hist_df.empty:
        print(f"Asset Index Type: {hist_df.index.dtype}")
        print(f"Asset Index Sample: {hist_df.index[0]}")

    # 2. Fetch FX Data
    fx_df = get_historical_data("INR=X", period=period)
    print(f"FX Data Shape: {fx_df.shape}")
    if not fx_df.empty:
        print(f"FX Index Type: {fx_df.index.dtype}")
        print(f"FX Index Sample: {fx_df.index[0]}")

    # 3. Attempt Join
    if not hist_df.empty and not fx_df.empty:
        # Mimic app.py logic
        combined = hist_df[['Close']].join(fx_df[['Close']], lsuffix='_Asset', rsuffix='_FX')
        print(f"Joined Data Shape (Raw Join): {combined.shape}")
        
        combined_cleaned = combined.dropna()
        print(f"Joined Data Shape (dropna): {combined_cleaned.shape}")
        
        if combined_cleaned.empty:
            print("JOIN FAILED: Result is empty.")
            
            # Debug: Try converting to tz-naive date
            print("Attempting to fix by converting to tz-naive dates...")
            hist_df.index = hist_df.index.tz_localize(None).normalize()
            fx_df.index = fx_df.index.tz_localize(None).normalize()
            
            combined_v3 = hist_df[['Close']].join(fx_df[['Close']], lsuffix='_Asset', rsuffix='_FX')
            print(f"Joined Data Shape (TZ Naive): {combined_v3.dropna().shape}")
            if not combined_v3.dropna().empty:
                print("SUCCESS with TZ Naive approach.")

test_data_join("Gold", "GC=F")
