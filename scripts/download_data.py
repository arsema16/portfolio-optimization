"""
Data download script for fetching financial data from YFinance.
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_data(tickers, start_date, end_date, save_dir="data/processed"):
    """
    Download historical data for multiple tickers.
    
    Args:
        tickers (list): List of ticker symbols
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        save_dir (str): Directory to save data
    
    Returns:
        dict: Dictionary of DataFrames for each ticker
    """
    os.makedirs(save_dir, exist_ok=True)
    
    data_dict = {}
    
    for ticker in tqdm(tickers, desc="Downloading data"):
        try:
            logger.info(f"Downloading data for {ticker}")
            
            # Download data
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                logger.warning(f"No data found for {ticker}")
                continue
            
            # Reset index to have Date as a column
            df.reset_index(inplace=True)
            
            # Save to CSV
            filepath = os.path.join(save_dir, f"{ticker}_data.csv")
            df.to_csv(filepath, index=False)
            
            data_dict[ticker] = df
            logger.info(f"Successfully saved data for {ticker}: {len(df)} rows")
            
        except Exception as e:
            logger.error(f"Error downloading data for {ticker}: {str(e)}")
            continue
    
    return data_dict

def combine_data(data_dict, save_dir="data/processed"):
    """
    Combine individual ticker data into a single DataFrame.
    
    Args:
        data_dict (dict): Dictionary of DataFrames for each ticker
        save_dir (str): Directory to save combined data
    
    Returns:
        pd.DataFrame: Combined DataFrame with MultiIndex columns
    """
    combined_dfs = []
    
    for ticker, df in data_dict.items():
        df_copy = df.copy()
        df_copy['Ticker'] = ticker
        combined_dfs.append(df_copy)
    
    combined_df = pd.concat(combined_dfs, ignore_index=True)
    
    # Save combined data
    filepath = os.path.join(save_dir, "combined_data.csv")
    combined_df.to_csv(filepath, index=False)
    
    logger.info(f"Combined data saved: {len(combined_df)} rows")
    
    return combined_df

def main():
    """Main execution function."""
    
    # Parameters
    TICKERS = ['TSLA', 'BND', 'SPY']
    START_DATE = '2015-01-01'
    END_DATE = '2026-06-30'
    
    logger.info("Starting data download process...")
    logger.info(f"Tickers: {TICKERS}")
    logger.info(f"Period: {START_DATE} to {END_DATE}")
    
    # Download data
    data_dict = download_data(TICKERS, START_DATE, END_DATE)
    
    if data_dict:
        # Combine data
        combined_df = combine_data(data_dict)
        
        # Print summary
        logger.info("\n" + "="*50)
        logger.info("Data Download Summary:")
        for ticker, df in data_dict.items():
            logger.info(f"{ticker}: {len(df)} rows, {df['Date'].min()} to {df['Date'].max()}")
        logger.info("="*50)
        
        logger.info("Data download completed successfully!")
    else:
        logger.error("No data downloaded. Check your internet connection and ticker symbols.")

if __name__ == "__main__":
    main()
