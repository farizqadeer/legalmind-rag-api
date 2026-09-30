#!/bin/sh
set -eu

: "${GEMINI_API_KEY:?GEMINI_API_KEY must be set at runtime}"
export CHROMA_PATH="${CHROMA_PATH:-chroma_db_gemini_embedding_001}"
export PORT="${PORT:-8000}"

if [ ! -f "$CHROMA_PATH/.ingestion_complete" ]; then
    python ingest.py
    mkdir -p "$CHROMA_PATH"
    touch "$CHROMA_PATH/.ingestion_complete"
fi

exec uvicorn main:app --host 0.0.0.0 --port "$PORT"