# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying the College Answer Generator on various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- Python 3.11 or higher
- A Google Gemini API key ([Get one here](https://ai.google.dev/))

## 🖥️ Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/college-answer-generator.git
cd college-answer-generator
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Rename the requirements file
mv requirements-github.txt requirements.txt

# Install packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Install System Dependencies (if using OCR)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 6. Run Locally
```bash
streamlit run app.py
```

## ☁️ Streamlit Cloud

### 1. Fork/Upload to GitHub
- Fork this repository or upload your code to GitHub
- Ensure all files are committed

### 2. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository

### 3. Configure Secrets
In Streamlit Cloud dashboard:
1. Go to app settings
2. Click "Secrets"
3. Add:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

### 4. Deploy
- Streamlit Cloud will automatically detect `requirements.txt`
- Your app will be available at `https://your-app-name.streamlit.app`

## 🐳 Docker Deployment

### 1. Build Image
```bash
docker build -t college-answer-generator .
```

### 2. Run Container
```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_actual_api_key_here \
  college-answer-generator
```

### 3. Using Docker Compose
```bash
# Edit docker-compose.yml with your API key
docker-compose up -d
```

## 🌐 Heroku Deployment

### 1. Prepare Files
```bash
# Rename requirements file
mv requirements-github.txt requirements.txt

# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

### 2. Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 3. Deploy
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_actual_api_key_here
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🔧 Railway Deployment

### 1. Connect Repository
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

### 2. Configure
```bash
# Rename requirements file
mv requirements-github.txt requirements.txt
```

### 3. Add Environment Variables
In Railway dashboard:
- Add `GEMINI_API_KEY` with your API key
- Set `PORT` to 8501 (if needed)

## 📱 Replit Deployment

### 1. Import to Replit
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Import from GitHub

### 2. Configure
```bash
# Install packages
pip install streamlit google-genai pdfplumber pillow pytesseract python-docx reportlab

# Set up environment
# Add GEMINI_API_KEY to Replit Secrets
```

### 3. Run
```bash
streamlit run app.py --server.port 5000
```

## 🔒 Environment Variables

All platforms require these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

## 🐛 Troubleshooting

### Common Issues

1. **OCR not working**
   - Install tesseract-ocr system package
   - Check pytesseract installation

2. **API key errors**
   - Verify API key is correct
   - Check quota limits on Google AI Studio

3. **Port issues**
   - Ensure correct port configuration for platform
   - Check firewall settings

4. **Dependencies not found**
   - Verify requirements.txt is in root directory
   - Check Python version compatibility

### Platform-Specific Issues

#### Streamlit Cloud
- Use secrets.toml format for environment variables
- Ensure repository is public or properly connected

#### Heroku
- Add system dependencies to Aptfile if needed
- Configure proper buildpacks

#### Docker
- Expose correct port (8501)
- Mount volumes for persistent data

## 📞 Support

If you encounter issues:
1. Check the logs for specific error messages
2. Verify all environment variables are set
3. Ensure API key has sufficient quota
4. Review platform-specific documentation

## 🔄 Updates

To update your deployment:
1. Pull latest changes from repository
2. Update dependencies if needed
3. Restart the application
4. Test functionality with sample PDFs