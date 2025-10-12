import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle
import re

def preprocess_text(text):
    """Clean and preprocess text data"""
    text = str(text).lower()
    # Remove URLs, emails, and special characters but keep some punctuation
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'[^a-zA-Z\s.,!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_model():
    # Load data
    data_fake = pd.read_csv('data/Fake.csv')
    data_true = pd.read_csv('data/True.csv')
    
    # Add labels
    data_fake['label'] = 0
    data_true['label'] = 1
    
    # Combine datasets
    data = pd.concat([data_fake, data_true], ignore_index=True)
    
    # Remove rows with missing text
    data = data.dropna(subset=['title', 'text'])
    
    # Combine title and text for better features
    data['content'] = data['title'] + ' ' + data['text']
    
    # Preprocess text
    data['content'] = data['content'].apply(preprocess_text)
    
    # Remove very short articles
    data = data[data['content'].str.len() > 50]
    
    # Prepare features and labels
    X = data['content']
    y = data['label']
    
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Vectorize text with better parameters
    vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model with balanced class weights
    model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Model and vectorizer saved successfully!")

if __name__ == "__main__":
    train_model()