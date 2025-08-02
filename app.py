import streamlit as st
import os
import json
import time
import re
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
if 'questions_approved' not in st.session_state:
    st.session_state.questions_approved = False
if 'extracted_questions' not in st.session_state:
    st.session_state.extracted_questions = []
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'editing_mode' not in st.session_state:
    st.session_state.editing_mode = False
if 'edited_questions' not in st.session_state:
    st.session_state.edited_questions = []

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
        st.subheader("📄 Question Bank Document")
        question_bank = st.file_uploader(
            "Upload your question bank (PDF or Word document)",
            type=['pdf', 'docx', 'doc'],
            key="question_bank"
        )
    
    with col2:
        st.subheader("📚 College Notes (Optional)")
        college_notes = st.file_uploader(
            "Upload college notes for reference (PDF or Word)",
            type=['pdf', 'docx', 'doc'],
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
            # Reset approval state for new generation
            st.session_state.questions_approved = False
            st.session_state.editing_mode = False
            st.session_state.edited_questions = []
            generate_answers(question_bank, college_notes, subject, mode, custom_prompt)
        else:
            st.error("Please upload a question bank document first.")
    
    # No longer need old processing status display
    
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
        progress_container = st.container()
        status_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0, text="Starting question extraction...")
        
        with status_container:
            status_text = st.empty()
            
        status_text.info("📄 Extracting text from document...")
        progress_bar.progress(20, text="Extracting text from document...")
        
        questions, extracted_text = pdf_processor.extract_questions(question_bank)
        
        progress_bar.progress(60, text="Parsing questions...")
        status_text.info("🔍 Parsing questions from extracted text...")
        
        if not questions:
            progress_bar.progress(100, text="Extraction completed")
            status_text.error("❌ No questions found in the uploaded document.")
            
            # Show extracted text for debugging
            if extracted_text:
                with st.expander("View Extracted Text (for debugging)", expanded=False):
                    st.text_area("Raw extracted text:", extracted_text[:2000] + "..." if len(extracted_text) > 2000 else extracted_text, height=200)
            
            return
        
        progress_bar.progress(100, text="Questions extracted successfully!")
        status_text.success(f"✅ Successfully extracted {len(questions)} questions!")
        
        # Store questions in session state
        st.session_state.extracted_questions = questions
        st.session_state.extracted_text = extracted_text
        
        # Show extracted questions for verification and editing
        st.write("---")
        st.subheader("📋 Review and Edit Questions")
        
        # Initialize editing mode if not set
        if 'editing_mode' not in st.session_state:
            st.session_state.editing_mode = False
        
        if not st.session_state.editing_mode:
            # Display mode - show questions with options
            st.write("**Extracted Questions:**")
            for i, question in enumerate(questions[:10]):  # Show first 10 questions
                st.write(f"**Q{i+1}:** {question}")
            if len(questions) > 10:
                st.write(f"... and {len(questions)-10} more questions")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Questions look good, continue", key="approve_questions"):
                    st.session_state.questions_approved = True
                    st.session_state.editing_mode = False
                    st.rerun()
            with col2:
                if st.button("✏️ Edit Questions", key="edit_questions"):
                    st.session_state.editing_mode = True
                    st.session_state.edited_questions = questions.copy()
                    st.rerun()
        
        else:
            # Editing mode - allow question modification
            st.write("**Edit Questions (one per line):**")
            
            # Initialize edited questions if not set
            if 'edited_questions' not in st.session_state:
                st.session_state.edited_questions = questions.copy()
            
            # Create text area with all questions
            questions_text = "\n\n".join([f"Q{i+1}: {q}" for i, q in enumerate(st.session_state.edited_questions)])
            
            edited_text = st.text_area(
                "Questions (you can edit, add, or remove questions):",
                value=questions_text,
                height=300,
                key="questions_editor"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save Changes", key="save_questions"):
                    # Parse edited questions
                    lines = [line.strip() for line in edited_text.split('\n') if line.strip()]
                    new_questions = []
                    
                    for line in lines:
                        # Remove question numbering if present
                        cleaned_line = re.sub(r'^Q?\d+[:\.\)]\s*', '', line).strip()
                        if cleaned_line and len(cleaned_line.split()) > 3:
                            new_questions.append(cleaned_line)
                    
                    if new_questions:
                        st.session_state.edited_questions = new_questions
                        st.session_state.extracted_questions = new_questions
                        st.success(f"✅ Updated! Now have {len(new_questions)} questions.")
                    else:
                        st.error("No valid questions found. Please check your formatting.")
            
            with col2:
                if st.button("✅ Use These Questions", key="confirm_edited"):
                    if st.session_state.edited_questions:
                        st.session_state.extracted_questions = st.session_state.edited_questions
                        st.session_state.questions_approved = True
                        st.session_state.editing_mode = False
                        st.success("Questions confirmed! Proceeding with generation...")
                        st.rerun()
                    else:
                        st.error("Please add at least one question.")
            
            with col3:
                if st.button("❌ Cancel", key="cancel_edit"):
                    st.session_state.editing_mode = False
                    st.rerun()
        
        # Wait for user approval before continuing
        if not st.session_state.get('questions_approved', False):
            return
        
        # Use stored questions for processing
        questions = st.session_state.extracted_questions
        
        # Stage 2: Process college notes if provided
        reference_content = ""
        if college_notes:
            progress_bar.progress(0, text="Processing college notes...")
            status_text.info("📚 Processing college notes for reference...")
            
            reference_content = pdf_processor.process_college_notes(college_notes)
            
            progress_bar.progress(100, text="Notes processed successfully!")
            status_text.success(f"✅ Processed {len(college_notes)} reference documents!")
            time.sleep(1)  # Brief pause to show completion
        
        # Stage 3: Generate answers with batch processing
        st.write("---")
        st.subheader("🤖 Generating AI Answers")
        
        # Configure batch settings and show API usage
        col1, col2 = st.columns([2, 1])
        
        with col1:
            batch_settings_expander = st.expander("⚙️ Batch Settings (Optional)", expanded=False)
            with batch_settings_expander:
                col_a, col_b = st.columns(2)
                with col_a:
                    batch_size = st.slider("Questions per batch", 1, 10, ai_generator.batch_size, 
                                         help="Smaller batches = slower but less likely to hit rate limits")
                with col_b:
                    rate_delay = st.slider("Delay between requests (seconds)", 0.5, 3.0, ai_generator.rate_limit_delay,
                                         help="Longer delays reduce chance of rate limiting")
                
                ai_generator.batch_size = batch_size
                ai_generator.rate_limit_delay = rate_delay
        
        with col2:
            # API usage tracker
            st.info(f"📊 **API Usage**")
            st.write(f"Requests this session: {ai_generator.request_count}")
            st.write(f"Session limit: {ai_generator.max_requests_per_session}")
            remaining = ai_generator.max_requests_per_session - ai_generator.request_count
            if remaining < 10:
                st.warning(f"⚠️ Only {remaining} requests remaining")
            
            estimated_requests = len(questions)
            if estimated_requests > remaining:
                st.error(f"❌ Not enough requests remaining for {estimated_requests} questions")
                st.info("💡 Tip: Restart the app to reset the session limit")
                return
        
        # Prepare questions for batch processing
        questions_data = [{"question": q, "question_number": i+1} for i, q in enumerate(questions)]
        
        main_progress = st.progress(0, text="Starting batch answer generation...")
        current_status = st.empty()
        batch_info = st.empty()
        answer_preview = st.empty()
        
        # Use batch processing
        answers = []
        total_batches = (len(questions) + ai_generator.batch_size - 1) // ai_generator.batch_size
        
        for batch_num in range(total_batches):
            batch_start = batch_num * ai_generator.batch_size
            batch_end = min(batch_start + ai_generator.batch_size, len(questions))
            batch_data = questions_data[batch_start:batch_end]
            
            # Update progress
            progress_percent = batch_num / total_batches
            main_progress.progress(progress_percent, text=f"Processing batch {batch_num+1} of {total_batches}")
            batch_info.info(f"📦 Batch {batch_num+1}: Processing questions {batch_start+1}-{batch_end}")
            
            # Process batch
            for i, item in enumerate(batch_data):
                current_question_num = batch_start + i + 1
                current_status.info(f"🔄 Question {current_question_num}: {item['question'][:100]}...")
                
                answer = ai_generator.generate_answer(
                    question=item['question'],
                    subject=subject,
                    mode=mode,
                    custom_prompt=custom_prompt,
                    reference_content=reference_content
                )
                
                answers.append({
                    "question": item['question'],
                    "answer": answer,
                    "question_number": item['question_number']
                })
                
                # Show preview of latest answer
                with answer_preview.container():
                    st.write(f"✅ **Question {current_question_num} completed**")
                    if len(answer) > 200:
                        st.write(f"Preview: {answer[:200]}...")
                    else:
                        st.write(f"Answer: {answer}")
            
            # Batch completion
            if batch_end < len(questions):
                batch_info.success(f"✅ Batch {batch_num+1} completed. Waiting before next batch...")
                time.sleep(2)  # Brief pause between batches
        
        main_progress.progress(1.0, text="All answers generated!")
        current_status.success(f"🎉 Generated {len(answers)} comprehensive answers!")
        batch_info.success(f"✅ Completed {total_batches} batches successfully!")
        
        # Stage 4: Compile PDF
        st.write("---")
        st.subheader("📄 Creating Professional PDF")
        
        pdf_progress = st.progress(0, text="Compiling PDF document...")
        pdf_status = st.empty()
        
        pdf_status.info("📋 Formatting answers and creating PDF...")
        pdf_progress.progress(50, text="Formatting content...")
        
        pdf_path = pdf_compiler.compile_answers_pdf(
            answers=answers,
            subject=subject,
            mode=mode,
            custom_prompt=custom_prompt
        )
        
        pdf_progress.progress(100, text="PDF created successfully!")
        pdf_status.success("✅ Professional PDF document ready for download!")
        
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
        
        # Reset approval state for next generation
        st.session_state.questions_approved = False
        st.session_state.extracted_questions = []
        st.session_state.editing_mode = False
        st.session_state.edited_questions = []
        
        st.balloons()
        st.success("🎉 Answer generation completed successfully!")
        st.info("📥 Scroll down to download your PDF or check the History tab for all generated sets.")
        
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        # Reset states on error
        st.session_state.questions_approved = False
        st.session_state.extracted_questions = []
        st.session_state.editing_mode = False
        st.session_state.edited_questions = []

def display_processing_status():
    """Legacy function - no longer used"""
    pass

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
