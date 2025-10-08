#!/usr/bin/env python3
"""
Quick demo script to test the fake news detector
"""
import pickle
import re

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Test samples
test_samples = [
    {
        "text": "Scientists at MIT have developed a new renewable energy technology that could revolutionize solar power generation, according to a peer-reviewed study published in Nature Energy.",
        "expected": "Real"
    },
    {
        "text": "BREAKING: Aliens have landed in New York City and the government is trying to cover it up! Share this before they delete it!",
        "expected": "Fake"
    },
    {
        "text": "The Federal Reserve announced a 0.25% interest rate cut following their monthly meeting, citing concerns about economic growth.",
        "expected": "Real"
    },
    {
        "text": "Local man discovers cure for all diseases using this one weird trick that doctors don't want you to know!",
        "expected": "Fake"
    },
    {
        "text": "Climate change researchers at NASA report that global temperatures have risen by 1.2 degrees Celsius since pre-industrial times.",
        "expected": "Real"
    },
    {
        "text": "SHOCKING: Celebrities are secretly lizard people controlling the world government - proof inside!",
        "expected": "Fake"
    }
]

print("🔍 Fake News Detector Demo")
print("=" * 50)
print("Testing model accuracy with sample articles...\n")

correct_predictions = 0
total_predictions = len(test_samples)

for i, sample in enumerate(test_samples, 1):
    text = sample["text"]
    expected = sample["expected"]
    
    processed = preprocess_text(text)
    text_vec = vectorizer.transform([processed])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    result = "Real" if prediction == 1 else "Fake"
    confidence = max(probability) * 100
    
    # Check if prediction matches expected
    is_correct = (result == expected)
    if is_correct:
        correct_predictions += 1
    
    status_icon = "✅" if is_correct else "❌"
    
    print(f"{i}. {status_icon} Expected: {expected} | Predicted: {result} ({confidence:.1f}%)")
    print(f"   Text: {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"   Real: {probability[1]*100:.1f}% | Fake: {probability[0]*100:.1f}%")
    print()

accuracy = (correct_predictions / total_predictions) * 100
print(f"Demo Accuracy: {correct_predictions}/{total_predictions} ({accuracy:.1f}%)")

print(f"\n🚀 Start the web app with: python app.py")
print(f"   Then open: http://127.0.0.1:5000")