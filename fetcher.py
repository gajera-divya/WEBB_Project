import sqlite3
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import timedelta
import requests
from datetime import datetime, date

# Define the path to the SQLite database
DB_DIR = Path(__file__).parent / "db"
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
                Adj_close REAL,
                Volume INTEGER,
                PRIMARY KEY (Ticker, Date)
            )
        """)

init_db()


def fetch_and_store_data(ticker, start_date=None, end_date=None, db_path=DB_PATH, interval='1d'):
    """
    Fetches and stores data for a single ticker using the working Yahoo Finance API
    Returns: True if successful, False otherwise
    """

    if start_date == None:
        start_date = pd.to_datetime("2005-01-01")
    if end_date == None:
        end_date = datetime.now()
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.min.time())

    period1 = int(start_dt.timestamp())
    period2 = int(end_dt.timestamp())

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1}&period2={period2}&interval={interval}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    try:
        # Fetch data
        print(f"⏳ Fetching data for {ticker}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch {ticker} (HTTP {response.status_code})")
            return False
            
        data = response.json()
        
        if not data.get('chart', {}).get('result'):
            print(f"⚠️ No data found for {ticker}")
            return False
            
        # Process data
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        adj_close = result['indicators']['adjclose'][0]['adjclose']
        quote = result['indicators']['quote'][0]
        
        df = pd.DataFrame({
            'Date': pd.to_datetime(timestamps, unit='s').date,
            'Ticker': ticker,
            'Open': quote['open'],
            'High': quote['high'],
            'Low': quote['low'],
            'Close': quote['close'],
            'Adj_close': adj_close,
            'Volume': quote['volume']
        }).dropna()  # Remove any rows with missing data
        
        # Store in database
        with sqlite3.connect(db_path) as conn:
            # Create table if not exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS price_data (
                    Date DATE,
                    Ticker TEXT,
                    Open REAL,
                    High REAL,
                    Low REAL,
                    Close REAL,
                    Adj_close REAL,
                    Volume INTEGER,
                    PRIMARY KEY (Date, Ticker)
                )
            ''')
            
            # Insert data
            df.to_sql('price_data', conn, if_exists='append', index=False)
        
        print(f"✅ Successfully stored {len(df)} days of data for {ticker}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error for {ticker}: {str(e)}")
    except KeyError as e:
        print(f"❌ Missing expected data field for {ticker}: {str(e)}")
    except sqlite3.Error as e:
        print(f"❌ Database error for {ticker}: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error processing {ticker}: {str(e)}")
    
    return False


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






