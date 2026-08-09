# AI Interview Agent

An adaptive, context-aware AI technical interviewer built for the AI Cohort hackathon.

Unlike standard chatbots, this agent behaves like a human interviewer:
- It **personalizes** the interview based on the candidate's journey (e.g. completed missions, attempt signals).
- It **adapts** the difficulty based on the candidate's responses.
- It asks **follow-up questions** to probe reasoning and engineering decisions.
- It provides **structured final feedback** identifying strengths and gaps.

## Architecture

The system is split into a modular backend and a modern frontend:

```text
Frontend (React/Vite)
   ↓ (REST API)
Interview API (FastAPI)
   ↓
Session Manager (In-memory dict for rapid dev, ready for Redis)
   ↓
Candidate Analyzer & Interview Controller (Phase routing & heuristics)
   ↓
LLM (OpenAI API with Structured Outputs)
   ↓
Answer Evaluator & Question Planner (Internal JSON evaluations)
```

## Adaptive Interview Logic

1. **Initialization**: The agent starts with a personalized question based on the candidate's profile and curriculum history.
2. **Evaluation & Planning**: Every user message is evaluated internally for correctness, depth, reasoning, and production-readiness.
3. **Question Selection**: Instead of randomly picking a question, the LLM determines the next best question based on the current evaluation and the required curriculum coverage.
4. **Phasing**: The interview progresses dynamically from Warm-up to Core Technical, Deep Dive, Production Scenarios, and a Final scenario.

## State Management

Interview state is maintained server-side mapping `sessionId` to an `InterviewState` Pydantic model. The state tracks asked questions, covered topics, history, internal LLM evaluations, and timestamps (`created_at`, `last_active`). To prevent memory leaks from abandoned sessions, an in-memory session TTL mechanism purges sessions that have been inactive for more than 2 hours (7200 seconds) on incoming requests. This prevents the LLM from losing context and ensures the mandatory constraints (e.g., maximum 15 questions) are enforced independently of the model.


## API Documentation

### `POST /api/interview`

Initializes an interview or submits the next turn.

**Request (Start Interview):**
```json
{
  "sessionId": "abc-123",
  "candidate": {
    "member": {
      "name": "Sarah Johnson",
      "jobRole": "Data Engineer",
      ...
    },
    ...
  }
}
```

**Request (Continue Interview):**
```json
{
  "sessionId": "abc-123",
  "message": "I used vector databases because..."
}
```

**Response:**
```json
{
  "reply": "That makes sense. How would you handle stale embeddings?",
  "done": false
}
```

**Final Response:**
```json
{
  "reply": "Thank you for your time.",
  "done": true,
  "feedback": {
    "summary": "Strong technical understanding...",
    "strengths": ["Clear explanation of RAG"],
    "gaps": ["Missed evaluation metrics"],
    "next": ["Practice writing eval datasets"]
  }
}
```

## Setup & Running

### Prerequisites
- Python 3.10+
- Node.js & npm

### Backend
1. `cd backend`
2. Create and activate a virtual environment: `python -m venv venv` and `source venv/bin/activate` (or `venv\Scripts\Activate.ps1` on Windows).
3. Install dependencies: `pip install -r requirements.txt`
4. Set your API Key: `export OPENAI_API_KEY=your_key_here` (or via `.env` file)
5. Start server: `uvicorn main:app --reload` (Runs on `${import.meta.env.VITE_API_URL}`)

### Frontend
1. `cd frontend`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev` (Runs on `http://localhost:5173`)

## Testing

Run tests by executing `pytest` inside the `backend/` directory. Tests cover the API endpoints, state persistence, and adaptive routing constraints.

## Design Decisions

- **FastAPI**: Chosen for rapid development, native Pydantic validation, and asynchronous support.
- **JSON-Mode & Pydantic Validation**: We use JSON-mode generation (`response_format={"type": "json_object"}`) combined with explicit Pydantic `.model_validate()` validation and safe fallback defaults on failure. This ensures robust parsing across OpenAI-compatible providers like Groq without relying on provider-specific `.parse()` methods.
- **React + TailwindCSS**: Provides a fast, dynamic, and aesthetically premium user interface with minimal bundle size. Glassmorphic effects and animations make the interview feel modern.

