from flask import Flask, render_template, request, jsonify
from fake_news_detector import AIFakeNewsDetector
import os

app = Flask(__name__)

# Initialize the detector (will try to load AI model)
detector = None

def init_detector():
    global detector
    if detector is None:
        try:
            detector = AIFakeNewsDetector(use_pretrained=True)
        except Exception as e:
            print(f"Error initializing detector: {e}")
            detector = AIFakeNewsDetector(use_pretrained=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        if detector is None:
            init_detector()
        
        data = request.get_json()
        text = data.get('text', '').strip()
        url = data.get('url', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided for analysis'}), 400
        
        # Perform analysis
        result = detector.analyze(text, url if url else None)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'ai_model_available': detector.use_pretrained if detector else False
    })

if __name__ == '__main__':
    init_detector()
    app.run(debug=True, host='0.0.0.0', port=5000)