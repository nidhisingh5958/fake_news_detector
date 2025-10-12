# AI Fake News Detector

A modern web application that uses AI and linguistic analysis to detect potential misinformation in news articles and text content.

## Features

- **AI-Powered Analysis**: Uses DistilBERT transformer model for advanced text classification
- **Real-Time News Verification**: Fetches current news from multiple credible sources (Reuters, BBC, AP, NPR, CNN)
- **Vague Content Detection**: Identifies and flags vague or non-specific content that lacks news relevance
- **Linguistic Analysis**: Analyzes sensational language, emotional manipulation, clickbait patterns
- **Visual Dashboard**: Modern, responsive web interface with real-time results
- **Risk Scoring**: Comprehensive risk assessment with detailed indicators
- **Mobile Friendly**: Fully responsive design that works on all devices

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Enter Text**: Paste news article text or content you want to analyze
2. **Optional URL**: Add the source URL for reference
3. **Analyze**: Click the "Analyze Content" button
4. **Review Results**: Get comprehensive analysis including:
   - Risk and credibility scores
   - AI model predictions
   - Linguistic risk indicators
   - News relevance scoring
   - Current news keyword matching
   - Text statistics

## AI Architecture

This system uses a **hybrid AI approach** combining multiple techniques for maximum accuracy:

### **1. Transformer-Based Deep Learning (60% weight)**
- **Model**: DistilBERT (Distilled BERT)
- **Type**: Pre-trained transformer for sequence classification
- **Purpose**: Core AI prediction using attention mechanisms
- **Fallback**: Graceful degradation to rule-based analysis if model unavailable

### **2. Retrieval-Augmented Generation (RAG) (20% weight)**
- **Real-time Data**: Fetches current news from Reuters, BBC, AP, NPR, CNN
- **Knowledge Base**: Uses live news as reference for relevance checking
- **Vague Content Detection**: Penalizes text with low relevance to current events
- **Keyword Matching**: Compares input against legitimate news topics

### **3. Traditional ML & Rule-Based (20% weight)**
- **TF-IDF Vectorization**: Text feature extraction
- **Linguistic Analysis**: Detects sensational language, clickbait patterns
- **Expert Rules**: Source credibility indicators, emotional manipulation
- **Ensemble Scoring**: Weighted combination of all risk factors

### **Hybrid Decision Process:**
```
Input Text → [DistilBERT AI] + [News RAG Check] + [Linguistic Rules] → Risk Score
```

## Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: DistilBERT (Hugging Face Transformers)
- **ML Libraries**: scikit-learn, PyTorch
- **News Sources**: RSS feeds from major news outlets
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome

## API Endpoints

- `GET /` - Main application interface
- `POST /analyze` - Analyze text content
- `GET /health` - Health check endpoint

## How It Works

1. **AI Analysis**: DistilBERT transformer analyzes text patterns and language structure
2. **News Verification**: System fetches current news and compares input relevance
3. **Linguistic Scoring**: Rule-based analysis detects suspicious patterns
4. **Risk Assessment**: All factors combined into final credibility score
5. **Vague Content Penalty**: Non-specific text gets higher risk scores

## Disclaimer

This hybrid AI tool provides indicators of potential misinformation but is not definitive. The RAG component helps identify vague content by comparing against current legitimate news. Always verify information through multiple credible sources and fact-checking websites.