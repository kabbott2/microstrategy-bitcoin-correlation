import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fetch_mstr import get_mstr_with_returns
from fetch_btc import get_btc_with_returns
from evaluate import merge_datasets


def filter_by_year(merged_data, year):
    """Filter merged data to a specific year."""
    return merged_data[pd.to_datetime(merged_data.index).year == year]


def calc_pearson(data):
    """Calculate Pearson correlation."""
    clean_data = data[["Daily_Return_BTC", "Daily_Return_MSTR"]].dropna()
    return clean_data["Daily_Return_MSTR"].corr(clean_data["Daily_Return_BTC"])


def calc_spearman(data):
    """Calculate Spearman correlation."""
    clean_data = data[["Daily_Return_BTC", "Daily_Return_MSTR"]].dropna()
    return clean_data["Daily_Return_MSTR"].corr(clean_data["Daily_Return_BTC"], method="spearman")


def calc_beta(data):
    """Calculate beta (regression slope)."""
    clean_data = data[["Daily_Return_BTC", "Daily_Return_MSTR"]].dropna()
    x = clean_data["Daily_Return_BTC"]
    y = clean_data["Daily_Return_MSTR"]
    slope, intercept = np.polyfit(x, y, 1)
    return slope


def analyze_all_years(merged_data, years):
    """
    Calculate Pearson, Spearman, and Beta for each year.
    
    Returns:
        pd.DataFrame: Statistics for each year
    """
    results = []
    
    for year in years:
        year_data = filter_by_year(merged_data, year)
        
        if len(year_data.dropna()) < 10:  # Skip years with insufficient data
            continue
            
        results.append({
            "Year": year,
            "Pearson": calc_pearson(year_data),
            "Spearman": calc_spearman(year_data),
            "Beta": calc_beta(year_data),
            "Trading Days": len(year_data.dropna())
        })
    
    return pd.DataFrame(results)


def plot_yearly_scatter(merged_data, years):
    """Create scatter plots with regression lines for each year."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, year in enumerate(years):
        if i >= len(axes):
            break
            
        year_data = filter_by_year(merged_data, year)
        clean_data = year_data[["Daily_Return_BTC", "Daily_Return_MSTR"]].dropna()
        
        if len(clean_data) < 10:
            continue
        
        x = clean_data["Daily_Return_BTC"]
        y = clean_data["Daily_Return_MSTR"]
        
        slope, intercept = np.polyfit(x, y, 1)
        pearson = calc_pearson(year_data)
        
        ax = axes[i]
        ax.scatter(x, y, alpha=0.4, edgecolors="none")
        ax.plot(x, slope * x + intercept, color="red", linewidth=2)
        ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
        ax.axvline(x=0, color="black", linestyle="-", linewidth=0.5)
        ax.set_xlabel("BTC Daily Return (%)")
        ax.set_ylabel("MSTR Daily Return (%)")
        ax.set_title(f"{year}\nPearson: {pearson:.2f}, Beta: {slope:.2f}")
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplot
    if len(years) < len(axes):
        axes[-1].axis("off")
    
    plt.suptitle("MSTR vs BTC Daily Returns by Year", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_yearly_trends(results_df):
    """Plot how Pearson, Spearman, and Beta change over the years."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    
    years = results_df["Year"].tolist()
    
    # Pearson over time
    axes[0].plot(results_df["Year"], results_df["Pearson"], marker="o", linewidth=2, color="blue")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Pearson Correlation")
    axes[0].set_title("Pearson Correlation by Year")
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1)
    axes[0].set_xticks(years)
    
    # Spearman over time
    axes[1].plot(results_df["Year"], results_df["Spearman"], marker="o", linewidth=2, color="green")
    axes[1].set_xlabel("Year")
    axes[1].set_ylabel("Spearman Correlation")
    axes[1].set_title("Spearman Correlation by Year")
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1)
    axes[1].set_xticks(years)
    
    # Beta over time
    axes[2].plot(results_df["Year"], results_df["Beta"], marker="o", linewidth=2, color="red")
    axes[2].set_xlabel("Year")
    axes[2].set_ylabel("Beta")
    axes[2].set_title("Beta by Year")
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xticks(years)
    
    plt.suptitle("MSTR vs BTC Relationship Over Time", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Fetching data...")
    mstr_data = get_mstr_with_returns()
    btc_data = get_btc_with_returns()
    
    print("Merging datasets...")
    merged_data = merge_datasets(mstr_data, btc_data)
    
    years = [2021, 2022, 2023, 2024, 2025]
    
    print("Analyzing by year...")
    results = analyze_all_years(merged_data, years)
    
    print("-" * 60)
    print("Yearly Statistics:")
    print("-" * 60)
    print(results.to_string(index=False))
    print("-" * 60)
    
    print("\nGenerating scatter plots by year...")
    plot_yearly_scatter(merged_data, years)
    
    print("Generating trend plots...")
    plot_yearly_trends(results)