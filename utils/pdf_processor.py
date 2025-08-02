import pdfplumber
import re
import streamlit as st
from typing import List, Optional, Tuple
import tempfile
import os
from docx import Document

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
    
    def extract_text_from_pdf(self, uploaded_file) -> str:
        """Extract text from uploaded PDF file with enhanced extraction"""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            try:
                full_text = ""
                with pdfplumber.open(tmp_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        # Try standard extraction first
                        text = page.extract_text()
                        
                        # If no text, try with different settings
                        if not text or len(text.strip()) < 10:
                            text = page.extract_text(
                                x_tolerance=2,
                                y_tolerance=2,
                                layout=True
                            )
                        
                        # If still no text, try table extraction
                        if not text or len(text.strip()) < 10:
                            tables = page.extract_tables()
                            if tables:
                                for table in tables:
                                    for row in table:
                                        if row:
                                            text += " ".join([cell for cell in row if cell]) + "\n"
                        
                        if text:
                            full_text += f"--- Page {page_num + 1} ---\n{text}\n\n"
                
                return full_text
            finally:
                os.unlink(tmp_path)
                
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_questions(self, text: str) -> List[str]:
        """Extract questions from text using improved pattern matching"""
        
        if not text or not text.strip():
            return []
        
        # Parse questions from the text
        questions = self._parse_questions(text)
        return questions
    
    def _extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            full_text = ""
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
            return full_text
        finally:
            os.unlink(tmp_path)
    
    def _extract_text_from_docx(self, docx_file) -> str:
        """Extract text from Word document"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(docx_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            doc = Document(tmp_path)
            full_text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text += paragraph.text + "\n"
            return full_text
        finally:
            os.unlink(tmp_path)
    
    def process_college_notes(self, notes_files) -> str:
        """Process multiple college notes files (PDF/Word) and extract reference content"""
        
        all_content = ""
        
        for notes_file in notes_files:
            try:
                # Extract text based on file type
                if notes_file.name.lower().endswith('.pdf'):
                    file_content = self._extract_text_from_pdf(notes_file)
                elif notes_file.name.lower().endswith(('.docx', '.doc')):
                    file_content = self._extract_text_from_docx(notes_file)
                else:
                    st.warning(f"Unsupported file format for {notes_file.name}. Skipping.")
                    continue
                
                if file_content.strip():
                    all_content += file_content + "\n\n"
                
            except Exception as e:
                st.warning(f"Could not process notes file {notes_file.name}: {str(e)}")
                continue
        
        return self._chunk_content(all_content)
    
    def _parse_questions(self, text: str) -> List[str]:
        """Parse text to identify and extract individual questions"""
        
        questions = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return questions
        
        current_question = ""
        question_started = False
        
        for i, line in enumerate(lines):
            # Check if line starts with a question pattern
            is_question_start = any(re.match(pattern, line) for pattern in self.question_patterns)
            
            if is_question_start:
                # Save previous question if exists
                if current_question.strip() and question_started:
                    questions.append(current_question.strip())
                
                # Start new question
                current_question = line
                question_started = True
            else:
                # Continue current question if we've started one
                if question_started:
                    # Check if this might be start of next question (common patterns)
                    next_line_is_question = (i + 1 < len(lines) and 
                                           any(re.match(pattern, lines[i + 1]) for pattern in self.question_patterns))
                    
                    # If current line looks like an answer or next line is a question, stop here
                    if (line.lower().startswith(('answer:', 'ans:', 'solution:', 'sol:')) or 
                        next_line_is_question):
                        if current_question.strip():
                            questions.append(current_question.strip())
                            current_question = ""
                            question_started = False
                    else:
                        # Continue building the question
                        current_question += " " + line
        
        # Add the last question
        if current_question.strip() and question_started:
            questions.append(current_question.strip())
        
        # Filter out very short questions and clean them
        filtered_questions = []
        for q in questions:
            # Remove common answer indicators from questions
            cleaned_q = re.sub(r'\s*(answer|ans|solution|sol)\s*:.*$', '', q, flags=re.IGNORECASE).strip()
            if len(cleaned_q.split()) > 3:
                filtered_questions.append(cleaned_q)
        
        return filtered_questions
    
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
