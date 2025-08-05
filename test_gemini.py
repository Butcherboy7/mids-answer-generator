#!/usr/bin/env python3
import os
import google.generativeai as genai

def test_gemini_api():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found")
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say hello")
        print(f"API Test Success: {response.text}")
        return True
    except Exception as e:
        print(f"API Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_gemini_api()