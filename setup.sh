#!/bin/bash

# College Answer Generator - Setup Script
# This script sets up the environment for the College Answer Generator

echo "🎓 College Answer Generator - Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>/dev/null | grep -oP '(?<=Python )\d+\.\d+')
if [[ -z "$python_version" ]]; then
    echo "❌ Python 3 not found. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python $python_version found"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Rename requirements file
echo "Setting up requirements file..."
if [ -f "requirements-github.txt" ]; then
    cp requirements-github.txt requirements.txt
    echo "✅ Requirements file created"
else
    echo "❌ requirements-github.txt not found"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir data
    echo "✅ Data directory created"
fi

# Install system dependencies (Tesseract for OCR)
echo "Checking system dependencies..."
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR found"
else
    echo "⚠️  Tesseract OCR not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y tesseract-ocr
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install tesseract
        else
            echo "❌ Homebrew not found. Please install Tesseract manually"
        fi
    else
        echo "❌ Please install Tesseract OCR manually for your system"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your GEMINI_API_KEY"
echo "2. Run: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "3. Run: streamlit run app.py"
echo ""
echo "📖 For detailed deployment instructions, see DEPLOYMENT.md"