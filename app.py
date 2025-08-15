import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime

# Import your live API function
from data_sentiment import analyze_sentiment

# Constants
DATA_DIR = Path("data")
RAW_REVIEWS_FILE = DATA_DIR / "raw_reviews.json"
PROCESSED_REVIEWS_FILE = DATA_DIR / "surat_restaurant_reviews.csv"
TSV_FILE = DATA_DIR / "Restaurant_Reviews.tsv"

# ---------------------------------------------------------
# Streamlit Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Surat Restaurant Sentiment Analysis",
    page_icon="🍽️",
    layout="wide"
)

@st.cache_data
def load_processed_data():
    if PROCESSED_REVIEWS_FILE.exists():
        return pd.read_csv(PROCESSED_REVIEWS_FILE)
    return None

@st.cache_data
def analyze_tsv_reviews():
    """
    Loads Restaurant_Reviews.tsv and analyzes each review using the live API.
    Caches the results to avoid re-processing.
    """
    if not TSV_FILE.exists():
        return None

    df_raw = pd.read_csv(TSV_FILE, sep="\t")  # columns: Review, Liked
    results = []
    for _, row in df_raw.iterrows():
        api_res = analyze_sentiment(row["Review"])
        results.append({
            "Review": row["Review"],
            "OriginalLiked": row["Liked"],
            "APISentiment": api_res.get("sentiment", "Error"),
            "Polarity": api_res.get("polarity", 0.0)
        })
    return pd.DataFrame(results)

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

# ---------------------------------------------------------
# Visualization Helpers
# ---------------------------------------------------------
def show_tsv_analysis(df):
    """
    Visualizes comparison between original TSV ratings and API results.
    """
    df["OriginalSentiment"] = df["OriginalLiked"].map({1: "Positive", 0: "Negative"})
    accuracy = (df["OriginalSentiment"] == df["APISentiment"]).mean() * 100

    st.subheader("TSV Review Analysis")
    st.metric("Total Reviews", len(df))
    st.metric("API Accuracy", f"{accuracy:.1f}%")
    st.metric("Average Polarity", f"{df['Polarity'].mean():.2f}")

    # Comparison bar chart
    comp = df.groupby(["OriginalSentiment", "APISentiment"]).size().reset_index(name="count")
    comp_fig = px.bar(
        comp,
        x="OriginalSentiment",
        y="count",
        color="APISentiment",
        title="Original vs API-reviewed Sentiment"
    )
    st.plotly_chart(comp_fig, use_container_width=True)

    # Polarity distribution histogram
    pol_fig = px.histogram(
        df,
        x="Polarity",
        nbins=30,
        title="Polarity Score Distribution"
    )
    st.plotly_chart(pol_fig, use_container_width=True)

    # Filterable review table
    st.markdown("### Detailed Results")
    col1, col2 = st.columns(2)
    with col1:
        o_filter = st.selectbox("Filter by Original", ["All"] + df["OriginalSentiment"].unique().tolist())
    with col2:
        a_filter = st.selectbox("Filter by API", ["All"] + df["APISentiment"].unique().tolist())

    df_show = df.copy()
    if o_filter != "All":
        df_show = df_show[df_show["OriginalSentiment"] == o_filter]
    if a_filter != "All":
        df_show = df_show[df_show["APISentiment"] == a_filter]

    st.dataframe(df_show, use_container_width=True)

# ---------------------------------------------------------
# Main App
# ---------------------------------------------------------
def main():
    st.title("🍽️ Surat Restaurant Sentiment Analysis")

    # Data Generation Buttons
    st.markdown("### 🔄 Data Generation")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("1️⃣ Generate Reviews (Gemini)"):
            with st.spinner("Running agent.py ..."):
                ok, out = run_script("agent.py")
                st.success("Done!") if ok else st.error(out)
    with c2:
        if st.button("2️⃣ Analyze Sentiments (CSV)"):
            with st.spinner("Running data_sentiment.py ..."):
                ok, out = run_script("data_sentiment.py")
                st.success("Done!") if ok else st.error(out)
    with c3:
        if st.button("3️⃣ Analyze Reviews from TSV"):
            st.session_state["tsv_analysis"] = True

    # Load CSV Dashboard
    csv_df = load_processed_data()
    if csv_df is not None:
        st.markdown("### 📊 Restaurant Dashboard (CSV)")
        total = len(csv_df)
        pos = (csv_df["sentiment"] == "Positive").sum()
        st.metric("Total Reviews", total)
        st.metric("Positive Reviews", pos)

        avg_fig = px.bar(csv_df.groupby("restaurant")["polarity"].mean().reset_index(),
                         x="polarity", y="restaurant", orientation="h",
                         title="Average Sentiment by Restaurant")
        st.plotly_chart(avg_fig, use_container_width=True)

    # TSV Analysis Section
    if st.session_state.get("tsv_analysis"):
        if not TSV_FILE.exists():
            st.error("Restaurant_Reviews.tsv not found in /data.")
        else:
            with st.spinner("Analyzing TSV reviews..."):
                tsv_df = analyze_tsv_reviews()
            show_tsv_analysis(tsv_df)
        st.session_state["tsv_analysis"] = False

if __name__ == "__main__":
    main()
