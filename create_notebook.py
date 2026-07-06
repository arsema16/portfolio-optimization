import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Task 2: ARIMA Model for TSLA\n",
    "\n",
    "## Build and evaluate ARIMA model for Tesla stock price prediction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "from statsmodels.tsa.arima.model import ARIMA\n",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error\n",
    "\n",
    "plt.style.use('seaborn-v0_8-darkgrid')\n",
    "\n",
    "# Load TSLA data\n",
    "df = pd.read_csv('../data/processed/TSLA_data.csv', parse_dates=['Date'])\n",
    "df.set_index('Date', inplace=True)\n",
    "\n",
    "print(f'Loaded {len(df)} rows of TSLA data')\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use closing prices\n",
    "series = df['Close']\n",
    "\n",
    "# Split into train and test (chronological)\n",
    "train_size = int(len(series) * 0.8)\n",
    "train, test = series[:train_size], series[train_size:]\n",
    "\n",
    "print(f'Training set: {len(train)} rows')\n",
    "print(f'Test set: {len(test)} rows')\n",
    "print(f'Train period: {train.index.min()} to {train.index.max()}')\n",
    "print(f'Test period: {test.index.min()} to {test.index.max()}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Fit ARIMA model with (p,d,q) = (1,1,1)\n",
    "model = ARIMA(train, order=(1,1,1))\n",
    "fitted_model = model.fit()\n",
    "\n",
    "print(fitted_model.summary())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Generate predictions\n",
    "predictions = fitted_model.forecast(len(test))\n",
    "\n",
    "# Calculate metrics\n",
    "mae = mean_absolute_error(test, predictions)\n",
    "rmse = np.sqrt(mean_squared_error(test, predictions))\n",
    "mape = np.mean(np.abs((test - predictions) / test)) * 100\n",
    "\n",
    "print(f'ARIMA(1,1,1) Performance:')\n",
    "print(f'  MAE: ${mae:.2f}')\n",
    "print(f'  RMSE: ${rmse:.2f}')\n",
    "print(f'  MAPE: {mape:.2f}%')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot results\n",
    "fig, ax = plt.subplots(figsize=(14, 6))\n",
    "ax.plot(train.index, train, label='Training Data', linewidth=1, alpha=0.7)\n",
    "ax.plot(test.index, test, label='Actual Test Data', linewidth=2, color='blue')\n",
    "ax.plot(test.index, predictions, label='Predictions', linewidth=2, linestyle='--', color='red')\n",
    "ax.set_title('ARIMA(1,1,1) - Tesla Stock Price Prediction')\n",
    "ax.set_xlabel('Date')\n",
    "ax.set_ylabel('Price ($)')\n",
    "ax.legend()\n",
    "ax.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Try different ARIMA orders\n",
    "orders = [(1,1,1), (2,1,2), (3,1,2)]\n",
    "results = []\n",
    "\n",
    "for order in orders:\n",
    "    try:\n",
    "        model = ARIMA(train, order=order)\n",
    "        fitted = model.fit()\n",
    "        pred = fitted.forecast(len(test))\n",
    "        \n",
    "        mae = mean_absolute_error(test, pred)\n",
    "        rmse = np.sqrt(mean_squared_error(test, pred))\n",
    "        mape = np.mean(np.abs((test - pred) / test)) * 100\n",
    "        \n",
    "        results.append({\n",
    "            'order': order,\n",
    "            'MAE': mae,\n",
    "            'RMSE': rmse,\n",
    "            'MAPE': mape,\n",
    "            'AIC': fitted.aic\n",
    "        })\n",
    "        print(f'ARIMA{order}: MAE=${mae:.2f}, RMSE=${rmse:.2f}, MAPE={mape:.2f}%, AIC={fitted.aic:.2f}')\n",
    "    except:\n",
    "        print(f'ARIMA{order}: Failed to converge')\n",
    "\n",
    "# Find best model\n",
    "if results:\n",
    "    best = min(results, key=lambda x: x['RMSE'])\n",
    "    print(f'Best model: ARIMA{best[\"order\"]} with RMSE=${best[\"RMSE\"]:.2f}')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('notebooks/02_arima_model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print('Notebook created successfully!')
