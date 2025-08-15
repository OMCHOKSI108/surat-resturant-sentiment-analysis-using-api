# main.py

import pandas as pd
import plotly.express as px

DATA_FILE = "data/surat_restaurant_reviews.csv"

def load_data():
    """Loads the review data from the CSV file."""
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return None

def get_overall_sentiment_distribution(df):
    """Calculates the count of Positive, Negative, and Neutral reviews."""
    sentiment_counts = df['sentiment'].value_counts()
    return sentiment_counts

def get_total_polarity_scores(df):
    """Calculates the sum of polarity for positive and negative reviews."""
    positive_polarity = df[df['polarity'] > 0]['polarity'].sum()
    negative_polarity = df[df['polarity'] < 0]['polarity'].sum()
    net_polarity = df['polarity'].sum()
    return positive_polarity, negative_polarity, net_polarity

def create_restaurant_ranking_chart(df):
    """Creates an interactive bar chart of restaurants ranked by average polarity."""
    avg_sentiment = df.groupby('restaurant')['polarity'].mean().sort_values(ascending=True).reset_index()
    fig = px.bar(
        avg_sentiment,
        x='polarity',
        y='restaurant',
        orientation='h',
        title='Restaurant Rankings by Average Customer Sentiment',
        labels={'polarity': 'Average Polarity Score (Higher is Better)', 'restaurant': 'Restaurant'},
        template='plotly_white'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def create_sentiment_pie_chart(df):
    """Creates an interactive pie chart of the overall sentiment distribution."""
    sentiment_counts = get_overall_sentiment_distribution(df)
    fig = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title='Overall Sentiment Distribution of All Reviews',
        color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'grey'}
    )
    return fig

# This allows you to run this file directly to test the analysis
if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print("--- Analysis Summary ---")
        
        pos_pol, neg_pol, net_pol = get_total_polarity_scores(df)
        print(f"Total Positive Polarity: {pos_pol:.2f}")
        print(f"Total Negative Polarity: {neg_pol:.2f}")
        print(f"Net Polarity Score: {net_pol:.2f}")
        
        print("\nSentiment Distribution:")
        print(get_overall_sentiment_distribution(df))
        
        print("\nData loaded and analysis functions are ready.")
    else:
        print(f"Error: Data file not found at '{DATA_FILE}'. Please run data_scraper.py first.")