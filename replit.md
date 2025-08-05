# Overview

The College Answer Generator is a comprehensive, GitHub-ready Streamlit-based web application that automates the creation of professional academic answers from question bank documents. The system uses AI (Google Gemini) to generate contextually appropriate answers with advanced formatting for all academic subjects. Now fully configured for easy deployment across multiple platforms with professional documentation, Docker support, and comprehensive setup instructions.

## Recent Changes (August 2025)
- ✅ **PDF Formatting Overhaul**: Completely eliminated HTML tag parsing issues with ultra-safe text processing
- ✅ **Smart Content Detection**: Added intelligent formatting for headings, lists, and code blocks
- ✅ **Markdown Cleanup**: Fixed hashtag rendering issues by properly removing markdown symbols
- ✅ **Subject-Aware Formatting**: Code blocks with colored backgrounds for programming subjects only
- ✅ **Enhanced API Reliability**: Improved retry mechanism with progressive delays and 2-question batches for better rate limiting
- ✅ **Clean Text Processing**: Removed all problematic HTML/markdown that caused parser conflicts
- ✅ **GitHub-Ready Package**: Complete with README, CONTRIBUTING guidelines, and deployment docs
- ✅ **Docker Support**: Full containerization with docker-compose configuration
- ✅ **Multi-Platform Deployment**: Support for local, Docker, Replit, and Streamlit Cloud
- ✅ **Professional Documentation**: Comprehensive setup guides and contribution workflows
- ✅ **Robust Error Handling**: Fixed PDF parsing issues and improved stability
- ✅ **Replit Migration**: Successfully migrated from Replit Agent to standard Replit environment with proper Streamlit configuration
- ⚠️ **API Quota Management**: Added handling for Gemini API free tier limits (50 requests/day)

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **Layout**: Multi-page application with sidebar navigation between "Generate Answers" and "History" pages
- **State Management**: Session state management for processing stages, answers, and history
- **UI Components**: File uploaders, progress bars, selectboxes, and download buttons for intuitive user interaction

## Backend Architecture
- **Modular Design**: Utility-based architecture with separate modules for distinct functionalities:
  - `PDFProcessor`: Handles PDF text extraction and question parsing using pdfplumber
  - `AIGenerator`: Manages AI-powered answer generation via Google Gemini API
  - `PDFCompiler`: Creates professional PDF documents using ReportLab
  - `HistoryManager`: Handles persistent storage of generated answer sets
- **Processing Pipeline**: Sequential workflow from PDF upload → question extraction → AI generation → PDF compilation → history storage

## Data Storage Solutions
- **Local File System**: JSON-based history storage in `data/` directory
- **Temporary Files**: Uses Python's tempfile module for secure PDF processing
- **Session State**: In-memory storage for current processing state and user data

## AI Integration
- **Provider**: Google Gemini 2.5 Flash model for answer generation
- **API Management**: Environment variable-based API key configuration
- **Rate Limiting**: Free tier allows 50 requests per day per project per model
- **Prompt Engineering**: Dynamic prompt construction based on subject, mode (Understand/Exam), and optional custom instructions
- **Error Handling**: Graceful fallback responses for API failures and quota exceeded errors

## Document Processing
- **Question Extraction**: Regex-based pattern matching for various question numbering formats
- **PDF Generation**: Professional formatting with custom styles, headers, and structured layouts
- **Text Processing**: Advanced cleaning and parsing of extracted PDF content

# External Dependencies

## AI Services
- **Google Gemini API**: Core AI service for answer generation requiring GEMINI_API_KEY environment variable

## Python Libraries
- **streamlit**: Web application framework and UI components
- **pdfplumber**: PDF text extraction and processing
- **reportlab**: Professional PDF document generation with custom styling
- **google-genai**: Official Google Gemini AI client library

## File System Dependencies
- **Local Storage**: Requires write permissions for `data/` directory to store history and generated PDFs
- **Temporary Files**: System temp directory access for secure PDF processing

## Environment Configuration
- **API Keys**: Requires GEMINI_API_KEY environment variable for AI functionality
- **File Permissions**: Read/write access to local filesystem for data persistence
- **Deployment Ready**: Complete with .env.example, .gitignore, and deployment scripts
- **Docker Support**: Dockerfile and docker-compose.yml for containerized deployment
- **GitHub Integration**: Professional README, CONTRIBUTING guidelines, and MIT license