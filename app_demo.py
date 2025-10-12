from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def analyze_text_simple(text):
    """Simple rule-based analysis for demo purposes"""
    text_lower = text.lower()
    
    # Simple fake news indicators
    fake_indicators = [
        'breaking', 'shocking', 'you won\'t believe', 'doctors hate',
        'one weird trick', 'secret', 'exposed', 'government doesn\'t want',
        'share before', 'delete', 'urgent', 'must read'
    ]
    
    real_indicators = [
        'reuters', 'associated press', 'ap news', 'bbc', 'cnn',
        'according to', 'study shows', 'research', 'university',
        'published', 'peer-reviewed'
    ]
    
    fake_score = sum(1 for indicator in fake_indicators if indicator in text_lower)
    real_score = sum(1 for indicator in real_indicators if indicator in text_lower)
    
    # Calculate scores
    total_indicators = max(1, fake_score + real_score)
    fake_probability = min(90, max(10, (fake_score / total_indicators) * 100 + 20))
    real_probability = 100 - fake_probability
    
    return {
        'fake_probability': fake_probability,
        'real_probability': real_probability,
        'prediction': 0 if fake_probability > real_probability else 1
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data['text']
        
        # Simple analysis
        analysis = analyze_text_simple(text)
        prediction = analysis['prediction']
        fake_prob = analysis['fake_probability']
        real_prob = analysis['real_probability']
        
        # Create response matching the expected format
        result = {
            'verdict_level': 'HIGH RISK' if prediction == 0 else 'LOW RISK',
            'verdict_message': 'This content appears to be fake news' if prediction == 0 else 'This content appears to be legitimate news',
            'risk_score': int(fake_prob),
            'credibility_score': int(real_prob),
            'ai_prediction': {
                'available': True,
                'prediction': 'Likely Fake' if prediction == 0 else 'Likely Real',
                'confidence': int(max(fake_prob, real_prob))
            },
            'risk_indicators': {
                'Content Analysis': {
                    'score': int(fake_prob),
                    'message': f'Rule-based analysis suggests this is {"fake" if prediction == 0 else "real"} news'
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