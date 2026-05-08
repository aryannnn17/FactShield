# FactShield - Intelligent Fake News Detection System

A modern web application that uses multiple machine learning models to detect fake news articles with high accuracy.

🌐 **Live Demo**: [https://factshield-three.vercel.app](https://factshield-three.vercel.app)

![Fake News Detection](https://img.shields.io/badge/Fake%20News%20Detection-AI%20Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-3.1%2B-lightgrey)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000)

## 🛡️ Features

- **Multi-Model Analysis**: Uses 5 different ML models for comprehensive analysis
- **Advanced AI**: Powered by RoBERTa transformer model for superior accuracy
- **Professional UI**: Modern glassmorphism design with dark/light theme toggle
- **Real-time Analysis**: Instant predictions with confidence scores
- **Weighted Consensus**: Smart voting system with RoBERTa getting double weight
- **Visual Analytics**: Interactive charts showing model confidence levels

## 🤖 ML Models Used

1. **🤖 RoBERTa** - Advanced transformer model with superior contextual understanding (2x voting weight)
2. **⚡ XGBoost** - Optimized gradient boosting for high-performance classification
3. **🌲 Random Forest** - Ensemble decision trees for robust pattern detection
4. **💡 LightGBM** - Fast gradient boosting framework with excellent speed
5. **📊 Logistic Regression** - Linear classification model for baseline comparison

## 📋 Repository Description

**FactShield** is an advanced fake news detection system that leverages the power of ensemble machine learning combined with cutting-edge transformer technology. Our system analyzes news articles using 5 different models, with RoBERTa (a state-of-the-art transformer) given double voting weight due to its superior accuracy.

### 🎯 Key Highlights:
- **🔬 Multi-Model Approach**: Combines traditional ML (XGBoost, Random Forest, LightGBM, Logistic Regression) with advanced AI (RoBERTa)
- **⚖️ Weighted Consensus**: Smart voting system where RoBERTa's predictions count twice, ensuring higher accuracy
- **🎨 Professional UI**: Modern glassmorphism design with dark/light theme toggle and responsive layout
- **📊 Visual Analytics**: Interactive charts showing confidence scores for each model
- **🚀 Production Ready**: Optimized for deployment with environment variable support

### 💡 Innovation:
Our weighted consensus mechanism ensures that while we benefit from diverse model perspectives, the most accurate model (RoBERTa) has proportionally more influence on the final decision, resulting in superior overall accuracy compared to single-model approaches.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/aryannnn17/Fake-News-Detection.git
   cd Fake-News-Detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application**
   ```bash
   python app.py
   ```

4. **Access application**
   Open your browser and go to `http://127.0.0.1:5000`

## 📁 Project Structure

```
FactShield/
├── app.py                    # Original Flask app with ML models (local)
├── app_simple.py             # Lightweight version for Vercel deployment
├── api/
│   └── index.py             # Vercel serverless function handler
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html           # Frontend UI with glassmorphism design
├── models/                  # Trained ML models (excluded from Vercel)
│   ├── xgboost_model.pkl
│   ├── random_forest_model.pkl
│   ├── light_gbm_model.pkl
│   ├── logistic_regression_model.pkl
│   └── vectorizer.pkl
├── vercel.json             # Vercel configuration
├── package.json            # Node.js configuration for Vercel
├── .vercelignore          # Files excluded from deployment
└── README.md              # This file
```

## 🎯 How It Works

1. **Input**: User enters news article text
2. **Preprocessing**: Text is cleaned and tokenized
3. **Prediction**: All 5 models analyze text
4. **Consensus**: Weighted voting determines final result
5. **Display**: Results shown with confidence scores and visualizations

## 🎨 UI Features

- **Responsive Design**: Works on all devices
- **Theme Toggle**: Switch between light and dark modes
- **Glassmorphism**: Modern frosted glass effect
- **Animated Elements**: Smooth transitions and micro-interactions
- **Professional Layout**: Clean, intuitive interface

## 🔧 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Frameworks**: scikit-learn, XGBoost, LightGBM
- **AI Model**: RoBERTa (Hugging Face Transformers)
- **Deployment**: Vercel Serverless Functions
- **Visualization**: Chart.js
- **Icons**: Font Awesome
- **Styling**: CSS Variables, Glassmorphism

## 📊 Model Performance

- **RoBERTa**: Highest accuracy, gets double voting weight
- **Traditional Models**: Provide diverse perspectives
- **Ensemble Approach**: Combines strengths of all models
- **Confidence Scores**: Shows model certainty levels

## 🌟 Why FactShield?

- **Accuracy**: Multiple models provide better accuracy than single approaches
- **Reliability**: Ensemble method reduces false positives/negatives
- **User-Friendly**: Simple interface for non-technical users
- **Professional**: Suitable for enterprise deployment
- **Open Source**: Transparent and customizable

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under MIT License.

## 👨‍💻 Author

Created with ❤️ by **Aryan**

- **GitHub**: [aryannnn17](https://github.com/aryannnn17)
- **Project**: [FactShield](https://github.com/aryannnn17/Fake-News-Detection)

---

**Made with ❤️ by Aryan | © 2024 FactShield**
