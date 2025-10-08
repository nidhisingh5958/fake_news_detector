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
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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
        
        result = {
            'prediction': 'Real News' if prediction == 1 else 'Fake News',
            'confidence': float(max(probability)) * 100,
            'fake_probability': float(probability[0]) * 100,
            'real_probability': float(probability[1]) * 100
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)