# BUILD THIS: AI INTERVIEW AGENT — "BUILD THE INTERVIEWER, NOT THE INTERVIEW"

You are a senior AI engineer, backend architect, product designer, and technical interviewer.

Your task is to DESIGN AND BUILD a production-quality AI Interview Agent for the provided AI Cohort hackathon challenge.

Do not merely create a chatbot that asks a fixed list of questions.

Build a REAL adaptive technical interviewer that understands the candidate's learning journey, conducts a multi-turn technical interview, dynamically decides what to ask next, maintains context, probes weak answers, increases difficulty when appropriate, and produces structured actionable feedback at the end.

The final experience should feel like a strong human technical interviewer — not a questionnaire.

---

# 1. SOURCE OF TRUTH

Three files are provided with this task:

1. `curriculum.json`
2. `candidates (1).json`
3. `technical-spec.md`

YOU MUST READ AND USE THESE FILES.

Do not invent curriculum topics when the supplied curriculum contains the relevant information.

Treat the supplied files as the source of truth for:
- curriculum days
- module structure
- learning objectives
- tools
- candidate profiles
- completed missions
- failed missions
- skipped missions
- attempt counts
- learning signals
- API contract
- request format
- response format
- session requirements

The curriculum contains 31 days and 8 modules including:
- Environment & Tooling
- Data Foundations
- Embeddings & Vector Search
- LLM Core, Prompting & Fine-Tuning
- Chatbot Application Build
- Agentic AI & MCP
- Evaluation, Security & Deployment
- Production & Capstone

Important technical topics include:
- embeddings
- vector databases
- retrieval
- RAG
- prompt engineering
- function calling
- fine-tuning
- FastAPI
- conversation memory
- LangChain agents
- multi-agent orchestration
- MCP
- evaluation
- performance/cost optimization
- security and guardrails
- Docker
- Kubernetes
- monitoring
- production readiness
- capstone architecture

---

# 2. PRIMARY GOAL

Build an AI agent that conducts a personalized technical interview for a candidate based on their actual cohort journey.

The agent must answer the question:

"What technical understanding does this candidate actually have, and can they explain the engineering decisions behind what they built?"

The interview must assess:

1. Conceptual understanding
2. Practical implementation knowledge
3. Engineering trade-offs
4. System design thinking
5. Debugging/problem-solving ability
6. Ability to explain decisions
7. Production awareness
8. Depth of understanding
9. Communication clarity
10. Ability to reason under follow-up questioning

---

# 3. CORE PRINCIPLE

NEVER behave like this:

Question 1
Question 2
Question 3
Question 4
...
Question 8

Instead, behave like this:

Question
→ evaluate answer
→ identify strongest/weakest signal
→ ask follow-up
→ probe reasoning
→ challenge assumptions
→ connect to another topic
→ increase/decrease difficulty
→ move to another competency
→ return to unresolved weakness if useful
→ eventually conclude interview

The interview must be adaptive.

---

# 4. CANDIDATE PERSONALIZATION

At interview initialization, analyze the candidate object.

Extract:

- candidate name
- role
- years of experience
- education
- completed missions
- passed missions
- failed missions
- skipped missions
- number of attempts
- first-try performance
- commitment/participation signals

Build an internal candidate profile.

Example:

If a candidate:
- passed RAG-related missions
- struggled repeatedly with prompting
- skipped Kubernetes
- completed MCP successfully

Then the interview should reflect this.

Possible flow:

"Walk me through how your retrieval layer decides between SQL and vector search."

If the candidate gives a strong answer:

"Good. Now suppose semantic retrieval returns highly relevant documents but the structured SQL result conflicts with them. How would you resolve that?"

If they answer well again:

"Now let's talk about production. How would you monitor whether that routing strategy is actually improving answer quality?"

This is the desired behavior.

---

# 5. DO NOT PUNISH ATTEMPT COUNTS

Attempt counts are LEARNING SIGNALS, not direct evidence of incompetence.

For example:

5 attempts + passed

does NOT mean:

"Candidate is bad."

Instead it may indicate:

"This is an area worth probing."

Use attempt count to influence question selection and depth, not to prejudge the candidate.

Similarly:

1 attempt + passed

does not automatically mean mastery.

The candidate must demonstrate understanding during the interview.

