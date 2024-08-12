# Trading Prediction with Machine Learning

This project demonstrates how to integrate machine learning models with backtesting frameworks to create and evaluate trading strategies. The core idea is to use a `RandomForestClassifier` to make trading decisions based on various technical indicators.

## Key Features

- **Machine Learning Model**: Utilizes `RandomForestClassifier` for prediction.
- **Indicators Used**: 
  - Simple Moving Averages (SMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- **Backtesting Framework**: Uses [Backtrader](https://www.backtrader.com/) for evaluating trading strategies.
- **Data Handling**: Processes historical stock data with pre-computed indicators.
