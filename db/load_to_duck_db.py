import duckdb
import pandas as pd
import os

def create_connection(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = duckdb.connect(db_path)
    print(f"Connected to DuckDB → {db_path}")
    return conn

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            date        TIMESTAMP,
            close       DOUBLE,
            high        DOUBLE,
            low         DOUBLE,
            open        DOUBLE,
            volume      BIGINT,
            ticker      VARCHAR,
            daily_return    DOUBLE,
            rolling_vol_20d DOUBLE,
            moving_avg_50d  DOUBLE
        )
    """)
    print("Table created → stocks")

def load_data(conn, clean_parquet_path):
    df = pd.read_parquet(clean_parquet_path)
    conn.execute("DELETE FROM stocks")
    conn.register("df", df)
    conn.execute("INSERT INTO stocks SELECT * FROM df")
    print(f"Loaded {len(df)} rows into stocks table")

def verify_data(conn):
    result = conn.execute("""
        SELECT 
            ticker,
            COUNT(*) as total_rows,
            MIN(date) as start_date,
            MAX(date) as end_date,
            ROUND(AVG(close), 2) as avg_close
        FROM stocks
        GROUP BY ticker
        ORDER BY ticker
    """).fetchdf()
    
    print(result)

def main():
    db_path = "db/bfsi.duckdb"
    clean_parquet_path = "clean_data/all_stocks_clean.parquet"
    
    conn = create_connection(db_path)
    create_tables(conn)
    load_data(conn, clean_parquet_path)
    verify_data(conn)
    conn.close()
    print("Done. Database closed.")

if __name__ == "__main__":
    main()