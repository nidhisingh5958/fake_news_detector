import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import warnings
from news_fetcher import NewsFetcher
warnings.filterwarnings('ignore')

class AIFakeNewsDetector:
    def __init__(self, use_pretrained=True):
        """
        Initialize the AI-powered fake news detector.
        
        Args:
            use_pretrained: Use pre-trained transformer model (requires internet)
        """
        self.use_pretrained = use_pretrained
        self.news_fetcher = NewsFetcher()
        
        if use_pretrained:
            print("🔄 Loading AI model... This may take a moment on first run.")
            try:
                # Using DistilBERT for fake news detection
                self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    "distilbert-base-uncased",
                    num_labels=2
                )
                self.model.eval()
                print("✅ AI model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not load transformer model: {e}")
                print("Falling back to traditional ML features only.")
                self.use_pretrained = False
        
        # Feature extraction
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
        # Linguistic features
        self.sensational_words = [
            'shocking', 'unbelievable', 'mind-blowing', 'devastating',
            'horrifying', 'incredible', 'jaw-dropping', 'explosive',
            'bombshell', 'stunning', 'outrageous', 'unprecedented'
        ]
        
        self.emotional_words = [
            'outrage', 'furious', 'terrifying', 'disgusting', 'alarming',
            'scary', 'panic', 'crisis', 'disaster', 'threat', 'danger'
        ]

    def extract_linguistic_features(self, text):
        """Extract linguistic and stylistic features."""
        features = {}
        
        # Basic statistics
        features['length'] = len(text)
        features['word_count'] = len(text.split())
        features['avg_word_length'] = np.mean([len(word) for word in text.split()]) if text.split() else 0
        
        # Punctuation analysis
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['caps_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Sensational language
        lower_text = text.lower()
        features['sensational_count'] = sum(1 for word in self.sensational_words if word in lower_text)
        features['emotional_count'] = sum(1 for word in self.emotional_words if word in lower_text)
        
        # Source indicators
        features['has_quotes'] = int(bool(re.search(r'"[^"]+"', text)))
        features['has_attribution'] = int(bool(re.search(r'according to|said|reported|stated', text, re.I)))
        features['has_url'] = int(bool(re.search(r'https?://', text)))
        
        # Clickbait patterns
        clickbait_patterns = [
            r'you won\'t believe', r'what happened next', r'this one trick',
            r'\d+ (reasons|ways|things)', r'shocking truth'
        ]
        features['clickbait_count'] = sum(1 for p in clickbait_patterns if re.search(p, text, re.I))
        
        # Sentence complexity
        sentences = text.split('.')
        features['sentence_count'] = len(sentences)
        features['avg_sentence_length'] = features['word_count'] / features['sentence_count'] if features['sentence_count'] > 0 else 0
        
        return features

    def get_transformer_prediction(self, text):
        """Get prediction from transformer model."""
        if not self.use_pretrained:
            return None, None
        
        try:
            # Tokenize and predict
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                prediction = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][prediction].item()
            
            return prediction, confidence
        except Exception as e:
            print(f"⚠️ Transformer prediction error: {e}")
            return None, None

    def analyze(self, text, url=None):
        """Perform AI-powered analysis on text."""
        if not text.strip():
            return {'error': 'No text provided for analysis'}
        
        # Extract linguistic features
        linguistic_features = self.extract_linguistic_features(text)
        
        # Check news relevance
        news_relevance = self.news_fetcher.check_news_relevance(text)
        
        # Get AI prediction
        ai_prediction = None
        ai_confidence = 0.5
        
        if self.use_pretrained:
            pred, conf = self.get_transformer_prediction(text)
            if pred is not None:
                ai_prediction = pred
                ai_confidence = conf
        
        # Calculate risk scores from linguistic features
        risk_scores = self._calculate_risk_scores(linguistic_features, news_relevance)
        
        # Combine AI and rule-based scores
        if ai_prediction is not None:
            # AI prediction: 1 = fake, 0 = real
            ai_risk_score = ai_prediction * 100 * ai_confidence
            combined_risk = (ai_risk_score * 0.5 + risk_scores['overall'] * 0.5)
        else:
            combined_risk = risk_scores['overall']
        
        credibility_score = 100 - combined_risk
        verdict_level, verdict_message = self._get_verdict(combined_risk)
        
        analysis = {
            'url': url,
            'risk_score': round(combined_risk, 1),
            'credibility_score': round(credibility_score, 1),
            'verdict_level': verdict_level,
            'verdict_message': verdict_message,
            'ai_prediction': {
                'available': ai_prediction is not None,
                'prediction': 'Likely Fake' if ai_prediction == 1 else 'Likely Real' if ai_prediction == 0 else 'N/A',
                'confidence': round(ai_confidence * 100, 1) if ai_prediction is not None else 0
            },
            'linguistic_features': linguistic_features,
            'risk_indicators': risk_scores['indicators'],
            'news_relevance': news_relevance
        }
        
        return analysis

    def _calculate_risk_scores(self, features, news_relevance):
        """Calculate risk scores from linguistic features and news relevance."""
        indicators = {}
        
        # Sensationalism
        sens_score = min(features['sensational_count'] * 15 + features['exclamation_count'] * 5, 100)
        indicators['sensationalism'] = {
            'score': sens_score,
            'message': f"Sensational language: {features['sensational_count']} instances, {features['exclamation_count']} exclamations"
        }
        
        # Source credibility
        source_indicators = features['has_quotes'] + features['has_attribution'] + features['has_url']
        source_score = 80 if source_indicators == 0 else 50 if source_indicators == 1 else 20
        indicators['sources'] = {
            'score': source_score,
            'message': f"Source indicators: {source_indicators}/3 found"
        }
        
        # Emotional manipulation
        emot_score = min(features['emotional_count'] * 12 + features['caps_ratio'] * 50, 100)
        indicators['emotional'] = {
            'score': emot_score,
            'message': f"Emotional language: {features['emotional_count']} instances, {features['caps_ratio']:.1%} caps"
        }
        
        # Clickbait
        click_score = min(features['clickbait_count'] * 30, 100)
        indicators['clickbait'] = {
            'score': click_score,
            'message': f"Clickbait patterns: {features['clickbait_count']} detected"
        }
        
        # News relevance check - vague content gets higher risk
        relevance_score = news_relevance['relevance_score']
        if relevance_score < 5:  # Very low relevance to current news
            vague_score = 70  # High risk for vague content
        elif relevance_score < 15:
            vague_score = 40  # Medium risk
        else:
            vague_score = 10  # Low risk for news-relevant content
        
        indicators['news_relevance'] = {
            'score': vague_score,
            'message': f"News relevance: {relevance_score:.1f}% - {'Low relevance to current events' if vague_score > 50 else 'Related to current news'}"
        }
        
        # Calculate overall with news relevance factor
        overall = (sens_score * 0.2 + source_score * 0.25 + 
                  emot_score * 0.2 + click_score * 0.15 + vague_score * 0.2)
        
        return {'overall': overall, 'indicators': indicators}

    def _get_verdict(self, score):
        """Determine risk level based on score."""
        if score >= 65:
            return 'HIGH RISK', 'Strong indicators of potential misinformation or vague content detected'
        elif score >= 35:
            return 'MEDIUM RISK', 'Some indicators of potential misinformation or unclear content detected'
        else:
            return 'LOW RISK', 'Content appears credible and relevant to current events'