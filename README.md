🍽️ Surat Restaurant Sentiment Analysis

This project provides a command-line and Streamlit-based dashboard for analyzing customer reviews of Surat restaurants.

The workflow combines:

an AI agent that automatically searches the web and collects real customer reviews (e.g. from Zomato, review blogs, listings, etc.)

a custom sentiment analysis API used to evaluate each collected review

an interactive dashboard that visualizes sentiment distribution, polarity trends, and review-level insights (TSV and CSV support)

────────────────────────────────────────────────────────────────────▶ MAIN COMPONENTS

Review Collection Agent (Web + API)
The agent (agent.py) fetches real restaurant reviews from the web and sends each review to your custom sentiment API. Results are saved to a CSV file in the /data folder.

Real Review TSV Analysis (API + Comparison)
A TSV file (Restaurant_Reviews.tsv) containing real reviews and ground-truth ratings can be analyzed using the same API. The dashboard compares the API prediction with the original rating and computes accuracy + detailed metrics.

────────────────────────────────────────────────────────────────────
▶ FEATURES

• Real-world review collection via autonomous agent• Sentiment scoring via custom REST API• TSV analysis with original vs API sentiment comparison• API accuracy and polarity metrics• Polarity distribution histogram• Restaurant-level comparison chart• Filterable review table• Caching to avoid re-processing• Streamlit dashboard with Plotly visualizations

────────────────────────────────────────────────────────────────────▶ PROJECT STRUCTURE

surat-foodie-dashboard-v2/
├── agent.py                     ← AI web review collection agent
├── data_sentiment.py            ← API sentiment enrichment script
├── app.py                       ← Streamlit dashboard
├── data/
│   ├── raw_reviews.json         ← Collected reviews (raw)
│   ├── surat_restaurant_reviews.csv ← API-scored reviews (CSV)
│   └── Restaurant_Reviews.tsv   ← Ground-truth TSV (real reviews + rating)
├── requirements.txt
└── README.md

────────────────────────────────────────────────────────────────────▶ REQUIREMENTS

• Python 3.9+• Environment variable:
export GOOGLE_API_KEY=<your_api_key>• Custom Sentiment API available at:
https://sentiment-api-service-fzdu57t2fa-uc.a.run.app/predict

Install dependencies:

$ pip install -r requirements.txt

────────────────────────────────────────────────────────────────────▶ USAGE

Place a TSV file named Restaurant_Reviews.tsv in the data/ folder (columns: Review, Liked).

Run the app:

$ streamlit run app.py

Use the buttons in the dashboard:

[1] Generate Reviews (Web Agent)→ Collects real reviews and saves them in CSV

[2] Analyze Sentiments (CSV)→ Sends collected reviews to API and stores results

[3] Analyze Reviews from TSV→ Loads Restaurant_Reviews.tsv and compares API predictions to the original ratings

────────────────────────────────────────────────────────────────────▶ OUTPUT (TSV ANALYSIS)

• Total number of reviews analyzed• API accuracy vs original rating• Average polarity score• Bar chart: Original vs API sentiment• Histogram: Polarity score distribution• Filterable table with review, original rating, and API prediction

────────────────────────────────────────────────────────────────────

