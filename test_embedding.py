# test_embedding.py
# Run this to find which embedding model name format works
# python test_embedding.py

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Every possible format to try
model_names_to_try = [
    "gemini-embedding-2",
    "models/gemini-embedding-2",
    "gemini-embedding-2-preview",
    "models/gemini-embedding-2-preview",
    "gemini-embedding-exp-03-07",
    "models/gemini-embedding-exp-03-07",
    "text-embedding-004",
    "models/text-embedding-004",
    "embedding-001",
    "models/embedding-001",
]

test_text = "This is a test sentence for embedding."

for model_name in model_names_to_try:
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        result = embeddings.embed_query(test_text)
        print(f"✅ WORKS: {model_name}  — vector length: {len(result)}")
    except Exception as e:
        print(f"❌ FAILS: {model_name}  — {str(e)[:60]}")