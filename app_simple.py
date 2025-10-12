from flask import Flask, render_template, request, jsonify
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def preprocess_text(text):
    """Clean and preprocess text data"""
    text = str(text).lower()
    # Remove URLs, emails, and special characters but keep some punctuation
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'[^a-zA-Z\s.,!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data['text']
        
        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Vectorize
        text_vec = vectorizer.transform([processed_text])
        
        # Predict
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        # Create response matching the expected format
        result = {
            'verdict_level': 'HIGH RISK' if prediction == 0 else 'LOW RISK',
            'verdict_message': 'This content appears to be fake news' if prediction == 0 else 'This content appears to be legitimate news',
            'risk_score': int(probability[0] * 100),
            'credibility_score': int(probability[1] * 100),
            'ai_prediction': {
                'available': True,
                'prediction': 'Likely Fake' if prediction == 0 else 'Likely Real',
                'confidence': int(max(probability) * 100)
            },
            'risk_indicators': {
                'AI Analysis': {
                    'score': int(probability[0] * 100),
                    'message': f'Machine learning model predicts this is {"fake" if prediction == 0 else "real"} news with {max(probability)*100:.1f}% confidence'
                }
            },
            'linguistic_features': {
                'word_count': len(text.split()),
                'sentence_count': text.count('.') + text.count('!') + text.count('?'),
                'avg_sentence_length': len(text.split()) / max(1, text.count('.') + text.count('!') + text.count('?')),
                'caps_ratio': sum(1 for c in text if c.isupper()) / max(1, len(text)),
                'exclamation_count': text.count('!'),
                'question_count': text.count('?')
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)