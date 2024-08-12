# src/data_collection.py

import yfinance as yf
import os

def download_data(symbol, start_date, end_date, save_path):
    data = yf.download(symbol, start=start_date, end=end_date)
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    data.to_csv(save_path)
    print(f"Data saved to {save_path}")

if __name__ == "__main__":
    download_data('AAPL', '2010-01-01', '2023-01-01', '../data/AAPL.csv')
