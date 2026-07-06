"""
Download from Alpha Vantage using free endpoints.
"""

import requests
import pandas as pd
import os
import time
import json

API_KEY = "O6MILG1S8ZV46LAB"

def download_alpha_vantage_free(ticker, api_key):
    """
    Download data using the free TIME_SERIES_DAILY endpoint.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # This is the free endpoint
        "symbol": ticker,
        "apikey": api_key,
        "outputsize": "full"
    }
    
    print(f"Downloading {ticker} from Alpha Vantage (free endpoint)...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"✗ HTTP Error: {response.status_code}")
        return None
    
    data = response.json()
    
    # Check for error messages
    if "Error Message" in data:
        print(f"✗ API Error: {data['Error Message']}")
        return None
    
    if "Note" in data:
        print(f"✗ API Note: {data['Note']}")
        print(f"  {data['Note']}")
        return None
    
    # Extract time series data
    time_series_key = "Time Series (Daily)"
    if time_series_key not in data:
        print(f"✗ No time series data found. Keys: {list(data.keys())}")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data[time_series_key], orient="index")
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    
    # Rename columns
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Filter to date range
    df = df[(df.index >= '2015-01-01') & (df.index <= '2026-06-30')]
    
    print(f"✓ Downloaded {len(df)} rows for {ticker}")
    print(f"  Date range: {df.index.min()} to {df.index.max()}")
    
    return df

def download_all_tickers(tickers, api_key):
    """Download all tickers with rate limiting."""
    data_dict = {}
    
    for i, ticker in enumerate(tickers):
        print(f"\n[{i+1}/{len(tickers)}] Processing {ticker}...")
        
        df = download_alpha_vantage_free(ticker, api_key)
        
        if df is not None and not df.empty:
            # Save to CSV
            os.makedirs("data/processed", exist_ok=True)
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Date'}, inplace=True)
            filepath = f"data/processed/{ticker}_data.csv"
            df.to_csv(filepath, index=False)
            data_dict[ticker] = df
            print(f"✓ Saved to {filepath}")
        else:
            print(f"✗ Failed to download {ticker}")
        
        # Rate limiting: 12 seconds between requests
        if i < len(tickers) - 1:
            print(f"  Waiting 12 seconds...")
            time.sleep(12)
    
    return data_dict

# Main
if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    
    print("="*60)
    print("Alpha Vantage Data Download (Free Endpoint)")
    print("="*60)
    print(f"API Key: {API_KEY[:8]}...")
    print(f"Tickers: {tickers}")
    print("="*60)
    
    data = download_all_tickers(tickers, API_KEY)
    
    print("\n" + "="*60)
    if data:
        print(f"✓ Successfully downloaded {len(data)} tickers:")
        for ticker, df in data.items():
            print(f"  - {ticker}: {len(df)} rows")
        print("\nData saved to: data/processed/")
    else:
        print("✗ No data downloaded. Trying Stooq as fallback...")
        print("\nRunning Stooq download...")
        os.system("python scripts/download_stooq.py")
    print("="*60)
