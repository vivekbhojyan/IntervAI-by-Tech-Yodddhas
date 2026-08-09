from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CandidateMember(BaseModel):
    id: str
    name: str
    jobRole: str
    yearsExperience: int
    education: str
    status: str

class CandidateMission(BaseModel):
    day: int
    title: str
    passed: Optional[bool] = None
    skipped: Optional[bool] = None
    attempts: Optional[int] = 0

class CandidateSignals(BaseModel):
    commitDays: int
    missionsCompleted: int
    missionsFirstTry: int

class Candidate(BaseModel):
    member: CandidateMember
    missions: List[CandidateMission]
    signals: CandidateSignals

class StartInterviewRequest(BaseModel):
    sessionId: str
    candidate: Candidate
    domain: Optional[int] = None


class ContinueInterviewRequest(BaseModel):
    sessionId: str
    message: str

class FinalFeedback(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]

class InterviewProgress(BaseModel):
    phase: str
    question_count: int
    max_questions: int
    topics_covered: List[int]

class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[FinalFeedback] = None
    progress: Optional[InterviewProgress] = None


# Internal Models for LLM Output

class LLMEvaluation(BaseModel):
    answer_quality: str = Field(description="One of: weak, partial, solid, strong, exceptional")
    technical_depth: int = Field(description="1-5 rating of technical depth")
    reasoning_depth: int = Field(description="1-5 rating of reasoning depth")
    identified_strengths: List[str]
    identified_gaps: List[str]
    recommended_action: str = Field(description="E.g., follow_up, change_topic, increase_difficulty, end_interview")
    is_non_answer: bool = Field(
        default=False,
        description="True when the candidate did not attempt a substantive answer",
    )

class LLMNextQuestion(BaseModel):
    curriculum_day: int = Field(description="The curriculum day number this question targets")
    competency: str = Field(description="The competency being tested (e.g., 'retrieval architecture')")
    reasoning: str = Field(description="Why this question is being asked next")
    next_question: str = Field(description="The actual question to ask the candidate")

class LLMFeedback(BaseModel):
    summary: str = Field(description="Overall technical level based on interview")
    strengths: List[str] = Field(description="Specific, evidence-based strengths")
    gaps: List[str] = Field(description="Specific knowledge gaps")
    next: List[str] = Field(description="Actionable next steps")

class LLMTurnOutput(BaseModel):
    evaluation: LLMEvaluation
    next_step: LLMNextQuestion
