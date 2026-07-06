"""
Create realistic sample data for development.
This generates data that mimics TSLA, BND, and SPY behavior.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_asset_data(ticker, start_date, end_date, params):
    """
    Generate realistic price data for an asset.
    """
    # Create date range (business days only)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    n = len(dates)
    
    # Set seed for reproducibility
    np.random.seed(params['seed'])
    
    # Generate returns with characteristics
    returns = np.random.normal(params['drift'], params['volatility'], n)
    
    # Add some autocorrelation for realism
    for i in range(1, n):
        returns[i] = params['autocorr'] * returns[i-1] + (1 - params['autocorr']) * returns[i]
    
    # Add occasional large moves (market shocks)
    shock_indices = np.random.choice(n, size=int(n * 0.01), replace=False)
    returns[shock_indices] += np.random.normal(0, params['volatility'] * 2, len(shock_indices))
    
    # Calculate prices
    prices = params['start_price'] * np.exp(np.cumsum(returns))
    
    # Create OHLC data
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices * (1 + np.random.normal(0, 0.002, n)),
        'High': prices * (1 + np.abs(np.random.normal(0.01, 0.005, n))),
        'Low': prices * (1 - np.abs(np.random.normal(0.01, 0.005, n))),
        'Close': prices,
        'Adj Close': prices,
        'Volume': np.random.randint(1000000, 50000000, n)
    })
    
    # Ensure High is highest and Low is lowest
    df['High'] = df[['Open', 'High', 'Close']].max(axis=1)
    df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1)
    
    return df

# Asset parameters
asset_params = {
    'TSLA': {
        'seed': 42,
        'start_price': 50,
        'drift': 0.0006,  # High growth
        'volatility': 0.03,  # High volatility
        'autocorr': 0.3
    },
    'BND': {
        'seed': 43,
        'start_price': 85,
        'drift': 0.00005,  # Low growth
        'volatility': 0.005,  # Low volatility
        'autocorr': 0.4
    },
    'SPY': {
        'seed': 44,
        'start_price': 200,
        'drift': 0.0002,  # Moderate growth
        'volatility': 0.015,  # Moderate volatility
        'autocorr': 0.35
    }
}

# Generate data
tickers = ['TSLA', 'BND', 'SPY']
start_date = '2015-01-01'
end_date = '2026-06-30'

os.makedirs("data/processed", exist_ok=True)

print("="*60)
print("GENERATING SAMPLE DATA")
print("="*60)

for ticker in tickers:
    params = asset_params[ticker]
    df = generate_asset_data(ticker, start_date, end_date, params)
    filepath = f"data/processed/{ticker}_data.csv"
    df.to_csv(filepath, index=False)
    
    print(f"✓ Generated {ticker}:")
    print(f"  Rows: {len(df)}")
    print(f"  Price range: ${df['Close'].min():.2f} to ${df['Close'].max():.2f}")
    print(f"  Saved to: {filepath}")

print("\n" + "="*60)
print("✓ Sample data created successfully!")
print("\nNOTE: This is SIMULATED data for development purposes.")
print("You can use this to complete all tasks.")
print("="*60)

# Show sample
print("\nSample of TSLA data:")
df = pd.read_csv("data/processed/TSLA_data.csv")
print(df.head())
