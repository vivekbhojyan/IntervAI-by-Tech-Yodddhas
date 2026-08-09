import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from models import StartInterviewRequest, ContinueInterviewRequest, InterviewResponse, InterviewProgress
from engine import InterviewState, generate_first_question, process_turn, MAX_QUESTIONS
from curriculum import get_curriculum

def make_progress(state: InterviewState) -> InterviewProgress:
    return InterviewProgress(
        phase=state.phase,
        question_count=state.question_count,
        max_questions=MAX_QUESTIONS,
        topics_covered=sorted(list(set(state.topics_covered)))
    )

app = FastAPI(title="AI Interview Agent")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: sessionId -> InterviewState
session_store: Dict[str, InterviewState] = {}
SESSION_TTL_SECONDS = 7200  # 2 hours TTL


def cleanup_expired_sessions():
    now = time.time()
    expired_ids = [
        sid for sid, state in list(session_store.items())
        if now - getattr(state, "last_active", getattr(state, "created_at", now)) > SESSION_TTL_SECONDS
    ]
    for sid in expired_ids:
        session_store.pop(sid, None)


from pydantic import ValidationError

@app.post("/api/interview", response_model=InterviewResponse)
async def interview_endpoint(request: Dict[str, Any]):
    cleanup_expired_sessions()
    if not isinstance(request, dict) or "sessionId" not in request or not request.get("sessionId"):
        raise HTTPException(status_code=422, detail="sessionId is required")
        
    session_id = request.get("sessionId")
    curriculum = get_curriculum()

    # Is this a new session?
    if "candidate" in request:
        try:
            start_req = StartInterviewRequest.model_validate(request)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

        state = InterviewState(
            session_id=session_id,
            candidate_profile=start_req.candidate.model_dump(),
            selected_domain=start_req.domain
        )
        try:
            reply = generate_first_question(state, curriculum)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
            
        session_store[session_id] = state
        return InterviewResponse(reply=reply, done=False, progress=make_progress(state))

    # Is this a continuing session?
    elif "message" in request:

        try:
            cont_req = ContinueInterviewRequest.model_validate(request)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

        if session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
            
        state = session_store[session_id]
        if state.done:
            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=state.feedback,
                progress=make_progress(state)
            )
            
        message = cont_req.message
        if not message.strip():
            # Gracefully handle empty message
            return InterviewResponse(
                reply="I didn't quite catch that. Could you please elaborate?",
                done=state.done,
                feedback=state.feedback,
                progress=make_progress(state)
            )
            
        try:
            reply = process_turn(state, message, curriculum)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
            
        if state.done:
            return InterviewResponse(
                reply=reply,
                done=True,
                feedback=state.feedback,
                progress=make_progress(state)
            )
        else:
            return InterviewResponse(reply=reply, done=False, progress=make_progress(state))

            
    else:
        raise HTTPException(status_code=422, detail="Invalid request format: payload must contain 'candidate' or 'message'")


@app.get("/api/domains")
async def get_domains():
    curriculum = get_curriculum()
    modules = curriculum.get("modules", [])
    res = []
    for mod in modules:
        start, end = mod.get("days", [0, 0])
        day_count = end - start + 1
        res.append({
            "number": mod.get("n"),
            "title": mod.get("title"),
            "startDay": start,
            "endDay": end,
            "dayCount": day_count
        })
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


