import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app, session_store
from models import Candidate

client = TestClient(app)

def test_missing_session_id():
    response = client.post("/api/interview", json={})
    assert response.status_code == 400
    assert "sessionId is required" in response.json()["detail"]

def test_invalid_continue_session():
    response = client.post("/api/interview", json={"sessionId": "invalid", "message": "hello"})
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_empty_message():
    # Setup mock session
    from engine import InterviewState
    session_store["test-session"] = InterviewState(
        session_id="test-session",
        candidate_profile={"member": {"name": "Test"}}
    )
    
    response = client.post("/api/interview", json={"sessionId": "test-session", "message": "   "})
    assert response.status_code == 200
    assert "elaborate" in response.json()["reply"]

# Note: We won't test the actual LLM calls here without mocking the OpenAI client,
# but these tests verify the API contract and session management logic.
