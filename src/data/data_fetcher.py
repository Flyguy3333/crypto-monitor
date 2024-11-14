import ccxt
import time
import sqlite3

def fetch_price_data(pair="BTC/USDT"):
    exchange = ccxt.binance()
    try:
        ticker = exchange.fetch_ticker(pair)
        price = ticker['last']
        timestamp = ticker['timestamp']
        return price, timestamp
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

def store_price_data(pair, price, timestamp):
    conn = sqlite3.connect('crypto_prices.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS prices (pair TEXT, price REAL, timestamp INTEGER)''')
    cursor.execute('''INSERT INTO prices (pair, price, timestamp) VALUES (?, ?, ?)''', (pair, price, timestamp))
    conn.commit()
    conn.close()