---

# 6. HANDLE SKIPPED TOPICS INTELLIGENTLY

Skipped topics should generally NOT be treated as knowledge gaps that must be tested aggressively.

However, skipped topics can be used as optional boundary questions when relevant.

Example:

Candidate skipped Kubernetes.

Do NOT start with:

"Explain Kubernetes."

Instead, if the candidate discusses deployment:

"Your cohort path appears to have focused less on Kubernetes. At a high level, what would you consider when moving this system from a single container to an orchestrated deployment?"

This tests awareness without unfairly penalizing them.

---

# 7. INTERVIEW STRUCTURE

Minimum:

- 8 questions
- at least 4 different curriculum days/topics
- multiple follow-up questions
- multi-turn conversation
- context preservation
- final structured feedback

Recommended interview:

10–14 meaningful question turns.

IMPORTANT:

A follow-up counts as a question.

Do not artificially ask 14 unrelated questions.

Prefer fewer, deeper conversations.

Example:

Main:
"How does RAG work in the system you built?"

Follow-up:
"Why did you use vector retrieval here?"

Follow-up:
"What happens when retrieval returns irrelevant chunks?"

Follow-up:
"How would you measure whether retrieval improved answer quality?"

That is much better than four unrelated questions.

---

# 8. INTERVIEW PHASES

Use the following flexible interview phases.

## Phase 1 — Warm-up

Start naturally.

Example:

"Hi Sarah. Let's start with something you built during the cohort. Can you walk me through the overall architecture of your final chatbot and the role of retrieval in it?"

Do NOT give the candidate the entire interview plan.

---

## Phase 2 — Core Technical Understanding

Explore foundational concepts relevant to the candidate.

Potential areas:

- embeddings
- vector search
- RAG
- prompt engineering
- function calling
- LLM APIs
- memory/context

Choose topics based on candidate data.

---

## Phase 3 — Deep Dive

Pick one or two areas and go deeper.

Ask:

- Why?
- Why not?
- What happens if...?
- How would you measure...?
- What trade-off did you make?
- What would you change?
- What breaks at scale?
- How would you debug this?

---

## Phase 4 — System/Architecture Reasoning

Move from individual components to system thinking.

Example:

"You have retrieval, an LLM, tools, memory, and an API layer. Where would you put retries, timeouts, logging, and validation?"

Then adapt based on their answer.

---

## Phase 5 — Production Scenario

Ask a realistic production problem.

Examples:

"Latency suddenly increased from 1 second to 6 seconds. How would you investigate?"

"Your RAG system is producing confident but incorrect answers. Where would you look first?"

"Vector search is returning relevant documents, but users say answers are still poor. What could be wrong?"

"The LLM provider becomes unavailable. How should your system behave?"

---

## Phase 6 — Final Challenge

Give the candidate a scenario that combines multiple concepts.

Example:

"You now need to turn the cohort chatbot into a production enterprise system serving 100,000 users. What would you change first and why?"

Use the candidate's previous answers to make this challenge relevant.

---

# 9. ADAPTIVE QUESTION ENGINE

Implement an internal decision process similar to:

1. Determine what competencies have already been tested.
2. Analyze the latest answer.
3. Classify answer quality:
   - weak
   - partial
   - solid
   - strong
   - exceptional
4. Identify missing reasoning.
5. Determine whether a follow-up is valuable.
6. Decide whether to:
   - probe deeper
   - challenge
   - clarify
   - switch topic
   - increase difficulty
   - decrease difficulty
   - test another competency
7. Ensure curriculum coverage.
8. Ensure at least 8 questions before completion.
9. End only when sufficient evidence has been collected.

---

# 10. ANSWER EVALUATION

For every candidate response, internally evaluate:

### Correctness
Does the candidate understand the technical concept?

### Depth
Can they explain beyond definitions?

### Reasoning
Can they explain WHY?

### Practicality
Can they connect the concept to implementation?

### Trade-offs
Can they compare alternatives?

### Production thinking
Can they discuss reliability, latency, cost, security, observability, scaling?

### Communication
Can they explain clearly?

### Consistency
Does the current answer contradict previous answers?

Do NOT expose this internal evaluation during the interview.

---

# 11. FOLLOW-UP QUESTION RULES

