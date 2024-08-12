# src/feature_engineering.py

import pandas as pd

def calculate_indicators(data):
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['RSI'] = calculate_rsi(data['Close'], 14)
    data = data.dropna()
    return data

def calculate_rsi(series, period):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if __name__ == "__main__":
    data = pd.read_csv('../data/AAPL.csv', index_col='Date', parse_dates=True)
    data = calculate_indicators(data)
    data.to_csv('../data/AAPL_with_indicators.csv')
    print("Indicators calculated and saved.")
