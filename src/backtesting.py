# src/backtesting.py

import backtrader as bt
import pandas as pd
import joblib
import os

class MLStrategy(bt.Strategy):
    def __init__(self):
        # Define indicators
        self.sma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
        self.sma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.macd = bt.indicators.MACD(self.data.close)

        # Load model
        self.model = joblib.load('../model/random_forest_model.pkl')

    def next(self):
        # Access indicators values
        features = [self.sma20[0], self.sma50[0], self.rsi[0], self.macd.macd[0], self.macd.signal[0], self.data.close[0], self.data.open[0]]
        
        # Ensure the feature list matches the training data
        if len(features) != 7:  # adjust this number based on the actual feature count
            raise ValueError("Feature list length does not match model expectations.")
        
        prediction = self.model.predict([features])[0]
        
        if prediction == 1 and not self.position:
            self.buy()
        elif prediction == 0 and self.position:
            self.sell()

def backtest():
    # Replace with your absolute path to the CSV file
    file_path = os.path.abspath('/Users/bryanzeng/Documents/Github/trading_prediction/data/AAPL_with_indicators.csv')
    
    data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    data_feed = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MLStrategy)
    cerebro.adddata(data_feed)
    cerebro.broker.setcash(10000)
    print("Starting Portfolio Value: $%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value: $%.2f" % cerebro.broker.getvalue())
    cerebro.plot()

if __name__ == "__main__":
    backtest()
