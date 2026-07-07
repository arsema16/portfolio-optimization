
# Portfolio Optimization Challenge

## Week 9: Time Series Forecasting for Portfolio Management Optimization

### Overview
This project implements time series forecasting and portfolio optimization for GMF Investments, using historical financial data from YFinance. The solution demonstrates:
- Data extraction and preprocessing from financial APIs
- Exploratory Data Analysis (EDA) with visualizations
- Time series forecasting using ARIMA/SARIMA and LSTM models
- Portfolio optimization using Modern Portfolio Theory (MPT)
- Strategy backtesting and performance evaluation

### Project Structure
```
portfolio-optimization/
├── .github/workflows/ # CI/CD pipeline configuration
├── data/ # Data storage
│ └── processed/ # Processed datasets
├── notebooks/ # Jupyter notebooks for analysis
│ ├── 01_data_exploration.ipynb
│ ├── 02_arima_model.ipynb
│ ├── 03_forecasting.ipynb
│ ├── 04_portfolio_optimization.ipynb
│ └── 05_backtesting.ipynb
├── src/ # Source code
│ ├── data_loader.py # Data fetching and loading
│ ├── preprocess.py # Data cleaning and feature engineering
│ ├── models.py # Time series models
│ └── portfolio.py # Portfolio optimization
├── tests/ # Unit tests
├── scripts/ # Utility scripts
│ ├── download_data.py
│ └── generate_sample_data.py
├── requirements.txt # Production dependencies
├── requirements-ci.txt # CI/CD dependencies
└── README.md # Project documentation
```

### Installation

#### Prerequisites
- Python 3.10 or 3.11
- pip package manager

#### Setup
```bash
# Clone the repository
git clone https://github.com/arsema16/portfolio-optimization.git
cd portfolio-optimization

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-ci.txt
```
### Usage
#### 1. Download Data
```bash
# Using Yahoo Finance API (requires internet)
python scripts/download_data.py

# Or generate sample data (if API is unavailable)
python scripts/generate_sample_data.py
```
#### 2. Run Jupyter Notebooks
```bash
jupyter notebook
```
#### 3. Run Individual Tasks
```bash
# Task 1: Data Exploration
python run_task1.py

# Task 2: ARIMA Model
python run_task2.py
```
#### 4. Run Tests
```bash
pytest tests/ -v
```
### Features
#### Task 1: Data Preprocessing and Exploration
- Data extraction from financial APIs

- Handling missing values and data cleaning

- Exploratory Data Analysis (EDA) with visualizations

- Stationarity testing using Augmented Dickey-Fuller test

- Risk metrics: Value at Risk (VaR) and Sharpe Ratio

#### Task 2: Time Series Forecasting Models
- ARIMA/SARIMA model implementation

- LSTM deep learning model

- Model evaluation metrics (MAE, RMSE, MAPE)

- Parameter optimization using auto_arima

#### Task 3: Future Market Trends
- 6-12 month forecasting with confidence intervals

- Trend analysis and pattern identification

- Market opportunities and risk assessment

#### Task 4: Portfolio Optimization
- Modern Portfolio Theory (MPT) implementation

- Efficient frontier generation

- Maximum Sharpe Ratio and Minimum Volatility portfolios

#### Task 5: Strategy Backtesting
- Portfolio performance simulation

- Benchmark comparison

- Performance metrics: total return, Sharpe ratio, maximum drawdown

### Technical Stack
- Data Processing: pandas, numpy, scipy

- Visualization: matplotlib, seaborn, plotly

- Machine Learning: scikit-learn, tensorflow, keras

- Time Series: statsmodels, pmdarima

- Financial Analysis: yfinance, pyportfolioopt

- Testing: pytest, pytest-cov

- Code Quality: black, flake8, mypy

### CI/CD Pipeline
The project uses GitHub Actions for continuous integration:

- Python 3.10 and 3.11 testing

- Code linting with flake8

- Code formatting check with black

- Unit tests with pytest

- Code coverage reporting

### Contributing
- Fork the repository

- Create a feature branch (git checkout -b feature/amazing-feature)

- Commit your changes (git commit -m 'Add amazing feature')

- Push to the branch (git push origin feature/amazing-feature)

- Open a Pull Request
