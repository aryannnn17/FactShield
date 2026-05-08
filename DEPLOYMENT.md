# Vercel Deployment Instructions

## Prerequisites
- Vercel CLI installed (`npm i -g vercel`)
- Vercel account

## Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy the project
From the project root directory:
```bash
vercel --prod
```

### 4. Environment Variables (if needed)
If you need to set environment variables:
```bash
vercel env add
```

## Project Structure
```
FactShield/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── models/               # ML model files
├── templates/            # HTML templates
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel configuration
├── package.json         # Node.js configuration for Vercel
└── .vercelignore        # Files to exclude from deployment
```

## Configuration Details

### vercel.json
- Configures Python runtime
- Routes all requests to the serverless function
- Uses Python 3.9 runtime

### api/index.py
- Handles Vercel serverless function requests
- Converts between Vercel/AWS Lambda format and WSGI
- Imports and runs the Flask app

### Notes
- The app automatically handles NLTK downloads
- Models are loaded once per function invocation
- RoBERTa model loading includes error handling for serverless environment
- Static files are served through Flask

## Troubleshooting

### Cold Start Issues
- First request may be slow due to model loading
- Subsequent requests should be faster

### Memory Limitations
- Large models may hit Vercel's memory limits
- Consider using smaller models or upgrading plan if needed

### NLTK Issues
- NLTK data is downloaded on-demand
- Should work in serverless environment with the current setup
