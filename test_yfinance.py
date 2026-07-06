import yfinance as yf
import pandas as pd
import time

print("Testing YFinance connection...")

# Test with a simple ticker
try:
    # Try to get TSLA data with a shorter period
    tsla = yf.Ticker("TSLA")
    print("✓ Created Ticker object")
    
    # Try to get info
    info = tsla.info
    print(f"✓ Got info for TSLA: {info.get('longName', 'N/A')}")
    
    # Try to get recent data
    df = tsla.history(period="5d")
    print(f"✓ Downloaded {len(df)} rows of recent data")
    print(df.head())
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check your internet connection")
    print("2. Try running: pip install --upgrade yfinance")
    print("3. Try using a VPN if in a restricted region")
    print("4. Wait a few minutes and try again (rate limiting)")
