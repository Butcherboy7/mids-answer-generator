"""
Basic tests for College Answer Generator components
"""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock

# Test imports work correctly
def test_imports():
    """Test that all modules can be imported"""
    try:
        from utils.pdf_processor import PDFProcessor
        from utils.pdf_compiler import PDFCompiler
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_pdf_processor_init():
    """Test PDFProcessor initialization"""
    from utils.pdf_processor import PDFProcessor
    processor = PDFProcessor()
    assert processor.question_patterns is not None
    assert len(processor.question_patterns) > 0

def test_pdf_compiler_init():
    """Test PDFCompiler initialization"""
    from utils.pdf_compiler import PDFCompiler
    compiler = PDFCompiler()
    assert compiler.styles is not None
    assert hasattr(compiler, 'title_style')
    assert hasattr(compiler, 'answer_style')

@patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
def test_ai_generator_init():
    """Test AIGenerator initialization with mock API key"""
    with patch('google.generativeai.configure'):
        from utils.ai_generator import AIGenerator
        generator = AIGenerator()
        assert generator.model == "gemini-1.5-flash"
        assert generator.rate_limit_delay > 0

def test_question_pattern_matching():
    """Test question pattern recognition"""
    from utils.pdf_processor import PDFProcessor
    processor = PDFProcessor()
    
    test_cases = [
        "1. What is Python?",
        "2) Define variables",
        "Q3. Explain functions",
        "Question 4. List comprehensions",
        "(5) What are classes?"
    ]
    
    for test_case in test_cases:
        for pattern in processor.question_patterns:
            import re
            if re.search(pattern, test_case):
                assert True, f"Pattern {pattern} should match {test_case}"
                break
        else:
            pytest.fail(f"No pattern matched {test_case}")

def test_data_directory_creation():
    """Test that data directory is created properly"""
    from utils.pdf_compiler import PDFCompiler
    compiler = PDFCompiler()
    assert os.path.exists("data"), "Data directory should be created automatically"

if __name__ == "__main__":
    pytest.main([__file__])