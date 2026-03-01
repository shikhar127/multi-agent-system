# Multi-Agent Deliberation System

Three AI models — **Solver**, **Challenger**, and **Scout** — debate every question in structured rounds before producing a synthesized answer. The system automatically classifies each question, routes it to the appropriate workflow, optionally clarifies ambiguities, then returns a final answer with confidence rating and full reasoning trace.

---

## Table of Contents

1. [How it works](#how-it-works)
2. [Quick start](#quick-start)
3. [Model tiers](#model-tiers)
4. [Configuration](#configuration)
5. [Workflows](#workflows)
6. [Programmatic API](#programmatic-api)
7. [Project structure](#project-structure)

---

## How it works

```
Question
   │
   ▼
[Classifier] ──────────────────────────────────────────────
   │ FACTUAL / ANALYTICAL / CREATIVE / JUDGMENT
   │
   ▼
[Ambiguity check] — asks user one clarifying question if needed
   │
   ▼
┌─────────────────────────────────────────────────┐
│            Deliberation Workflow                │
│                                                 │
│  SOLVER      ←── builds / proposes             │
│  CHALLENGER  ←── attacks / stress-tests        │
│  SCOUT       ←── finds alternatives / reframes │
│                                                 │
│  2–4 structured rounds depending on type       │
└─────────────────────────────────────────────────┘
   │
   ▼
Final answer  +  confidence  +  dissent  +  trace
```

Each role can be assigned to **any model** — mix and match free open-source models with paid proprietary ones.

---

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API keys

Create a `.env` file (or export to your shell):

```bash
# Free tier — get a free key at https://console.groq.com
GROQ_API_KEY=gsk_...

# Paid — Anthropic (https://console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-...

# Paid — OpenAI (https://platform.openai.com)
OPENAI_API_KEY=sk-...
```

You only need the key(s) for the provider(s) you actually use.

### 3. Run

**Interactive** (model picker + question prompt):

```bash
python main.py
```

**With a preset pre-selected** (skips the picker):

```bash
MODEL_PRESET=free python main.py
```

**Fully non-interactive** (env vars + piped question):

```bash
MODEL_PRESET=free python -c "from main import run; print(run('What is the speed of light?'))"
```

---

## Model tiers

### Free — open-source models via [Groq](https://console.groq.com)

Groq offers a generous free tier with no credit card required.

| Model ID | Display name | Best for |
|---|---|---|
| `groq/llama-3.3-70b-versatile` | Llama 3.3 70B | General purpose — default Solver |
| `groq/llama-3.1-8b-instant` | Llama 3.1 8B Instant | Fastest responses |
| `groq/mixtral-8x7b-32768` | Mixtral 8x7B | Structured reasoning — default Challenger |
| `groq/gemma2-9b-it` | Gemma 2 9B | Diverse perspective — default Scout |

### Paid — proprietary models

| Model ID | Display name | Provider | Best for |
|---|---|---|---|
| `claude-opus-4-6` | Claude Opus 4.6 | Anthropic | Deep complex reasoning |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | Anthropic | Balanced (default paid preset) |
| `claude-haiku-4-5-20251001` | Claude Haiku 4.5 | Anthropic | Fast, cost-efficient |
| `gpt-4o` | GPT-4o | OpenAI | Strong reasoning |
| `gpt-4o-mini` | GPT-4o Mini | OpenAI | Efficient, cost-effective |

---

## Configuration

### Presets

Set `MODEL_PRESET` in your `.env` or shell to pick a full role assignment in one step.

| Preset | Solver | Challenger | Scout |
|---|---|---|---|
| `free` | `groq/llama-3.3-70b-versatile` | `groq/mixtral-8x7b-32768` | `groq/gemma2-9b-it` |
| `paid` *(default)* | `claude-sonnet-4-6` | `claude-sonnet-4-6` | `claude-sonnet-4-6` |
| `premium` | `claude-opus-4-6` | `claude-sonnet-4-6` | `claude-sonnet-4-6` |

### Override individual roles

Role-level env vars take priority over the preset:

```bash
# Use the paid preset but swap the Scout for a free Llama model
MODEL_PRESET=paid
SCOUT_MODEL=groq/llama-3.3-70b-versatile
```

```bash
# Mix OpenAI + Groq
SOLVER_MODEL=gpt-4o
CHALLENGER_MODEL=groq/mixtral-8x7b-32768
SCOUT_MODEL=groq/gemma2-9b-it
```

### Resolution order (highest → lowest priority)

1. `SOLVER_MODEL` / `CHALLENGER_MODEL` / `SCOUT_MODEL` — individual overrides
2. `MODEL_PRESET=free|paid|premium` — preset
3. Default: `paid` preset

### Example `.env` file

```bash
# --- Provider keys ---
GROQ_API_KEY=gsk_...
ANTHROPIC_API_KEY=sk-ant-...

# --- Model preset ---
MODEL_PRESET=free

# --- Optional role overrides ---
# SOLVER_MODEL=claude-sonnet-4-6
# CHALLENGER_MODEL=groq/mixtral-8x7b-32768
# SCOUT_MODEL=groq/gemma2-9b-it
```

---

## Workflows

The classifier picks one of four workflows automatically based on the question type.

### Workflow A — Factual Verification (2–3 rounds)

*Technique: Multi-Agent Debate + Cross-Verification*

Used for questions with a single correct answer ("What is the capital of France?").

| Round | Who | Does what |
|---|---|---|
| 1 | Solver, Challenger, Scout | Answer independently — no shared context |
| 2 | All | See all Round-1 answers; compare and argue |
| 3* | Solver | Arbitration if still no consensus |

\* Round 3 only runs if Round 2 does not converge.

### Workflow B — Analytical Reasoning (3–4 rounds)

*Technique: Dialectical Debate + Devil's Advocate*

Used for multi-step reasoning, math, code, and proofs.

| Round | Who | Does what |
|---|---|---|
| 1 | Solver | Builds a full step-by-step solution |
| 2 | Challenger, Scout | Attack flaws / find an alternative approach |
| 3 | Solver | Revises — accepts valid objections, rebuts invalid ones |
| 4 | Challenger, Scout, Solver | Convergence check → final answer |

### Workflow C — Creative / Strategic (4 rounds)

*Technique: Nominal Group Technique + Adversarial Collaboration*

Used for open-ended strategy, design, and brainstorming.

| Round | Who | Does what |
|---|---|---|
| 1 | Solver (Pragmatic), Challenger (Contrarian), Scout (Ambitious) | Generate 3 independent approaches |
| 2 | All | Cross-pollinate — rank all approaches, propose a hybrid |
| 3 | Solver | Synthesize the three hybrids into one recommendation |
| 4 | Challenger (pre-mortem), Scout (best-case), Solver | Stress test → final recommendation |

### Workflow D — Judgment / Evaluation (4 rounds)

*Technique: Analysis of Competing Hypotheses + Adversarial Collaboration*

Used for trade-offs, ethical questions, and comparative evaluation.

| Round | Who | Does what |
|---|---|---|
| 1 | Solver, Challenger, Scout | Each takes a distinct position |
| 2 | All | Build an ACH evidence matrix (score each position against evidence) |
| 3 | All | Identify cruxes — "I would change my position if ____" |
| 4 | Solver | Final judgment with confidence, caveats, and reversal conditions |

---

## Programmatic API

```python
from main import run

# Simplest call — uses MODEL_PRESET / *_MODEL env vars
answer = run("Should we rewrite the legacy service in Go or keep Python?")
print(answer)
```

```python
from main import run
from model_config import ModelConfig

# Explicit model config — no env vars needed
config = ModelConfig(
    solver="claude-sonnet-4-6",
    challenger="groq/mixtral-8x7b-32768",
    scout="groq/gemma2-9b-it",
)
answer = run("Explain the trade-offs between microservices and a monolith.", config=config)
```

```python
from orchestrator import run_deliberation
from model_config import FREE_PRESET

# Full result with trace
result = run_deliberation(
    "Design a rate-limiting strategy for a public API.",
    config=FREE_PRESET,
    interactive=False,
)
print(result["answer"])
print(result["confidence"])   # HIGH / MEDIUM / LOW
print(result["question_type"])  # CREATIVE
for round_data in result["reasoning_trace"]:
    print(round_data)
```

### `run_deliberation()` return value

```python
{
    "answer":          str,         # Final synthesized answer
    "confidence":      str,         # "HIGH" | "MEDIUM" | "LOW"
    "dissent":         str | None,  # Minority position if unresolved
    "question_type":   str,         # "FACTUAL" | "ANALYTICAL" | "CREATIVE" | "JUDGMENT"
    "reasoning_trace": list[dict],  # One dict per round: {"round": int, "solver": str, ...}
}
```

---

## Project structure

```
multi-agent-system/
├── main.py           Entry point — interactive mode + run() helper
├── orchestrator.py   Pipeline: classify → clarify → workflow → result
├── classifier.py     Question type classifier + ambiguity detector
├── workflows.py      Workflow A / B / C / D implementations
├── prompts.py        All prompt template functions
├── models.py         call_model() — thin litellm wrapper
├── model_config.py   Model catalogue, presets, config loader
└── requirements.txt
```

### Key data flow

```
main.py
  └─ orchestrator.run_deliberation(question, config)
       ├─ classifier.classify_question(question, model)   → question type
       ├─ classifier.detect_ambiguities(question, type, model)
       └─ workflows.workflow_{a|b|c|d}(question, config)
            └─ models.call_model(system, user, model)     → str
                 └─ litellm.completion(model, messages)   → provider API
```

### Adding a new model

1. Add a `ModelInfo` entry to `AVAILABLE_MODELS` in `model_config.py`.
2. Set it via `SOLVER_MODEL`, `CHALLENGER_MODEL`, or `SCOUT_MODEL` — or define a new preset.
3. Ensure the corresponding API key env var is set.

litellm handles routing automatically; no other code changes are required.
