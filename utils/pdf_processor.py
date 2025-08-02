import pdfplumber
import re
import streamlit as st
from typing import List, Optional
import tempfile
import os

class PDFProcessor:
    """Handles PDF text extraction and processing"""
    
    def __init__(self):
        self.question_patterns = [
            r'^\d+\.\s+',  # 1. Question
            r'^\d+\)\s+',  # 1) Question
            r'^Q\d+[\.\)]\s+',  # Q1. or Q1) Question
            r'^Question\s+\d+[\.\)]\s+',  # Question 1. or Question 1)
            r'^\(\d+\)\s+',  # (1) Question
        ]
    
    def extract_questions(self, pdf_file) -> List[str]:
        """Extract questions from uploaded question bank PDF"""
        
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                tmp_path = tmp_file.name
            
            questions = []
            
            with pdfplumber.open(tmp_path) as pdf:
                full_text = ""
                
                # Extract text from all pages
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                
                # Clean and split text into potential questions
                questions = self._parse_questions(full_text)
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return questions
            
        except Exception as e:
            st.error(f"Error extracting questions: {str(e)}")
            return []
    
    def process_college_notes(self, notes_files) -> str:
        """Process multiple college notes PDFs and extract reference content"""
        
        all_content = ""
        
        for notes_file in notes_files:
            try:
                # Save uploaded file to temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(notes_file.getvalue())
                    tmp_path = tmp_file.name
                
                with pdfplumber.open(tmp_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            all_content += page_text + "\n\n"
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.warning(f"Could not process notes file {notes_file.name}: {str(e)}")
                continue
        
        return self._chunk_content(all_content)
    
    def _parse_questions(self, text: str) -> List[str]:
        """Parse text to identify and extract individual questions"""
        
        questions = []
        lines = text.split('\n')
        current_question = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a question pattern
            is_question_start = any(re.match(pattern, line) for pattern in self.question_patterns)
            
            if is_question_start:
                # Save previous question if exists
                if current_question.strip():
                    questions.append(current_question.strip())
                
                # Start new question
                current_question = line
            else:
                # Continue current question
                if current_question:
                    current_question += " " + line
        
        # Add the last question
        if current_question.strip():
            questions.append(current_question.strip())
        
        # Filter out very short questions (likely not actual questions)
        questions = [q for q in questions if len(q.split()) > 3]
        
        return questions
    
    def _chunk_content(self, content: str, max_chunk_size: int = 2000) -> str:
        """Chunk large content for better processing"""
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # If adding this sentence would exceed max size, start new chunk
            if len(current_chunk) + len(sentence) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Return first few chunks to avoid overwhelming the AI
        return "\n\n".join(chunks[:5])
