import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_btc_data(start_date="2020-08-10", end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    ticker = yf.Ticker("BTC-USD")
    df = ticker.history(start=start_date, end=end_date)

    return df

def filter_weekends(df):
    df = df.copy()
    df = df[df.index.dayofweek < 5]  # Keep only weekdays (0-4)
    return df

def calculate_daily_returns(df, price_column="Close"):
    df = df.copy()
    df["Daily_Return"] = df[price_column].pct_change() * 100
    df = df.dropna(subset=['Daily_Return'])
    return df

def get_btc_with_returns(start_date="2020-08-10", end_date=None, filter_weekends_flag=True):
    df = fetch_btc_data(start_date, end_date)
    if filter_weekends_flag:
        df = filter_weekends(df)
    df = calculate_daily_returns(df)
    return df

if __name__ == "__main__":
    print("Fetching Bitcoin data from August 10, 2020 to present...")
    print("(Weekends filtered out to match MSTR trading days)")
    print("-" * 60)
    
    btc_data = get_btc_with_returns()
    
    print(f"Data range: {btc_data.index[0].strftime('%Y-%m-%d')} to {btc_data.index[-1].strftime('%Y-%m-%d')}")
    print(f"Total trading days (weekdays only): {len(btc_data)}")
    print()
    print("First 5 rows:")
    print(btc_data.head())
    print()
    print("Last 5 rows:")
    print(btc_data.tail())