# data_scraper.py

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm

# --- CONFIGURATION ---
API_URL = "https://sentiment-api-service-fzdu57t2fa-uc.a.run.app/predict"
RESTAURANT_URLS = {
    "Ziba Restaurant": "https://www.zomato.com/surat/ziba-restaurant-adajan/reviews",
    "The Royal Cafe": "https://www.zomato.com/surat/the-royal-cafe-athwa/reviews",
    "Coffee Culture": "https://www.zomato.com/surat/coffee-culture-1-vesu/reviews",
    "Jugaad Nights": "https://www.zomato.com/surat/jugaad-nights-vesu/reviews",
    "Tomatoes": "https://www.zomato.com/surat/tomatoes-piplod/reviews",
    "Level 5": "https://www.zomato.com/surat/level-5-vesu/reviews"
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "surat_restaurant_reviews.csv")

# --- HELPER FUNCTIONS ---
def analyze_sentiment(text):
    """Calls the live API to get the sentiment of a text."""
    payload = {"text": text}
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nAPI call failed: {e}")
    return {"sentiment": "Error", "polarity": 0.0}

def scrape_reviews(url):
    """Scrapes review texts from a given restaurant URL."""
    reviews = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # Will raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Updated selector for review text
        review_elements = soup.find_all('div', class_='sc-1q7bklc-1')
        for elem in review_elements:
            review_text = elem.find('p')
            if review_text:
                reviews.append(review_text.text.strip())
    except requests.exceptions.RequestException as e:
        print(f"\nCould not scrape {url}. Error: {e}")
    return reviews

# --- MAIN EXECUTION ---
def main():
    """Main function to run the scraper and analyzer."""
    print("Starting the data collection and analysis process...")
    
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = []
    
    # Use tqdm for a master progress bar over restaurants
    for name, url in tqdm(RESTAURANT_URLS.items(), desc="Processing Restaurants"):
        try:
            time.sleep(2)  # Add delay between restaurant requests
            reviews = scrape_reviews(url)
            if not reviews:
                print(f"\nNo reviews found for {name}, skipping.")
                continue
                
            for review_text in reviews:
                if review_text:
                    sentiment_result = analyze_sentiment(review_text)
                    all_data.append({
                        "restaurant": name,
                        "review": review_text,
                        "sentiment": sentiment_result.get('sentiment', 'Error'),
                        "polarity": sentiment_result.get('polarity', 0.0)
                    })
                    time.sleep(1)  # Increased delay between API calls
        except Exception as e:
            print(f"\nError processing {name}: {str(e)}")

    if not all_data:
        print("\nNo data was collected. Exiting.")
        return

    # Convert to DataFrame and save
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nProcess complete! Scraped and analyzed {len(df)} reviews.")
    print(f"Data saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()