# 🍽️ Surat Restaurant Sentiment Analysis

An advanced sentiment analysis platform that combines AI-powered review collection, custom API sentiment analysis, and interactive visualization for Surat restaurants. The system supports both real-time web scraping and TSV/CSV file analysis, providing comprehensive insights into customer experiences.

## ✨ Key Features

### 🤖 Multi-Source Analysis
- **Web Scraping**: Autonomous AI agent for collecting real reviews
- **File Processing**: Support for TSV and CSV file analysis
- **API Integration**: Custom sentiment analysis service
- **Comparative Analysis**: Original vs API sentiment comparison

### 📊 Interactive Dashboard
- **Real-time Processing**
  - Live progress tracking
  - Cached results for performance
  - Instant visualization updates

### 📈 Advanced Visualizations
- Sentiment comparison charts
- Polarity distribution graphs
- Restaurant performance metrics
- Interactive filtering system

### 📋 Comprehensive Metrics
- Total review statistics
- API accuracy measurements
- Sentiment polarity analysis
- Restaurant-wise comparisons

## 🛠️ Technical Architecture

### Project Structure
```
surat-foodie-dashboard/
├── agent.py                     # AI web review collection
├── data_sentiment.py            # API sentiment processing
├── app.py                       # Streamlit dashboard
├── data/
│   ├── raw_reviews.json        # Collected raw reviews
│   ├── surat_restaurant_reviews.csv  # Processed reviews
│   └── Restaurant_Reviews.tsv  # Ground-truth dataset
├── requirements.txt
└── README.md
```

### Requirements
- Python 3.9+
- Environment setup:
  ```bash
  export GOOGLE_API_KEY=<your_api_key>
  ```
- API Endpoint:
  ```
  https://sentiment-api-service-fzdu57t2fa-uc.a.run.app/predict
  ```

## 🚀 Getting Started

### Installation
```bash
# Clone repository
git clone https://github.com/OMCHOKSI108/surat-resturant-sentiment-analysis-using-api.git
cd surat-resturant-sentiment-analysis-using-api

# Install dependencies
pip install -r requirements.txt
```

### Data Setup
1. For TSV Analysis:
   - Place `Restaurant_Reviews.tsv` in `data/` folder
   - Required columns: 
     - Review (text)
     - Liked (sentiment)

2. For Web Scraping:
   - Configure API key in environment
   - Ensure internet connectivity

### Running the Dashboard
```bash
streamlit run app.py
```

## 💡 Usage Guide

### Dashboard Controls

1. **Generate Reviews** 
   - Activates web scraping agent
   - Collects real restaurant reviews
   - Saves to CSV format

2. **Analyze Sentiments**
   - Processes collected reviews
   - Applies API sentiment analysis
   - Generates detailed metrics

3. **Analyze TSV Reviews**
   - Loads TSV file data
   - Compares with API predictions
   - Shows accuracy metrics

### Analysis Features

#### Data Processing
- Custom API integration
- Sentiment classification
- Polarity scoring
- Accuracy metrics

#### Visualization Tools
- Comparison charts
- Distribution graphs
- Interactive filters
- Detailed results table

#### Performance Features
- Progress tracking
- Data caching
- Real-time updates

## 📊 Output Analysis

### Metrics Dashboard
- Total review count
- API accuracy percentage
- Average sentiment polarity
- Restaurant-wise performance

### Interactive Components
- Sentiment comparison charts
- Polarity distribution
- Filterable results
- Detailed review analysis

## 🤝 Contributing

1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit changes:
   ```bash
   git commit -m 'Add YourFeature'
   ```
4. Push to branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open Pull Request

## 📞 Contact & Support

- GitHub: [@OMCHOKSI108](https://github.com/OMCHOKSI108)
- Project Link: [surat-resturant-sentiment-analysis-using-api](https://github.com/OMCHOKSI108/surat-resturant-sentiment-analysis-using-api)

## 📝 License

This project is licensed under the MIT License.