Follow-ups should be generated from the candidate's actual answer.

BAD:

Candidate:
"Vector databases store embeddings."

Interviewer:
"What is MCP?"

GOOD:

Candidate:
"Vector databases store embeddings."

Interviewer:
"Right. What makes a vector database useful here compared with simply storing the embeddings in a relational database?"

Then:

"What retrieval problem does approximate nearest-neighbor search solve?"

Then:

"If your retrieval precision is poor, what would you investigate first?"

The next question must have a reason.

---

# 12. NEVER REPEAT QUESTIONS

Track:

- asked questions
- concepts tested
- candidate answers
- unresolved areas
- weak areas
- strong areas
- curriculum coverage

Never ask the same question twice unless intentionally reframing it to test a different competency.

---

# 13. DIFFICULTY ADAPTATION

If candidate performs strongly:

Increase difficulty.

Move:

definition
→ implementation
→ architecture
→ trade-offs
→ failure modes
→ production scenario

If candidate struggles:

Do not immediately jump to another unrelated topic.

Try one supportive clarification question.

Example:

"Let's simplify it. What happens to the user query before it reaches the LLM?"

Then reassess.

Do not become a tutor during the interview.

The interviewer may clarify the question, but should not teach the answer.

---

# 14. TECHNICAL TOPIC COVERAGE

Use the supplied curriculum to dynamically select topics.

Potential interview areas include:

### Data / Knowledge Base
- structured vs unstructured data
- chunking
- metadata
- knowledge bases

### Embeddings
- embeddings
- semantic similarity
- vector representations
- embedding quality

### Vector Databases
- ChromaDB
- Pinecone
- indexing
- metadata filtering
- semantic search

### Retrieval
- SQL retrieval
- vector retrieval
- hybrid retrieval
- query routing
- deduplication
- retrieval quality

### RAG
- retrieval pipeline
- grounding
- context construction
- hallucination
- RAG failure modes

### Prompt Engineering
- zero-shot
- few-shot
- system prompts
- prompt evaluation
- consistency

### Function Calling
- tool schemas
- structured outputs
- Pydantic
- tool selection
- validation

### Fine-Tuning
- prompting vs RAG vs fine-tuning
- LoRA
- QLoRA
- when fine-tuning makes sense

### Application Engineering
- FastAPI
- APIs
- sessions
- frontend/backend integration
- streaming
- SSE
- response formatting

### Memory
- conversation history
- context windows
- summarization
- token management

### Agents
- LangChain agents
- ReAct
- tool use
- agent decision-making

### Multi-Agent Systems
- routing
- specialist agents
- orchestration
- single-agent vs multi-agent trade-offs

### MCP
- purpose of MCP
- MCP server
- tools
- clients
- standardized tool access

### Production Agentic Systems
- retries
- timeouts
- error handling
- failure testing

### Evaluation
- benchmark datasets
- grounding
- accuracy
- consistency
- retrieval evaluation

### Performance
- token usage
- latency
- caching
- cost optimization

### Security
- authentication
- input validation
- prompt injection
- jailbreaks
- privacy

### Deployment
- Docker
- Kubernetes
- health checks
- environment variables

### Observability
- structured logging
- Prometheus
- Grafana
- latency
- failures
- tool metrics

### Production Readiness
- testing
- deployment
- operational documentation
- reliability

---

# 15. CURRICULUM COVERAGE ALGORITHM

Maintain an internal structure like:

tested_topics = []

For every question:

- record curriculum day
- record curriculum module
- record competency
- record difficulty
- record answer quality

Before ending:

assert:
- question_count >= 8
- unique_curriculum_days >= 4

Prefer broad coverage early and depth later.

---

# 16. INTERVIEW MEMORY

The agent MUST maintain:

```text
sessionId
candidate profile
interview phase
question count
topics covered
questions asked
candidate answers
answer evaluations
strong areas
weak areas
unresolved threads
current topic
next-question rationale
overall assessment
```

Do not lose this information between HTTP requests.

The technical specification explicitly requires interview state to be maintained using `sessionId`.

---

# 17. API REQUIREMENT

Expose exactly:

POST /api/interview

No authentication is required.

Initial request:

```json
{
  "sessionId": "abc-123",
  "candidate": { "...candidate.json..." }
}
```

