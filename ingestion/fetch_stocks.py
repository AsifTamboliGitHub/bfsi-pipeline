import yfinance as yf
import pandas as pd
import yaml
import os

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    
def fetch_stock_data(ticker, period, interval):
    print(f"Fetching {ticker}...")
    df = yf.download(ticker, period=period, interval=interval)
    df["ticker"] = ticker
    return df

def save_data(df, ticker):
    clean_ticker = ticker.replace(".","_")

    csv_path = f"raw_data/csv/{clean_ticker}.csv"
    parquet_path = f"raw_data/parquet/{clean_ticker}.parquet"

    df.to_csv(csv_path)
    df.to_parquet(parquet_path)

    print(f"Saved {ticker} CSV and Parquet")

def main():
    config = load_config("config/stocks.yaml")

    for ticker in config["tickers"]:
        df = fetch_stock_data(ticker, config["period"], config["interval"])
        save_data(df, ticker)

if __name__ == "__main__":
    main()