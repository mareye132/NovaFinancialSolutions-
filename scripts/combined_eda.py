import pandas as pd
from textblob import TextBlob
from collections import Counter
import re

def load_dataset(file_path):
    """Load the dataset from the provided file path."""
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the dataset: {e}")
        return None

def preprocess_date_column(df):
    """Preprocess the 'date' column by extracting only the date portion."""
    try:
        # Extract only the date part (YYYY-MM-DD)
        df['date'] = df['date'].apply(lambda x: x.split(' ')[0] if isinstance(x, str) else x)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        print("Date column preprocessed successfully.")
    except Exception as e:
        print(f"An error occurred while preprocessing 'date': {e}")

def headline_length_statistics(df):
    """Compute and print headline length statistics."""
    df['headline_length'] = df['headline'].apply(len)
    print("Headline Length Statistics:\n", df['headline_length'].describe())

def articles_per_publisher(df):
    """Count and print the number of articles per publisher."""
    publisher_count = df['publisher'].value_counts()
    print("Articles per Publisher:\n", publisher_count)

def publication_date_trends(df):
    """Analyze and print trends over publication dates."""
    try:
        publication_trends = df['date'].value_counts().sort_index()
        print("Publication Date Trends:\n", publication_trends)
    except Exception as e:
        print(f"An error occurred while analyzing publication date trends: {e}")

def perform_sentiment_analysis(df):
    """Perform sentiment analysis on the headlines."""
    df['sentiment'] = df['headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
    sentiment_counts = df['sentiment'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral').value_counts()
    print("Sentiment Analysis:\n", sentiment_counts)

def common_keywords(df):
    """Identify common keywords or phrases in the headlines."""
    all_words = ' '.join(df['headline']).lower().split()
    most_common_words = Counter(all_words).most_common(10)
    print("Most Common Keywords:\n", most_common_words)

def analyze_publication_frequency(df):
    """Analyze how publication frequency varies over time."""
    try:
        frequency = df.groupby(df['date'].dt.date).size()
        print("Publication Frequency Over Time:\n", frequency)
    except Exception as e:
        print(f"An error occurred while analyzing publication frequency: {e}")

def perform_publisher_analysis(df):
    """Analyze publishers' contribution to the news feed."""
    publisher_analysis = df['publisher'].value_counts()
    print("Publisher Analysis:\n", publisher_analysis)

def perform_eda(file_path):
    """Perform the entire EDA process."""
    df = load_dataset(file_path)
    if df is not None:
        preprocess_date_column(df)  # Preprocess the date column
        headline_length_statistics(df)
        articles_per_publisher(df)
        publication_date_trends(df)
        perform_sentiment_analysis(df)
        common_keywords(df)
        analyze_publication_frequency(df)
        perform_publisher_analysis(df)

if __name__ == "__main__":
    file_path = 'C:/Users/user/Desktop/Github/NovaFinancialSolutions-/scripts/raw_analyst_ratings.csv'
    perform_eda(file_path)