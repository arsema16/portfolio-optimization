"""
Time series forecasting models.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesModels:
    """Class for building and evaluating time series models."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def check_stationarity(self, series: pd.Series, significance_level: float = 0.05) -> Dict[str, Any]:
        """
        Perform Augmented Dickey-Fuller test for stationarity.
        
        Args:
            series (pd.Series): Time series data
            significance_level (float): Significance level for test
            
        Returns:
            Dict[str, Any]: Test results
        """
        result = adfuller(series.dropna())
        
        return {
            'statistic': result[0],
            'p_value': result[1],
            'critical_values': result[4],
            'is_stationary': result[1] < significance_level
        }
    
    def fit_arima(self, train_data: pd.Series, order: Tuple[int, int, int]) -> ARIMA:
        """
        Fit ARIMA model.
        
        Args:
            train_data (pd.Series): Training data
            order (Tuple[int, int, int]): (p, d, q) parameters
            
        Returns:
            ARIMA: Fitted ARIMA model
        """
        model = ARIMA(train_data, order=order)
        fitted_model = model.fit()
        self.models['arima'] = fitted_model
        return fitted_model
    
    def fit_sarima(self, train_data: pd.Series, order: Tuple[int, int, int], 
                   seasonal_order: Tuple[int, int, int, int]) -> SARIMAX:
        """
        Fit SARIMA model.
        
        Args:
            train_data (pd.Series): Training data
            order (Tuple[int, int, int]): (p, d, q) parameters
            seasonal_order (Tuple[int, int, int, int]): (P, D, Q, m) parameters
            
        Returns:
            SARIMAX: Fitted SARIMA model
        """
        model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
        fitted_model = model.fit(disp=False)
        self.models['sarima'] = fitted_model
        return fitted_model
    
    def auto_arima_optimize(self, train_data: pd.Series, max_p: int = 5, 
                           max_q: int = 5, seasonal: bool = False) -> Dict[str, Any]:
        """
        Automatically find optimal ARIMA/SARIMA parameters.
        
        Args:
            train_data (pd.Series): Training data
            max_p (int): Maximum p value
            max_q (int): Maximum q value
            seasonal (bool): Whether to search for seasonal parameters
            
        Returns:
            Dict[str, Any]: Model and parameters
        """
        if seasonal:
            model = auto_arima(train_data, max_p=max_p, max_q=max_q, seasonal=True, 
                               trace=True, error_action='ignore', suppress_warnings=True)
        else:
            model = auto_arima(train_data, max_p=max_p, max_q=max_q, seasonal=False,
                               trace=True, error_action='ignore', suppress_warnings=True)
        
        self.models['auto_arima'] = model
        return {
            'model': model,
            'order': model.order,
            'seasonal_order': model.seasonal_order if seasonal else None
        }
    
    def build_lstm(self, input_shape: Tuple[int, int], units: int = 50, 
                   dropout_rate: float = 0.2, learning_rate: float = 0.001) -> tf.keras.Model:
        """
        Build LSTM model.
        
        Args:
            input_shape (Tuple[int, int]): Input shape (timesteps, features)
            units (int): Number of LSTM units
            dropout_rate (float): Dropout rate
            learning_rate (float): Learning rate
            
        Returns:
            tf.keras.Model: LSTM model
        """
        model = Sequential([
            LSTM(units, return_sequences=True, input_shape=input_shape),
            Dropout(dropout_rate),
            LSTM(units // 2, return_sequences=False),
            Dropout(dropout_rate),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mse')
        self.models['lstm'] = model
        return model
    
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate model evaluation metrics.
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            
        Returns:
            Dict[str, float]: Evaluation metrics
        """
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }
