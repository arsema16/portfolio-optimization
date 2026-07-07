import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

print('='*60)
print('TASK 2: ARIMA MODEL RESULTS')
print('='*60)

# Load data
df = pd.read_csv('data/processed/TSLA_data.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

series = df['Close']
train_size = int(len(series) * 0.8)
train, test = series[:train_size], series[train_size:]

print(f'Training: {len(train)} rows, Test: {len(test)} rows')
print(f'Train: {train.index.min()} to {train.index.max()}')
print(f'Test: {test.index.min()} to {test.index.max()}')
print()

# Try different orders
orders = [(1,1,1), (2,1,2), (3,1,2)]
results = []

print('Model Performance:')
print('-'*60)

for order in orders:
    try:
        model = ARIMA(train, order=order)
        fitted = model.fit()
        pred = fitted.forecast(len(test))
        
        mae = mean_absolute_error(test, pred)
        rmse = np.sqrt(mean_squared_error(test, pred))
        mape = np.mean(np.abs((test - pred) / test)) * 100
        
        results.append({
            'order': order,
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'AIC': fitted.aic
        })
        print(f'ARIMA{order}: MAE=${mae:.2f}, RMSE=${rmse:.2f}, MAPE={mape:.2f}%, AIC={fitted.aic:.2f}')
    except Exception as e:
        print(f'ARIMA{order}: Failed')

# Find best model
if results:
    best = min(results, key=lambda x: x['RMSE'])
    print()
    print('-'*60)
    print(f'Best Model: ARIMA{best["order"]}')
    print(f'  RMSE: ${best["RMSE"]:.2f}')
    print(f'  MAE: ${best["MAE"]:.2f}')
    print(f'  MAPE: {best["MAPE"]:.2f}%')
    print(f'  AIC: {best["AIC"]:.2f}')
    print('-'*60)

print('\n Task 2 completed successfully!')
