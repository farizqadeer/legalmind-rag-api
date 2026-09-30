from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
from rag_engine import CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME, answer_question
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# VALIDATE ENVIRONMENT AT STARTUP
# ─────────────────────────────────────────────

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file locally, "
        "or add it as an environment variable on Railway."
    )


# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

app = FastAPI(
    title="LegalMind RAG API",
    description="AI legal document Q&A system — Built by Fariz Qadeer",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# PYDANTIC MODELS
# ─────────────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model: str


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the Q&A chat interface"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>LegalMind RAG API Running</h1>"
                    "<p>Visit <a href='/docs'>/docs</a> to test the API</p>"
        )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check — Railway pings this to confirm the app is alive"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model=CHAT_MODEL_NAME
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Main RAG endpoint.
    Receives a question, retrieves relevant document chunks,
    generates an answer citing sources.
    """
    try:
        result = answer_question(request.question)

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG processing error: {str(e)}"
        )


@app.get("/api-info")
async def api_info():
    """Returns API information"""
    return {
        "api_name": "LegalMind RAG API",
        "version": "2.0.0",
        "model": f"{CHAT_MODEL_NAME} + {EMBEDDING_MODEL_NAME}",
        "endpoints": {
            "GET  /": "Q&A interface (HTML)",
            "GET  /health": "Health check",
            "POST /ask": "Ask a question about legal documents",
            "GET  /docs": "Interactive API documentation"
        },
        "sample_request": {
            "question": "Can I terminate the employment contract immediately for breach?"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )