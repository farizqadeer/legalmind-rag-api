from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_returns_html():
    response = client.get("/")
    assert response.status_code == 200


def test_api_info():
    response = client.get("/api-info")
    assert response.status_code == 200
    assert "endpoints" in response.json()
    assert response.json()["model"] == "gemini-3.8-flash + models/gemini-embedding-001"


def test_ask_empty_question_rejected():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422


def test_ask_whitespace_question_rejected():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422


def test_ask_missing_question_rejected():
    response = client.post("/ask", json={})
    assert response.status_code == 422