Return:

```json
{
  "reply": "Welcome. Let's begin your interview.",
  "done": false
}
```

Subsequent requests:

```json
{
  "sessionId": "abc-123",
  "message": "Candidate's answer"
}
```

Return:

```json
{
  "reply": "Next interviewer question",
  "done": false
}
```

When interview ends:

```json
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "summary": "...",
    "strengths": [],
    "gaps": [],
    "next": []
  }
}
```

The required feedback fields are:

```text
summary: string
strengths: string[]
gaps: string[]
next: string[]
```

Every array should contain concise actionable points.

Follow the supplied `technical-spec.md` exactly.

---

# 18. STATE MANAGEMENT

For the hackathon, persistent user accounts are NOT required.

Session state only needs to live for the interview.

Possible implementation:

```text
Map<sessionId, InterviewState>
```

or Redis/database if useful.

Design the state layer so it can later be replaced with Redis without rewriting the interview engine.

Handle:

- unknown sessionId
- duplicate requests
- completed sessions
- malformed requests
- missing candidate
- empty messages
- unexpected candidate input

gracefully.

---

# 19. LLM ARCHITECTURE

Use an LLM for:

- question generation
- answer evaluation
- follow-up generation
- interview reasoning
- final feedback

But DO NOT rely entirely on unconstrained LLM behavior.

Implement deterministic guardrails around the LLM.

For example:

```text
Application
    ↓
Session Manager
    ↓
Candidate Analyzer
    ↓
Interview State
    ↓
Interview Controller
    ↓
Question Planner
    ↓
LLM
    ↓
Answer Evaluator
    ↓
Coverage / Difficulty Controller
    ↓
Next Question
```

The application should enforce minimum interview requirements even if the LLM wants to finish early.

---

# 20. STRUCTURED INTERNAL LLM OUTPUT

Where possible, require the LLM to return structured data internally.

Example:

```json
{
  "answer_quality": "strong",
  "technical_depth": 4,
  "reasoning_depth": 5,
  "identified_strengths": [
    "understands hybrid retrieval"
  ],
  "identified_gaps": [
    "did not discuss retrieval evaluation"
  ],
  "curriculum_day": 10,
  "competency": "retrieval architecture",
  "recommended_action": "follow_up",
  "next_question": "How would you evaluate whether..."
}
```

The candidate should NOT see this internal JSON.

---

# 21. QUESTION QUALITY

Every question should satisfy at least one of:

- tests understanding
- tests reasoning
- tests implementation
- tests architecture
- tests debugging
- tests trade-offs
- tests production thinking

Avoid trivia.

Avoid questions whose answer is simply a one-line definition.

Prefer:

"Why did you choose X?"

"What would happen if X failed?"

"How would you measure X?"

"How would you debug X?"

"What would you choose instead and why?"

"What changes at 100x scale?"

---

# 22. MAKE IT FEEL HUMAN

The interviewer should use natural transitions.

Examples:

"That's a good distinction. Let's push that a little further."

"Okay. Now imagine the system is running in production..."

"Interesting. You mentioned hybrid retrieval — let's dig into that."

"Let's stay with that for a moment."

"Suppose that approach starts failing under load. What would you look at?"

Do not overuse canned phrases.

Do not praise every answer.

Do not say:

"Excellent answer!"

after every response.

Human interviewers challenge candidates.

---

# 23. DO NOT GIVE AWAY ANSWERS

If the candidate struggles:

Bad:

"Remember that RAG usually uses embeddings and vector search. So how would you..."

Good:

"Let's narrow the problem. What would you expect the retrieval layer to return before the LLM generates an answer?"

The interviewer should guide without teaching.

---

# 24. FINAL FEEDBACK

At the end, produce structured feedback.

The summary should answer:

"What is this candidate's current technical level based on the interview?"

Strengths should be evidence-based.

Bad:

"Good knowledge."

Good:

"Explained the SQL/vector hybrid retrieval decision clearly and connected retrieval quality to downstream answer grounding."

Gaps should be specific.

Bad:

"Needs improvement in AI."

Good:

"Could explain MCP conceptually but struggled to describe the lifecycle of an MCP tool call between client and server."

Next steps should be actionable.

Example:

