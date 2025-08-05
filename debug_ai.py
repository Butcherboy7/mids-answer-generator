#!/usr/bin/env python3
import os
import sys
sys.path.append('.')
from utils.ai_generator import AIGenerator

def test_ai_generator():
    print("Testing AIGenerator class...")
    try:
        ai_gen = AIGenerator()
        print("✓ AIGenerator initialized successfully")
        
        # Test single question
        test_question = "What is object-oriented programming?"
        answer = ai_gen.generate_answer(
            question=test_question,
            subject="Computer Science", 
            mode="Understand Mode"
        )
        print(f"✓ Single question test successful: {answer[:100]}...")
        
        # Test batch questions
        test_batch = [
            {"question": "What is Python?", "question_number": 1},
            {"question": "What is a variable?", "question_number": 2}
        ]
        batch_answers = ai_gen.generate_multi_question_answer(
            questions_batch=test_batch,
            subject="Computer Science",
            mode="Understand Mode"
        )
        print(f"✓ Batch test successful: {len(batch_answers)} answers generated")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ai_generator()