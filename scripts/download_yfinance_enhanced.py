"""
YFinance download with proper error handling and different approach.
"""

import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime

def download_yfinance(ticker, start_date, end_date):
    """
    Download data using yfinance with multiple attempts.
    """
    print(f"Downloading {ticker}...")
    
    # Try different approaches
    approaches = [
        # Approach 1: Standard download
        lambda: yf.download(ticker, start=start_date, end=end_date, progress=False),
        
        # Approach 2: Using Ticker object
        lambda: yf.Ticker(ticker).history(start=start_date, end=end_date),
        
        # Approach 3: Using period
        lambda: yf.download(ticker, period="10y", progress=False),
        
        # Approach 4: Using max period
        lambda: yf.download(ticker, period="max", progress=False)
    ]
    
    for i, approach in enumerate(approaches, 1):
        try:
            print(f"  Attempt {i}...")
            df = approach()
            
            if df is not None and not df.empty:
                print(f"  ✓ Got {len(df)} rows")
                
                # If we got data with period, filter to date range
                if i >= 3:
                    df = df[(df.index >= start_date) & (df.index <= end_date)]
                    print(f"  ✓ Filtered to {len(df)} rows in date range")
                
                return df
                
        except Exception as e:
            print(f"  ✗ Attempt {i} failed: {str(e)[:50]}")
            continue
        
        time.sleep(2)  # Wait between attempts
    
    return pd.DataFrame()

def main():
    """Main execution."""
    tickers = ["TSLA", "BND", "SPY"]
    start_date = "2015-01-01"
    end_date = "2026-06-30"
    
    print("="*60)
    print("YFINANCE DATA DOWNLOADER")
    print("="*60)
    print(f"Period: {start_date} to {end_date}")
    print(f"Tickers: {tickers}")
    print("="*60)
    
    os.makedirs("data/processed", exist_ok=True)
    data_dict = {}
    
    for ticker in tickers:
        print(f"\nProcessing {ticker}...")
        df = download_yfinance(ticker, start_date, end_date)
        
        if not df.empty:
            # Reset index and save
            df.reset_index(inplace=True)
            df.to_csv(f"data/processed/{ticker}_data.csv", index=False)
            data_dict[ticker] = df
            print(f"✓ Saved {ticker}: {len(df)} rows")
        else:
            print(f"✗ Failed to download {ticker}")
        
        # Wait between tickers
        if ticker != tickers[-1]:
            print("Waiting 5 seconds...")
            time.sleep(5)
    
    # Summary
    print("\n" + "="*60)
    if data_dict:
        print(f"✓ Successfully downloaded {len(data_dict)} tickers:")
        for ticker, df in data_dict.items():
            print(f"  - {ticker}: {len(df)} rows")
        print("\nData saved to: data/processed/")
    else:
        print("✗ No data downloaded. Please check your internet connection.")
        print("\nIf this continues, try the manual download method.")
    print("="*60)

if __name__ == "__main__":
    main()
