"""
Run this file directly whenever you add, remove, or update
documents in the documents/ folder.

Usage:
    python ingest.py
"""

from dotenv import load_dotenv
from rag_engine import ingest_all_documents

load_dotenv()

if __name__ == "__main__":
    print("Starting document ingestion...")
    print("=" * 50)
    ingest_all_documents()
    print("=" * 50)
    print("Ingestion complete. You can now run main.py and ask questions.")