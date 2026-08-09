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

- User attachment
is the structure correct?

Yes — the structure is correct. ✅

Your .env is directly inside the frontend folder:

vicodathon/
└── frontend/
    ├── .env                  ✅
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── components/
    └── public/
Your .env should contain exactly:

VITE_API_URL=https://intervai-by-tech-yodddhas.onrender.com
And your API call should be:

fetch(`${import.meta.env.VITE_API_URL}/api/interview`)
One thing to check
Make sure the file is actually named:

.env
and not:

.env.txt
Windows sometimes hides extensions.

Then restart your frontend:

cd frontend
npm run dev
For Vercel, also add the same VITE_API_URL under Project → Settings → Environment Variables, then redeploy.

So far, your folder structure is exactly where it should be. 👍

in localhost it woeks well but on render and vercel it does not working

Yes — and this actually gives us a useful clue.

Your local app working does not prove the deployed app is configured correctly. You now have two separate things to verify:

Vercel frontend
      ↓
Render backend
      ↓
FastAPI
I checked your Render URL, and the root / currently returns 404. That's not necessarily a problem—your FastAPI app may simply not define a / route. The important test is /docs and your actual /api/interview endpoint.

1. Test Render first
Open this in your browser:

Render API documentation

If /docs doesn't open, your problem is with the Render backend.

If /docs opens, then Render is running and we need to check the frontend → backend connection.

2. Check your Render start command
In Render → your backend service → Settings, make sure:

Root Directory

backend
Build Command

pip install -r requirements.txt
Start Command

uvicorn main:app --host 0.0.0.0 --port $PORT
Then look at Render → Logs.

You should see something similar to:

Application startup complete.
Uvicorn running on http://0.0.0.0:10000
3. Test the actual API
Your frontend calls:

/api/interview
So the deployed API is:

https://intervai-by-tech-yodddhas.onrender.com/api/interview
If that endpoint expects a POST request, opening it directly in the browser may give 405 Method Not Allowed. That's okay.

What's important is that your frontend sends the correct POST request.

4. Check your frontend code
You've already changed:

