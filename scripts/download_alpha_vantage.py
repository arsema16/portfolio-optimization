"""
Download historical data from Alpha Vantage using API key.
"""

import requests
import pandas as pd
import os
import time
from datetime import datetime

# Your Alpha Vantage API key
API_KEY = "O6MILG1S8ZV46LAB"

def download_alpha_vantage(ticker, api_key, outputsize="full"):
    """
    Download historical data from Alpha Vantage.
    
    Args:
        ticker (str): Ticker symbol (e.g., TSLA)
        api_key (str): Alpha Vantage API key
        outputsize (str): "full" for full history, "compact" for last 100 days
    
    Returns:
        pd.DataFrame: Downloaded data
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key,
        "outputsize": outputsize,
        "datatype": "csv"
    }
    
    try:
        print(f"Downloading {ticker} from Alpha Vantage...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Save the CSV content to a file
            os.makedirs("data/processed", exist_ok=True)
            filepath = f"data/processed/{ticker}_data.csv"
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            # Read it back to verify
            df = pd.read_csv(filepath)
            print(f"✓ Downloaded {len(df)} rows for {ticker}")
            print(f"  Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            return df
        else:
            print(f"✗ Error downloading {ticker}: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def download_all_tickers(tickers, api_key):
    """
    Download data for multiple tickers with rate limiting.
    Alpha Vantage free tier: 5 requests per minute.
    """
    data_dict = {}
    
    for i, ticker in enumerate(tickers):
        print(f"\n[{i+1}/{len(tickers)}] Processing {ticker}...")
        
        df = download_alpha_vantage(ticker, api_key)
        
        if df is not None:
            # Filter to our date range (2015-01-01 to 2026-06-30)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df[(df['timestamp'] >= '2015-01-01') & (df['timestamp'] <= '2026-06-30')]
            
            if not df.empty:
                # Rename columns to match Yahoo Finance format
                df.rename(columns={
                    'timestamp': 'Date',
                    'open': 'Open',
                    'high': 'High',
                    'low': 'Low',
                    'close': 'Close',
                    'adjusted_close': 'Adj Close',
                    'volume': 'Volume'
                }, inplace=True)
                
                # Save filtered data
                filepath = f"data/processed/{ticker}_data.csv"
                df.to_csv(filepath, index=False)
                data_dict[ticker] = df
                print(f"✓ Filtered data saved: {len(df)} rows ({df['Date'].min()} to {df['Date'].max()})")
            else:
                print(f"✗ No data in date range for {ticker}")
        else:
            print(f"✗ Failed to download {ticker}")
        
        # Rate limiting: wait 12 seconds between requests (5 per minute)
        if i < len(tickers) - 1:
            print(f"  Waiting 12 seconds before next request...")
            time.sleep(12)
    
    return data_dict

# Main execution
if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    
    print("="*60)
    print("Alpha Vantage Data Download")
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
        print("✗ No data downloaded. Please check your API key and try again.")
    print("="*60)