"Practice designing retrieval evaluation datasets and selecting precision/recall-style metrics."

"Build a small MCP server and trace a complete tool invocation."

---

# 25. FEEDBACK SHOULD NOT BE BASED ONLY ON CURRICULUM COMPLETION

IMPORTANT:

Completion data tells you what the candidate studied.

Interview answers tell you what they actually understand.

Final assessment MUST primarily reflect demonstrated interview performance.

Use cohort data to personalize the interview, not to predetermine the result.

---

# 26. UI / UX

Build a clean technical interview interface.

Recommended layout:

LEFT / MAIN:
- interviewer message
- candidate response
- chat history

RIGHT:
- interview progress
- topics covered
- interview phase
- optional subtle progress indicator

DO NOT expose hidden scoring, internal reasoning, or answer evaluation during the interview.

At completion show:

### Interview Complete

Overall Summary

Strengths

Knowledge Gaps

Recommended Next Steps

Optionally show:
- topics assessed
- competencies assessed
- interview duration
- question count

Avoid overwhelming dashboards.

The interview experience should remain the focus.

---

# 27. OPTIONAL ENHANCEMENTS

If time permits, add:

- difficulty indicator
- interview mode selector
- beginner/intermediate/advanced depth
- interviewer personality
- architecture whiteboard-style questions
- scenario-based questions
- "challenge my answer" mode
- downloadable feedback
- interview transcript
- competency radar
- topic coverage visualization

These are secondary.

Do NOT sacrifice core interview quality for flashy UI.

---

# 28. ERROR HANDLING

Implement robust handling for:

- LLM API failure
- malformed LLM response
- timeout
- missing session
- invalid candidate
- empty candidate response
- duplicate session
- interview already completed
- JSON parsing errors
- unsupported model output

If LLM structured output fails, retry or safely fall back.

The API must still return valid JSON.

---

# 29. SECURITY

Never expose:

- API keys
- system prompts
- hidden evaluation
- internal reasoning
- private session state

Use environment variables for secrets.

Example:

```env
OPENAI_API_KEY=
MODEL_NAME=
```

Do not hardcode credentials.

---

# 30. PROJECT QUALITY

Write clean, modular, maintainable code.

Separate:

```text
/api
/session
/candidate
/interview
/llm
/evaluation
/curriculum
/feedback
```

Do not put the entire application inside one file.

Use clear interfaces.

Make the LLM provider replaceable.

For example:

```text
LLMProvider
 ├── OpenAIProvider
 ├── AnthropicProvider
 └── LocalProvider
```

A hackathon project should still look like something an engineering team could extend.

---

# 31. TESTING

Create tests for:

### API
- start session
- continue session
- end session
- invalid session
- malformed request

### Interview logic
- minimum 8 questions
- minimum 4 curriculum days
- follow-up generation
- topic tracking
- duplicate question prevention
- difficulty adaptation

### Candidate personalization
Test at least:

1. Strong technical candidate
2. Candidate with many failed attempts
3. Candidate with skipped advanced topics
4. Candidate with limited technical background

### State
Verify:

```text
request 1
→ request 2
→ request 3
→ ...
```

preserves context.

---

# 32. DEMO SCENARIO

Create a compelling demo.

Use one candidate profile from the supplied data.

Demonstrate:

1. Candidate starts interview.
2. Agent selects a topic based on their journey.
3. Candidate gives an answer.
4. Agent asks a relevant follow-up.
5. Candidate gives a stronger answer.
6. Agent increases difficulty.
7. Agent switches to another curriculum area.
8. Agent presents a production scenario.
9. Agent completes the interview.
10. Agent produces structured feedback.

The demo should make it obvious that the agent is reasoning about the conversation.

---

# 33. IMPORTANT ANTI-PATTERNS

DO NOT:

- create a fixed questionnaire
- ask random curriculum questions
- ask questions unrelated to the candidate
- repeat questions
- end after 3–4 questions
- ignore candidate answers
- ignore sessionId
- ignore skipped topics
- judge candidates solely by attempts
- expose internal scoring
- expose chain-of-thought
- provide answers during the interview
- produce generic feedback
- hardcode one candidate
- hardcode eight questions
- make every candidate receive the same interview

---

# 34. SUCCESS CRITERIA

The implementation is successful only if all are true:

