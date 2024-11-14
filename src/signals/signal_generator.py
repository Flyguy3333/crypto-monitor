import pandas as pd
import logging

def generate_signals(df):
    # Set up logging configuration
    logging.basicConfig(filename='logs/signals.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    
    df['Signal'] = 0
    for i in range(1, len(df)):
        if not pd.isna(df['SMA_20'].iloc[i]) and not pd.isna(df['EMA_20'].iloc[i]):
            if df['SMA_20'].iloc[i] > df['EMA_20'].iloc[i] and df['SMA_20'].iloc[i - 1] <= df['EMA_20'].iloc[i - 1]:
                df['Signal'].iloc[i] = 1  # Buy signal
                logging.info(f"Buy signal generated at index {i}")
            elif df['SMA_20'].iloc[i] < df['EMA_20'].iloc[i] and df['SMA_20'].iloc[i - 1] >= df['EMA_20'].iloc[i - 1]:
                df['Signal'].iloc[i] = -1  # Sell signal
                logging.info(f"Sell signal generated at index {i}")
    return df
