import ccxt
import sqlite3
import time
from datetime import datetime, timedelta
import threading

# Database setup
def initialize_database():
    conn = sqlite3.connect('crypto_prices.db')
    cursor = conn.cursor()
    # Create table for price data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY,
        pair TEXT,
        price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Insert price data into the database with a new connection for each thread
def insert_price(pair, price):
    conn = sqlite3.connect('crypto_prices.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (pair, price, timestamp) VALUES (?, ?, ?)", (pair, price, datetime.now()))
    conn.commit()
    conn.close()

# Fetch all Binance USDT futures pairs
def get_usdt_futures_pairs():
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'}
    })
    markets = exchange.load_markets()
    usdt_futures_pairs = [symbol for symbol in markets if symbol.endswith('/USDT')]
    return usdt_futures_pairs

# Fetch and store prices for all pairs
def fetch_and_store_prices():
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'}
    })
    pairs = get_usdt_futures_pairs()

    while True:
        for pair in pairs:
            try:
                ticker = exchange.fetch_ticker(pair)
                price = ticker['last']
                insert_price(pair, price)
                print(f"{datetime.now()} - {pair}: {price}")
            except ccxt.BaseError as e:
                print(f"Market symbol not available for {pair}: {e}")
            except Exception as e:
                print(f"Error fetching data for {pair}: {e}")
        
        # Wait for 10 minutes before fetching data again
        time.sleep(600)

# Cleanup old data older than 120 days with a new connection for each cleanup
def cleanup_old_data():
    conn = sqlite3.connect('crypto_prices.db')
    cursor = conn.cursor()
    retention_period = datetime.now() - timedelta(days=120)
    cursor.execute("DELETE FROM prices WHERE timestamp < ?", (retention_period,))
    conn.commit()
    conn.close()
    print("Old data cleaned up")

# Run cleanup periodically
def run_cleanup_periodically():
    while True:
        cleanup_old_data()
        time.sleep(86400)  # Run cleanup every 24 hours

# Main function to start both data fetching and cleanup
def main():
    # Initialize the database
    initialize_database()

    # Create threads for continuous data fetching and cleanup
    data_fetching_thread = threading.Thread(target=fetch_and_store_prices)
    cleanup_thread = threading.Thread(target=run_cleanup_periodically)

    # Start threads
    data_fetching_thread.start()
    cleanup_thread.start()

    # Wait for threads to complete (they run indefinitely)
    data_fetching_thread.join()
    cleanup_thread.join()

# Run the main function
if __name__ == '__main__':
    main()
