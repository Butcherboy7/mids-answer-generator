from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="college-answer-generator",
    version="1.0.0",
    author="College Answer Generator Team",
    description="AI-powered academic answer generation with advanced formatting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/college-answer-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "google-genai>=1.28.0",
        "pdfplumber>=0.9.0",
        "python-docx>=0.8.11",
        "Pillow>=10.0.0",
        "pytesseract>=0.3.10",
        "reportlab>=4.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "college-answer-generator=app:main",
        ],
    },
)