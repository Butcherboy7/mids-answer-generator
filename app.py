import streamlit as st
import os
import tempfile
from datetime import datetime
from utils.pdf_processor import PDFProcessor
from utils.ai_generator import AIGenerator
from utils.pdf_compiler import PDFCompiler

# Page configuration
st.set_page_config(
    page_title="College Answer Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 College Answer Generator")
st.write("Upload your question bank PDF and get comprehensive AI-generated answers instantly!")

# Sidebar for configuration
with st.sidebar:
    st.header("📋 Configuration")
    
    # Subject selection
    subject = st.selectbox(
        "📚 Subject",
        ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", 
         "History", "Geography", "Economics", "Literature", "Philosophy", "Psychology", "Other"]
    )
    
    if subject == "Other":
        subject = st.text_input("Enter subject name:")
    
    # Mode selection
    mode = st.radio(
        "🎯 Answer Mode",
        ["Understand Mode", "Exam Mode"],
        help="Understand Mode: Detailed explanations with examples\nExam Mode: Concise, exam-focused answers"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📄 Upload Documents")
    
    # Question bank upload
    question_bank = st.file_uploader(
        "**Question Bank (Required)**",
        type=['pdf'],
        help="Upload a PDF containing the questions you want answers for"
    )
    
    # College notes upload (optional)
    college_notes = st.file_uploader(
        "**College Notes (Optional)**",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload reference materials to improve answer quality"
    )

with col2:
    st.subheader("⚙️ Settings")
    
    # Custom instructions
    custom_prompt = st.text_area(
        "**Custom Instructions**",
        placeholder="Enter any specific instructions for answer generation...",
        height=100
    )

# Main processing button
if st.button("🚀 Generate Answers", type="primary", disabled=not question_bank):
    if question_bank:
        with st.spinner("Processing your document and generating answers..."):
            try:
                # Initialize processors
                pdf_processor = PDFProcessor()
                ai_generator = AIGenerator()
                pdf_compiler = PDFCompiler()
                
                # Step 1: Extract text
                st.info("📄 Extracting text from your document...")
                extracted_text = pdf_processor.extract_text_from_pdf(question_bank)
                
                if not extracted_text or len(extracted_text.strip()) < 50:
                    st.error("❌ Could not extract readable text from the PDF. Please ensure your document contains text (not just images).")
                    st.stop()
                
                # Step 2: Find questions
                st.info("🔍 Searching for questions in the document...")
                questions = pdf_processor.extract_questions(extracted_text)
                
                if not questions:
                    st.error("❌ No questions found in the document.")
                    with st.expander("📝 View extracted text for debugging"):
                        st.text(extracted_text[:2000])
                    st.stop()
                
                st.success(f"✅ Found {len(questions)} questions!")
                
                # Show extracted questions
                with st.expander(f"📋 Preview of {len(questions)} extracted questions"):
                    for i, q in enumerate(questions[:5]):
                        st.write(f"**Q{i+1}:** {q}")
                    if len(questions) > 5:
                        st.write(f"... and {len(questions)-5} more questions")
                
                # Step 3: Process reference notes
                reference_content = ""
                if college_notes:
                    st.info("📚 Processing your reference notes...")
                    reference_content = pdf_processor.process_college_notes(college_notes)
                    if reference_content:
                        st.success(f"✅ Processed {len(college_notes)} reference documents")
                
                # Step 4: Generate answers
                st.info("🤖 Generating comprehensive AI answers...")
                answers = []
                
                # Process in batches for efficiency
                batch_size = 3
                total_batches = (len(questions) + batch_size - 1) // batch_size
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for batch_num in range(total_batches):
                    start_idx = batch_num * batch_size
                    end_idx = min(start_idx + batch_size, len(questions))
                    batch_questions = questions[start_idx:end_idx]
                    
                    # Update progress
                    progress = (batch_num + 1) / total_batches
                    progress_bar.progress(progress)
                    status_text.info(f"Processing batch {batch_num + 1} of {total_batches} ({len(batch_questions)} questions)")
                    
                    # Prepare batch data
                    questions_data = [
                        {"question": q, "question_number": start_idx + i + 1} 
                        for i, q in enumerate(batch_questions)
                    ]
                    
                    # Generate answers for this batch
                    batch_answers = ai_generator.generate_multi_question_answer(
                        questions_batch=questions_data,
                        subject=subject,
                        mode=mode,
                        custom_prompt=custom_prompt,
                        reference_content=reference_content
                    )
                    
                    answers.extend(batch_answers)
                
                progress_bar.progress(1.0)
                status_text.success(f"✅ Generated {len(answers)} comprehensive answers!")
                
                # Step 5: Create PDF
                st.info("📄 Creating your professional answer PDF...")
                pdf_path = pdf_compiler.compile_answers_pdf(
                    answers=answers,
                    subject=subject,
                    mode=mode,
                    custom_prompt=custom_prompt
                )
                
                # Success message and results
                st.balloons()
                st.success("🎉 Answer generation completed successfully!")
                
                # Preview answers
                with st.expander("📖 Preview Generated Answers", expanded=True):
                    for i, ans in enumerate(answers[:3]):
                        st.write(f"**Q{ans['question_number']}: {ans['question']}**")
                        st.write(ans['answer'][:400] + "..." if len(ans['answer']) > 400 else ans['answer'])
                        st.write("---")
                    if len(answers) > 3:
                        st.write(f"📚 Plus {len(answers)-3} more detailed answers in the complete PDF")
                
                # Download button
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                        
                    filename = f"answers_{subject.replace(' ', '_')}_{mode.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    
                    st.download_button(
                        label="📥 Download Complete Answer PDF",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                else:
                    st.error("Failed to create PDF file")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                import traceback
                with st.expander("🔧 Technical Details"):
                    st.code(traceback.format_exc())
    else:
        st.warning("Please upload a question bank PDF to get started.")