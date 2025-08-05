#!/usr/bin/env python3
import sys
sys.path.append('.')
from utils.pdf_compiler import PDFCompiler

def test_pdf_formatting():
    """Test the improved PDF formatting with code blocks"""
    
    # Create sample answers with code blocks to test formatting
    test_answers = [
        {
            "question": "Explain Angular directives with examples",
            "answer": """# Angular Directives

Angular directives are a fundamental concept in Angular development.

## Structural Directives
These control the structure of the DOM:

```javascript
// *ngIf example
<div *ngIf="showElement">This element is conditionally rendered</div>

// *ngFor example  
<li *ngFor="let item of items">{{item.name}}</li>

// *ngSwitch example
<div [ngSwitch]="status">
  <div *ngSwitchCase="'loading'">Loading...</div>
  <div *ngSwitchCase="'success'">Success!</div>
  <div *ngSwitchDefault>Default</div>
</div>
```

These directives provide powerful control over DOM manipulation and rendering.""",
            "question_number": 1
        }
    ]
    
    compiler = PDFCompiler()
    try:
        pdf_path = compiler.compile_answers_pdf(
            answers=test_answers,
            subject="Computer Science",
            mode="Understand Mode",
            custom_prompt="Test formatting"
        )
        print(f"✓ Test PDF created successfully: {pdf_path}")
        return True
    except Exception as e:
        print(f"✗ PDF creation failed: {e}")
        return False

if __name__ == "__main__":
    test_pdf_formatting()