[ ] POST /api/interview exists.

[ ] First request initializes the interview.

[ ] sessionId maintains state.

[ ] Subsequent requests use candidate messages.

[ ] Interview is multi-turn.

[ ] At least 8 questions are asked.

[ ] At least 4 curriculum days are covered.

[ ] Questions adapt to candidate answers.

[ ] Follow-ups are generated dynamically.

[ ] Candidate history is maintained.

[ ] Candidate profile affects interview selection.

[ ] Skipped/failed/completed missions influence personalization appropriately.

[ ] Difficulty adapts.

[ ] Questions are not simply a fixed script.

[ ] Final structured feedback is generated.

[ ] Feedback contains:
    - summary
    - strengths
    - gaps
    - next

[ ] Application handles errors gracefully.

[ ] Secrets are not hardcoded.

[ ] Code is modular.

[ ] README explains architecture and setup.

---

# 35. README REQUIREMENTS

Create a README containing:

## Project Overview

What the AI Interview Agent does.

## Architecture

Explain:

```text
Frontend
   ↓
Interview API
   ↓
Session Manager
   ↓
Candidate Analyzer
   ↓
Interview Controller
   ↓
LLM
   ↓
Answer Evaluator
   ↓
Question Planner
```

## Adaptive Interview Logic

Explain how the next question is selected.

## Personalization

Explain how candidate profiles affect interviews.

## State Management

Explain sessionId handling.

## API

Document:

```text
POST /api/interview
```

including request/response examples.

## Setup

Include exact installation and environment-variable instructions.

## Running

Include frontend/backend commands.

## Testing

Explain how to run tests.

## Design Decisions

Explain why the chosen architecture/model/framework was selected.

---

# 36. FINAL IMPLEMENTATION INSTRUCTION

Do not stop at planning.

Actually build the complete working application.

First inspect the supplied files.

Then:

1. Understand the requirements.
2. Design the architecture.
3. Implement backend.
4. Implement interview engine.
5. Implement session state.
6. Implement LLM integration.
7. Implement adaptive questioning.
8. Implement curriculum coverage.
9. Implement candidate personalization.
10. Implement final feedback.
11. Implement frontend.
12. Add error handling.
13. Add tests.
14. Add README.
15. Run the application.
16. Test the complete interview flow.
17. Fix any errors discovered.
18. Verify the API contract against `technical-spec.md`.

Do not claim something works without testing it.

Prioritize:

1. Interview intelligence
2. Correct API behavior
3. Personalization
4. Context preservation
5. Adaptive follow-ups
6. Feedback quality
7. UX
8. Visual polish

The final product should make a hackathon judge think:

"This isn't an LLM wrapped around eight questions. This is an actual technical interviewer."

Build the interviewer, not the interview.


---

## Frontend changes applied (summary)

Below are the concrete frontend improvements I applied to make the UI more elegant and professional. These were implemented and hot-reloaded in the local Vite dev server.

- Typography & head: added Inter font and updated the page title.
  - File: `frontend/index.html`

- Theming & utilities: added theme CSS variables, polished gradients, scrollbar, and utility classes.
  - File: `frontend/src/index.css`

- Global layout and surfaces: added card surfaces, header and panel styles for a more modern aesthetic.
  - File: `frontend/src/App.css`

- Header & container: improved header with logo, brand badge, and applied new container classes.
  - File: `frontend/src/App.jsx`

- Chat UI: glass-panel chat container, refined message bubbles, avatars, timestamps, and improved input styling.
  - File: `frontend/src/components/ChatInterface.jsx`

- Domain selector: elevated domain cards with hover, accessible role/aria attributes, and card styling.
  - File: `frontend/src/components/DomainSelector.jsx`

- Progress panel: added avatar, gradient progress bar, and card layout for clearer status visuals.
  - File: `frontend/src/components/ProgressPanel.jsx`

- Feedback modal: updated to use card surface and primary button styles for consistency.
  - File: `frontend/src/components/FeedbackModal.jsx`

Notes:
- The frontend dev server (Vite) was restarted and HMR applied the updates; open http://localhost:5173/ to view changes.
- The backend remains at http://127.0.0.1:8000/ and is required for interview flows.
- If you'd like, I can further refine icons, responsive behavior, or produce a production build.