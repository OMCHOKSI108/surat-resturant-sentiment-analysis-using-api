# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime

# Constants
DATA_DIR = Path("data")
RAW_REVIEWS_FILE = DATA_DIR / "raw_reviews.json"
PROCESSED_REVIEWS_FILE = DATA_DIR / "surat_restaurant_reviews.csv"

# Page configuration
st.set_page_config(
    page_title="Surat Restaurant Sentiment Analysis",
    page_icon="🍽️",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache the restaurant review data"""
    try:
        # First try to load processed CSV file
        if PROCESSED_REVIEWS_FILE.exists():
            df = pd.read_csv(PROCESSED_REVIEWS_FILE)
            if all(col in df.columns for col in ['restaurant', 'review', 'sentiment', 'polarity']):
                return df
        
        # If CSV doesn't exist or is invalid, try loading from raw JSON
        if RAW_REVIEWS_FILE.exists():
            with open(RAW_REVIEWS_FILE, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                df = pd.DataFrame(raw_data)
                # Keep only necessary columns
                if 'review' in df.columns and 'restaurant' in df.columns:
                    return df
                
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_restaurant_chart(df):
    """Create restaurant sentiment chart"""
    if 'restaurant' not in df.columns or 'sentiment' not in df.columns:
        return None
        
    avg_sentiment = df.groupby('restaurant')['sentiment'].agg(
        positive_count=lambda x: (x == 'Positive').sum(),
        total_count='size'
    ).reset_index()
    
    avg_sentiment['positive_percentage'] = (avg_sentiment['positive_count'] / avg_sentiment['total_count']) * 100
    
    fig = px.bar(
        avg_sentiment,
        x='positive_percentage',
        y='restaurant',
        orientation='h',
        title='Restaurant Performance by Positive Reviews',
        labels={
            'positive_percentage': 'Positive Reviews (%)',
            'restaurant': 'Restaurant'
        },
        color='positive_percentage',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Positive Reviews (%)",
        yaxis_title="Restaurant"
    )
    
    return fig

def create_sentiment_distribution(df):
    """Create sentiment distribution chart"""
    if 'sentiment' not in df.columns:
        return None
        
    sentiment_counts = df['sentiment'].value_counts()
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Sentiment Distribution',
        color=sentiment_counts.index,
        color_discrete_map={
            'Positive': '#2ECC71',
            'Negative': '#E74C3C',
            'Neutral': '#95A5A6'
        }
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
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
            if st.button("1️⃣ Generate Reviews", use_container_width=True):
                with st.spinner("Generating reviews using AI..."):
                    success, output = run_script("agent.py")
                    if success:
                        st.success("Reviews generated successfully!")
                        st.code(output, language="text")
                    else:
                        st.error(output)
        
        with col2:
            if st.button("2️⃣ Analyze Sentiments", use_container_width=True):
                with st.spinner("Analyzing sentiments..."):
                    success, output = run_script("data_sentiment.py")
                    if success:
                        st.success("Sentiment analysis completed!")
                        st.code(output, language="text")
                    else:
                        st.error(output)
    
    # Load and display data
    df = load_data()
    
    if df is not None and not df.empty:
        # Display metrics
        total_reviews = len(df)
        positive_reviews = df[df['sentiment'] == 'Positive'].shape[0]
        positive_percentage = (positive_reviews / total_reviews) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reviews", f"{total_reviews:,}")
        with col2:
            st.metric("Positive Reviews", f"{positive_reviews:,}")
        with col3:
            st.metric("Positive Percentage", f"{positive_percentage:.1f}%")
        
        # Create visualizations
        st.markdown("### 📊 Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            restaurant_chart = create_restaurant_chart(df)
            if restaurant_chart:
                st.plotly_chart(restaurant_chart, use_container_width=True)
        
        with col2:
            sentiment_chart = create_sentiment_distribution(df)
            if sentiment_chart:
                st.plotly_chart(sentiment_chart, use_container_width=True)
        
        # Show filtered data
        st.markdown("### 📝 Review Details")
        
        # Add filters
        col1, col2 = st.columns(2)
        with col1:
            selected_restaurant = st.selectbox(
                "Filter by Restaurant",
                ["All"] + sorted(df['restaurant'].unique().tolist())
            )
        
        with col2:
            selected_sentiment = st.selectbox(
                "Filter by Sentiment",
                ["All"] + sorted(df['sentiment'].unique().tolist())
            )
        
        # Apply filters
        filtered_df = df.copy()
        if selected_restaurant != "All":
            filtered_df = filtered_df[filtered_df['restaurant'] == selected_restaurant]
        if selected_sentiment != "All":
            filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]
        
        # Display filtered dataframe
        st.dataframe(
            filtered_df,
            column_config={
                "restaurant": "Restaurant",
                "review": st.column_config.TextColumn(
                    "Review",
                    width="large",
                ),
                "sentiment": "Sentiment",
            },
            hide_index=True
        )
        
        # Show last update time
        if RAW_REVIEWS_FILE.exists():
            modified_time = datetime.fromtimestamp(RAW_REVIEWS_FILE.stat().st_mtime)
            st.caption(f"Last data update: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
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
