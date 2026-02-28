"""
Four deliberation workflows implementing the Multi-Agent Deliberation Framework.

Each workflow accepts a ModelConfig so callers can route different roles to
different models (e.g. free Groq models vs paid Claude/GPT-4 models).

Workflow A — Factual Verification      (2-3 rounds)
Workflow B — Analytical / Reasoning    (3-4 rounds)
Workflow C — Creative / Strategic      (3-4 rounds)
Workflow D — Judgment / Evaluation     (4 rounds)
"""

from typing import Optional
from model_config import ModelConfig
from models import call_model
from prompts import (
    wa_solver_r1, wa_challenger_r1, wa_scout_r1, wa_compare_r2, wa_arbitration_r3,
    wb_solver_r1, wb_challenger_r2, wb_scout_r2, wb_solver_r3, wb_convergence_r4, wb_final_r4,
    wc_solver_r1, wc_challenger_r1, wc_scout_r1, wc_crosspollinate_r2,
    wc_synthesis_r3, wc_stresstest_r4, wc_final_r4,
    wd_solver_r1, wd_challenger_r1, wd_scout_r1, wd_ach_matrix_r2, wd_crux_r3, wd_final_r4,
)


# ════════════════════════════════════════════════════════════
# Internal helpers
# ════════════════════════════════════════════════════════════

def _log(role: str, text: str) -> None:
    preview = text[:90].replace("\n", " ")
    print(f"    [{role}] {preview}{'...' if len(text) > 90 else ''}")


def _extract_confidence(text: str) -> str:
    upper = text.upper()
    for level in ["HIGH", "MEDIUM", "LOW"]:
        if f"CONFIDENCE: {level}" in upper or f"CONFIDENCE:{level}" in upper:
            return level
    return "MEDIUM"


def _extract_dissent(texts: list) -> Optional[str]:
    for text in texts:
        if text and "OBJECTION:" in text.upper():
            idx = text.upper().find("OBJECTION:")
            return text[idx: idx + 300].strip()
    return None


def _check_convergence(a: str, b: str, c: str) -> bool:
    """
    Heuristic: converged when at most one output signals active disagreement.
    """
    markers = [
        "disagree", "incorrect", "wrong answer", "different answer",
        "actually the answer", "not converged", "diverge",
    ]
    disagreeing = sum(
        any(m in t.lower() for m in markers) for t in [a, b, c]
    )
    return disagreeing <= 1


# ════════════════════════════════════════════════════════════
# WORKFLOW A — Factual Verification
# ════════════════════════════════════════════════════════════

def workflow_a(question: str, config: ModelConfig) -> dict:
    """Multi-Agent Debate + Cross-Verification. 2-3 rounds."""
    print("\n[Workflow A: Factual Verification]")
    trace = []

    # Round 1: Independent answers — each model sees only the question
    print("  [Round 1] Independent answers...")
    solver_r1 = call_model(*wa_solver_r1(question), config.solver)
    challenger_r1 = call_model(*wa_challenger_r1(question), config.challenger)
    scout_r1 = call_model(*wa_scout_r1(question), config.scout)
    _log("Solver", solver_r1)
    _log("Challenger", challenger_r1)
    _log("Scout", scout_r1)

    trace.append({"round": 1, "solver": solver_r1, "challenger": challenger_r1, "scout": scout_r1})

    # Round 2: All models see all Round-1 outputs
    print("  [Round 2] Compare & verify...")
    solver_r2 = call_model(*wa_compare_r2(question, solver_r1, challenger_r1, scout_r1, "SOLVER"), config.solver)
    challenger_r2 = call_model(*wa_compare_r2(question, solver_r1, challenger_r1, scout_r1, "CHALLENGER"), config.challenger)
    scout_r2 = call_model(*wa_compare_r2(question, solver_r1, challenger_r1, scout_r1, "SCOUT"), config.scout)
    _log("Solver", solver_r2)
    _log("Challenger", challenger_r2)
    _log("Scout", scout_r2)

    trace.append({"round": 2, "solver": solver_r2, "challenger": challenger_r2, "scout": scout_r2})

    if _check_convergence(solver_r2, challenger_r2, scout_r2):
        print("  [Convergence] Agreement reached in Round 2.")
        return {
            "answer": solver_r2,
            "confidence": _extract_confidence(solver_r2),
            "dissent": None,
            "reasoning_trace": trace,
        }

    # Round 3: Arbitration — still no consensus
    print("  [Round 3] Arbitration (full visibility)...")
    final = call_model(*wa_arbitration_r3(question, solver_r2, challenger_r2, scout_r2), config.solver)
    _log("Solver", final)

    trace.append({"round": 3, "solver": final, "challenger": None, "scout": None})

    return {
        "answer": final,
        "confidence": _extract_confidence(final),
        "dissent": None,
        "reasoning_trace": trace,
    }


