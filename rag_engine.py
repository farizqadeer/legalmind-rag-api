from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
import os

CHROMA_PATH = "chroma_db"
DOCUMENTS_PATH = "documents"

# ─────────────────────────────────────────────
# CORRECT MODEL NAMES — do not change these
# ─────────────────────────────────────────────
CHAT_MODEL_NAME = "gemini-3.8-flash"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-2-preview"


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


def get_llm():
    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL_NAME,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )


def get_vectorstore():
    return Chroma(
        collection_name="legal_documents",
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_PATH
    )


def ingest_all_documents():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    vectorstore = get_vectorstore()

    all_files = [f for f in os.listdir(DOCUMENTS_PATH) if f.endswith(".txt")]

    if not all_files:
        print("No .txt files found in documents/ folder.")
        return

    total_chunks = 0

    for filename in all_files:
        filepath = os.path.join(DOCUMENTS_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = splitter.split_text(text)
        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

        vectorstore.add_texts(
            texts=chunks,
            metadatas=metadatas,
            ids=ids
        )

        total_chunks += len(chunks)
        print(f"Ingested {len(chunks)} chunks from {filename}")

    print(f"\nTotal chunks ingested: {total_chunks}")
    print(f"Vector database saved to: {CHROMA_PATH}")


def retrieve_context(query: str, n_results: int = 4):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=n_results)

    chunks = []
    sources = []
    scores = []

    for doc, score in results:
        chunks.append(doc.page_content)
        sources.append(doc.metadata.get("source", "unknown"))
        scores.append(round(1 - score, 3))

    return chunks, sources, scores


def answer_question(query: str):
    chunks, sources, scores = retrieve_context(query, n_results=4)

    if not chunks:
        return {
            "answer": "I could not find any relevant information in the uploaded documents. "
                      "Please make sure documents have been ingested first by running: python ingest.py",
            "sources": [],
            "confidence": "none"
        }

    context_text = "\n\n".join([
        f"[Source: {source}]\n{chunk}"
        for chunk, source in zip(chunks, sources)
    ])

    system_prompt = f"""You are a legal document assistant.
Answer the user's question using ONLY the context provided below.
If the context does not contain enough information to fully answer,
say so clearly rather than guessing.
Always mention which source document your answer is based on.
Keep your answer clear, concise, and professional.

Context:
{context_text}"""

    llm = get_llm()
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])

    unique_sources = list(dict.fromkeys(sources))
    avg_score = sum(scores) / len(scores) if scores else 0
    confidence = "high" if avg_score > 0.7 else "medium" if avg_score > 0.4 else "low"

    return {
        "answer": response.content,
        "sources": unique_sources,
        "confidence": confidence
    }