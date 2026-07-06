"""
YFinance downloader with proper rate limiting and headers.
"""

import yfinance as yf
import pandas as pd
import time
import logging
from datetime import datetime
import random
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set custom headers to avoid 429 errors
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_with_rate_limit(ticker, start_date, end_date, max_retries=5):
    """
    Download data with exponential backoff and rate limiting.
    """
    retry_delay = 5  # Start with 5 seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Downloading {ticker} (attempt {attempt + 1}/{max_retries})")
            
            # Add random delay between requests
            time.sleep(random.uniform(2, 5))
            
            # Create ticker with custom session
            ticker_obj = yf.Ticker(ticker)
            
            # Try to get data with a shorter period first to test
            test_data = ticker_obj.history(period="1mo")
            if test_data.empty:
                logger.warning(f"No data for {ticker} on attempt {attempt + 1}")
                retry_delay *= 2
                time.sleep(retry_delay)
                continue
            
            # If test works, get full data
            df = ticker_obj.history(start=start_date, end=end_date)
            
            if not df.empty:
                logger.info(f"✓ Successfully downloaded {len(df)} rows for {ticker}")
                return df
            else:
                logger.warning(f"Empty data for {ticker} on attempt {attempt + 1}")
                
        except Exception as e:
            logger.warning(f"Error on attempt {attempt + 1} for {ticker}: {str(e)}")
            
        # Exponential backoff
        retry_delay *= 2
        logger.info(f"Waiting {retry_delay} seconds before retry...")
        time.sleep(retry_delay)
    
    return pd.DataFrame()

def download_all_tickers(tickers, start_date, end_date, save_dir="data/processed"):
    """Download all tickers with rate limiting."""
    import os
    os.makedirs(save_dir, exist_ok=True)
    
    data_dict = {}
    
    logger.info(f"Starting download for {len(tickers)} tickers...")
    logger.info(f"Period: {start_date} to {end_date}")
    logger.info("="*60)
    
    for ticker in tqdm(tickers, desc="Downloading"):
        try:
            df = download_with_rate_limit(ticker, start_date, end_date)
            
            if not df.empty:
                # Reset index and save
                df.reset_index(inplace=True)
                filepath = os.path.join(save_dir, f"{ticker}_data.csv")
                df.to_csv(filepath, index=False)
                data_dict[ticker] = df
                logger.info(f"✓ Saved {ticker} data to {filepath}")
            else:
                logger.error(f"✗ Failed to download {ticker} after all retries")
                
            # Add extra delay between different tickers
            if len(data_dict) < len(tickers):
                delay = random.uniform(3, 8)
                logger.info(f"Waiting {delay:.1f} seconds before next ticker...")
                time.sleep(delay)
                
        except Exception as e:
            logger.error(f"Unexpected error for {ticker}: {e}")
    
    return data_dict

def main():
    """Main execution with rate limiting."""
    
    # Parameters
    TICKERS = ['TSLA', 'BND', 'SPY']
    START_DATE = '2015-01-01'
    END_DATE = '2026-06-30'
    
    logger.info("="*60)
    logger.info("YFinance Data Download with Rate Limiting")
    logger.info("="*60)
    
    # Download data
    data_dict = download_all_tickers(TICKERS, START_DATE, END_DATE)
    
    if data_dict:
        logger.info("\n" + "="*60)
        logger.info(f"✓ Successfully downloaded {len(data_dict)} tickers:")
        for ticker, df in data_dict.items():
            logger.info(f"  - {ticker}: {len(df)} rows ({df['Date'].min()} to {df['Date'].max()})")
        logger.info("="*60)
    else:
        logger.error("✗ No data downloaded. Please try:")
        logger.error("  1. Wait 30 minutes (Yahoo Finance rate limit)")
        logger.error("  2. Try using a VPN")
        logger.error("  3. Try again tomorrow")
        logger.error("  4. Use an alternative data source")

if __name__ == "__main__":
    main()
