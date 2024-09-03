import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import talib

def load_data(ticker):
    # Download stock price data
    df = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    df.reset_index(inplace=True)
    return df

def calculate_indicators(df):
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['SMA_200'] = talib.SMA(df['Close'], timeperiod=200)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )
    return df

def calculate_financial_metrics(df):
    daily_returns = df['Close'].pct_change().dropna()
    return daily_returns

def visualize_data(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.plot(df['Date'], df['SMA_50'], label='50-Day SMA')
    plt.plot(df['Date'], df['SMA_200'], label='200-Day SMA')
    plt.title('Stock Price with Moving Averages')
    plt.legend()
    plt.show()

    plt.figure(figsize=(14, 5))
    plt.plot(df['Date'], df['RSI'], label='RSI')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.show()

    plt.figure(figsize=(14, 5))
    plt.plot(df['Date'], df['MACD'], label='MACD')
    plt.plot(df['Date'], df['MACD_signal'], label='Signal Line')
    plt.bar(df['Date'], df['MACD_hist'], label='MACD Histogram', color='gray')
    plt.title('MACD')
    plt.legend()
    plt.show()

def main():
    ticker = 'AAPL'
    df = load_data(ticker)
    df = calculate_indicators(df)
    daily_returns = calculate_financial_metrics(df)
    visualize_data(df)
    print(daily_returns.head())

if __name__ == '__main__':
    main()
