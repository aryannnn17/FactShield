from flask import Flask, render_template, request
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os

# Create an app object using the flask class
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Production deployment configuration
port = int(os.environ.get('PORT', 5000))
host = os.environ.get('HOST', '0.0.0.0')

# Download NLTK resources (only if not already downloaded)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
portStemmer = PorterStemmer()

# Lightweight text analysis functions
def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def preprocess(text):
    text = clean(text)
    tokens = [portStemmer.stem(word)
              for word in text.split() if word not in stop_words]
    return ' '.join(tokens)

def simple_sentiment_analysis(text):
    """Simple rule-based analysis for demonstration"""
    fake_indicators = [
        'shocking', 'unbelievable', 'secret', 'revealed', 'conspiracy',
        'hoax', 'fake', 'false', 'lie', 'misleading', 'debunked'
    ]
    real_indicators = [
        'study', 'research', 'according', 'official', 'confirmed',
        'verified', 'evidence', 'data', 'report', 'analysis'
    ]
    
    text_lower = text.lower()
    fake_score = sum(1 for word in fake_indicators if word in text_lower)
    real_score = sum(1 for word in real_indicators if word in text_lower)
    
    if fake_score > real_score:
        return "FAKE", min(80, 50 + fake_score * 10)
    elif real_score > fake_score:
        return "REAL", min(80, 50 + real_score * 10)
    else:
        return "UNCERTAIN", 50

def analyze_text_features(text):
    """Analyze text features for fake news detection"""
    words = text.split()
    sentences = text.split('.')
    
    # Feature extraction
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    avg_sentence_length = sum(len(sent.split()) for sent in sentences) / len(sentences) if sentences else 0
    exclamation_count = text.count('!')
    question_count = text.count('?')
    all_caps_count = sum(1 for word in words if word.isupper() and len(word) > 1)
    
    # Simple scoring based on features
    fake_score = 0
    if exclamation_count > 2:
        fake_score += 20
    if all_caps_count > 3:
        fake_score += 15
    if avg_sentence_length > 25:
        fake_score += 10
    if avg_word_length > 6:
        fake_score += 5
    
    confidence = min(90, max(30, 50 + fake_score))
    label = "FAKE" if fake_score > 20 else "REAL"
    
    return label, confidence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    article = request.form['article']
    
    if not article or len(article.strip()) < 50:
        return render_template('index.html',
                             error="Please enter a longer article (minimum 50 characters)",
                             article=article)
    
    # Multiple analysis methods
    results = {}
    
    # Method 1: Rule-based sentiment analysis
    sentiment_label, sentiment_confidence = simple_sentiment_analysis(article)
    results["Rule-Based Analysis"] = {
        "label": sentiment_label,
        "confidence": sentiment_confidence
    }
    
    # Method 2: Text feature analysis
    feature_label, feature_confidence = analyze_text_features(article)
    results["Text Feature Analysis"] = {
        "label": feature_label,
        "confidence": feature_confidence
    }
    
    # Method 3: Length-based analysis
    word_count = len(article.split())
    if word_count < 100:
        length_label = "UNCERTAIN"
        length_confidence = 40
    elif word_count > 500:
        length_label = "REAL"
        length_confidence = 60
    else:
        length_label = "REAL"
        length_confidence = 55
    
    results["Length Analysis"] = {
        "label": length_label,
        "confidence": length_confidence
    }
    
    # Sort by confidence descending
    results = dict(sorted(results.items(),
                         key=lambda item: item[1]['confidence'], reverse=True))
    
    # Calculate consensus
    votes = [info['label'] for info in results.values()]
    fake_votes = votes.count("FAKE")
    real_votes = votes.count("REAL")
    uncertain_votes = votes.count("UNCERTAIN")
    
    if fake_votes > real_votes:
        consensus = "FAKE"
    elif real_votes > fake_votes:
        consensus = "REAL"
    else:
        consensus = "UNCERTAIN"
    
    # Descriptions for each method
    descriptions = {
        "Rule-Based Analysis": "Uses keyword matching to identify fake news indicators",
        "Text Feature Analysis": "Analyzes writing style and text patterns",
        "Length Analysis": "Evaluates article length and complexity"
    }
    
    return render_template('index.html',
                           results=results,
                           consensus=consensus,
                           descriptions=descriptions,
                           article=article)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=False, host=host, port=port)
