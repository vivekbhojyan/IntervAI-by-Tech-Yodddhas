
import os
import json
import logging
import time
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from models import (
    LLMEvaluation,
    LLMNextQuestion,
    LLMTurnOutput,
    LLMFeedback,
    FinalFeedback,
)
from curriculum import (
    get_active_domain_curriculum,
    get_allowed_domain_day_ids,
    get_relevant_curriculum,
)

logger = logging.getLogger(__name__)

MAX_QUESTIONS = 15


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
    question_days: list[int] = Field(default_factory=list)

    history: list[dict] = Field(default_factory=list)

    evaluations: list[dict] = Field(default_factory=list)

    running_summary: str = ""
    created_at: float = Field(default_factory=time.time)
    last_active: float = Field(default_factory=time.time)

    selected_domain: Optional[int] = None

    done: bool = False
    feedback: Optional[FinalFeedback] = None


    def get_context_summary(self) -> str:
        tested_days = sorted(set(self.topics_covered))
        profile = self.candidate_profile if isinstance(self.candidate_profile, dict) else {}
        member = profile.get("member", {}) if isinstance(profile.get("member"), dict) else {}

        return f"""
Candidate: {member.get('name', 'Unknown')}
Role: {member.get('jobRole', '')}
Experience: {member.get('yearsExperience', 0)} years
Phase: {self.phase}
Questions Asked: {self.question_count}
Topics Covered (Days): {tested_days}
"""



def generate_first_question(
    state: InterviewState,
    curriculum: dict
) -> str:

    client = get_client()

    effective_curriculum = (
        get_active_domain_curriculum(state.selected_domain, state.topics_covered)
        if state.selected_domain else curriculum
    )
    allowed_day_ids = [day["day"] for day in effective_curriculum.get("days", [])]

    system_prompt = f"""
You are an expert AI Technical Interviewer.

Your goal is to conduct a personalized technical interview
based on the candidate's actual learning journey.

Do not ask a fixed list of questions.

Be conversational, rigorous, and adaptive.

Candidate Profile:
{json.dumps(state.candidate_profile, indent=2)}

Curriculum:
{json.dumps(effective_curriculum, indent=2)}

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
10. When a domain is selected, ask only about these allowed curriculum days:
    {allowed_day_ids}
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


def build_curriculum_fallback_question(
    curriculum: dict, allowed_day_ids: list[int], topics_covered: list[int]
) -> tuple[int, str]:
    """Build a question for an allowed, preferably unvisited curriculum day."""
    fallback_day = next(
        (day for day in allowed_day_ids if day not in topics_covered),
        allowed_day_ids[0],
    )
    day_data = next(
        (day for day in curriculum.get("days", []) if day.get("day") == fallback_day),
        {},
    )
    objectives = day_data.get("objectives", [])
    if objectives:
        return fallback_day, f"Walk me through how you approached: {objectives[0]}"
    return fallback_day, f"Walk me through the key concepts from {day_data.get('title', 'this topic')}."


def build_teach_and_move_response(
    curriculum: dict, taught_day: int, next_day: int, original_question: str
) -> str:
    """Create a single encouraging teaching reply without trusting LLM prose."""
    taught_data = next(
        (day for day in curriculum.get("days", []) if day.get("day") == taught_day),
        {},
    )
    objectives = taught_data.get("objectives") or [taught_data.get("title", "this concept")]
    primary_objective = objectives[0]
    supporting_objective = objectives[1] if len(objectives) > 1 else primary_objective
    _, next_question = build_curriculum_fallback_question(
        curriculum, [next_day], []
    )
    return (
        "No worries - that is a tricky one, and it is completely fine not to know it yet. "
        f"Quick rundown: {primary_objective}. "
        f"For your question about '{original_question}', connect that core idea to its practical use: {supporting_objective}. "
        "For example, explain what goes in, what the system learns or produces, and how you would check that it works in a real application. "
        f"Now you have a useful starting point for next time. Let's move on: {next_question}"
    )


def is_substantive_teach_and_move_response(reply: str) -> bool:
    """Require the LLM's non-answer reply to have all three user-facing parts."""
    normalized = reply.lower()
    has_acknowledgment = any(phrase in normalized for phrase in (
        "no worries", "that's okay", "that is okay", "totally okay", "common area",
    ))
    transition_index = max(normalized.rfind("let's move"), normalized.rfind("let us move"))
    sentence_count = sum(reply.count(mark) for mark in (".", "!", "?"))
    return (
        has_acknowledgment
        and transition_index > 0
        and sentence_count >= 3
        and len(reply.strip()) >= 240
    )


