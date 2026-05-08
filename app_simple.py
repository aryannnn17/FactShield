from flask import Flask, render_template, request
import re
import os

# Create an app object using the flask class
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Production deployment configuration
port = int(os.environ.get('PORT', 5000))
host = os.environ.get('HOST', '0.0.0.0')

# Simple stopwords list (no NLTK dependency)
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
    'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
    'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 
    'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
    'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
}

# Lightweight text analysis functions
def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def preprocess(text):
    text = clean(text)
    tokens = [word for word in text.split() if word not in STOP_WORDS]
    return ' '.join(tokens)

def simple_sentiment_analysis(text):
    """Simple rule-based analysis for demonstration"""
    fake_indicators = [
        'shocking', 'unbelievable', 'secret', 'revealed', 'conspiracy',
        'hoax', 'fake', 'false', 'lie', 'misleading', 'debunked', 'scam',
        'bizarre', 'incredible', 'amazing', 'miracle', 'breakthrough'
    ]
    real_indicators = [
        'study', 'research', 'according', 'official', 'confirmed',
        'verified', 'evidence', 'data', 'report', 'analysis', 'scientist',
        'expert', 'doctor', 'professor', 'university', 'journal', 'published'
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
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    # Feature extraction
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    avg_sentence_length = sum(len(sent.split()) for sent in sentences) / len(sentences) if sentences else 0
    exclamation_count = text.count('!')
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

def analyze_credibility_indicators(text):
    """Check for credibility indicators"""
    credibility_indicators = [
        'source said', 'according to', 'reported', 'stated', 'announced',
        'claimed', 'alleged', 'sources say', 'experts say', 'officials say'
    ]
    
    text_lower = text.lower()
    credibility_count = sum(1 for indicator in credibility_indicators if indicator in text_lower)
    
    if credibility_count >= 3:
        return "REAL", min(75, 40 + credibility_count * 10)
    elif credibility_count >= 1:
        return "UNCERTAIN", 55
    else:
        return "FAKE", 45

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
    results["Keyword Analysis"] = {
        "label": sentiment_label,
        "confidence": sentiment_confidence
    }
    
    # Method 2: Text feature analysis
    feature_label, feature_confidence = analyze_text_features(article)
    results["Style Analysis"] = {
        "label": feature_label,
        "confidence": feature_confidence
    }
    
    # Method 3: Credibility indicators
    credibility_label, credibility_confidence = analyze_credibility_indicators(article)
    results["Credibility Check"] = {
        "label": credibility_label,
        "confidence": credibility_confidence
    }
    
    # Method 4: Length-based analysis
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
    
    if fake_votes > real_votes:
        consensus = "FAKE"
    elif real_votes > fake_votes:
        consensus = "REAL"
    else:
        consensus = "UNCERTAIN"
    
    # Descriptions for each method
    descriptions = {
        "Keyword Analysis": "Analyzes for fake news indicators and credible sources",
        "Style Analysis": "Evaluates writing style and emotional language patterns",
        "Credibility Check": "Looks for source attribution and reporting indicators",
        "Length Analysis": "Assesses article length and complexity"
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
