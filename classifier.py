from typing import Optional
from models import call_model

_CLASSIFIER_SYSTEM = """\
You are a question classifier. Classify the question into exactly one of these types:

FACTUAL   — Has a single definitive, verifiable answer ("What is X?", "Who did Y?", "When did Z?")
ANALYTICAL — Requires multi-step derivation, reasoning, math, code, debugging, or proof
CREATIVE  — Open-ended strategy, design, brainstorming, "how might we", exploration
JUDGMENT  — Trade-offs, ethical questions, comparative evaluation, "should we X or Y?"

Respond with ONLY the type word: FACTUAL, ANALYTICAL, CREATIVE, or JUDGMENT"""

_AMBIGUITY_SYSTEM = """\
You check whether a question has critical ambiguities that would prevent it from being
properly answered. Check for: ambiguous scope, unclear constraints, missing domain context,
unclear success criteria.

If the question is clear enough to answer: respond exactly "CLEAR"
If clarification is needed: respond "AMBIGUOUS: <one concise clarifying question>"
Keep your clarifying question short."""


def classify_question(question: str) -> str:
    """Classify a question into FACTUAL, ANALYTICAL, CREATIVE, or JUDGMENT."""
    result = call_model(_CLASSIFIER_SYSTEM, question)
    for q_type in ["FACTUAL", "ANALYTICAL", "CREATIVE", "JUDGMENT"]:
        if q_type in result.upper():
            return q_type
    return "ANALYTICAL"  # Safe default


def detect_ambiguities(question: str, q_type: str) -> Optional[str]:
    """Return a clarifying question if the question is ambiguous, else None."""
    prompt = f"Type: {q_type}\nQuestion: {question}"
    result = call_model(_AMBIGUITY_SYSTEM, prompt).strip()
    if result.upper().startswith("AMBIGUOUS"):
        parts = result.split(":", 1)
        return parts[1].strip() if len(parts) > 1 else None
    return None
