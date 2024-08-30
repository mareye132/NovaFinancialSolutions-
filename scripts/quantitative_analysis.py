# quantitative_analysis.py

import pandas as pd
import talib
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    # Perform any necessary data cleaning steps
    return df

def calculate_technical_indicators(df):
    df['SMA'] = talib.SMA(df['Close'])
    df['RSI'] = talib.RSI(df['Close'])
    df['MACD'], df['MACD_SIGNAL'], df['MACD_DIFF'] = talib.MACD(df['Close'])
    return df

def visualize_data(df):
    plt.figure(figsize=(12, 6))

    # Plot Close Prices and Moving Average
    plt.subplot(2, 1, 1)
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['SMA'], label='SMA')
    plt.title('Close Price and SMA')
    plt.legend()

    # Plot RSI
    plt.subplot(2, 1, 2)
    plt.plot(df['RSI'], label='RSI')
    plt.title('RSI')
    plt.legend()

    plt.tight_layout()
    plt.show()