# ════════════════════════════════════════════════════════════
# WORKFLOW B — Analytical / Reasoning
# ════════════════════════════════════════════════════════════

def workflow_b(question: str, config: ModelConfig) -> dict:
    """Dialectical Debate + Devil's Advocate. 3-4 rounds."""
    print("\n[Workflow B: Analytical Reasoning]")
    trace = []

    # Round 1: Solver builds full solution
    print("  [Round 1] Solver builds solution...")
    solver_r1 = call_model(*wb_solver_r1(question), config.solver)
    _log("Solver", solver_r1)

    trace.append({"round": 1, "solver": solver_r1, "challenger": None, "scout": None})

    # Round 2: Dual critique — Challenger attacks structure, Scout finds alt path
    print("  [Round 2] Challenger attacks + Scout finds alternative...")
    challenger_r2 = call_model(*wb_challenger_r2(question, solver_r1), config.challenger)
    scout_r2 = call_model(*wb_scout_r2(question, solver_r1), config.scout)
    _log("Challenger", challenger_r2)
    _log("Scout", scout_r2)

    trace.append({"round": 2, "solver": None, "challenger": challenger_r2, "scout": scout_r2})

    # Round 3: Solver responds to both critiques
    print("  [Round 3] Solver revises...")
    solver_r3 = call_model(*wb_solver_r3(question, solver_r1, challenger_r2, scout_r2), config.solver)
    _log("Solver", solver_r3)

    trace.append({"round": 3, "solver": solver_r3, "challenger": None, "scout": None})

    # Round 4: Convergence check
    print("  [Round 4] Convergence check...")
    challenger_r4 = call_model(*wb_convergence_r4(question, solver_r3, challenger_r2, "CHALLENGER"), config.challenger)
    scout_r4 = call_model(*wb_convergence_r4(question, solver_r3, scout_r2, "SCOUT"), config.scout)
    _log("Challenger review", challenger_r4)
    _log("Scout review", scout_r4)

    final = call_model(*wb_final_r4(question, solver_r3, challenger_r4, scout_r4), config.solver)

    trace.append({"round": 4, "solver": final, "challenger": challenger_r4, "scout": scout_r4})

    return {
        "answer": final,
        "confidence": _extract_confidence(final),
        "dissent": _extract_dissent([challenger_r4, scout_r4]),
        "reasoning_trace": trace,
    }


# ════════════════════════════════════════════════════════════
# WORKFLOW C — Creative / Strategic
# ════════════════════════════════════════════════════════════

def workflow_c(question: str, config: ModelConfig) -> dict:
    """Nominal Group Technique + Adversarial Collaboration. 4 rounds."""
    print("\n[Workflow C: Creative / Strategic]")
    trace = []

    # Round 1: Divergent generation — independent, distinct approaches
    print("  [Round 1] Divergent idea generation (independent)...")
    solver_r1 = call_model(*wc_solver_r1(question), config.solver)
    challenger_r1 = call_model(*wc_challenger_r1(question), config.challenger)
    scout_r1 = call_model(*wc_scout_r1(question), config.scout)
    _log("Solver (Pragmatic)", solver_r1)
    _log("Challenger (Contrarian)", challenger_r1)
    _log("Scout (Ambitious)", scout_r1)

    trace.append({"round": 1, "solver": solver_r1, "challenger": challenger_r1, "scout": scout_r1})

    # Round 2: Cross-pollination — all see all, each proposes a hybrid
    print("  [Round 2] Cross-pollination...")
    solver_r2 = call_model(*wc_crosspollinate_r2(question, solver_r1, challenger_r1, scout_r1, "SOLVER"), config.solver)
    challenger_r2 = call_model(*wc_crosspollinate_r2(question, solver_r1, challenger_r1, scout_r1, "CHALLENGER"), config.challenger)
    scout_r2 = call_model(*wc_crosspollinate_r2(question, solver_r1, challenger_r1, scout_r1, "SCOUT"), config.scout)
    _log("Solver hybrid", solver_r2)
    _log("Challenger hybrid", challenger_r2)
    _log("Scout hybrid", scout_r2)

    trace.append({"round": 2, "solver": solver_r2, "challenger": challenger_r2, "scout": scout_r2})

    # Round 3: Solver synthesizes from the three hybrids
    print("  [Round 3] Synthesis...")
    synthesis = call_model(*wc_synthesis_r3(question, solver_r2, challenger_r2, scout_r2), config.solver)
    _log("Solver synthesis", synthesis)

    trace.append({"round": 3, "solver": synthesis, "challenger": None, "scout": None})

    # Round 4: Stress test — pre-mortem + best-case → final
    print("  [Round 4] Stress test (pre-mortem + best-case)...")
    challenger_r4 = call_model(*wc_stresstest_r4(question, synthesis, "CHALLENGER"), config.challenger)
    scout_r4 = call_model(*wc_stresstest_r4(question, synthesis, "SCOUT"), config.scout)
    _log("Challenger (pre-mortem)", challenger_r4)
    _log("Scout (best-case)", scout_r4)

    final = call_model(*wc_final_r4(question, synthesis, challenger_r4, scout_r4), config.solver)

    trace.append({"round": 4, "solver": final, "challenger": challenger_r4, "scout": scout_r4})

    return {
        "answer": final,
        "confidence": _extract_confidence(final),
        "dissent": None,
        "reasoning_trace": trace,
    }


