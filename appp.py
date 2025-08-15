import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime
from data_sentiment import enrich_reviews_with_sentiment  # if needed

# Constants
DATA_DIR = Path("data")
RAW_REVIEWS_FILE = DATA_DIR / "raw_reviews.json"
PROCESSED_REVIEWS_FILE = DATA_DIR / "surat_restaurant_reviews.csv"

# Page config
st.set_page_config(
    page_title="Surat Restaurant Sentiment Analysis",
    page_icon="🍽️",
    layout="wide"
)

# Styling
st.markdown("""
    <style>
        .metric-container {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }
        .metric-label {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the restaurant review data"""
    try:
        if PROCESSED_REVIEWS_FILE.exists():
            return pd.read_csv(PROCESSED_REVIEWS_FILE)
        else:
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_sentiment_chart(df):
    sentiment_counts = df['sentiment'].value_counts()
    colors = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Overall Sentiment Distribution',
        color=sentiment_counts.index,
        color_discrete_map=colors
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_restaurant_chart(df):
    metrics = df.groupby('restaurant').agg({
        'polarity': 'mean',
        'sentiment': lambda x: (x == 'Positive').mean() * 100,
        'review': 'count'
    }).reset_index()
    metrics.columns = ['restaurant', 'avg_sentiment', 'positive_percent', 'review_count']
    metrics = metrics.sort_values('avg_sentiment', ascending=True)

    fig = px.bar(
        metrics,
        x='avg_sentiment',
        y='restaurant',
        orientation='h',
        title='Restaurant Performance Analysis',
        color='positive_percent',
        color_continuous_scale='RdYlGn',
        custom_data=['review_count', 'positive_percent']
    )
    fig.update_traces(
        hovertemplate="<br>".join([
            "Restaurant: %{y}",
            "Average Sentiment: %{x:.2f}",
            "Review Count: %{customdata[0]}",
            "Positive Reviews: %{customdata[1]:.1f}%"
        ])
    )
    fig.update_layout(
        xaxis_title="Average Sentiment Score",
        yaxis_title="Restaurant",
        coloraxis_colorbar_title="% Positive Reviews"
    )
    return fig

def run_script(script_name):
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def main():
    st.title("🍽️ Surat Restaurant Sentiment Analysis")
    st.markdown("""
    Analyze customer sentiments for popular restaurants in Surat using AI-powered review analysis.
    """)

    # Buttons
    with st.container():
        st.markdown("### 🔄 Data Generation Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("1️⃣ Generate Reviews"):
                with st.spinner("Generating reviews using AI..."):
                    success, out = run_script("agent.py")
                    if success:
                        st.success("Reviews generated successfully!")
                        st.code(out)
                    else:
                        st.error(out)

        with col2:
            if st.button("2️⃣ Analyze Sentiments"):
                with st.spinner("Analyzing sentiments..."):
                    success, out = run_script("data_sentiment.py")
                    if success:
                        st.success("Sentiment analysis completed!")
                        st.code(out)
                    else:
                        st.error(out)

        if RAW_REVIEWS_FILE.exists():
            t = datetime.fromtimestamp(RAW_REVIEWS_FILE.stat().st_mtime)
            st.caption(f"Last update: {t.strftime('%Y-%m-%d %H:%M:%S')}")

    df = load_data()
    if df is not None:
        total_reviews = len(df)
        avg_sentiment = df['polarity'].mean()
        positive_reviews = (df['sentiment'] == 'Positive').mean() * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-container"><div class="metric-label">Total Reviews</div>'
                        f'<div class="metric-value">{total_reviews}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-container"><div class="metric-label">Average Sentiment</div>'
                        f'<div class="metric-value">{avg_sentiment:.2f}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-container"><div class="metric-label">Positive Reviews</div>'
                        f'<div class="metric-value">{positive_reviews:.1f}%</div></div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Restaurant Comparison", "Sentiment Distribution"])
        with tab1:
            st.plotly_chart(create_restaurant_chart(df), use_container_width=True)
        with tab2:
            st.plotly_chart(create_sentiment_chart(df), use_container_width=True)

        st.markdown("### 🔍 Review Explorer")
        r_filter = st.selectbox("Restaurant", ["All"] + df['restaurant'].unique().tolist())
        s_filter = st.selectbox("Sentiment", ["All"] + df['sentiment'].unique().tolist())

        filtered = df.copy()
        if r_filter != "All":
            filtered = filtered[filtered['restaurant'] == r_filter]
        if s_filter != "All":
            filtered = filtered[filtered['sentiment'] == s_filter]

        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("No data found. Use the buttons above to generate / analyze data.")

if __name__ == "__main__":
    main()
