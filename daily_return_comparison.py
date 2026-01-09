import matplotlib.pyplot as plt
from fetch_mstr import get_mstr_with_returns
from fetch_btc import get_btc_with_returns
from evaluate import merge_datasets


def plot_daily_returns(merged_data):
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(merged_data.index, merged_data["Daily_Return_MSTR"], label="MSTR", alpha=0.7)
    ax.plot(merged_data.index, merged_data["Daily_Return_BTC"], label="BTC", alpha=0.7)
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Return (%)")
    ax.set_title("MSTR vs BTC Daily Returns (August 2020 - Present)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Fetching data...")
    mstr_data = get_mstr_with_returns()
    btc_data = get_btc_with_returns()
    
    print("Merging datasets...")
    merged_data = merge_datasets(mstr_data, btc_data)
    
    print("Generating plot...")
    plot_daily_returns(merged_data)