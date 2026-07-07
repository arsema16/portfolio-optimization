# src/data_loader.py - Complete with error handling
"""
Data loading module with comprehensive error handling.
"""

import pandas as pd
import yfinance as yf
import logging
from typing import Optional, List, Dict
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoader:
    """Robust data loader with validation and error handling."""
    
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = data_dir
        self.data = {}
        os.makedirs(data_dir, exist_ok=True)
    
    def validate_dataframe(self, df: pd.DataFrame, ticker: str) -> bool:
        """Validate downloaded data has required columns and non-empty."""
        try:
            if df is None or df.empty:
                logger.error(f"✗ Empty data for {ticker}")
                return False
            
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                logger.error(f"✗ Missing columns for {ticker}: {missing}")
                return False
            
            if len(df) < 100:  # Minimum threshold
                logger.warning(f"⚠️ Very few rows for {ticker}: {len(df)}")
            
            logger.info(f"✓ Validated {ticker}: {len(df)} rows")
            return True
            
        except Exception as e:
            logger.error(f"✗ Validation failed for {ticker}: {e}")
            return False
    
    def fetch_data(self, tickers: List[str], start: str, end: str, max_retries: int = 3) -> Dict[str, pd.DataFrame]:
        """Fetch data with retry logic and error handling."""
        for ticker in tickers:
            for attempt in range(max_retries):
                try:
                    logger.info(f"Fetching {ticker} (attempt {attempt+1}/{max_retries})...")
                    stock = yf.Ticker(ticker)
                    df = stock.history(start=start, end=end)
                    
                    if self.validate_dataframe(df, ticker):
                        df.index = pd.to_datetime(df.index)
                        self.data[ticker] = df
                        logger.info(f"✓ Successfully fetched {ticker}")
                        break
                    else:
                        logger.warning(f"⚠️ Attempt {attempt+1} failed for {ticker}")
                        
                except Exception as e:
                    logger.error(f"✗ Error fetching {ticker}: {e}")
                    
                if attempt == max_retries - 1:
                    logger.error(f"✗ All retries exhausted for {ticker}")
                    self.data[ticker] = pd.DataFrame()  # Empty DataFrame as placeholder
        
        return self.data