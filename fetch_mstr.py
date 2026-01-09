import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_mstr_data(start_date="2020-08-10", end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    ticker = yf.Ticker("MSTR")
    df = ticker.history(start=start_date, end=end_date)

    return df

def calculate_daily_returns(df, price_column="Close"):
    df = df.copy()
    df["Daily_Return"] = df[price_column].pct_change() * 100
    df = df.dropna(subset=['Daily_Return'])
    return df

def get_mstr_with_returns(start_date="2020-08-10", end_date=None):
    df = fetch_mstr_data(start_date, end_date)
    df = calculate_daily_returns(df)
    return df

if __name__ == "__main__":
    print("Fetching MSTR data from August 10, 2020 to present...")
    print("-" * 60)
    
    mstr_data = get_mstr_with_returns()
    
    print(f"Data range: {mstr_data.index[0].strftime('%Y-%m-%d')} to {mstr_data.index[-1].strftime('%Y-%m-%d')}")
    print(f"Total trading days: {len(mstr_data)}")
    print()
    print("First 5 rows:")
    print(mstr_data.head())
    print()
    print("Last 5 rows:")
    print(mstr_data.tail())