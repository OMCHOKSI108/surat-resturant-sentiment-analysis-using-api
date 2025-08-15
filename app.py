# app.py

import streamlit as st
import pandas as pd
from data_sentiment import analyze_sentiment

import plotly.express as px
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime


def load_data():
    """Load and cache the restaurant review data"""
    try:
        # First try to load from JSON (raw reviews)
        if RAW_REVIEWS_FILE.exists():
            with open(RAW_REVIEWS_FILE, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                df = pd.DataFrame(raw_data)
                
                # Add polarity if not present
                if 'polarity' not in df.columns:
                    df['sentiment'] = df.apply(lambda x: analyze_sentiment(x['review']), axis=1)
                    df['polarity'] = df['sentiment'].map({'Positive': 1.0, 'Negative': -1.0, 'Neutral': 0.0})
                
                return df
                
        # If JSON doesn't exist, try CSV
        elif PROCESSED_REVIEWS_FILE.exists():
            return pd.read_csv(PROCESSED_REVIEWS_FILE)
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
    

# Constants
DATA_DIR = Path("data")
RAW_REVIEWS_FILE = DATA_DIR / "raw_reviews.json"
PROCESSED_REVIEWS_FILE = DATA_DIR / "surat_restaurant_reviews.tsv"

# Page configuration
st.set_page_config(
    page_title="Surat Restaurant Sentiment Analysis",
    page_icon="🍽️",
    layout="wide"
)

# Custom styling
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
    """Load and cache the restaurant reviews data"""
    try:
        return pd.read_csv(PROCESSED_REVIEWS_FILE)
    except FileNotFoundError:
        return None

def create_sentiment_chart(df):
    """Create sentiment distribution chart"""
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
    """Create restaurant comparison chart"""
    restaurant_metrics = df.groupby('restaurant').agg({
        'polarity': ['mean', 'count'],
        'sentiment': lambda x: (x == 'Positive').mean() * 100
    }).reset_index()
    
    restaurant_metrics.columns = ['restaurant', 'avg_sentiment', 'review_count', 'positive_percent']
    restaurant_metrics = restaurant_metrics.sort_values('avg_sentiment', ascending=True)
    
    fig = px.bar(
        restaurant_metrics,
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
    """Run a Python script and return its output"""
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
    # Header
    st.title("🍽️ Surat Restaurant Sentiment Analysis")
    st.markdown("""
    Analyze customer sentiments for popular restaurants in Surat using AI-powered review analysis.
    This dashboard provides insights into customer experiences and overall restaurant performance.
    """)
    
    # Add control buttons in a container
    with st.container():
        st.markdown("### 🔄 Data Generation Controls")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("1️⃣ Generate Reviews", key="generate_reviews", use_container_width=True):
                with st.spinner("Generating reviews using AI..."):
                    success, output = run_script("agent.py")
                    if success:
                        st.success("Reviews generated successfully!")
                        st.code(output, language="text")
                    else:
                        st.error(output)
        
        with col2:
            if st.button("2️⃣ Analyze Sentiments", key="analyze_sentiments", use_container_width=True):
                with st.spinner("Analyzing sentiments..."):
                    success, output = run_script("data_sentiment.py")
                    if success:
                        st.success("Sentiment analysis completed!")
                        st.code(output, language="text")
                    else:
                        st.error(output)
        
        # Add last update time if data exists
        if RAW_REVIEWS_FILE.exists():
            modified_time = datetime.fromtimestamp(RAW_REVIEWS_FILE.stat().st_mtime)
            st.caption(f"Last data update: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    df = load_data()
    
    if df is not None:
        # Calculate metrics
        total_reviews = len(df)
        avg_sentiment = df['polarity'].mean()
        positive_reviews = (df['sentiment'] == 'Positive').mean() * 100
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Total Reviews</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{total_reviews:,}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Average Sentiment</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{avg_sentiment:.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Positive Reviews</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{positive_reviews:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("### 📊 Sentiment Analysis")
        
        tab1, tab2 = st.tabs(["Restaurant Comparison", "Sentiment Distribution"])
        
        with tab1:
            st.plotly_chart(create_restaurant_chart(df), use_container_width=True)
        
        with tab2:
            st.plotly_chart(create_sentiment_chart(df), use_container_width=True)
        
        # Review Explorer
        st.markdown("### 🔍 Review Explorer")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_restaurant = st.selectbox(
                "Filter by Restaurant",
                ["All Restaurants"] + sorted(df['restaurant'].unique().tolist())
            )
        
        with col2:
            selected_sentiment = st.selectbox(
                "Filter by Sentiment",
                ["All Sentiments"] + sorted(df['sentiment'].unique().tolist())
            )
        
        # Apply filters
        filtered_df = df.copy()
        if selected_restaurant != "All Restaurants":
            filtered_df = filtered_df[filtered_df['restaurant'] == selected_restaurant]
        if selected_sentiment != "All Sentiments":
            filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]
        
        # Show filtered reviews
        st.dataframe(
            filtered_df,
            column_config={
                "restaurant": st.column_config.TextColumn("Restaurant"),
                "review": st.column_config.TextColumn(
                    "Review",
                    width="large",
                ),
                "sentiment": st.column_config.TextColumn(
                    "Sentiment",
                    help="Classification of the review sentiment"
                ),
                "polarity": st.column_config.NumberColumn(
                    "Sentiment Score",
                    help="Numerical score from -1 (most negative) to 1 (most positive)",
                    format="%.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
    else:
        st.error("""
        ### No Data Found! 
        
        Please use the buttons above to generate and analyze the data:
        
        1. Click "Generate Reviews" to create AI-generated restaurant reviews
        2. Click "Analyze Sentiments" to process the reviews
        
        The dashboard will automatically update once the data is ready.
        """)

if __name__ == "__main__":
    main()
