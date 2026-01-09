import matplotlib.pyplot as plt
import numpy as np
from fetch_mstr import get_mstr_with_returns
from fetch_btc import get_btc_with_returns
from evaluate import merge_datasets

def calc_pearson(merged_data):
    return merged_data["Daily_Return_MSTR"].corr(merged_data["Daily_Return_BTC"])

def calc_spearman(merged_data):
    return merged_data["Daily_Return_MSTR"].corr(merged_data["Daily_Return_BTC"], method='spearman')

def calc_regression(merged_data):
    x = merged_data["Daily_Return_BTC"]
    y = merged_data["Daily_Return_MSTR"]

    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

def plot_correlation(merged_data):
    pearson = calc_pearson(merged_data)
    spearman = calc_spearman(merged_data)
    slope, intercept = calc_regression(merged_data)

    clean_data = merged_data[["Daily_Return_BTC", "Daily_Return_MSTR"]].dropna()
    x = clean_data["Daily_Return_BTC"]
    y = clean_data["Daily_Return_MSTR"]

    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.scatter(x, y, alpha=0.4, edgecolors="none")
    ax.plot(x, slope * x + intercept, color="red", linewidth=2, label=f"y = {slope:.2f}x + {intercept:.2f}")
    
    ax.set_xlabel("BTC Daily Return (%)")
    ax.set_ylabel("MSTR Daily Return (%)")
    ax.set_title("MSTR vs BTC Daily Returns Correlation")
    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add statistics text box
    stats_text = f"Pearson: {pearson:.3f}\nSpearman: {spearman:.3f}\nBeta: {slope:.2f}"
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, fontsize=11,
            verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Fetching data...")
    mstr_data = get_mstr_with_returns()
    btc_data = get_btc_with_returns()
    
    print("Merging datasets...")
    merged_data = merge_datasets(mstr_data, btc_data)
    
    print("Calculating correlations...")
    pearson = calc_pearson(merged_data)
    spearman = calc_spearman(merged_data)
    slope, intercept = calc_regression(merged_data)
    
    print("-" * 60)
    print(f"Pearson correlation:  {pearson:.4f}")
    print(f"Spearman correlation: {spearman:.4f}")
    print(f"Beta (slope):         {slope:.4f}")
    print(f"Intercept:            {intercept:.4f}")
    print()
    print(f"Interpretation: For every 1% BTC moves, MSTR moves ~{slope:.2f}%")
    print("-" * 60)
    
    print("Generating scatter plot...")
    plot_correlation(merged_data)