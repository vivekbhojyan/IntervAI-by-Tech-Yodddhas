import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app, session_store
from models import Candidate

client = TestClient(app)

def test_missing_session_id():
    response = client.post("/api/interview", json={})
    assert response.status_code == 422
    assert "sessionId is required" in response.json()["detail"]

def test_missing_candidate_member():
    payload = {
        "sessionId": "s1",
        "candidate": {
            "missions": [],
            "signals": {"commitDays": 1, "missionsCompleted": 1, "missionsFirstTry": 1}
        }
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 422

def test_wrong_years_experience_type():
    payload = {
        "sessionId": "s2",
        "candidate": {
            "member": {
                "id": "1",
                "name": "Alex",
                "jobRole": "Dev",
                "yearsExperience": "five",
                "education": "CS",
                "status": "COMPLETED"
            },
            "missions": [],
            "signals": {"commitDays": 1, "missionsCompleted": 1, "missionsFirstTry": 1}
        }
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 422

def test_missing_missions_array():
    payload = {
        "sessionId": "s3",
        "candidate": {
            "member": {
                "id": "1",
                "name": "Alex",
                "jobRole": "Dev",
                "yearsExperience": 5,
                "education": "CS",
                "status": "COMPLETED"
            },
            "signals": {"commitDays": 1, "missionsCompleted": 1, "missionsFirstTry": 1}
        }
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 422


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

def test_max_questions_termination():
    from unittest.mock import patch
    from engine import InterviewState, process_turn, MAX_QUESTIONS

    state = InterviewState(
        session_id="max-test",
        candidate_profile={"member": {"name": "Test Candidate"}},
        question_count=MAX_QUESTIONS,
        topics_covered=[1],
        phase="Warm-up"
    )
    with patch("engine.generate_final_feedback") as mock_feedback:
        mock_feedback.return_value = "Thank you for your time. The interview is now complete."
        result = process_turn(state, "My answer", {})
        assert mock_feedback.called
        assert result == "Thank you for your time. The interview is now complete."

def test_malformed_llm_json_fallback():
    from unittest.mock import patch, MagicMock
    from engine import InterviewState, process_turn, generate_final_feedback

    state = InterviewState(
        session_id="malformed-json-test",
        candidate_profile={"member": {"name": "Test Candidate"}},
        question_count=2,
        evaluations=[
            {
                "identified_strengths": ["Clear RAG explanation"],
                "identified_gaps": ["Lacks monitoring details"]
            }
        ]
    )

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "INVALID_JSON_OR_MALFORMED_SCHEMA"

    with patch("engine.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        turn_result = process_turn(state, "My response", {})
        assert isinstance(turn_result, str)
        assert len(turn_result) > 0

        feedback_msg = generate_final_feedback(state)
        assert state.done is True
        assert state.feedback is not None
        assert "Clear RAG explanation" in state.feedback.strengths
        assert "Lacks monitoring details" in state.feedback.gaps

def test_get_relevant_curriculum():
    from curriculum import get_relevant_curriculum
    sample_curriculum = {
        "cohort": "Test Cohort",
        "modules": [],
        "days": [
            {"day": 1, "title": "Day 1 Title", "objectives": ["Obj 1", "Obj 2"]},
            {"day": 2, "title": "Day 2 Title", "objectives": ["Obj A", "Obj B"]},
            {"day": 3, "title": "Day 3 Title", "objectives": ["Obj X", "Obj Y"]}
        ]
    }
    topics_covered = [1]
    candidate_missions = [{"day": 2, "title": "Day 2 Title"}]

    res = get_relevant_curriculum(sample_curriculum, topics_covered, candidate_missions)

    day1 = next(d for d in res["days"] if d["day"] == 1)
    assert "objectives" in day1

    day2 = next(d for d in res["days"] if d["day"] == 2)
    assert "objectives" in day2

    day3 = next(d for d in res["days"] if d["day"] == 3)
    assert "objectives" not in day3
    assert day3 == {"day": 3, "title": "Day 3 Title"}

def test_session_expiration():
    import time
    from main import session_store, cleanup_expired_sessions
    from engine import InterviewState

    old_state = InterviewState(
        session_id="expired-session",
        candidate_profile={"member": {"name": "Old"}},
        last_active=time.time() - 8000
    )
    new_state = InterviewState(
        session_id="active-session",
        candidate_profile={"member": {"name": "New"}},
        last_active=time.time()
    )

    session_store["expired-session"] = old_state
    session_store["active-session"] = new_state

    cleanup_expired_sessions()

    assert "expired-session" not in session_store
    assert "active-session" in session_store

def test_progress_payload_response():
    from engine import InterviewState
    session_store["prog-session"] = InterviewState(
        session_id="prog-session",
        candidate_profile={"member": {"name": "Progress User"}},
        phase="Core Technical",
        question_count=3,
        topics_covered=[1, 2]
    )

    response = client.post("/api/interview", json={"sessionId": "prog-session", "message": "   "})
    assert response.status_code == 200
    data = response.json()
    assert "progress" in data
    assert data["progress"]["phase"] == "Core Technical"
    assert data["progress"]["question_count"] == 3
    assert data["progress"]["max_questions"] == 15
    assert data["progress"]["topics_covered"] == [1, 2]

def test_get_domains_endpoint():
    response = client.get("/api/domains")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8
    first_mod = data[0]
    assert "number" in first_mod
    assert "title" in first_mod
    assert "startDay" in first_mod
    assert "endDay" in first_mod
    assert "dayCount" in first_mod

def test_get_domain_curriculum_filtering():
    from curriculum import get_domain_curriculum, get_curriculum

    mod3_curr = get_domain_curriculum(3)
    mod3_day_ids = [d["day"] for d in mod3_curr["days"]]
    assert mod3_day_ids == [7, 8, 9, 10]

    mod1_curr = get_domain_curriculum(1)
    mod1_day_ids = [d["day"] for d in mod1_curr["days"]]
    assert set(mod1_day_ids) == {1, 2, 3, 4, 5, 6}

    full_curr = get_curriculum()
    assert len(get_domain_curriculum(None)["days"]) == len(full_curr["days"])
    assert len(get_domain_curriculum(999)["days"]) == len(full_curr["days"])

def test_start_interview_with_domain():
    from unittest.mock import patch
    from main import session_store

    payload = {
        "sessionId": "domain-session-123",
        "candidate": {
            "member": {
                "id": "CAND-001",
                "name": "Sarah",
                "jobRole": "Engineer",
                "yearsExperience": 5,
                "education": "BS",
                "status": "COMPLETED"
            },
            "missions": [],
            "signals": {"commitDays": 10, "missionsCompleted": 10, "missionsFirstTry": 5}
        },
        "domain": 3
    }

    with patch("main.generate_first_question") as mock_gen:
        mock_gen.return_value = "What are vector embeddings?"
        response = client.post("/api/interview", json=payload)
        assert response.status_code == 200
        assert "domain-session-123" in session_store
        assert session_store["domain-session-123"].selected_domain == 3


def _mock_turn(day):
    from unittest.mock import MagicMock

    response = MagicMock()
    response.choices[0].message.content = __import__("json").dumps({
        "evaluation": {
            "answer_quality": "solid", "technical_depth": 3,
            "reasoning_depth": 3, "identified_strengths": [],
            "identified_gaps": [], "recommended_action": "change_topic",
            "is_non_answer": False,
        },
        "next_step": {
            "curriculum_day": day, "competency": "agents",
            "reasoning": "test", "next_question": "Test question?",
        },
    })
    return response


def test_domain_scope_uses_adjacent_day_only_after_selected_days_exhausted():
    from unittest.mock import MagicMock, patch
    session_id = "short-domain-session"
    payload = {
        "sessionId": session_id,
        "candidate": {
            "member": {
                "id": "CAND-SHORT", "name": "Test", "jobRole": "Engineer",
                "yearsExperience": 1, "education": "BS", "status": "COMPLETED",
            },
            "missions": [],
            "signals": {"commitDays": 1, "missionsCompleted": 1, "missionsFirstTry": 1},
        },
        "domain": 1,
    }
    first_question = MagicMock()
    first_question.choices[0].message.content = "Domain question?"
    with patch("engine.get_client") as get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = [
            first_question, _mock_turn(1), _mock_turn(2), _mock_turn(3), _mock_turn(4)
        ]
        get_client.return_value = mock_client
        for _ in range(5):
            if _ == 0:
                response = client.post("/api/interview", json=payload)
            else:
                response = client.post(
                    "/api/interview", json={"sessionId": session_id, "message": "answer"}
                )
            assert response.status_code == 200

    state = session_store[session_id]
    assert state.topics_covered == [1, 2, 3, 4]
    assert all(day in {1, 2, 3} for day in state.topics_covered[:3])


def test_out_of_domain_llm_day_is_remapped_before_recording():
    from unittest.mock import MagicMock, patch
    from engine import InterviewState, process_turn

    state = InterviewState(
        session_id="agentic-domain-leak", candidate_profile={"member": {"name": "Test"}},
        selected_domain=6, question_count=1,
    )
    with patch("engine.get_client") as get_client:
        mock_client = MagicMock()
        first_invalid = _mock_turn(28)
        first_invalid.choices[0].message.content = first_invalid.choices[0].message.content.replace(
            "Test question?", "How would you deploy Kubernetes?"
        )
        second_invalid = _mock_turn(28)
        second_invalid.choices[0].message.content = second_invalid.choices[0].message.content.replace(
            "Test question?", "How would you deploy Kubernetes?"
        )
        mock_client.chat.completions.create.side_effect = [first_invalid, second_invalid]
        get_client.return_value = mock_client
        question = process_turn(state, "answer", {})

    assert state.topics_covered == [21]
    assert question == (
        "Walk me through how you approached: "
        "Convert function-calling workflows into a reasoning agent"
    )
    assert "Kubernetes" not in question


def test_non_answers_teach_then_cover_four_distinct_days():
    from unittest.mock import MagicMock, patch
    from curriculum import get_curriculum
    from engine import InterviewState, process_turn

    state = InterviewState(
        session_id="non-answer-diversity", candidate_profile={"member": {"name": "Test"}},
        question_count=1,
    )
    non_answer = _mock_turn(12)
    payload = __import__("json").loads(non_answer.choices[0].message.content)
    payload["evaluation"]["is_non_answer"] = True
    payload["evaluation"]["identified_strengths"] = ["Incorrectly credited strength"]
    payload["next_step"]["next_question"] = "Repeat the prompt engineering question."
    non_answer.choices[0].message.content = __import__("json").dumps(payload)

    with patch("engine.get_client") as get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = non_answer
        get_client.return_value = mock_client
        replies = [process_turn(state, "I don't know", get_curriculum()) for _ in range(4)]

    assert len(set(state.topics_covered)) == 4
    assert state.topics_covered == [1, 2, 3, 4]
    assert "No worries" in replies[0]
    assert "Quick rundown:" in replies[0]
    assert "Let's move on:" in replies[0]
    assert "Walk me through how you approached:" in replies[0]
    assert "Incorrectly credited strength" not in state.evaluations[0]["identified_strengths"]
    assert "Could not demonstrate understanding" in state.evaluations[0]["identified_gaps"][0]


def test_all_non_answers_complete_an_eight_question_interview_with_diversity():
    from unittest.mock import MagicMock, patch
    from curriculum import get_curriculum
    from engine import InterviewState, process_turn

    state = InterviewState(
        session_id="all-no-full-run", candidate_profile={"member": {"name": "Test"}},
        question_count=1,
        history=[{"role": "assistant", "content": "Explain word embeddings and how sentiment analysis uses them."}],
    )
    non_answer = _mock_turn(7)
    turn_payload = __import__("json").loads(non_answer.choices[0].message.content)
    turn_payload["evaluation"]["is_non_answer"] = True
    turn_payload["next_step"]["next_question"] = "Embeddings are vectors."
    non_answer.choices[0].message.content = __import__("json").dumps(turn_payload)
    final_response = MagicMock()
    final_response.choices[0].message.content = __import__("json").dumps({
        "summary": "Completed", "strengths": [],
        "gaps": ["Could not demonstrate understanding"], "next": ["Practice"],
    })

    with patch("engine.get_client") as get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = [non_answer] * 7 + [final_response]
        get_client.return_value = mock_client
        transcript = [process_turn(state, "no, I don't know", get_curriculum()) for _ in range(8)]

    assert state.done is True
    assert state.question_count == 8
    assert len(set(state.topics_covered)) >= 4
    assert "No worries" in transcript[0]
    assert "Quick rundown:" in transcript[0]
    assert "Let's move on:" in transcript[0]
    assert "Embeddings are vectors." not in transcript[0]


def test_final_feedback_keeps_taught_non_answer_as_a_gap():
    from unittest.mock import MagicMock, patch
    from engine import InterviewState, generate_final_feedback

    state = InterviewState(
        session_id="non-answer-feedback", candidate_profile={"member": {"name": "Test"}},
        evaluations=[{
            "is_non_answer": True,
            "identified_strengths": [],
            "identified_gaps": ["Could not demonstrate understanding of curriculum day 12"],
        }],
    )
    invalid_response = MagicMock()
    invalid_response.choices[0].message.content = "not json"
    with patch("engine.get_client") as get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = invalid_response
        get_client.return_value = mock_client
        generate_final_feedback(state)

    assert state.feedback.strengths == []
    assert state.feedback.gaps == ["Could not demonstrate understanding of curriculum day 12"]
