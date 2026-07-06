"""
Data loading and management module.
"""

import pandas as pd
import yfinance as yf
from typing import Optional, List, Dict
import os

class DataLoader:
    """Class for loading and managing financial data."""
    
    def __init__(self, data_dir: str = "data/processed"):
        """
        Initialize DataLoader.
        
        Args:
            data_dir (str): Directory containing data files
        """
        self.data_dir = data_dir
        self.data = {}
        
    def load_from_csv(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Load data from CSV files.
        
        Args:
            tickers (List[str]): List of ticker symbols
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames
        """
        for ticker in tickers:
            filepath = os.path.join(self.data_dir, f"{ticker}_data.csv")
            if os.path.exists(filepath):
                df = pd.read_csv(filepath, parse_dates=['Date'])
                df.set_index('Date', inplace=True)
                self.data[ticker] = df
                
        return self.data
    
    def fetch_data(self, tickers: List[str], start: str, end: str) -> Dict[str, pd.DataFrame]:
        """
        Fetch data from YFinance API.
        
        Args:
            tickers (List[str]): List of ticker symbols
            start (str): Start date in 'YYYY-MM-DD' format
            end (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames
        """
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start, end=end)
            df.index = pd.to_datetime(df.index)
            self.data[ticker] = df
            
        return self.data
