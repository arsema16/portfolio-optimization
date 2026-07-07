import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

# Load data
df = pd.read_csv('data/processed/TSLA_data.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

print('='*60)
print('TASK 1: DATA EXPLORATION - TSLA')
print('='*60)
print(f'Loaded {len(df)} rows')
print(f'Period: {df.index.min()} to {df.index.max()}')

# Basic statistics
print('\n Basic Statistics:')
print(df[['Open', 'High', 'Low', 'Close', 'Volume']].describe())

# Calculate returns
df['Return'] = df['Close'].pct_change()
df['Volatility'] = df['Return'].rolling(30).std()

print(f'\n Daily Returns:')
print(f'  Mean: {df["Return"].mean():.6f}')
print(f'  Std: {df["Return"].std():.6f}')
print(f'  Skew: {df["Return"].skew():.6f}')
print(f'  Kurtosis: {df["Return"].kurtosis():.6f}')

# Stationarity tests
result_price = adfuller(df['Close'].dropna())
print(f'\n Stationarity Test (Closing Price):')
print(f'  ADF Statistic: {result_price[0]:.4f}')
print(f'  p-value: {result_price[1]:.6f}')
print(f'  Stationary: {"Yes" if result_price[1] < 0.05 else "No"}')

result_returns = adfuller(df['Return'].dropna())
print(f'\n Stationarity Test (Returns):')
print(f'  ADF Statistic: {result_returns[0]:.4f}')
print(f'  p-value: {result_returns[1]:.6f}')
print(f'  Stationary: {"Yes" if result_returns[1] < 0.05 else "No"}')

print('\n Task 1 completed successfully!')
