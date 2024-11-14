from src.data.data_fetcher import fetch_price_data, store_price_data
from src.indicators.indicator_calculator import calculate_moving_average, calculate_rsi
from src.signals.signal_generator import generate_signal
from src.utils.helpers import timestamp_to_date
import pandas as pd
import time

# Main function to fetch data, calculate indicators, and generate signals
def main():
    # Configuration
    pair = "BTC/USDT"
    ma_window_short = 10
    ma_window_long = 50
    rsi_window = 14
    data = []

    # Fetch price data in a loop
    for _ in range(5):  # Fetch 5 samples for testing
        price, timestamp = fetch_price_data(pair)
        if price is not None and timestamp is not None:
            # Store data in database
            store_price_data(pair, price, timestamp)
            
            # Add data to our in-memory list for calculations
            data.append({'price': price, 'timestamp': timestamp_to_date(timestamp)})
            print(f"Fetched and stored: {price} at {timestamp_to_date(timestamp)}")

        # Wait a bit before fetching next data point (simulate real-time)
        time.sleep(2)

    # Convert data to DataFrame for indicator calculations
    df = pd.DataFrame(data)

    # Calculate indicators
    df['MA_Short'] = calculate_moving_average(df, ma_window_short)
    df['MA_Long'] = calculate_moving_average(df, ma_window_long)
    df['RSI'] = calculate_rsi(df, rsi_window)

    # Generate signals based on indicators
    for i in range(len(df)):
        ma_short = df['MA_Short'].iloc[i]
        ma_long = df['MA_Long'].iloc[i]
        if pd.notnull(ma_short) and pd.notnull(ma_long):
            signal = generate_signal(ma_short, ma_long)
            print(f"Price: {df['price'].iloc[i]}, MA_Short: {ma_short}, MA_Long: {ma_long}, Signal: {signal}")

if __name__ == "__main__":
    main()
