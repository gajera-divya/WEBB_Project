import sqlite3
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import timedelta

# Define the path to the SQLite database
DB_DIR = Path(__file__).parent.parent / "db"
DB_PATH = DB_DIR / "market_data.db"
DB_DIR.mkdir(parents=True, exist_ok=True)

def init_db():
    """Creates the database table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                Date TEXT,
                Ticker TEXT,
                Close REAL,
                High REAL,
                Low REAL,
                Open REAL,
                Volume INTEGER,
                PRIMARY KEY (Ticker, Date)
            )
        """)

init_db()

def fetch_and_store_data(ticker, start_date=None):
    """Fetches data from Yahoo Finance and stores it in the database."""
    df = yf.download(ticker, start=start_date)
    if df.empty:
        print(f"No new data for {ticker} from {start_date}.")
        return

    df = df.stack().reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df[["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]]

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("price_data", conn, if_exists="append", index=False)

def check_ticker_exists(ticker):
    """
    Checks if a ticker exists in the database. If yes, fetches new data
    from the last available date. If no, fetches all data.
    """
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT MAX(Date) FROM price_data WHERE Ticker = ?"
        last_date = conn.execute(query, (ticker,)).fetchone()[0]

    if last_date:
        last_date = pd.to_datetime(last_date).date()
        next_date = last_date + timedelta(days=1)
        if next_date.weekday() < 5:
            fetch_and_store_data(ticker, start_date=next_date)
        else:
            print(f"No trading on {next_date}, skipping fetch.")
    else:
        fetch_and_store_data(ticker)

def get_data(ticker, start, end):
    """
    Returns stock data for a given ticker between two dates.
    """
    check_ticker_exists(ticker)
    query = """
        SELECT * FROM price_data
        WHERE Ticker = ? AND Date BETWEEN ? AND ?
        ORDER BY Date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(query, conn, params=(ticker, start, end))
    return df



