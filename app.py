from flask import Flask, render_template, request
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

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

# Load models and vectorizer once
xgboost_model = joblib.load("models/xgboost_model.pkl")
random_forest_model = joblib.load("models/random_forest_model.pkl")
lightgbm_model = joblib.load("models/light_gbm_model.pkl")
logistic_regression_model = joblib.load("models/logistic_regression_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

# Load RoBERTa model
try:
    roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-base')
    roberta_model = AutoModelForSequenceClassification.from_pretrained('roberta-base', num_labels=2)
    roberta_available = True
    print("✅ RoBERTa model loaded successfully")
except Exception as e:
    print(f"❌ Error loading RoBERTa: {e}")
    roberta_available = False

models = {
    "XGBoost": xgboost_model,
    "Random Forest": random_forest_model,
    "LightGBM": lightgbm_model,
    "Logistic Regression": logistic_regression_model
}

if roberta_available:
    models["RoBERTa"] = roberta_model


def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


def preprocess(text):
    text = clean(text)
    tokens = [portStemmer.stem(word)
              for word in text.split() if word not in stop_words]
    return ' '.join(tokens)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    article = request.form['article']

    results, consensus = predict_single_article(article, return_detailed=True)

    # Add description for each model
    descriptions = {
        "XGBoost": "An optimized gradient boosting library designed for high performance.",
        "Random Forest": "An ensemble of decision trees trained on random subsets of data.",
        "LightGBM": "A fast, gradient-boosting framework using tree-based learning algorithms.",
        "Logistic Regression": "A simple linear model for binary classification problems."
    }
    
    if roberta_available:
        descriptions["RoBERTa"] = "A robustly optimized BERT approach for superior language understanding."

    # Pass article back to the template so it remains in the textarea
    return render_template('index.html',
                           results=results,
                           consensus=consensus,
                           descriptions=descriptions,
                           article=article)  # Pass the article text back


def predict_with_roberta(article):
    """Make prediction using RoBERTa model"""
    try:
        # Tokenize the input
        inputs = roberta_tokenizer(article, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # Get model prediction
        with torch.no_grad():
            outputs = roberta_model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probs, dim=-1).item()
            confidence = probs[0][prediction].item() * 100
        
        label = "FAKE" if prediction == 1 else "REAL"
        return label, confidence
    except Exception as e:
        print(f"❌ RoBERTa prediction error: {e}")
        return "REAL", 50.0  # Fallback


def predict_single_article(article, return_detailed=False):
    model_results = {}

    # Run traditional ML models
    processed_article = preprocess(article)
    article_vectorized = vectorizer.transform([processed_article])
    
    for name, model in models.items():
        if name == "RoBERTa":
            continue  # Handle RoBERTa separately
        prob = model.predict_proba(article_vectorized)[0]
        prediction = model.predict(article_vectorized)[0]
        confidence = max(prob) * 100
        label = "FAKE" if prediction == 1 else "REAL"
        model_results[name] = {
            "label": label,
            "confidence": confidence
        }

    # Run RoBERTa if available
    if roberta_available:
        label, confidence = predict_with_roberta(article)
        model_results["RoBERTa"] = {
            "label": label,
            "confidence": confidence
        }

    # Sort by confidence descending
    model_results = dict(sorted(model_results.items(),
                         key=lambda item: item[1]['confidence'], reverse=True))

    # Calculate consensus with weighted voting (RoBERTa gets double weight)
    votes = []
    for name, info in model_results.items():
        weight = 2 if name == "RoBERTa" else 1
        votes.extend([info['label']] * weight)
    
    consensus_label = "FAKE" if votes.count("FAKE") > len(votes) / 2 else "REAL"

    if return_detailed:
        return model_results, consensus_label
    else:
        return {
            "article": article,
            "results": model_results,
            "consensus": consensus_label
        }


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=False, host=host, port=port)
