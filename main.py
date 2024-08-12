# main.py

from src.data_collection import download_data
from src.feature_engineering import calculate_indicators
from src.model_training import train_model
from src.backtesting import backtest
import pandas as pd

def main():
    # Step 1: Data Collection
    download_data('AAPL', '2010-01-01', '2023-01-01', 'data/AAPL.csv')
    
    # Step 2: Feature Engineering
    data = pd.read_csv('data/AAPL.csv', index_col='Date', parse_dates=True)
    data = calculate_indicators(data)
    data.to_csv('data/AAPL_with_indicators.csv')
    
    # Step 3: Model Training
    train_model(data)
    
    # Step 4: Backtesting
    backtest()

if __name__ == "__main__":
    main()
