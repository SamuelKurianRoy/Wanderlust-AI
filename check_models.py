"""
Quick script to check available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    api_key = input("Enter your Gemini API key: ")

genai.configure(api_key=api_key)

print("Fetching available models...\n")

try:
    models = genai.list_models()
    
    print("=" * 60)
    print("AVAILABLE MODELS THAT SUPPORT generateContent:")
    print("=" * 60)
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✅ {model.name}")
            print(f"   Display name: {model.display_name}")
            print(f"   Description: {model.description[:100] if model.description else 'N/A'}...")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"Error: {e}")
