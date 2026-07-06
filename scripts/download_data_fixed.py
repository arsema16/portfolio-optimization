"""
Improved data download script for fetching financial data from YFinance.
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging
import time
from tqdm import tqdm
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_connection():
    """Test internet connection and yfinance API."""
    try:
        requests.get('https://finance.yahoo.com', timeout=5)
        return True
    except:
        return False

def download_data_with_retry(ticker, start_date, end_date, max_retries=3, delay=2):
    """
    Download data with retry logic.
    
    Args:
        ticker (str): Ticker symbol
        start_date (str): Start date
        end_date (str): End date
        max_retries (int): Maximum number of retries
        delay (int): Delay between retries in seconds
    
    Returns:
        pd.DataFrame: Downloaded data
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1}/{max_retries} for {ticker}")
            
            # Create Ticker object
            stock = yf.Ticker(ticker)
            
            # Try to get info first to verify connection
            info = stock.info
            logger.info(f"✓ Successfully connected to {ticker}")
            
            # Download history
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                logger.warning(f"No data found for {ticker} on attempt {attempt + 1}")
                time.sleep(delay)
                continue
                
            logger.info(f"✓ Downloaded {len(df)} rows for {ticker}")
            return df
            
        except Exception as e:
            logger.warning(f"Error on attempt {attempt + 1}: {str(e)}")
            time.sleep(delay)
            
    return pd.DataFrame()

def download_data(tickers, start_date, end_date, save_dir="data/processed"):
    """
    Download historical data for multiple tickers.
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # Test connection first
    logger.info("Testing connection to Yahoo Finance...")
    if not test_connection():
        logger.error("No internet connection or Yahoo Finance is unreachable")
        logger.info("Please check your internet connection and try again")
        return {}
    
    data_dict = {}
    
    for ticker in tqdm(tickers, desc="Downloading data"):
        try:
            logger.info(f"Downloading data for {ticker}")
            
            # Download with retry
            df = download_data_with_retry(ticker, start_date, end_date)
            
            if df.empty:
                logger.warning(f"No data found for {ticker} after all retries")
                continue
            
            # Reset index to have Date as a column
            df.reset_index(inplace=True)
            
            # Save to CSV
            filepath = os.path.join(save_dir, f"{ticker}_data.csv")
            df.to_csv(filepath, index=False)
            
            data_dict[ticker] = df
            logger.info(f"✓ Successfully saved data for {ticker}: {len(df)} rows")
            
        except Exception as e:
            logger.error(f"Unexpected error for {ticker}: {str(e)}")
            continue
    
    return data_dict

def combine_data(data_dict, save_dir="data/processed"):
    """Combine individual ticker data into a single DataFrame."""
    if not data_dict:
        logger.warning("No data to combine")
        return pd.DataFrame()
    
    combined_dfs = []
    
    for ticker, df in data_dict.items():
        df_copy = df.copy()
        df_copy['Ticker'] = ticker
        combined_dfs.append(df_copy)
    
    combined_df = pd.concat(combined_dfs, ignore_index=True)
    
    # Save combined data
    filepath = os.path.join(save_dir, "combined_data.csv")
    combined_df.to_csv(filepath, index=False)
    
    logger.info(f"✓ Combined data saved: {len(combined_df)} rows")
    
    return combined_df

def main():
    """Main execution function."""
    
    # Parameters
    TICKERS = ['TSLA', 'BND', 'SPY']
    START_DATE = '2015-01-01'
    END_DATE = '2026-06-30'
    
    logger.info("="*60)
    logger.info("Starting data download process...")
    logger.info(f"Tickers: {TICKERS}")
    logger.info(f"Period: {START_DATE} to {END_DATE}")
    logger.info("="*60)
    
    # Download data
    data_dict = download_data(TICKERS, START_DATE, END_DATE)
    
    if data_dict:
        # Combine data
        combined_df = combine_data(data_dict)
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("Data Download Summary:")
        for ticker, df in data_dict.items():
            logger.info(f"✓ {ticker}: {len(df)} rows, {df['Date'].min()} to {df['Date'].max()}")
        logger.info("="*60)
        
        logger.info("✓ Data download completed successfully!")
        
        # Display first few rows
        if not combined_df.empty:
            logger.info("\nPreview of combined data:")
            print(combined_df[['Ticker', 'Date', 'Close']].head())
    else:
        logger.error("✗ No data downloaded. Please check:")
        logger.error("1. Your internet connection")
        logger.error("2. Yahoo Finance is accessible")
        logger.error("3. The ticker symbols are correct")
        logger.error("4. Try again later (Yahoo Finance may have rate limits)")

if __name__ == "__main__":
    main()