def process_turn(
    state: InterviewState,
    candidate_message: str,
    curriculum: dict
) -> str:

    client = get_client()

    state.last_active = time.time()

    state.history.append(
        {
            "role": "user",
            "content": candidate_message,
        }
    )

    unique_days = len(set(state.topics_covered))

    if state.question_count >= MAX_QUESTIONS or (
        state.question_count >= 8
        and unique_days >= 4
        and state.phase == "Final"
    ):
        return generate_final_feedback(state)

    # Trim history for prompt bloat while updating running_summary
    if len(state.history) > 10:
        older_messages = state.history[:-10]
        summary_parts = []
        for msg in older_messages:
            role = "Interviewer" if msg.get("role") == "assistant" else "Candidate"
            content = msg.get("content", "")
            snippet = content[:80] + "..." if len(content) > 80 else content
            summary_parts.append(f"{role}: {snippet}")
        state.running_summary = "Earlier turns summary: " + " | ".join(summary_parts[-6:])

    candidate_missions = state.candidate_profile.get("missions", []) if isinstance(state.candidate_profile, dict) else []
    domain_curriculum = (
        get_active_domain_curriculum(state.selected_domain, state.topics_covered)
        if state.selected_domain else curriculum
    )
    allowed_day_ids = get_allowed_domain_day_ids(
        state.selected_domain, state.topics_covered
    ) if state.selected_domain else None
    available_day_ids = allowed_day_ids or [
        day.get("day") for day in domain_curriculum.get("days", [])
    ]
    unvisited_day_ids = [
        day for day in available_day_ids if day not in state.topics_covered
    ]
    repeated_day = (
        len(state.question_days) >= 3
        and len(set(state.question_days[-3:])) == 1
    )
    diversity_is_urgent = (
        repeated_day
        or (state.question_count > 5 and len(set(state.topics_covered)) < 2)
    )
    diversity_targets = unvisited_day_ids[:3]
    filtered_curriculum = get_relevant_curriculum(domain_curriculum, state.topics_covered, candidate_missions)
    curriculum_context = json.dumps(
        filtered_curriculum,
        indent=2
    )


    eval_prompt = f"""
You are conducting a realistic adaptive technical interview.

Analyze the candidate's latest answer.

Candidate context:
{state.get_context_summary()}

Running summary of earlier turns:
{state.running_summary or 'None'}

Curriculum (Relevant topics):
{curriculum_context}

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
14. If an allowed-day list is provided below, curriculum_day MUST be one of it.
15. Set is_non_answer to true when the candidate did not provide a substantive
    answer, including an expressed lack of knowledge. When true, next_question
    is NOT just a question: it must be one natural reply with these parts IN ORDER:
    (a) an explicit warm acknowledgement such as "No worries - that's a tricky
    one", (b) a teaching-oriented mini-explanation of 2-4 substantive sentences,
    and (c) a warm "Let's move on" transition followed by a new question.
    The mini-explanation must answer every part of the immediately previous
    question. If it asks for both a definition and an application, explain both;
    use a concrete example when it clarifies the application. A one-sentence
    definition is insufficient. Select the new question from a different,
    unvisited day in the suggested list below.
16. When diversity is urgent, select a different unvisited curriculum_day from
    the suggested days below; do not rephrase the current topic.

Allowed curriculum days for the next question:
{allowed_day_ids if allowed_day_ids is not None else 'All curriculum days'}

Suggested unvisited days for a topic change:
{diversity_targets or 'No unvisited days remain'}

Diversity is urgent:
{diversity_is_urgent}

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

    trimmed_history = state.history[-10:] if len(state.history) > 10 else state.history
    messages = trimmed_history + [
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
        raw_dict = json.loads(raw_json)
        validated = LLMTurnOutput.model_validate(raw_dict)
        data = validated.model_dump()

    except (json.JSONDecodeError, ValidationError, Exception) as e:
        logger.warning("LLM response validation failed in process_turn: %s", e)
        data = {
            "evaluation": {
                "answer_quality": "partial",
                "technical_depth": 3,
                "reasoning_depth": 3,
                "identified_strengths": [],
            "identified_gaps": [],
            "recommended_action": "follow_up",
            "is_non_answer": False,
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
    curriculum_day = next_step.get("curriculum_day")
    proposed_curriculum_day = curriculum_day

    if allowed_day_ids is not None and curriculum_day not in allowed_day_ids:
        logger.warning(
            "Rejected out-of-domain curriculum day %r for domain %s; retrying once",
            curriculum_day,
            state.selected_domain,
        )
        retry_messages = messages + [{
            "role": "system",
            "content": (
                "Your previous proposed curriculum_day was outside the selected domain. "
                f"Return a replacement JSON response with curriculum_day strictly in {allowed_day_ids}. "
                "The next_question must be about that allowed day only."
            ),
        }]
        retry_response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "llama-3.1-8b-instant"),
            messages=retry_messages,
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        try:
            retry_data = LLMTurnOutput.model_validate(
                json.loads(retry_response.choices[0].message.content)
            ).model_dump()
            retry_next_step = retry_data["next_step"]
            retry_day = retry_next_step.get("curriculum_day")
        except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as exc:
            logger.warning("LLM retry validation failed in process_turn: %s", exc)
            retry_data = None
            retry_day = None

        if retry_data is not None and retry_day in allowed_day_ids:
            evaluation = retry_data["evaluation"]
            next_step = retry_next_step
            curriculum_day = retry_day
        else:
            curriculum_day, fallback_question = build_curriculum_fallback_question(
                domain_curriculum, allowed_day_ids, state.topics_covered
            )
            next_step = {
                **next_step,
                "curriculum_day": curriculum_day,
                "competency": "domain-scoped fallback",
                "reasoning": "The model repeatedly selected an out-of-domain curriculum day.",
                "next_question": fallback_question,
            }
            logger.warning(
                "LLM retry remained out of domain; using deterministic question for day %s",
                curriculum_day,
            )

    is_non_answer = bool(evaluation.get("is_non_answer"))
    force_new_day = is_non_answer or diversity_is_urgent
    if force_new_day and diversity_targets and curriculum_day not in diversity_targets:
        curriculum_day, replacement_question = build_curriculum_fallback_question(
            domain_curriculum, diversity_targets, state.topics_covered
        )
        next_step = {
            **next_step,
            "curriculum_day": curriculum_day,
            "next_question": replacement_question,
        }

    if is_non_answer:
        taught_day = state.question_days[-1] if state.question_days else proposed_curriculum_day
        if taught_day not in available_day_ids:
            taught_day = curriculum_day
        next_day = curriculum_day
        original_question = next(
            (message.get("content", "") for message in reversed(state.history[:-1])
             if message.get("role") == "assistant"),
            "the previous topic",
        )
        if not is_substantive_teach_and_move_response(next_step.get("next_question", "")):
            next_step["next_question"] = build_teach_and_move_response(
                domain_curriculum, taught_day, next_day, original_question
            )
        # Teaching is not evidence of knowledge. Preserve it as a gap and do
        # not allow an LLM to accidentally credit the candidate with a strength.
        evaluation["identified_strengths"] = []
        gap = f"Could not demonstrate understanding of curriculum day {taught_day}"
        if gap not in evaluation["identified_gaps"]:
            evaluation["identified_gaps"].append(gap)

    state.evaluations.append(evaluation)

    if isinstance(curriculum_day, int):
        if curriculum_day not in state.topics_covered:
            state.topics_covered.append(curriculum_day)
        state.question_days.append(curriculum_day)

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
- An evaluation with is_non_answer=true means the candidate did not demonstrate
  that topic. Treat it as a gap and never credit it as a strength, even if the
  interviewer explained the concept during the interview.

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
        raw_dict = json.loads(raw_json)
        validated = LLMFeedback.model_validate(raw_dict)
        data = validated.model_dump()

    except (json.JSONDecodeError, ValidationError, Exception) as e:
        logger.warning("LLM response validation failed in generate_final_feedback: %s", e)

        fallback_strengths = []
        fallback_gaps = []
        for ev in state.evaluations:
            for s in ev.get("identified_strengths", []):
                if s and s not in fallback_strengths:
                    fallback_strengths.append(s)
            for g in ev.get("identified_gaps", []):
                if g and g not in fallback_gaps:
                    fallback_gaps.append(g)

        data = {
            "summary": "Interview completed successfully.",
            "strengths": fallback_strengths,
            "gaps": fallback_gaps,
            "next": ["Review the curriculum days that weren't covered in depth"],
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
