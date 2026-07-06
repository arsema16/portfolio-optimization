"""
Data preprocessing and feature engineering module.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Optional, Tuple, List

class DataPreprocessor:
    """Class for preprocessing financial data."""
    
    def __init__(self):
        self.scalers = {}
        
    def calculate_returns(self, df: pd.DataFrame, price_col: str = 'Close') -> pd.DataFrame:
        """
        Calculate daily returns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            price_col (str): Column name for price data
            
        Returns:
            pd.DataFrame: DataFrame with returns added
        """
        df_copy = df.copy()
        df_copy['Daily_Return'] = df_copy[price_col].pct_change()
        df_copy['Log_Return'] = np.log(df_copy[price_col] / df_copy[price_col].shift(1))
        return df_copy
    
    def calculate_volatility(self, df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
        """
        Calculate rolling volatility.
        
        Args:
            df (pd.DataFrame): Input DataFrame with returns
            window (int): Rolling window size
            
        Returns:
            pd.DataFrame: DataFrame with volatility metrics
        """
        df_copy = df.copy()
        df_copy['Rolling_Volatility'] = df_copy['Daily_Return'].rolling(window=window).std()
        df_copy['Rolling_Mean'] = df_copy['Close'].rolling(window=window).mean()
        df_copy['Rolling_Std'] = df_copy['Close'].rolling(window=window).std()
        return df_copy
    
    def handle_missing_values(self, df: pd.DataFrame, method: str = 'forward_fill') -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            method (str): Method for handling missing values
            
        Returns:
            pd.DataFrame: DataFrame with missing values handled
        """
        df_copy = df.copy()
        
        if method == 'forward_fill':
            df_copy.fillna(method='ffill', inplace=True)
        elif method == 'backward_fill':
            df_copy.fillna(method='bfill', inplace=True)
        elif method == 'interpolate':
            df_copy.interpolate(method='time', inplace=True)
        elif method == 'drop':
            df_copy.dropna(inplace=True)
        
        # Fill any remaining NaN with 0
        df_copy.fillna(0, inplace=True)
        
        return df_copy
    
    def scale_data(self, df: pd.DataFrame, columns: List[str], method: str = 'standard') -> pd.DataFrame:
        """
        Scale data using specified method.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Columns to scale
            method (str): Scaling method ('standard' or 'minmax')
            
        Returns:
            pd.DataFrame: DataFrame with scaled data
        """
        df_copy = df.copy()
        
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        self.scalers[method] = scaler
        df_copy[columns] = scaler.fit_transform(df_copy[columns])
        
        return df_copy
    
    def detect_outliers(self, df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
        """
        Detect outliers using specified method.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            column (str): Column to analyze
            method (str): Method for outlier detection
            
        Returns:
            pd.Series: Boolean series indicating outliers
        """
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            outliers = z_scores > 3
            
        return outliers