fetch(`${import.meta.env.VITE_API_URL}/api/interview')
to:

fetch(`${import.meta.env.VITE_API_URL}/api/interview`)
Good.

But now search your entire src folder:

Ctrl + Shift + F

Search:

localhost:8000
You need to make sure there are no remaining frontend API calls pointing to localhost.

Also search:

127.0.0.1
If you find another API request using it, change that too.

5. Check Vercel environment variable
In Vercel:

Project → Settings → Environment Variables

You should have:

Name:
VITE_API_URL

Value:
https://intervai-by-tech-yodddhas.onrender.com
Then redeploy the frontend.

This is important because adding .env locally does not automatically configure the Vercel deployment.

6. Check CORS
If Render /docs works but your Vercel app gives something like:

Failed to fetch
or the browser console says:

Access to fetch has been blocked by CORS policy
then your backend's CORS configuration is the problem.

In backend/main.py, you need something like:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://YOUR-VERCEL-APP.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Replace the Vercel URL with your actual deployed Vercel URL.

But don't change more things blindly
At this point, the fastest way to find the exact problem is:

First open:
Your Render /docs endpoint

Then tell me what you see.

If it opens, send me the Vercel URL and the error from:

Vercel website → F12 → Console

For example:

Failed to fetch
or

CORS policy
or

500 Internal Server Error
or whatever appears.

Then we can pinpoint whether it's Render, CORS, environment variables, API path, or Vercel instead of guessing.

User attachment
it is working well

Great — if your localhost is working perfectly, then your frontend structure and .env setup are likely fine. 👍

The problem is specifically in the deployment connection:

Vercel frontend
      ↓
      ? 
Render backend
Let's isolate it.

Do these 2 checks
1. Open your Render backend:

https://intervai-by-tech-yodddhas.onrender.com/docs
If the FastAPI Swagger page opens → Render backend is running.

2. Open your Vercel website → press F12 → Console

Try the feature that calls /api/interview.

If you see an error, send me a screenshot of the Console.

Especially look for:

CORS policy
Failed to fetch
404
500
502
ERR_FAILED
One correction from earlier
Your .env being here:

frontend/.env
is correct.

And this:

VITE_API_URL=https://intervai-by-tech-yodddhas.onrender.com
is also correct.

And this:

fetch(`${import.meta.env.VITE_API_URL}/api/interview`)
is correct for Vite.

So don't change those again.

The next thing we need is the actual Vercel browser error. Send me that screenshot and I'll tell you exactly what to fix.

https://intervai-by-tech-yodddhas.onrender.com/docs
it is wrking well

Perfect. That confirms Render is working. Your FastAPI backend is alive and Swagger is accessible. 

So the remaining problem is almost certainly:

Vercel frontend → Render API

Your Vite setup is correct: Vite exposes VITE_* variables through import.meta.env, and .env is loaded when Vite builds the app. 

Now do this exact test
Open your Vercel deployed website.

Press F12
Go to Console
Use the part of your website that starts an interview.
Look at the error.
Also go to Network → Fetch/XHR and click the /api/interview request.

You should see something like:

Request URL:
https://intervai-by-tech-yodddhas.onrender.com/api/interview
If you see this instead:
${import.meta.env.VITE_API_URL}/api/interview
then Vercel is still serving your old build.

In that case:

Vercel → Settings → Environment Variables
Confirm:
VITE_API_URL
=
https://intervai-by-tech-yodddhas.onrender.com
Go to Deployments
Redeploy the latest deployment.
Make sure you don't have an old .env.production overriding it.
Vite gives mode-specific .env files higher priority than the normal .env, so an existing .env.production could override your value. 

One more very important check
In VS Code press:

Ctrl + Shift + F

Search:

localhost:8000
If any actual frontend source file still contains:

${import.meta.env.VITE_API_URL}
change it.

Send me this next
I don't want you changing random things now. Since Render is confirmed working, send me a screenshot of your Vercel website's F12 → Console after clicking the interview button.

That error will tell us exactly what is left.

contentscript.js:14083 MaxListenersExceededWarning: Possible EventEmitter memory leak detected. 11 close listeners added. Use emitter.setMaxListeners() to increase limit
contentscript.js:14083 MaxListenersExceededWarning: Possible EventEmitter memory leak detected. 11 end listeners added. Use emitter.setMaxListeners() to increase limit
2
contentscript.js:14083 ObjectMultiplex - orphaned data for stream "app-init-liveness"
2
contentscript.js:14083 ObjectMultiplex - orphaned data for stream "background-liveness"
16
The resource <URL> was preloaded using link preload but not used within a few seconds from the window's load event. Please make sure it has an appropriate as value and it is preloaded intentionally.
2okpd0efl30i_.js:19 Deprecated API for given entry type.

…

Show more
Those messages do not look like the actual reason your Vercel → Render connection is failing.

In particular, contentscript.js usually comes from a browser extension, not your React application. The preload and deprecated-API warnings are also generally non-fatal.

What we need now is the actual API request.

Do this
Open your Vercel website and:

Press F12
Select Network
Select Fetch/XHR at the top
Clear the existing requests 🗑️
Click your Start Interview / Send / whatever triggers the backend
A new request should appear.
Click that request.
Then send me a screenshot showing:

Headers
  Request URL
  Request Method
  Status Code
The most important thing is Request URL.

It should be:

https://intervai-by-tech-yodddhas.onrender.com/api/interview
If it says:

${import.meta.env.VITE_API_URL}/api/interview
then we've found the problem immediately.

If the URL is correct but you get something like:

CORS error
401
404
422
500
502
then we'll fix that specific backend/deployment issue.

Don't change your code yet. Send me the Network request details first; that's much more useful than these Console warnings.

Request URL
https://vercel.com/3628f7ea4ecd82e3/vitals
Request Method
POST
Status Code
200 OK
Remote Address
64.239.109.65:443
Referrer Policy
origin-when-cross-origin
cache-control
public, max-age=0, must-revalidate
content-length
0
content-type
text/plain; charset=utf-8
cross-origin-resource-policy
cross-origin
date
Sun, 09 Aug 2026 13:48:30 GMT
server
Vercel
strict-transport-security
max-age=63072000; includeSubDomains; preload
x-ratelimit-limit
1000
x-ratelimit-remaining
999
x-ratelimit-reset
60
x-vercel-cache
MISS
x-vercel-id
bom1::6lpdt-1786283310132-810e5d07e1ab
:authority
vercel.com
:method
POST
:path
/3628f7ea4ecd82e3/vitals
:scheme
https
accept
/
accept-encoding
gzip, deflate, br, zstd
accept-language
en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6
content-length
1547
content-type
text/plain
cookie
_ga=GA1.2.771389116.1763925510; signals-sdk-user-id=5c647bb1-d015-4e7f-b304-384620e93bbd; __ssid=17eab8707337bad135c8239c6b1fe6f; authorization=Bearer%20PWQKo9UUP0ywvWTCRqIwqnEn; isLoggedIn=1; scope=viveks-projects-0109e3c0; __stripe_mid=0e22744d-5367-490a-b715-02a9747db8f583e778; rl_page_init_referrer=RS_ENC_v3_Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20vIg%3D%3D; rl_page_init_referring_domain=RS_ENC_v3_Ind3dy5nb29nbGUuY29tIg%3D%3D; rl_trait=RS_ENC_v3_eyJlbWFpbCI6InZpdmVrYmlqMDVAZ21haWwuY29tIiwic2Vjb25kYXJ5X2VtYWlscyI6W10sIm5hbWUiOm51bGwsInVzZXJuYW1lIjoidml2ZWtiaWowNS02NDYzIn0%3D; _v-consent=%7B%22essential%22%3Atrue%2C%22analytics%22%3Atrue%2C%22marketing%22%3Atrue%2C%22functional%22%3Atrue%2C%22version%22%3A1%7D; rl_user_id=RS_ENC_v3_IkZNdTM3bllCUW90eTNKUU1qQXNRSE9kciI%3D; _v-anonymous-id=JOdgibXqVbsNkJJKbYq5o; rl_anonymous_id=RS_ENC_v3_IkpPZGdpYlhxVmJzTmtKSktiWXE1byI%3D; visitor-id=kViiozFIb7iYUCrJ7_Hzl; _v-anonymous-id-renewed=1; vercel_session_id=MTkwMjQ1MjE2NSwzMDc1NDk5MDgwLDM1MTYyNTE4NTYsMTY2NzQyMTc5MiwxNzc5NzU5ODA=; Lda_aKUr6BGRn=duertry.com/r/v2?; Lda_aKUr6BGRr=0; _v-session={%22id%22:%22240d5b5c-3462-47aa-a49a-664a34ef9199%22%2C%22landing_page%22:%22; __stripe_sid=b85c18c9-e747-4011-bcd4-3350604e196acfaa24; Fm_kZf8ZQvmX=1; Ac_aqK8DtrDS=6; userCache=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLWluZm8tY2FjaGUiLCJpYXQiOjE3ODYyODMyMTQsImV4cCI6MTgxNzgxOTIxNCwidWlkIjoiRk11MzduWUJRb3R5M0pRTWpBc1FIT2RyIiwidXNlcm5hbWUiOiJ2aXZla2JpajA1LTY0NjMiLCJlbWFpbCI6InZpdmVrYmlqMDVAZ21haWwuY29tIiwiaXNWZXJjZWxpYW4iOmZhbHNlLCJpc1BhcnRPZkFueUVudGVycHJpc2VUZWFtIjpmYWxzZSwiaGFzTm9UZWFtIjpmYWxzZSwiZGVmYXVsdFRlYW1JZCI6InRlYW1fclhCdE5uOUlZVjJPYlI2emhZZllVSE9WIiwiZGVmYXVsdFRlYW1TbHVnIjoidml2ZWtzLXByb2plY3RzLTAxMDllM2MwIiwiaXNOb3J0aHN0YXIiOnRydWUsIm5hbWUiOm51bGwsImF2YXRhciI6bnVsbH0.1sFmxiEzydYMYviWHeolLrPnf2LeTwhGIWUfitRac-Y; teamsCache=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLXRlYW0tY2FjaGUiLCJpYXQiOjE3ODYyODMyMTQsImV4cCI6MTgxNzgxOTIxNCwidGVhbVNsdWdJZE1hcCI6eyJ2aXZla3MtcHJvamVjdHMtMDEwOWUzYzAiOiJ0ZWFtX3JYQnRObjlJWVYyT2JSNnpoWWZZVUhPViJ9fQ.hoJZK6quFMuKD4UvDm_eVV0sQELXS6X7JAu6_xQUxf8; rl_session=RS_ENC_v3_eyJhdXRvVHJhY2siOnRydWUsInRpbWVvdXQiOjE4MDAwMDAsImV4cGlyZXNBdCI6MTc4NjI4NTAyMDA0MywiaWQiOjE3ODYyODIzNzMxMjcsInNlc3Npb25TdGFydCI6ZmFsc2V9
origin

priority
u=1, i
referer

sec-ch-prefers-color-scheme
dark
sec-ch-ua
"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
no-cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36

…

Show more
That request is not your API request. It is Vercel's own telemetry:

https://vercel.com/.../vitals
So it doesn't tell us whether your frontend can reach Render.

Also, your pasted headers contain Vercel session/authentication cookies. Don't share those publicly. Since you've exposed them here, it's safest to log out of Vercel and log back in.

Do this instead
Open your actual deployed Vercel website, not the Vercel dashboard.
Press F12.
Go to Network.
Select Fetch/XHR.
Click Clear.
Use your app — click the button that sends the interview request.
Look for a request containing:
/api/interview
Click it and send me only these 4 things:

Request URL:
Request Method:
Status Code:
Response:
The Request URL should look like:

https://intervai-by-tech-yodddhas.onrender.com/api/interview
If instead you see:

${import.meta.env.VITE_API_URL}/api/interview
then your Vercel frontend is still using the local backend.

If you don't see any /api/interview request at all, tell me that too — that means the problem is likely in the frontend code/config rather than Render.
