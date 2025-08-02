#!/usr/bin/env python3

# Quick test to verify AI generation works
import os
from utils.ai_generator import AIGenerator

def test_basic_generation():
    print("Testing AI generation...")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        print("ERROR: No GEMINI_API_KEY found")
        return False
    
    print(f"API key found: {api_key[:10]}...")
    
    try:
        # Create generator
        generator = AIGenerator()
        print(f"Generator created. Current request count: {generator.request_count}")
        
        # Test simple question
        test_question = "What is the capital of France?"
        print(f"Testing question: {test_question}")
        
        answer = generator.generate_answer(
            question=test_question,
            subject="Geography",
            mode="Understand Mode",
            custom_prompt="",
            reference_content=""
        )
        
        print(f"Answer received: {answer[:100]}...")
        print(f"Answer length: {len(answer)} characters")
        print(f"New request count: {generator.request_count}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_basic_generation()
    print(f"Test {'PASSED' if success else 'FAILED'}")