# Fake News Detector

A machine learning project to detect false news and reporting utilizing Natural Language Processing (NLP). The model uses logistic regression with TF-IDF vectorization to classify news articles as real or fake based on content analysis.

## Features

- **Web Interface**: Clean, responsive web application for easy news analysis
- **High Accuracy**: Achieves 98.94% accuracy on test data
- **Real-time Predictions**: Instant classification with confidence scores
- **Text Preprocessing**: Advanced NLP preprocessing for better accuracy
- **Visual Results**: Progress bars showing real vs fake news probabilities

## Tech Stack

- **Language**: Python
- **Web Framework**: Flask
- **ML Libraries**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Model**: Logistic Regression with TF-IDF Vectorization

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model** (if not already trained):
   ```bash
   python train_model.py
   ```

3. **Run the web application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to: `http://127.0.0.1:8000`

## Usage

### Web Interface
1. Open the web application in your browser
2. Paste or type news article text in the text area
3. Click "Analyze News" to get predictions
4. View results with confidence scores and probability breakdown

### Command Line Demo
```bash
python demo.py
```

## Model Performance

- **Accuracy**: 98.94%
- **Precision**: 99%
- **Recall**: 99%
- **F1-Score**: 99%
