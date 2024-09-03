import pandas as pd
from textblob import TextBlob
from datetime import datetime
import numpy as np

# Paths to datasets
news_path = 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/raw_analyst_ratings.csv'
stock_paths = {
    'AAPL': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/AAPL_historical_data.csv',
    'AMZN': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/AMZN_historical_data.csv',
    'GOOG': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/GOOG_historical_data.csv',
    'META': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/META_historical_data.csv',
    'MSFT': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/MSFT_historical_data.csv',
    'NVDA': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/NVDA_historical_data.csv',
    'TSLA': 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/TSLA_historical_data.csv'
}

# Load and preprocess news data
def load_news_data(news_path):
    news_df = pd.read_csv(news_path)
    
    # Print column names to confirm
    print("Columns in news data:", news_df.columns)
    
    # Use the correct column names
    if 'date' not in news_df.columns:
        raise KeyError("The 'date' column is not present in the dataset.")
    
    if 'headline' not in news_df.columns:
        raise KeyError("The 'headline' column is not present in the dataset.")
    
    try:
        news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce')
    except Exception as e:
        raise ValueError(f"Error parsing date: {e}")
    
    news_df.dropna(subset=['date'], inplace=True)
    
    # Perform sentiment analysis on the 'headline' column
    news_df['Sentiment'] = news_df['headline'].apply(lambda headline: TextBlob(headline).sentiment.polarity)
    daily_sentiment = news_df.groupby(news_df['date'].dt.date)['Sentiment'].mean()
    return daily_sentiment

# Load and preprocess stock data
def load_stock_data(stock_paths):
    stock_data = {}
    for stock, path in stock_paths.items():
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Daily_Return'] = df['Close'].pct_change()
        df.set_index('Date', inplace=True)
        stock_data[stock] = df['Daily_Return']
    return stock_data

# Merge news sentiment with stock data
def merge_data(sentiment_data, stock_data):
    merged_data = {}
    for stock, returns in stock_data.items():
        merged_df = pd.DataFrame({'Sentiment': sentiment_data, 'Daily_Return': returns})
        merged_df.dropna(inplace=True)
        merged_data[stock] = merged_df
    return merged_data

# Calculate Pearson correlation
def calculate_correlation(merged_data):
    correlations = {}
    for stock, data in merged_data.items():
        correlation = data['Sentiment'].corr(data['Daily_Return'])
        correlations[stock] = correlation
    return correlations

def main():
    sentiment_data = load_news_data(news_path)
    stock_data = load_stock_data(stock_paths)
    merged_data = merge_data(sentiment_data, stock_data)
    correlations = calculate_correlation(merged_data)
    
    for stock, correlation in correlations.items():
        print(f"Correlation between sentiment and {stock} stock returns: {correlation:.4f}")

    # Saving the correlation results
    correlation_df = pd.DataFrame(list(correlations.items()), columns=['Stock', 'Correlation'])
    correlation_df.to_csv('C:/Users/user/Desktop/Github/NovaFinancialSolutions-/Data/correlation_results.csv', index=False)

if __name__ == '__main__':
    main()
