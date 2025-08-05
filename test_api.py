#!/usr/bin/env python3
"""
Simple API test to verify Gemini API is working
"""

import os
from google import genai

def test_gemini_api():
    """Test if the Gemini API is working properly"""
    
    try:
        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            return False
        
        print(f"✓ Found GEMINI_API_KEY: {api_key[:10]}...")
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✓ Gemini client initialized")
        
        # Test simple request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'Hello, API test successful!' if you can read this."
        )
        
        if response.text:
            print(f"✓ API Response: {response.text}")
            return True
        else:
            print("❌ Empty response from API")
            return False
            
    except Exception as e:
        print(f"❌ API Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Gemini API connection...")
    success = test_gemini_api()
    
    if success:
        print("\n🎉 API test completed successfully!")
    else:
        print("\n💥 API test failed. Check your API key and try again.")