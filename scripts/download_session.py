"""
YFinance download with proxy and different approach.
"""

import yfinance as yf
import pandas as pd
import time
import random
import os
from datetime import datetime
import requests

# Disable yfinance's internal caching and use different headers
def download_with_session(ticker, start_date, end_date):
    """Download using a custom session."""
    try:
        # Create a session with different headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Use the session with yfinance
        yf.set_tz_cache_location("tz_cache")
        ticker_obj = yf.Ticker(ticker, session=session)
        
        # Try with different parameters
        df = ticker_obj.history(start=start_date, end=end_date, 
                               interval="1d", auto_adjust=True,
                               backadjust=False, repair=True)
        
        if not df.empty:
            print(f"✓ Downloaded {len(df)} rows for {ticker}")
            return df
        else:
            print(f"✗ Empty data for {ticker}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"✗ Error for {ticker}: {e}")
        return pd.DataFrame()

def download_with_different_period(ticker):
    """Try different periods to get data."""
    periods = ['2y', '5y', '10y', 'max']
    
    for period in periods:
        try:
            print(f"  Trying period={period}...")
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0'})
            yf.set_tz_cache_location("tz_cache")
            
            ticker_obj = yf.Ticker(ticker, session=session)
            df = ticker_obj.history(period=period)
            
            if not df.empty:
                print(f"  ✓ Got {len(df)} rows with period={period}")
                # Filter to date range
                df = df[df.index >= '2015-01-01']
                if not df.empty:
                    return df
        except:
            continue
            
        time.sleep(random.uniform(3, 5))
    
    return pd.DataFrame()

# Main execution
tickers = ['TSLA', 'BND', 'SPY']
os.makedirs("data/processed", exist_ok=True)

print("Starting download with different approach...")
print("="*60)

data_dict = {}

for ticker in tickers:
    print(f"\nProcessing {ticker}...")
    
    # Try method 1: with specific date range
    df = download_with_session(ticker, '2015-01-01', '2026-06-30')
    
    # If that fails, try method 2: with period
    if df.empty:
        print(f"  Method 1 failed, trying period approach...")
        df = download_with_different_period(ticker)
    
    # Save if we got data
    if not df.empty:
        df.reset_index(inplace=True)
        filepath = f"data/processed/{ticker}_data.csv"
        df.to_csv(filepath, index=False)
        data_dict[ticker] = df
        print(f"✓ Saved {ticker} data: {len(df)} rows")
    else:
        print(f"✗ Failed to get data for {ticker}")
    
    # Wait between tickers
    if ticker != tickers[-1]:
        wait_time = random.uniform(10, 20)
        print(f"Waiting {wait_time:.1f} seconds...")
        time.sleep(wait_time)

print("\n" + "="*60)
print(f"Downloaded {len(data_dict)} of {len(tickers)} tickers:")
for ticker, df in data_dict.items():
    print(f"  ✓ {ticker}: {len(df)} rows")
print("="*60)
