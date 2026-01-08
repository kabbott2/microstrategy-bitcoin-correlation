import matplotlib.pyplot as plt
import pandas as pd
from fetch_mstr import fetch_mstr_data
from fetch_btc import fetch_btc_data

# Rolling window for beta and covariance calculations
# 60 days balances responsiveness with noise reduction
ROLLING_WINDOW = 60


def align_dataframes(mstr_df: pd.DataFrame, btc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge MSTR and BTC data on common dates.
    MSTR only trades on market days, so we align to its schedule.
    """
    combined = pd.DataFrame({
        "mstr_close": mstr_df["close"],
        "mstr_return": mstr_df["daily_return"],
        "btc_close": btc_df["close"],
        "btc_return": btc_df["daily_return"],
    })
    
    # Drop any rows with missing data
    combined = combined.dropna()
    return combined


def calculate_rolling_beta(df: pd.DataFrame, window: int = ROLLING_WINDOW) -> pd.Series:
    """
    Calculate MSTR's rolling beta relative to BTC.
    Beta = Cov(MSTR, BTC) / Var(BTC)
    
    Interpretation:
        beta > 1: MSTR amplifies BTC moves
        beta = 1: MSTR moves 1:1 with BTC
        beta < 1: MSTR dampens BTC moves
    """
    covariance = df["mstr_return"].rolling(window).cov(df["btc_return"])
    variance = df["btc_return"].rolling(window).var()
    
    return covariance / variance


def calculate_rolling_covariance(df: pd.DataFrame, window: int = ROLLING_WINDOW) -> pd.Series:
    """
    Calculate rolling covariance between MSTR and BTC returns.
    Higher values indicate returns move together more strongly.
    """
    return df["mstr_return"].rolling(window).cov(df["btc_return"])


def plot_analysis(df: pd.DataFrame):
    """Generate the three analysis charts."""
    
    # Calculate metrics
    rolling_beta = calculate_rolling_beta(df)
    rolling_cov = calculate_rolling_covariance(df)
    
    # Set up the figure with three subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle("MSTR vs BTC Correlation Analysis (Since Aug 11, 2020)", fontsize=14, fontweight="bold")
    
    # Chart 1: Daily close prices
    ax1a = axes[0]
    ax1b = ax1a.twinx()
    
    ax1a.plot(df.index, df["mstr_close"], color="tab:blue", linewidth=1, label="MSTR")
    ax1b.plot(df.index, df["btc_close"], color="tab:orange", linewidth=1, label="BTC")
    
    ax1a.set_ylabel("MSTR Price ($)", color="tab:blue")
    ax1b.set_ylabel("BTC Price ($)", color="tab:orange")
    ax1a.tick_params(axis="y", labelcolor="tab:blue")
    ax1b.tick_params(axis="y", labelcolor="tab:orange")
    ax1a.set_title("Daily Close Prices")
    
    # Combined legend
    lines1, labels1 = ax1a.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1a.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    
    # Chart 2: Rolling beta
    axes[1].plot(df.index, rolling_beta, color="tab:green", linewidth=1)
    axes[1].axhline(y=1.0, color="gray", linestyle="--", alpha=0.7, label="Beta = 1")
    axes[1].set_ylabel("Beta")
    axes[1].set_title(f"MSTR Beta Relative to BTC ({ROLLING_WINDOW}-Day Rolling)")
    axes[1].legend(loc="upper right")
    
    # Add interpretation band
    axes[1].fill_between(df.index, 1, rolling_beta, 
                         where=(rolling_beta > 1), alpha=0.3, color="tab:red", label="Amplified")
    axes[1].fill_between(df.index, 1, rolling_beta,
                         where=(rolling_beta < 1), alpha=0.3, color="tab:blue", label="Dampened")
    
    # Chart 3: Rolling covariance
    axes[2].plot(df.index, rolling_cov, color="tab:purple", linewidth=1)
    axes[2].axhline(y=0, color="gray", linestyle="--", alpha=0.7)
    axes[2].set_ylabel("Covariance")
    axes[2].set_xlabel("Date")
    axes[2].set_title(f"MSTR-BTC Return Covariance ({ROLLING_WINDOW}-Day Rolling)")
    
    # Highlight high covariance periods
    cov_mean = rolling_cov.mean()
    cov_std = rolling_cov.std()
    axes[2].axhline(y=cov_mean, color="tab:purple", linestyle=":", alpha=0.5, label=f"Mean: {cov_mean:.1f}")
    axes[2].legend(loc="upper right")
    
    plt.tight_layout()
    plt.savefig("mstr_btc_analysis.png", dpi=150, bbox_inches="tight")
    plt.show()
    
    return rolling_beta, rolling_cov


def print_summary_stats(df: pd.DataFrame, rolling_beta: pd.Series, rolling_cov: pd.Series):
    """Print key statistics from the analysis."""
    
    # Overall correlation
    correlation = df["mstr_return"].corr(df["btc_return"])
    
    print("\n" + "=" * 50)
    print("MSTR-BTC CORRELATION SUMMARY")
    print("=" * 50)
    
    print(f"\nDate Range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    print(f"Trading Days Analyzed: {len(df)}")
    
    print(f"\nOverall Correlation: {correlation:.3f}")
    
    print(f"\nBeta Statistics ({ROLLING_WINDOW}-day rolling):")
    print(f"  Current: {rolling_beta.iloc[-1]:.2f}")
    print(f"  Mean: {rolling_beta.mean():.2f}")
    print(f"  Min: {rolling_beta.min():.2f}")
    print(f"  Max: {rolling_beta.max():.2f}")
    
    print(f"\nCovariance Statistics ({ROLLING_WINDOW}-day rolling):")
    print(f"  Current: {rolling_cov.iloc[-1]:.2f}")
    print(f"  Mean: {rolling_cov.mean():.2f}")
    print(f"  Min: {rolling_cov.min():.2f}")
    print(f"  Max: {rolling_cov.max():.2f}")
    
    # Interpretation
    current_beta = rolling_beta.iloc[-1]
    print(f"\nInterpretation:")
    if current_beta > 1.5:
        print(f"  MSTR currently acts as a leveraged BTC play (beta={current_beta:.2f})")
    elif current_beta > 1:
        print(f"  MSTR amplifies BTC movements slightly (beta={current_beta:.2f})")
    elif current_beta > 0.5:
        print(f"  MSTR tracks BTC with some dampening (beta={current_beta:.2f})")
    else:
        print(f"  MSTR shows weak correlation to BTC (beta={current_beta:.2f})")


def main():
    print("Fetching MSTR data...")
    mstr_df = fetch_mstr_data()
    
    print("Fetching BTC data...")
    btc_df = fetch_btc_data()
    
    print("Aligning datasets...")
    combined_df = align_dataframes(mstr_df, btc_df)
    
    print("Generating analysis charts...")
    rolling_beta, rolling_cov = plot_analysis(combined_df)
    
    print_summary_stats(combined_df, rolling_beta, rolling_cov)
    
    print("\nChart saved to: mstr_btc_analysis.png")


if __name__ == "__main__":
    main()