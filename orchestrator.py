"""
Main orchestrator for the Multi-Agent Deliberation Framework.

Phase 0   — Classify the question (FACTUAL / ANALYTICAL / CREATIVE / JUDGMENT)
Phase 0.5 — Detect ambiguities and optionally ask the user for clarification
Phase 1   — Run the appropriate workflow (A / B / C / D)
Phase 2   — Return structured result with answer, confidence, dissent, and full trace
"""

from typing import Optional
from classifier import classify_question, detect_ambiguities
from workflows import workflow_a, workflow_b, workflow_c, workflow_d

_WORKFLOW_MAP = {
    "FACTUAL": workflow_a,
    "ANALYTICAL": workflow_b,
    "CREATIVE": workflow_c,
    "JUDGMENT": workflow_d,
}

_WORKFLOW_LABELS = {
    "FACTUAL": "A — Factual Verification",
    "ANALYTICAL": "B — Analytical Reasoning",
    "CREATIVE": "C — Creative / Strategic",
    "JUDGMENT": "D — Judgment / Evaluation",
}


def run_deliberation(question: str, interactive: bool = True) -> dict:
    """
    Run the full multi-agent deliberation pipeline on a question.

    Parameters
    ----------
    question    : The question to deliberate on.
    interactive : When True, prompts the user for clarification if ambiguities
                  are detected (Phase 0.5). Set to False for programmatic use.

    Returns
    -------
    dict with keys:
        answer          — str: the final synthesized answer
        confidence      — str: HIGH / MEDIUM / LOW
        dissent         — str | None: minority position if unresolved
        question_type   — str: FACTUAL / ANALYTICAL / CREATIVE / JUDGMENT
        reasoning_trace — list: full audit trail of every round
    """
    print(f"\n{'═' * 64}")
    print(f"QUESTION: {question[:110]}{'...' if len(question) > 110 else ''}")
    print('═' * 64)

    # ── Phase 0: Classify ──────────────────────────────────────────
    print("\n[Phase 0] Classifying question...")
    q_type = classify_question(question)
    print(f"          → {_WORKFLOW_LABELS.get(q_type, q_type)}")

    # ── Phase 0.5: Ambiguity detection (interactive only) ──────────
    if interactive:
        print("[Phase 0.5] Checking for ambiguities...")
        clarification_q = detect_ambiguities(question, q_type)
        if clarification_q:
            print(f"\n  Clarification needed: {clarification_q}")
            user_input = input("  Your answer (or press Enter to skip): ").strip()
            if user_input:
                question = f"{question}\n\nAdditional context: {user_input}"
                print("  [Question enriched with user context.]")
        else:
            print("          → Question is clear, proceeding.")

    # ── Phase 1: Run workflow ───────────────────────────────────────
    workflow_fn = _WORKFLOW_MAP.get(q_type, workflow_b)
    result = workflow_fn(question)
    result["question_type"] = q_type

    # ── Phase 2: Display result ────────────────────────────────────
    print(f"\n{'═' * 64}")
    print("FINAL ANSWER")
    print('═' * 64)
    print(result["answer"])
    print(f"\nConfidence : {result.get('confidence', 'MEDIUM')}")
    print(f"Type       : {q_type}")
    rounds = len(result.get("reasoning_trace", []))
    print(f"Rounds     : {rounds}")
    if result.get("dissent"):
        print(f"\n[Minority dissent]\n{result['dissent']}")
    print('═' * 64)

    return result
