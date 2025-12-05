#!/usr/bin/env python3
"""
faang.py

Command-line script to:
1. Download five days of hourly FAANG stock data into the `data` folder.
2. Plot the Close prices for each stock into the `plots` folder.

This script reuses the logic developed in problems.ipynb.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


# List of FAANG tickers
FAANG_TICKERS: List[str] = ["META", "AAPL", "AMZN", "NFLX", "GOOG"]


def get_data(
    tickers: Optional[List[str]] = None,
    period: str = "5d",
    interval: str = "1h",
) -> Path:
    """
    Download hourly stock data for the previous five days for the given tickers
    using the yfinance package, and save the results to a timestamped CSV file
    inside the `data` folder in the repository root.

    Args:
        tickers: List of ticker symbols to download. If None, FAANG_TICKERS is used.
        period: Period of historical data to download (default "5d").
        interval: Data interval (default "1h" for hourly).

    Returns:
        Path object pointing to the saved CSV file.
    """
    if tickers is None:
        tickers = FAANG_TICKERS

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    tickers_str = " ".join(tickers)

    df = yf.download(
        tickers=tickers_str,
        period=period,
        interval=interval,
        auto_adjust=False,
        threads=True,
    )

    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = data_dir / f"{timestamp_str}.csv"
    df.to_csv(file_path)

    return file_path


def get_latest_data_file(data_dir: Path = Path("data")) -> Path:
    """
    Return the path to the most recently modified CSV file in the given
    data directory.
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")

    latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
    return latest_file


def plot_data() -> Path:
    """
    Open the latest data CSV in the `data` folder and plot the Close prices
    for each of the five FAANG stocks on a single figure.

    The figure is saved into a `plots` directory using a timestamped filename.
    """
    data_file = get_latest_data_file()

    df = pd.read_csv(data_file, header=[0, 1], index_col=0)
    df.index = pd.to_datetime(df.index)

    close_df = df["Close"]

    plots_dir = Path("plots")
    plots_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    for ticker in close_df.columns:
        ax.plot(close_df.index, close_df[ticker], label=ticker)

    ax.set_xlabel("Datetime")
    ax.set_ylabel("Close price (USD)")

    latest_timestamp = close_df.index.max()
    date_str = latest_timestamp.strftime("%Y-%m-%d")
    ax.set_title(f"FAANG Close Prices – {date_str}")

    ax.legend()
    fig.autofmt_xdate()

    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    plot_path = plots_dir / f"{timestamp_str}.png"

    fig.savefig(plot_path, bbox_inches="tight")
    plt.close(fig)

    return plot_path


def main() -> None:
    """
    Entry point for the command-line script.

    1. Download the latest FAANG data.
    2. Generate a plot of the Close prices.
    """
    print("Downloading FAANG data...")
    csv_path = get_data()
    print(f"Data saved to: {csv_path}")

    print("Generating plot...")
    plot_path = plot_data()
    print(f"Plot saved to: {plot_path}")


if __name__ == "__main__":
    main()