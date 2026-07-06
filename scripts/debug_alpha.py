"""
Debug Alpha Vantage API response.
"""

import requests
import pandas as pd

API_KEY = "O6MILG1S8ZV46LAB"

def test_alpha_vantage(ticker):
    """Test the API response and show what's being returned."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": API_KEY,
        "outputsize": "compact",  # Start with compact to test
        "datatype": "csv"
    }
    
    print(f"\nTesting {ticker}...")
    response = requests.get(url, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers.get('content-type')}")
    print(f"Response (first 500 chars):")
    print(response.text[:500])
    
    # Try to parse as CSV
    try:
        import io
        df = pd.read_csv(io.StringIO(response.text))
        print(f"\nParsed CSV - Columns: {list(df.columns)}")
        print(f"Parsed CSV - Shape: {df.shape}")
        print(df.head())
    except Exception as e:
        print(f"Error parsing CSV: {e}")
    
    return response.text

# Test with TSLA
test_alpha_vantage("TSLA")
