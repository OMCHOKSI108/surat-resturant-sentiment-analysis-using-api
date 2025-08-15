# agent.py

import os
import google.generativeai as genai
from typing import List, Dict
import json
import time
from tqdm import tqdm

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Restaurant list in Surat
RESTAURANTS = [
    "Ziba Restaurant, Adajan",
    "The Royal Cafe, Athwa",
    "Coffee Culture, Vesu",
    "Jugaad Nights, Vesu",
    "Tomatoes, Piplod",
    "Level 5, Vesu"
]

def setup_gemini_model():
    """Initialize and return the Gemini model."""
    return genai.GenerativeModel('gemini-1.5-flash')

def get_restaurant_reviews(model, restaurant_name: str, num_reviews: int = 5) -> List[Dict]:
    prompt = f"""
    Generate {num_reviews} realistic customer reviews for {restaurant_name} in Surat, Gujarat.
    Each review should be 2-3 sentences about food quality, service, ambiance, or value.
    Format as JSON array with 'review' key for each entry.
    Reviews should vary in sentiment (positive, negative, neutral).
    """

    try:
        response = model.generate_content(prompt)
        # Gemini response is nested in candidates → parts → text
        reviews_text = response.candidates[0].content.parts[0].text
        # Remove markdown fences if present
        cleaned = reviews_text.strip().strip("```json").strip("```")
        reviews_json = json.loads(cleaned)
        return reviews_json
    except Exception as e:
        print(f"Error generating reviews for {restaurant_name}: {str(e)}")
        return []

def collect_all_reviews(num_reviews_per_restaurant: int = 10) -> List[Dict]:
    """
    Collect reviews for all restaurants using Gemini.
    
    Args:
        num_reviews_per_restaurant: Number of reviews to generate per restaurant
        
    Returns:
        List of dictionaries containing restaurant names and reviews
    """
    model = setup_gemini_model()
    all_reviews = []
    
    for restaurant in tqdm(RESTAURANTS, desc="Collecting reviews"):
        reviews = get_restaurant_reviews(model, restaurant, num_reviews_per_restaurant)
        for review in reviews:
            review_entry = {
                "restaurant": restaurant,
                "review": review["review"]
            }
            all_reviews.append(review_entry)
        time.sleep(1)  # Rate limiting
        
    return all_reviews

if __name__ == "__main__":
    print("Starting review collection process...")
    reviews = collect_all_reviews()
    
    # Save raw reviews to JSON for backup
    output_path = "data/raw_reviews.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    print(f"\nCollected {len(reviews)} reviews total")
    print(f"Raw reviews saved to {output_path}")
