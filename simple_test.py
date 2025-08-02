import streamlit as st
import os
from utils.ai_generator import AIGenerator

st.title("Simple Answer Generator Test")

# Test the AI generation directly
if st.button("Test AI Generation"):
    try:
        # Create AI generator
        ai_gen = AIGenerator()
        
        # Test questions
        test_questions = [
            {"question": "What is artificial intelligence?", "question_number": 1},
            {"question": "Explain machine learning concepts.", "question_number": 2},
            {"question": "What are neural networks?", "question_number": 3}
        ]
        
        st.write("Testing multi-question batch processing...")
        
        # Call the multi-question function
        answers = ai_gen.generate_multi_question_answer(
            questions_batch=test_questions,
            subject="Computer Science",
            mode="Understand Mode",
            custom_prompt="",
            reference_content=""
        )
        
        st.write(f"Generated {len(answers)} answers:")
        
        for ans in answers:
            st.write(f"**Q{ans['question_number']}**: {ans['question']}")
            st.write(f"**Answer**: {ans['answer'][:200]}...")
            st.write("---")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.write(traceback.format_exc())