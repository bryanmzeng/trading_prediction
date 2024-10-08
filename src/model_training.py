# src/model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from imblearn.over_sampling import SMOTE

def calculate_indicators(data):
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['MACD'] = data['Close'].ewm(span=12).mean() - data['Close'].ewm(span=26).mean()
    data['BB_upper'], data['BB_middle'], data['BB_lower'] = bollinger_bands(data['Close'])
    data['RSI'] = calculate_rsi(data['Close'], 14)
    data = data.dropna()  # Drop rows with NaN values generated by indicators
    return data

def bollinger_bands(series, window=20, num_std_dev=2):
    middle_band = series.rolling(window).mean()
    std_dev = series.rolling(window).std()
    upper_band = middle_band + num_std_dev * std_dev
    lower_band = middle_band - num_std_dev * std_dev
    return upper_band, middle_band, lower_band

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def train_model(data):
    # Calculate additional indicators
    data = calculate_indicators(data)

    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    X = data[['SMA_20', 'SMA_50', 'MACD', 'BB_upper', 'BB_middle', 'BB_lower', 'RSI']]
    y = data['Target']

    # Handle class imbalance using SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Use TimeSeriesSplit for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Set up the RandomForestClassifier with GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, n_jobs=-1, verbose=2)
    grid_search.fit(X_resampled, y_resampled)

    best_model = grid_search.best_estimator_
    print(f"Best Hyperparameters: {grid_search.best_params_}")

    # Perform the final train-test split to evaluate the model
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, shuffle=False)
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Model Accuracy: {accuracy}')

    # Ensure the model directory exists
    model_dir = '../model/'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the best model
    joblib.dump(best_model, os.path.join(model_dir, 'random_forest_model.pkl'))
    print("Model saved.")

if __name__ == "__main__":
    data = pd.read_csv('../data/AAPL_with_indicators.csv', index_col='Date', parse_dates=True)
    train_model(data)
