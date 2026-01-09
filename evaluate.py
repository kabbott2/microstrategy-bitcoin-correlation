from fetch_mstr import get_mstr_with_returns
from fetch_btc import get_btc_with_returns
import pandas as pd
import matplotlib.pyplot as plt

mstr_data = get_mstr_with_returns()
btc_data = get_btc_with_returns()

# Merge datasets
def merge_datasets(mstr_df, btc_df):
    mstr_df = mstr_df.copy()
    btc_df = btc_df.copy()
    mstr_df.index = mstr_df.index.date
    btc_df.index = btc_df.index.date

    merged = mstr_df.merge(
        btc_df,
        left_index=True,
        right_index=True,
        how="inner",
        suffixes=("_MSTR", "_BTC"),
    )

    return merged

merged_data = merge_datasets(mstr_data, btc_data)
print(merged_data.head())

# Calculate correlation btwn MSTR and BTC daily returns
def calc_corr():
    return merged_data["Daily_Return_MSTR"].corr(merged_data["Daily_Return_BTC"])

correlation = calc_corr()
print(f"Correlation between MSTR and BTC daily returns: {correlation:.4f}")