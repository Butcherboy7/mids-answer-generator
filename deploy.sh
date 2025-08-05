#!/bin/bash

# College Answer Generator Deployment Script
# This script sets up the application for various deployment environments

set -e  # Exit on any error

echo "🎓 College Answer Generator Deployment Script"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    
    if command_exists pip; then
        pip install --upgrade pip
        pip install streamlit google-genai pdfplumber python-docx Pillow pytesseract reportlab python-dotenv
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ pip not found. Please install Python and pip first."
        exit 1
    fi
}

# Function to set up environment
setup_environment() {
    echo "🔧 Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📝 Created .env file from template"
        echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
    else
        echo "✅ .env file already exists"
    fi
    
    # Create data directory
    mkdir -p data
    echo "✅ Created data directory"
    
    # Create .streamlit directory and config
    mkdir -p .streamlit
    if [ ! -f .streamlit/config.toml ]; then
        cat > .streamlit/config.toml << EOF
[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
EOF
        echo "✅ Created Streamlit configuration"
    fi
}

# Function to run tests
run_tests() {
    echo "🧪 Running basic functionality tests..."
    
    python -c "
import sys
try:
    from utils.pdf_processor import PDFProcessor
    from utils.ai_generator import AIGenerator
    from utils.pdf_compiler import PDFCompiler
    from utils.history_manager import HistoryManager
    print('✅ All modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
}

# Function to check system requirements
check_requirements() {
    echo "🔍 Checking system requirements..."
    
    # Check Python version
    python_version=$(python --version 2>&1 | cut -d' ' -f2)
    echo "Python version: $python_version"
    
    # Check if tesseract is available (for OCR)
    if command_exists tesseract; then
        tesseract_version=$(tesseract --version 2>&1 | head -n1)
        echo "✅ $tesseract_version"
    else
        echo "⚠️  Tesseract OCR not found. Image processing may not work."
        echo "   Install with: sudo apt-get install tesseract-ocr (Ubuntu/Debian)"
        echo "   Or: brew install tesseract (macOS)"
    fi
}

# Function to start the application
start_app() {
    echo "🚀 Starting College Answer Generator..."
    echo "📍 The application will be available at: http://localhost:8501"
    echo "🔑 Make sure your GEMINI_API_KEY is set in .env file"
    echo ""
    
    # Check if .env has API key
    if [ -f .env ] && grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
        echo "⚠️  WARNING: Please update your GEMINI_API_KEY in .env file"
        echo "   Get your API key from: https://ai.google.dev/"
        echo ""
    fi
    
    streamlit run app.py --server.port 8501
}

# Main deployment logic
main() {
    case "${1:-setup}" in
        "setup")
            echo "Setting up College Answer Generator..."
            check_requirements
            install_dependencies
            setup_environment
            run_tests
            echo ""
            echo "🎉 Setup completed successfully!"
            echo "💡 Run './deploy.sh start' to launch the application"
            ;;
        "start")
            start_app
            ;;
        "test")
            run_tests
            ;;
        "docker")
            echo "🐳 Building and starting Docker container..."
            if command_exists docker; then
                docker build -t college-answer-generator .
                docker run -p 8501:8501 --env-file .env college-answer-generator
            else
                echo "❌ Docker not found. Please install Docker first."
                exit 1
            fi
            ;;
        "help"|"-h"|"--help")
            echo "Usage: ./deploy.sh [command]"
            echo ""
            echo "Commands:"
            echo "  setup    Set up the application (default)"
            echo "  start    Start the Streamlit application"
            echo "  test     Run functionality tests"
            echo "  docker   Build and run with Docker"
            echo "  help     Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  GEMINI_API_KEY    Your Google Gemini API key (required)"
            ;;
        *)
            echo "Unknown command: $1"
            echo "Run './deploy.sh help' for usage information"
            exit 1
            ;;
    esac
}

# Make sure we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the project root directory."
    exit 1
fi

main "$@"