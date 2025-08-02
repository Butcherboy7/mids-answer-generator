import streamlit as st
import os
import json
import time
from datetime import datetime
from utils.pdf_processor import PDFProcessor
from utils.ai_generator import AIGenerator
from utils.pdf_compiler import PDFCompiler
from utils.history_manager import HistoryManager

# Initialize session state
if 'processing_stage' not in st.session_state:
    st.session_state.processing_stage = None
if 'current_answers' not in st.session_state:
    st.session_state.current_answers = None
if 'history' not in st.session_state:
    st.session_state.history = HistoryManager()

def main():
    st.set_page_config(
        page_title="College Answer Generator",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 College Answer Generator")
    st.markdown("Generate comprehensive answers for your college question banks using AI")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Generate Answers", "History"]
    )
    
    if page == "Generate Answers":
        generate_answers_page()
    elif page == "History":
        history_page()

def generate_answers_page():
    st.header("Generate New Answer Set")
    
    # File upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Question Bank PDF")
        question_bank = st.file_uploader(
            "Upload your question bank PDF (computer-typed, selectable text)",
            type=['pdf'],
            key="question_bank"
        )
    
    with col2:
        st.subheader("📚 College Notes PDFs (Optional)")
        college_notes = st.file_uploader(
            "Upload college notes for reference",
            type=['pdf'],
            accept_multiple_files=True,
            key="college_notes"
        )
    
    # Subject selection
    st.subheader("📖 Subject Selection")
    subject = st.selectbox(
        "Select the subject of your question bank:",
        ["Mathematics", "Physics", "Computer Science", "History", "Literature", "Chemistry", "Biology", "Economics", "Psychology", "Engineering"]
    )
    
    # Answer generation mode
    st.subheader("🎯 Answer Generation Mode")
    mode = st.radio(
        "Choose your preferred answer style:",
        ["Understand Mode", "Exam Mode"],
        help="Understand Mode: Detailed explanations with analogies and examples. Exam Mode: Concise, focused answers for exam preparation."
    )
    
    # Custom prompt instructions
    custom_prompt_enabled = st.checkbox("Add Custom Prompt Instructions")
    custom_prompt = ""
    if custom_prompt_enabled:
        custom_prompt = st.text_area(
            "Custom Instructions:",
            placeholder="Enter any specific instructions for answer generation...",
            height=100
        )
    
    # Generate button
    if st.button("Generate Answers", type="primary", disabled=not question_bank):
        if question_bank:
            generate_answers(question_bank, college_notes, subject, mode, custom_prompt)
        else:
            st.error("Please upload a question bank PDF first.")
    
    # Display current processing status
    if st.session_state.processing_stage:
        display_processing_status()
    
    # Display download button if answers are ready
    if st.session_state.current_answers:
        display_download_section()

def generate_answers(question_bank, college_notes, subject, mode, custom_prompt):
    """Main function to orchestrate the answer generation process"""
    
    try:
        # Initialize processors
        pdf_processor = PDFProcessor()
        ai_generator = AIGenerator()
        pdf_compiler = PDFCompiler()
        
        # Stage 1: Extract questions from question bank
        st.session_state.processing_stage = "extracting_questions"
        st.rerun()
        
        with st.spinner("Extracting questions from question bank..."):
            questions = pdf_processor.extract_questions(question_bank)
        
        if not questions:
            st.error("No questions found in the uploaded PDF. Please ensure the PDF contains selectable text.")
            st.session_state.processing_stage = None
            return
        
        st.success(f"Successfully extracted {len(questions)} questions!")
        
        # Stage 2: Process college notes if provided
        reference_content = ""
        if college_notes:
            st.session_state.processing_stage = "processing_notes"
            st.rerun()
            
            with st.spinner("Processing college notes for reference..."):
                reference_content = pdf_processor.process_college_notes(college_notes)
            
            st.success(f"Processed {len(college_notes)} reference documents!")
        
        # Stage 3: Generate answers
        st.session_state.processing_stage = "generating_answers"
        st.rerun()
        
        answers = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, question in enumerate(questions):
            status_text.text(f"Generating answer for question {i+1} of {len(questions)}")
            
            answer = ai_generator.generate_answer(
                question=question,
                subject=subject,
                mode=mode,
                custom_prompt=custom_prompt,
                reference_content=reference_content
            )
            
            answers.append({
                "question": question,
                "answer": answer,
                "question_number": i + 1
            })
            
            progress_bar.progress((i + 1) / len(questions))
            time.sleep(0.1)  # Small delay to show progress
        
        # Stage 4: Compile PDF
        st.session_state.processing_stage = "compiling_pdf"
        st.rerun()
        
        with st.spinner("Compiling professional PDF..."):
            pdf_path = pdf_compiler.compile_answers_pdf(
                answers=answers,
                subject=subject,
                mode=mode,
                custom_prompt=custom_prompt
            )
        
        # Store results
        st.session_state.current_answers = {
            "pdf_path": pdf_path,
            "subject": subject,
            "mode": mode,
            "question_count": len(questions),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to history
        st.session_state.history.add_entry(st.session_state.current_answers)
        
        st.session_state.processing_stage = "completed"
        st.success("🎉 Answer generation completed successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        st.session_state.processing_stage = None

def display_processing_status():
    """Display current processing status with progress indicators"""
    
    stage = st.session_state.processing_stage
    
    if stage == "extracting_questions":
        st.info("📄 Extracting questions from PDF...")
    elif stage == "processing_notes":
        st.info("📚 Processing college notes...")
    elif stage == "generating_answers":
        st.info("🤖 Generating AI answers...")
    elif stage == "compiling_pdf":
        st.info("📋 Compiling professional PDF...")
    elif stage == "completed":
        st.success("✅ All stages completed!")
        st.session_state.processing_stage = None

def display_download_section():
    """Display download section for generated answers"""
    
    st.subheader("📥 Download Your Answers")
    
    answers = st.session_state.current_answers
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Subject:** {answers['subject']}")
        st.write(f"**Mode:** {answers['mode']}")
        st.write(f"**Questions:** {answers['question_count']}")
        st.write(f"**Generated:** {answers['generated_at']}")
    
    with col2:
        if os.path.exists(answers['pdf_path']):
            with open(answers['pdf_path'], 'rb') as file:
                st.download_button(
                    label="📥 Download PDF",
                    data=file.read(),
                    file_name=f"answers_{answers['subject']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )

def history_page():
    """Display history of generated answer sets"""
    
    st.header("📋 Answer Generation History")
    
    history = st.session_state.history.get_history()
    
    if not history:
        st.info("No answer sets generated yet. Go to 'Generate Answers' to create your first set!")
        return
    
    st.write(f"Total answer sets: {len(history)}")
    
    for i, entry in enumerate(reversed(history)):
        with st.expander(f"Answer Set {len(history) - i} - {entry['subject']} ({entry['generated_at']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Subject:** {entry['subject']}")
                st.write(f"**Mode:** {entry['mode']}")
                st.write(f"**Questions:** {entry['question_count']}")
                st.write(f"**Generated:** {entry['generated_at']}")
            
            with col2:
                if os.path.exists(entry['pdf_path']):
                    with open(entry['pdf_path'], 'rb') as file:
                        st.download_button(
                            label="📥 Re-download",
                            data=file.read(),
                            file_name=f"answers_{entry['subject']}_{entry['generated_at'].replace(' ', '_').replace(':', '')}.pdf",
                            mime="application/pdf",
                            key=f"download_{i}"
                        )
                else:
                    st.error("File not found")

if __name__ == "__main__":
    main()
