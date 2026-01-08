"""
fetch_btc.py
Fetches Bitcoin (BTC-USD) price and volume data from Yahoo Finance.
Data starts August 11, 2020 - aligned with MSTR's first BTC acquisition.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

# Aligned with MSTR's BTC strategy start
START_DATE = "2020-08-11"
TICKER = "BTC-USD"


def fetch_btc_data(end_date: str = None) -> pd.DataFrame:
    """
    Fetch BTC historical data and compute derived metrics.
    
    Returns DataFrame with columns:
        - close: daily closing price
        - volume: daily trading volume (in USD)
        - daily_return: percentage change from previous day
        - cumulative_return: total return since start date
        - rolling_volatility: 30-day rolling standard deviation of returns
    """
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")
    
    # Pull raw data from yFinance
    btc = yf.Ticker(TICKER)
    df = btc.history(start=START_DATE, end=end_date)
    
    # Keep only what we need, rename for clarity
    df = df[["Close", "Volume"]].copy()
    df.columns = ["close", "volume"]
    
    # Daily returns as percentage
    df["daily_return"] = df["close"].pct_change() * 100
    
    # Cumulative return: how much $1 invested on day 1 is worth now
    df["cumulative_return"] = (1 + df["daily_return"] / 100).cumprod() - 1
    df["cumulative_return"] *= 100  # convert to percentage
    
    # 30-day rolling volatility (standard deviation of daily returns)
    df["rolling_volatility"] = df["daily_return"].rolling(window=30).std()
    
    # Clean up the index (BTC trades 24/7, so more data points than MSTR)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.index.name = "date"
    
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Quick summary statistics for the dataset."""
    return {
        "ticker": TICKER,
        "start_date": df.index.min().strftime("%Y-%m-%d"),
        "end_date": df.index.max().strftime("%Y-%m-%d"),
        "trading_days": len(df),
        "total_return_pct": df["cumulative_return"].iloc[-1],
        "avg_daily_return_pct": df["daily_return"].mean(),
        "avg_volatility": df["rolling_volatility"].mean(),
        "max_daily_gain_pct": df["daily_return"].max(),
        "max_daily_loss_pct": df["daily_return"].min(),
    }


if __name__ == "__main__":
    # Quick test
    data = fetch_btc_data()
    print(f"Fetched {len(data)} trading days of BTC data\n")
    print(data.tail())
    print("\nSummary:")
    for key, val in get_summary_stats(data).items():
        if isinstance(val, float):
            print(f"  {key}: {val:.2f}")
        else:
            print(f"  {key}: {val}")