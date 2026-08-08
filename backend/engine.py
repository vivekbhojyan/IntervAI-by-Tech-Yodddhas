```python
import os
import json
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from models import (
    LLMEvaluation,
    LLMNextQuestion,
    LLMFeedback,
    FinalFeedback,
)

# Load variables from .env during local development
load_dotenv()


def get_client():
    """
    Create the Groq client using the API key stored
    in the GROQ_API_KEY environment variable.
    """

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Create a .env file with GROQ_API_KEY=<your-key>."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


class InterviewState(BaseModel):
    session_id: str
    candidate_profile: dict

    phase: str = "Warm-up"
    question_count: int = 0

    topics_covered: list[int] = Field(default_factory=list)

    history: list[dict] = Field(default_factory=list)

    evaluations: list[dict] = Field(default_factory=list)

    done: bool = False
    feedback: Optional[FinalFeedback] = None

    def get_context_summary(self) -> str:
        tested_days = sorted(set(self.topics_covered))

        return f"""
Candidate: {self.candidate_profile.get('member', {}).get('name', 'Unknown')}
Role: {self.candidate_profile.get('member', {}).get('jobRole', '')}
Experience: {self.candidate_profile.get('member', {}).get('yearsExperience', 0)} years
Phase: {self.phase}
Questions Asked: {self.question_count}
Topics Covered (Days): {tested_days}
"""


def generate_first_question(
    state: InterviewState,
    curriculum: dict
) -> str:

    client = get_client()

    system_prompt = f"""
You are an expert AI Technical Interviewer.

Your goal is to conduct a personalized technical interview
based on the candidate's actual learning journey.

Do not ask a fixed list of questions.

Be conversational, rigorous, and adaptive.

Candidate Profile:
{json.dumps(state.candidate_profile, indent=2)}

Curriculum:
{json.dumps(curriculum, indent=2)}

Instructions:

1. Start naturally.
2. Select a topic relevant to the candidate.
3. Prefer topics the candidate actually completed.
4. Use failed or repeatedly attempted missions as areas worth probing.
5. Do not assume that passing a mission means mastery.
6. Do not aggressively penalize skipped topics.
7. Ask one meaningful technical question.
8. Do not reveal the interview plan.
9. Do not provide the answer.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": (
                "Start the interview. "
                "Output ONLY the first interviewer message/question."
            )
        }
    ]

    response = client.chat.completions.create(
        model=os.environ.get(
            "MODEL_NAME",
            "llama-3.1-8b-instant"
        ),
        messages=messages,
        temperature=0.7,
    )

    first_question = response.choices[0].message.content.strip()

    state.history.append(
        {
            "role": "assistant",
            "content": first_question,
        }
    )

    state.question_count += 1

    return first_question


def process_turn(
    state: InterviewState,
    candidate_message: str,
    curriculum: dict
) -> str:

    client = get_client()

    state.history.append(
        {
            "role": "user",
            "content": candidate_message,
        }
    )

    unique_days = len(set(state.topics_covered))

    # Minimum interview requirement:
    # at least 8 questions and 4 curriculum days.
    if (
        state.question_count >= 8
        and unique_days >= 4
        and state.phase == "Final"
    ):
        return generate_final_feedback(state)

    curriculum_context = json.dumps(
        curriculum,
        indent=2
    )

    eval_prompt = f"""
You are conducting a realistic adaptive technical interview.

Analyze the candidate's latest answer.

Candidate context:
{state.get_context_summary()}

Curriculum:
{curriculum_context}

Previous conversation:
{json.dumps(state.history, indent=2)}

Evaluate:

- correctness
- technical depth
- reasoning
- implementation understanding
- engineering trade-offs
- production awareness
- communication clarity

Important rules:

1. Do not ask a fixed sequence of questions.
2. Generate the next question based on the candidate's actual answer.
3. Do not repeat an already answered question.
4. If the answer is strong, increase difficulty.
5. If the answer is weak, probe the same concept once before changing topic.
6. Use "why", "what if", debugging, architecture, and trade-off questions.
7. Use candidate learning history for personalization.
8. Do not reveal internal evaluation.
9. Do not teach the candidate the answer.
10. Track curriculum day coverage.
11. The interview must eventually cover at least 4 different curriculum days.
12. The interview must contain at least 8 meaningful questions.
13. Prefer depth over asking many unrelated questions.

Interview phases:

Warm-up
→ Core Technical
→ Deep Dive
→ Architecture
→ Production
→ Final

Current question count:
{state.question_count}

Return ONLY valid JSON.

Schema:

{{
    "evaluation": {{
        "answer_quality":
            "weak | partial | solid | strong | exceptional",

        "technical_depth": 1,

        "reasoning_depth": 1,

        "identified_strengths": [],

        "identified_gaps": [],

        "recommended_action":
            "follow_up | change_topic | increase_difficulty | end_interview"
    }},

    "next_step": {{
        "curriculum_day": 1,

        "competency": "string",

        "reasoning": "string",

        "next_question": "string"
    }}
}}
"""

    messages = state.history + [
        {
            "role": "system",
            "content": eval_prompt,
        }
    ]

    response = client.chat.completions.create(
        model=os.environ.get(
            "MODEL_NAME",
            "llama-3.1-8b-instant"
        ),
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    raw_json = response.choices[0].message.content

    try:
        data = json.loads(raw_json)

    except json.JSONDecodeError:

        data = {
            "evaluation": {
                "answer_quality": "partial",
                "technical_depth": 3,
                "reasoning_depth": 3,
                "identified_strengths": [],
                "identified_gaps": [],
                "recommended_action": "follow_up",
            },
            "next_step": {
                "curriculum_day": 10,
                "competency": "technical reasoning",
                "reasoning": "Unable to parse model evaluation.",
                "next_question": (
                    "Can you elaborate on your last answer "
                    "and explain why you chose that approach?"
                ),
            },
        }

    evaluation = data.get("evaluation", {})
    next_step = data.get("next_step", {})

    state.evaluations.append(evaluation)

    curriculum_day = next_step.get(
        "curriculum_day"
    )

    if isinstance(curriculum_day, int):
        if curriculum_day not in state.topics_covered:
            state.topics_covered.append(curriculum_day)

    next_question = next_step.get(
        "next_question",
        "Could you elaborate on your last answer?"
    )

    # Update interview phase.
    if state.question_count >= 7:
        state.phase = "Final"
    elif state.question_count >= 6:
        state.phase = "Production"
    elif state.question_count >= 4:
        state.phase = "Deep Dive"
    elif state.question_count >= 2:
        state.phase = "Core Technical"
    else:
        state.phase = "Warm-up"

    state.history.append(
        {
            "role": "assistant",
            "content": next_question,
        }
    )

    state.question_count += 1

    return next_question


def generate_final_feedback(
    state: InterviewState
) -> str:

    client = get_client()

    eval_prompt = f"""
The technical interview is now complete.

Generate structured final feedback based on the
candidate's entire interview conversation.

Candidate:
{json.dumps(state.candidate_profile, indent=2)}

Interview evaluations:
{json.dumps(state.evaluations, indent=2)}

Topics covered:
{sorted(set(state.topics_covered))}

Conversation:
{json.dumps(state.history, indent=2)}

Answer this question:

"What technical understanding does this candidate
actually have, and can they explain the engineering
decisions behind what they built?"

Important:

- Base the assessment primarily on demonstrated interview performance.
- Use candidate learning history only for context.
- Strengths must be evidence-based.
- Gaps must be specific.
- Next steps must be actionable.
- Do not provide generic feedback.

Return ONLY valid JSON:

{{
    "summary": "Overall technical assessment",

    "strengths": [
        "Specific evidence-based strength"
    ],

    "gaps": [
        "Specific knowledge or reasoning gap"
    ],

    "next": [
        "Specific actionable improvement"
    ]
}}
"""

    messages = state.history + [
        {
            "role": "system",
            "content": eval_prompt,
        }
    ]

    response = client.chat.completions.create(
        model=os.environ.get(
            "MODEL_NAME",
            "llama-3.1-8b-instant"
        ),
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    raw_json = response.choices[0].message.content

    try:
        data = json.loads(raw_json)

    except json.JSONDecodeError:

        data = {
            "summary": "Interview completed successfully.",
            "strengths": [],
            "gaps": [],
            "next": [],
        }

    state.done = True

    state.feedback = FinalFeedback(
        summary=data.get(
            "summary",
            "Interview completed."
        ),
        strengths=data.get(
            "strengths",
            []
        ),
        gaps=data.get(
            "gaps",
            []
        ),
        next=data.get(
            "next",
            []
        ),
    )

    closing_message = (
        "Thank you for your time. "
        "The interview is now complete."
    )

    state.history.append(
        {
            "role": "assistant",
            "content": closing_message,
        }
    )

    return closing_message

