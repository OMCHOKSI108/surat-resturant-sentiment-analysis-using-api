# data_sentiment.py

import pandas as pd
import requests
import json
import time
from tqdm import tqdm

# API Configuration
API_URL = "https://sentiment-api-service-fzdu57t2fa-uc.a.run.app/predict"
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def load_raw_reviews():
    """Load the raw reviews from JSON file."""
    try:
        with open('data/raw_reviews.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: raw_reviews.json not found. Please run agent.py first.")
        return None

def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text using the sentiment API.
    
    Args:
        text: The review text to analyze
        
    Returns:
        Dictionary containing sentiment and polarity
    """
    try:
        payload = {"text": text}
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return {"sentiment": "Error", "polarity": 0.0}

def process_reviews(reviews):
    """
    Process all reviews through the sentiment analysis API.
    
    Args:
        reviews: List of dictionaries containing restaurant names and reviews
        
    Returns:
        Pandas DataFrame with sentiment analysis results
    """
    processed_data = []
    
    for review in tqdm(reviews, desc="Analyzing sentiments"):
        sentiment_result = analyze_sentiment(review['review'])
        
        processed_data.append({
            'restaurant': review['restaurant'],
            'review': review['review'],
            'sentiment': sentiment_result.get('sentiment', 'Error'),
            'polarity': sentiment_result.get('polarity', 0.0)
        })
        
        time.sleep(0.5)  # Rate limiting
        
    return pd.DataFrame(processed_data)

def main():
    """Main function to run the sentiment analysis process."""
    print("Starting sentiment analysis process...")
    
    # Load raw reviews
    reviews = load_raw_reviews()
    if not reviews:
        return
    
    # Process reviews through sentiment API
    df = process_reviews(reviews)
    
    # Save to CSV
    output_path = 'data/surat_restaurant_reviews.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nProcessed {len(df)} reviews")
    print(f"Data saved to {output_path}")
    
    # Print quick summary
    print("\nSentiment Distribution:")
    print(df['sentiment'].value_counts())

if __name__ == "__main__":
    main()