# ════════════════════════════════════════════════════════════
# WORKFLOW D — Judgment / Evaluation
# ════════════════════════════════════════════════════════════

def workflow_d(question: str, config: ModelConfig) -> dict:
    """Analysis of Competing Hypotheses + Adversarial Collaboration. 4 rounds."""
    print("\n[Workflow D: Judgment / Evaluation]")
    trace = []

    # Round 1: Each model takes a distinct position
    print("  [Round 1] Position generation...")
    solver_r1 = call_model(*wd_solver_r1(question), config.solver)
    challenger_r1 = call_model(*wd_challenger_r1(question, solver_r1), config.challenger)
    scout_r1 = call_model(*wd_scout_r1(question, solver_r1, challenger_r1), config.scout)
    _log("Solver", solver_r1)
    _log("Challenger", challenger_r1)
    _log("Scout", scout_r1)

    trace.append({"round": 1, "solver": solver_r1, "challenger": challenger_r1, "scout": scout_r1})

    # Round 2: ACH matrix — each model contributes evidence and scores
    print("  [Round 2] Building ACH evidence matrix...")
    solver_r2 = call_model(*wd_ach_matrix_r2(question, solver_r1, challenger_r1, scout_r1, "SOLVER"), config.solver)
    challenger_r2 = call_model(*wd_ach_matrix_r2(question, solver_r1, challenger_r1, scout_r1, "CHALLENGER"), config.challenger)
    scout_r2 = call_model(*wd_ach_matrix_r2(question, solver_r1, challenger_r1, scout_r1, "SCOUT"), config.scout)
    _log("Solver matrix", solver_r2)
    _log("Challenger matrix", challenger_r2)
    _log("Scout matrix", scout_r2)

    trace.append({"round": 2, "solver": solver_r2, "challenger": challenger_r2, "scout": scout_r2})

    # Round 3: Crux identification — what would change each model's mind?
    print("  [Round 3] Crux identification...")
    positions = f"Solver: {solver_r1}\n\nChallenger: {challenger_r1}\n\nScout: {scout_r1}"
    matrices = (
        f"Solver's matrix:\n{solver_r2}\n\n"
        f"Challenger's matrix:\n{challenger_r2}\n\n"
        f"Scout's matrix:\n{scout_r2}"
    )
    solver_r3 = call_model(*wd_crux_r3(question, positions, matrices, "SOLVER"), config.solver)
    challenger_r3 = call_model(*wd_crux_r3(question, positions, matrices, "CHALLENGER"), config.challenger)
    scout_r3 = call_model(*wd_crux_r3(question, positions, matrices, "SCOUT"), config.scout)
    _log("Solver crux", solver_r3)
    _log("Challenger crux", challenger_r3)
    _log("Scout crux", scout_r3)

    trace.append({"round": 3, "solver": solver_r3, "challenger": challenger_r3, "scout": scout_r3})

    # Round 4: Final judgment
    print("  [Round 4] Final judgment...")
    full_history = (
        f"ROUND 1 — POSITIONS:\n{positions}\n\n"
        f"ROUND 2 — ACH MATRICES:\n{matrices}\n\n"
        f"ROUND 3 — CRUX ANALYSIS:\n"
        f"Solver crux: {solver_r3}\n\n"
        f"Challenger crux: {challenger_r3}\n\n"
        f"Scout crux: {scout_r3}"
    )
    final = call_model(*wd_final_r4(question, full_history), config.solver)
    _log("Final judgment", final)

    trace.append({"round": 4, "solver": final, "challenger": None, "scout": None})

    return {
        "answer": final,
        "confidence": _extract_confidence(final),
        "dissent": _extract_dissent([challenger_r3, scout_r3]),
        "reasoning_trace": trace,
    }
