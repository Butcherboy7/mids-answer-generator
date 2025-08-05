# 🎓 College Answer Generator

A comprehensive Streamlit-based Academic Answer Generator that automates the creation of professional academic answers from question bank PDFs. The system uses AI (Google Gemini) to generate contextually appropriate answers with advanced formatting for all academic subjects.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🔥 Core Functionality
- **Multi-Format Document Support**: PDF, Word (.docx/.doc), and Images with OCR
- **AI-Powered Answer Generation**: Google Gemini 2.5 Flash for comprehensive responses
- **Advanced PDF Compilation**: Professional formatting with LaTeX math, code highlighting, and special characters
- **Dual Answer Modes**: Understand Mode (detailed explanations) vs Exam Mode (concise answers)
- **Subject-Specific Formatting**: Tailored for Computer Science, Mathematics, Chemistry, Physics, Biology, Economics, and more

### 📝 Enhanced Formatting
- **Code Blocks**: Syntax highlighting for multiple programming languages
- **Mathematical Formulas**: LaTeX support with proper symbols (α, β, π, ∞, ≤, ≥, ≠, ±)
- **Special Characters**: Full Unicode support for chemistry formulas (H₂SO₄, Fe³⁺)
- **Professional Typography**: Clean layouts with monospace fonts for code and italic formulas
- **Academic References**: Proper citation formatting and structured layouts

### 💼 User Experience
- **Clean Interface**: Intuitive Streamlit web application
- **Real-Time Progress**: Live updates during answer generation
- **History Management**: Persistent storage of generated answer sets
- **Batch Processing**: Handle multiple questions efficiently
- **Downloadable PDFs**: Professional documents ready for printing

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/college-answer-generator.git
   cd college-answer-generator
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501` to start using the application.

## 📁 Project Structure

```
college-answer-generator/
├── app.py                    # Main Streamlit application
├── utils/                    # Core utilities
│   ├── pdf_processor.py      # PDF text extraction and question parsing
│   ├── ai_generator.py       # AI-powered answer generation
│   ├── pdf_compiler.py       # Professional PDF document creation
│   └── history_manager.py    # Persistent storage management
├── data/                     # Generated PDFs and history
├── .streamlit/              # Streamlit configuration
│   └── config.toml
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🛠️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI generation | Yes |

### Streamlit Configuration
The application includes optimized settings in `.streamlit/config.toml`:
- Server configuration for deployment
- Theme and UI customizations
- Performance optimizations

## 📚 Usage Guide

### 1. Upload Documents
- **Supported formats**: PDF, Word documents (.docx/.doc), Images (PNG, JPG)
- **OCR support**: Automatic text extraction from images
- **Question detection**: Intelligent parsing of numbered questions

### 2. Configure Generation
- **Subject selection**: Choose from predefined subjects or enter custom
- **Answer mode**: 
  - **Understand Mode**: Detailed explanations with examples
  - **Exam Mode**: Concise, exam-focused responses
- **Custom instructions**: Add specific requirements or focus areas
- **Reference materials**: Upload college notes for additional context

### 3. Generate Answers
- **Batch processing**: Handles multiple questions efficiently  
- **Real-time progress**: Live updates during generation
- **Error handling**: Robust retry mechanisms for API failures

### 4. Review and Download
- **Professional PDFs**: Clean, printable documents
- **History tracking**: Access previously generated answer sets
- **Export options**: Download individual or bulk PDFs

## 🔧 Advanced Features

### Subject-Specific Formatting

#### Computer Science
```javascript
// Syntax highlighted code blocks
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    const pivot = arr[arr.length - 1];
    const left = arr.filter(x => x < pivot);
    const right = arr.filter(x => x > pivot);
    return [...quickSort(left), pivot, ...quickSort(right)];
}
```

#### Mathematics
```latex
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

For quadratic equations: $ax^2 + bx + c = 0$
Solution: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
```

#### Chemistry
```
Balanced equation: 2H₂ + O₂ → 2H₂O
Ionic: Na⁺ + Cl⁻ → NaCl
Temperature: 25°C, Pressure: 1 atm
```

### Error Handling
- **API rate limiting**: Automatic retry with exponential backoff
- **PDF parsing errors**: Robust HTML tag validation
- **File format validation**: Comprehensive format checking
- **Memory management**: Efficient handling of large documents

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment

#### Replit (Recommended)
1. Fork this repository on Replit
2. Set environment variables in Secrets tab
3. Run the application

#### Docker Deployment
```dockerfile
# Dockerfile included in repository
docker build -t college-answer-generator .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key college-answer-generator
```

#### Streamlit Cloud
1. Connect your GitHub repository
2. Set secrets in Streamlit Cloud dashboard
3. Deploy automatically

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Test individual components:
```bash
# Test PDF compilation
python test_pdf_compiler.py

# Test AI generation
python test_ai_generator.py

# Test document processing
python test_pdf_processor.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Submit a pull request

### Coding Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

#### API Key Problems
- Ensure your Gemini API key is valid and has sufficient quota
- Check the key is properly set in environment variables
- Verify API key permissions for text generation

#### PDF Generation Errors
- Check document format compatibility
- Ensure sufficient system memory for large documents
- Verify write permissions for data directory

#### Performance Issues
- Large documents may take longer to process
- Consider splitting very large question banks
- Monitor API rate limits and quotas

### Getting Help
- 📚 [Documentation](https://github.com/your-username/college-answer-generator/wiki)
- 🐛 [Issue Tracker](https://github.com/your-username/college-answer-generator/issues)
- 💬 [Discussions](https://github.com/your-username/college-answer-generator/discussions)

## 🔮 Roadmap

### Upcoming Features
- [ ] Multiple AI provider support (OpenAI, Claude)
- [ ] Advanced template customization
- [ ] Collaborative answer editing
- [ ] Integration with learning management systems
- [ ] Mobile-responsive interface
- [ ] Offline mode capabilities

### Performance Improvements
- [ ] Async processing for better performance
- [ ] Caching layer for frequently used content
- [ ] Database integration for scalability
- [ ] Real-time collaboration features

## 🎯 Use Cases

### For Students
- Generate comprehensive study materials
- Create practice exam answers
- Understand complex academic concepts
- Prepare professional documentation

### For Educators
- Create answer keys for assignments
- Generate teaching materials
- Provide detailed explanations for students
- Standardize answer formatting

### For Institutions
- Automate answer sheet generation
- Maintain consistent academic standards
- Reduce manual grading workload
- Create digital learning resources

---

**Built with ❤️ using Python, Streamlit, and Google Gemini AI**

*Last updated: August 2025*