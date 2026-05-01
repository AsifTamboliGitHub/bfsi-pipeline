import pandas as pd
import os

def load_all_stocks(parquet_folder):
    all_dfs = []

    for file in os.listdir(parquet_folder):
        if file.endswith(".parquet"):
            path = os.path.join(parquet_folder, file)
            df = pd.read_parquet(path)
            all_dfs.append(df)
    combined = pd.concat(all_dfs)
    combined = combined.reset_index()        # ← add this line
    combined.columns.name = None  
    return combined

def clean_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    else:
        df.columns = [col[0] if isinstance(col, tuple) else col 
                      for col in df.columns]
    
    df.columns = [str(col).lower().strip() for col in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]

    return df

def add_financial_metrics(df):
    df = df.sort_values(["ticker","date"])

    df["daily_return"] = df.groupby("ticker")["close"].pct_change()

    df["rolling_vol_20d"] = (
        df.groupby("ticker")["daily_return"]
        .transform(lambda x: x.rolling(20).std())
    )

    df["moving_avg_50d"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(50).mean())
    )
    
    return df

def save_clean_data(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    output_path = os.path.join(output_folder, "all_stocks_clean.parquet")
    df.to_parquet(output_path)
    
    print(f"Saved clean data → {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

def main():
    raw_folder = "raw_data/parquet"
    clean_folder = "clean_data"

    df = load_all_stocks(raw_folder)
    df = clean_columns(df)
    df = add_financial_metrics(df)
    save_clean_data(df, clean_folder)

if __name__ == "__main__":
    main()