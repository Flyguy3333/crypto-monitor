import pandas as pd

# Calculate the Simple Moving Average (SMA)
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

# Calculate the Exponential Moving Average (EMA)
def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

# Calculate the Relative Strength Index (RSI)
def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Calculate the Bollinger Bands
def calculate_bollinger_bands(data, window=20, num_std=2):
    sma = calculate_sma(data, window)
    rolling_std = data.rolling(window=window).std()
    upper_band = sma + (rolling_std * num_std)
    lower_band = sma - (rolling_std * num_std)
    return upper_band, lower_band

# Main function to calculate all indicators
def calculate_indicators(df):
    df['SMA_20'] = calculate_sma(df['price'], 20)
    df['EMA_20'] = calculate_ema(df['price'], 20)
    df['RSI'] = calculate_rsi(df['price'])
    df['BB_upper'], df['BB_lower'] = calculate_bollinger_bands(df['price'])
    return df
