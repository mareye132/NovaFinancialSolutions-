import pandas as pd
import talib
import pynance as pn
import matplotlib.pyplot as plt

def load_data(file_path):
    # Load your stock price data into a pandas DataFrame
    df = pd.read_csv(file_path)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]  # Corrected the string literal
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def calculate_indicators(df):
    # Moving Averages
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['SMA_200'] = talib.SMA(df['Close'], timeperiod=200)

    # RSI (Relative Strength Index)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)

    # MACD (Moving Average Convergence Divergence)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )

    return df

def calculate_financial_metrics(df):
    # Example: Calculate daily returns
    daily_returns = df['Close'].pct_change().dropna()
    return daily_returns

def visualize_data(df):
    plt.figure(figsize=(14, 7))

    # Plot Close Price and Moving Averages
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['SMA_50'], label='50-Day SMA')
    plt.plot(df.index, df['SMA_200'], label='200-Day SMA')
    plt.title('Stock Price with Moving Averages')
    plt.legend()
    plt.show()

    # Plot RSI
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df['RSI'], label='RSI')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.show()

    # Plot MACD
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df['MACD'], label='MACD')
    plt.plot(df.index, df['MACD_signal'], label='Signal Line')
    plt.bar(df.index, df['MACD_hist'], label='MACD Histogram', color='gray')
    plt.title('MACD')
    plt.legend()
    plt.show()

def main():
    # Path to your stock data CSV file
    file_path = 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/scripts/AAPL_historical_data.csv'
    
    # Load and prepare the data
    df = load_data(file_path)

    # Calculate technical indicators
    df = calculate_indicators(df)

    # Calculate financial metrics
    daily_returns = calculate_financial_metrics(df)

    # Visualize the data
    visualize_data(df)

    # Print daily returns as an example
    print(daily_returns.head())

if __name__ == '__main__':
    main()
