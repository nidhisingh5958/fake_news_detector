import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle
import re
import string

def preprocess_text(text):
    """Clean and preprocess text data"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
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
    
    # Combine title and text for better features
    data['content'] = data['title'] + ' ' + data['text']
    
    # Preprocess text
    data['content'] = data['content'].apply(preprocess_text)
    
    # Prepare features and labels
    X = data['content']
    y = data['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model
    model = LogisticRegression()
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