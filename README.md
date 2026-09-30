# LegalMind — AI Legal Document Assistant ⚖️

An AI-powered legal document Q&A system using Retrieval Augmented Generation (RAG). Ask questions in plain English about your contracts and get accurate answers with source citations — grounded only in your actual documents, never hallucinated.

## Live Demo


## What It Does
- Answers questions about employment contracts, NDAs, and rental agreements
- Cites exactly which document and section the answer comes from
- Shows confidence level for every answer
- Searches across multiple documents simultaneously
- Never invents information — answers only from your actual documents

## Tech Stack
| Layer | Technology |
|---|---|
| AI Model | Google Gemini 3.8 Flash |
| Embeddings | Google Gemini Embedding 2 Preview |
| Vector Database | ChromaDB |
| Orchestration | LangChain |
| API Server | FastAPI |
| Frontend | Vanilla HTML + CSS + JavaScript |
| Deployment | Docker + Railway |

## How RAG Works
Documents → Split into chunks → Embed into vectors → Store in ChromaDB
↓
User Question → Embed question → Search for similar chunks → Retrieve top 4
↓
Gemini reads chunks → Generates grounded answer
↓
Answer + Source citations returned

## Project Structure
legalmind-rag-api/
├── main.py # FastAPI server
├── rag_engine.py # Full RAG pipeline
├── ingest.py # Document ingestion script
├── documents/ # Your legal documents go here
│ ├── employment_contract.txt
│ ├── nda_agreement.txt
│ └── rental_agreement.txt
├── templates/
│ └── index.html # Q&A interface
├── tests/
│ └── test_api.py
├── Dockerfile # Runs ingest during build
├── docker-compose.yml
└── requirements.txt

## Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/legalmind-rag-api.git
cd legalmind-rag-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "GEMINI_API_KEY=your-key-here" > .env

# IMPORTANT: Ingest documents first (creates the vector database)
python ingest.py

# Run the server
python main.py
```

Visit `http://localhost:8000` to use the Q&A interface.

## Adding Your Own Documents
```bash
# 1. Drop any .txt file into the documents/ folder
# 2. Re-run ingestion
python ingest.py
# 3. Restart the server
python main.py
# System immediately knows about the new document
```

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Q&A interface |
| GET | /health | Health check |
| POST | /ask | Ask a question |
| GET | /docs | Interactive API docs |

## Sample Questions to Test
Can I terminate the employment contract immediately for a material breach?
How long does confidentiality last after the NDA ends?
What is the security deposit and when is it refunded?
What is the non-compete period after leaving the job?
Who is responsible for major repairs in the rental property?

## Key Concepts Demonstrated
- **RAG Pipeline** — retrieval before generation prevents hallucination
- **Vector Embeddings** — semantic search finds relevant chunks by meaning not keywords
- **ChromaDB** — persistent vector database with similarity search
- **Chunk Strategy** — RecursiveCharacterTextSplitter with overlap preserves context
- **Source Citation** — every answer traces back to its source document
- **Confidence Scoring** — answers rated high/medium/low based on retrieval similarity

## Built By
Fariz Qadeer — AI Engineer
[LinkedIn](https://linkedin.com/in/farizqadeer) | [GitHub](https://github.com/farizqadeer)
