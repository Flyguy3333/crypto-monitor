import pandas as pd
from src.indicators.indicator_calculator import calculate_indicators
from src.signals.signal_generator import generate_signals

# Adjusted test data to ensure SMA and EMA cross
data = {
    'price': [100, 101, 99, 102, 98, 103, 97, 104, 96, 105, 95, 106, 94, 107, 93, 108, 92, 109, 91, 110]
}
df = pd.DataFrame(data)

# Calculate indicators
df_with_indicators = calculate_indicators(df)

# Generate signals
df_with_signals = generate_signals(df_with_indicators)

# Print results
print("Sample Data with Calculated Indicators and Signals:")
print(df_with_signals)

# Check log file to verify signals were logged
with open("logs/signals.log", "r") as log_file:
    print("\nSignal Log:")
    print(log_file.read())
