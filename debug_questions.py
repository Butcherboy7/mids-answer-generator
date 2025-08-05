import streamlit as st
from utils.pdf_processor import PDFProcessor
import tempfile
import os

def debug_question_extraction():
    """Debug function to test question extraction"""
    
    st.title("Question Extraction Debug Tool")
    
    uploaded_file = st.file_uploader("Upload PDF to debug", type=['pdf'])
    
    if uploaded_file:
        processor = PDFProcessor()
        
        # Extract raw text
        st.subheader("Raw Text Extracted:")
        raw_text = processor.extract_text_from_document(uploaded_file)
        st.text_area("Raw Text", raw_text[:2000] + "..." if len(raw_text) > 2000 else raw_text, height=300)
        
        # Show question patterns being used
        st.subheader("Question Patterns Used:")
        for i, pattern in enumerate(processor.question_patterns, 1):
            st.write(f"{i}. `{pattern}`")
        
        # Extract questions
        st.subheader("Questions Extracted:")
        questions = processor.extract_questions(raw_text)
        
        if questions:
            st.success(f"Found {len(questions)} questions:")
            for i, q in enumerate(questions, 1):
                st.write(f"**Question {i}:** {q}")
        else:
            st.error("No questions found!")
            
            # Show lines that might contain questions
            st.subheader("Lines that might be questions:")
            lines = raw_text.split('\n')
            potential_questions = []
            
            for line in lines:
                line = line.strip()
                if len(line) > 20 and any(char.isalpha() for char in line):
                    # Look for lines with numbers, letters, or question words
                    if any(word in line.lower() for word in ['what', 'how', 'why', 'when', 'where', 'which', 'who', 'define', 'explain', 'describe', 'calculate', 'find', 'solve']):
                        potential_questions.append(line)
                    elif any(line.startswith(prefix) for prefix in ['1', '2', '3', '4', '5', 'Q', 'a)', 'b)', '(1)', '(2)']):
                        potential_questions.append(line)
            
            for i, pq in enumerate(potential_questions[:10], 1):  # Show first 10
                st.write(f"{i}. {pq}")

if __name__ == "__main__":
    debug_question_extraction()