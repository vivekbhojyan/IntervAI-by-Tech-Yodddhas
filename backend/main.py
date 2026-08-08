from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from models import StartInterviewRequest, ContinueInterviewRequest, InterviewResponse
from engine import InterviewState, generate_first_question, process_turn
from curriculum import get_curriculum

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

@app.post("/api/interview", response_model=InterviewResponse)
async def interview_endpoint(request: Dict[str, Any]):
    session_id = request.get("sessionId")
    if not session_id:
        raise HTTPException(status_code=400, detail="sessionId is required")
        
    curriculum = get_curriculum()

    # Is this a new session?
    if "candidate" in request:
        candidate_data = request.get("candidate")
        # Initialize state
        state = InterviewState(
            session_id=session_id,
            candidate_profile=candidate_data
        )
        try:
            reply = generate_first_question(state, curriculum)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
            
        session_store[session_id] = state
        return InterviewResponse(reply=reply, done=False)
        
    # Is this a continuing session?
    elif "message" in request:
        if session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")
            
        state = session_store[session_id]
        if state.done:
            return InterviewResponse(
                reply="Interview completed.",
                done=True,
                feedback=state.feedback
            )
            
        message = request.get("message")
        if not message.strip():
            # Gracefully handle empty message
            return InterviewResponse(
                reply="I didn't quite catch that. Could you please elaborate?",
                done=state.done,
                feedback=state.feedback
            )
            
        try:
            reply = process_turn(state, message, curriculum)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
            
        if state.done:
            return InterviewResponse(
                reply=reply,
                done=True,
                feedback=state.feedback
            )
        else:
            return InterviewResponse(reply=reply, done=False)
            
    else:
        raise HTTPException(status_code=400, detail="Invalid request format")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
