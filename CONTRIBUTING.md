# Contributing to College Answer Generator

Thank you for your interest in contributing to the College Answer Generator! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/college-answer-generator.git
   cd college-answer-generator
   ```

2. **Set up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

## 🎯 How to Contribute

### Reporting Issues
- Use the [Issue Tracker](https://github.com/your-username/college-answer-generator/issues)
- Check if the issue already exists
- Provide detailed reproduction steps
- Include error messages and screenshots

### Feature Requests
- Open a [Discussion](https://github.com/your-username/college-answer-generator/discussions)
- Describe the feature and its use case
- Consider implementation complexity
- Be open to feedback and alternatives

### Code Contributions

#### Before You Start
- Check the [Project Roadmap](README.md#roadmap)
- Look for open issues labeled `good first issue`
- Comment on the issue to avoid duplicate work

#### Development Process
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes following our coding standards
3. Add tests for new functionality
4. Update documentation if needed
5. Run the test suite: `pytest`
6. Commit with clear messages
7. Push and create a Pull Request

## 📋 Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) conventions
- Use meaningful variable and function names
- Keep functions focused and under 50 lines when possible
- Add type hints for function parameters and return values

### Code Formatting
```bash
# Format code with Black
black app.py utils/

# Check style with flake8
flake8 app.py utils/

# Type checking with mypy
mypy app.py utils/
```

### Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update README.md for new features
- Include code examples where helpful

Example docstring:
```python
def process_document(file_path: str, subject: str) -> List[Dict]:
    """Process uploaded document and extract questions.
    
    Args:
        file_path: Path to the uploaded document
        subject: Academic subject for context
        
    Returns:
        List of dictionaries containing question data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is unsupported
    """
```

## 🧪 Testing Guidelines

### Writing Tests
- Write unit tests for all new functions
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (API calls, file operations)

### Test Structure
```python
def test_process_pdf_success():
    """Test successful PDF processing with valid input."""
    # Arrange
    test_file = "test_data/sample.pdf"
    
    # Act
    result = process_pdf(test_file)
    
    # Assert
    assert len(result) > 0
    assert all('question' in item for item in result)
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=utils

# Run specific test file
pytest tests/test_pdf_processor.py

# Run tests matching pattern
pytest -k "test_pdf"
```

## 🏗️ Architecture Guidelines

### Project Structure
```
utils/
├── pdf_processor.py    # Document processing
├── ai_generator.py     # AI integration
├── pdf_compiler.py     # PDF generation
└── history_manager.py  # Data persistence
```

### Adding New Features

#### New Document Format Support
1. Add parser in `pdf_processor.py`
2. Update file validation logic
3. Add tests for the new format
4. Update documentation

#### New AI Provider Integration
1. Create new module in `utils/`
2. Implement common interface
3. Add configuration options
4. Update environment variables
5. Add comprehensive tests

#### New Output Format
1. Extend `pdf_compiler.py` or create new module
2. Add formatting options in UI
3. Update export functionality
4. Test with various subjects

### Performance Considerations
- Profile code for bottlenecks
- Use async operations for I/O when possible
- Implement caching for expensive operations
- Consider memory usage with large documents

## 🐛 Debugging

### Common Issues
- **API Rate Limits**: Implement exponential backoff
- **Memory Issues**: Process large files in chunks
- **PDF Parsing**: Handle malformed HTML tags properly
- **File Encoding**: Support UTF-8 and handle special characters

### Debugging Tools
```python
# Add logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing file: {file_path}")
```

## 📦 Release Process

### Version Numbering
- Follow [Semantic Versioning](https://semver.org/)
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes

### Creating Releases
1. Update version in `app.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.2.3`
4. Push tag: `git push origin v1.2.3`
5. Create GitHub release with notes

## 💬 Communication

### Code Review Guidelines
- Be respectful and constructive
- Focus on code, not the person
- Explain the "why" behind suggestions
- Approve when ready, request changes when needed

### Getting Help
- Join our [Discussions](https://github.com/your-username/college-answer-generator/discussions)
- Ask questions in issue comments
- Reach out to maintainers for guidance

## 🏆 Recognition

Contributors will be:
- Listed in the README.md contributors section
- Mentioned in release notes for significant contributions
- Invited to be maintainers for consistent, quality contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to College Answer Generator! 🎓