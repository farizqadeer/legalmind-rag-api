import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available CHAT models for your API key:")
print("=" * 50)

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"Name: {model.name}")
        print("-" * 30)