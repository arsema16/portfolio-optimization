"""
Download data from Stooq - FREE, NO API KEY REQUIRED, ALWAYS WORKS.
Stooq is a reliable financial data provider that doesn't block requests.
"""

import pandas as pd
import pandas_datareader.data as web
import datetime
import os
import time

def download_from_stooq(ticker, start_date, end_date):
    """
    Download data from Stooq.
    Stooq format: TICKER.US for US stocks
    """
    try:
        # Format for Stooq
        stooq_ticker = f"{ticker}.US"
        print(f"Downloading {ticker} from Stooq...")
        
        # Download data
        df = web.DataReader(stooq_ticker, "stooq", start_date, end_date)
        
        if df.empty:
            print(f"✗ No data found for {ticker}")
            return None
        
        # Reset index to have Date as column
        df.reset_index(inplace=True)
        
        print(f"✓ Downloaded {len(df)} rows for {ticker}")
        print(f"  Period: {df['Date'].min()} to {df['Date'].max()}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error for {ticker}: {e}")
        return None

def save_data(ticker, df):
    """Save data to CSV."""
    os.makedirs("data/processed", exist_ok=True)
    filepath = f"data/processed/{ticker}_data.csv"
    df.to_csv(filepath, index=False)
    print(f"✓ Saved to {filepath}")
    return filepath

def main():
    """Main execution."""
    # Date range
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2026, 6, 30)
    
    # Tickers
    tickers = ["TSLA", "BND", "SPY"]
    
    print("="*60)
    print("STOOQ DATA DOWNLOADER")
    print("="*60)
    print(f"Period: {start.date()} to {end.date()}")
    print(f"Tickers: {tickers}")
    print("="*60)
    
    data_dict = {}
    
    for ticker in tickers:
        df = download_from_stooq(ticker, start, end)
        
        if df is not None and not df.empty:
            # Save the data
            save_data(ticker, df)
            data_dict[ticker] = df
        else:
            print(f"✗ Failed to download {ticker}")
        
        # Small delay to be respectful
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    if data_dict:
        print(f"✓ SUCCESS! Downloaded {len(data_dict)} tickers:")
        for ticker, df in data_dict.items():
            print(f"  - {ticker}: {len(df)} rows")
        print("\nData saved to: data/processed/")
        print("\nYou can now run the Jupyter notebook!")
    else:
        print("✗ No data downloaded. Please check your internet connection.")
    print("="*60)

if __name__ == "__main__":
    main()
