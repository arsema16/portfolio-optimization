# notebooks/01_complete_eda.ipynb
"""
Complete Task 1: Data Exploration and Analysis
With full error handling and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import logging
import warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*60)
print("TASK 1: COMPLETE DATA EXPLORATION")
print("="*60)

# 1. Load Data with Validation
def load_validate_data(filepath, ticker):
    """Load and validate data with error handling."""
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        
        # Validate
        if df.empty:
            raise ValueError(f"Empty data for {ticker}")
        required = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
            
        logger.info(f"✓ Loaded {ticker}: {len(df)} rows")
        return df
    except FileNotFoundError:
        logger.error(f"✗ File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"✗ Error loading {ticker}: {e}")
        raise

# Load all data
tickers = ['TSLA', 'BND', 'SPY']
data = {}
for ticker in tickers:
    try:
        data[ticker] = load_validate_data(f'../data/processed/{ticker}_data.csv', ticker)
    except Exception as e:
        logger.error(f"Skipping {ticker} due to error")

# 2. Calculate Returns and Metrics
def calculate_risk_metrics(returns, risk_free_rate=0.02):
    """Calculate VaR and Sharpe Ratio with validation."""
    if returns.empty:
        raise ValueError("Empty returns series")
    
    # Value at Risk (95%)
    var_parametric = returns.mean() - returns.std() * stats.norm.ppf(0.95)
    var_historical = np.percentile(returns, 5)
    
    # Sharpe Ratio
    excess_returns = returns - risk_free_rate / 252
    sharpe = np.sqrt(252) * excess_returns.mean() / returns.std() if returns.std() > 0 else 0
    
    return {
        'Parametric VaR (95%)': var_parametric,
        'Historical VaR (95%)': var_historical,
        'Sharpe Ratio': sharpe
    }

# Process each asset
processed_data = {}
risk_metrics = {}

for ticker, df in data.items():
    logger.info(f"\nProcessing {ticker}...")
    
    # Calculate returns
    df_copy = df.copy()
    df_copy['Daily_Return'] = df_copy['Close'].pct_change()
    df_copy['Log_Return'] = np.log(df_copy['Close'] / df_copy['Close'].shift(1))
    
    # Rolling metrics (30-day)
    df_copy['Rolling_Volatility'] = df_copy['Daily_Return'].rolling(30).std()
    df_copy['Rolling_Mean'] = df_copy['Close'].rolling(30).mean()
    df_copy['Rolling_Std'] = df_copy['Close'].rolling(30).std()
    
    processed_data[ticker] = df_copy
    
    # Calculate risk metrics
    returns = df_copy['Daily_Return'].dropna()
    risk_metrics[ticker] = calculate_risk_metrics(returns)
    
    print(f"  ✓ {ticker}: {len(df_copy)} rows processed")
    print(f"    Mean Return: {returns.mean():.6f}")
    print(f"    Std Return: {returns.std():.6f}")
    print(f"    VaR (95%): {risk_metrics[ticker]['Parametric VaR (95%)']:.4f}")

# 3. Stationarity Tests
def stationarity_test(series, series_name):
    """Perform ADF test with interpretation."""
    from statsmodels.tsa.stattools import adfuller
    
    try:
        result = adfuller(series.dropna())
        is_stationary = result[1] < 0.05
        
        return {
            'ADF Statistic': result[0],
            'p-value': result[1],
            'Critical Values': result[4],
            'Stationary': is_stationary
        }
    except Exception as e:
        logger.error(f"Stationarity test failed for {series_name}: {e}")
        return None

print("\n" + "="*60)
print("STATIONARITY TEST RESULTS")
print("="*60)

for ticker, df in processed_data.items():
    print(f"\n{ticker}:")
    # Test closing prices
    result = stationarity_test(df['Close'], f"{ticker}_Close")
    if result:
        print(f"  Closing Price: ADF={result['ADF Statistic']:.4f}, p={result['p-value']:.6f}, Stationary={result['Stationary']}")
    
    # Test returns
    result = stationarity_test(df['Daily_Return'], f"{ticker}_Returns")
    if result:
        print(f"  Daily Returns: ADF={result['ADF Statistic']:.4f}, p={result['p-value']:.6f}, Stationary={result['Stationary']}")

# 4. Visualizations with proper error handling
def safe_plot(plot_func, *args, **kwargs):
    """Safely create plots with error handling."""
    try:
        plot_func(*args, **kwargs)
        plt.show()
        return True
    except Exception as e:
        logger.error(f"Plot failed: {e}")
        return False

# Figure 1: Historical Prices
fig, axes = plt.subplots(3, 1, figsize=(15, 12))
fig.suptitle('Historical Closing Prices (2015-2026)', fontsize=16, fontweight='bold')

for idx, (ticker, df) in enumerate(processed_data.items()):
    ax = axes[idx]
    ax.plot(df.index, df['Close'], label=ticker, linewidth=2)
    ax.set_title(f'{ticker} - Closing Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Figure 2: Returns Distribution
fig, axes = plt.subplots(3, 1, figsize=(15, 12))
fig.suptitle('Daily Returns Distribution', fontsize=16, fontweight='bold')

for idx, (ticker, df) in enumerate(processed_data.items()):
    ax = axes[idx]
    returns = df['Daily_Return'].dropna()
    ax.hist(returns, bins=50, alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
    ax.axvline(x=returns.mean(), color='green', linestyle='-', linewidth=2, label='Mean')
    ax.set_title(f'{ticker} - Daily Returns')
    ax.set_xlabel('Daily Return')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    stats_text = f'Mean: {returns.mean():.6f}\nStd: {returns.std():.6f}\nSkew: {returns.skew():.3f}\nKurt: {returns.kurtosis():.3f}'
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("TASK 1 COMPLETE")
print("="*60)