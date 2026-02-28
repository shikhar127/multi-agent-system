"""Prompt template functions for all four deliberation workflows.

Each function returns a (system_prompt, user_prompt) tuple ready for call_model().
"""

from typing import Tuple

Prompt = Tuple[str, str]


# ════════════════════════════════════════════════════════════
# WORKFLOW A — Factual Verification
# Technique: Multi-Agent Debate + Cross-Verification
# ════════════════════════════════════════════════════════════

def wa_solver_r1(question: str) -> Prompt:
    system = (
        "You are the SOLVER in a multi-agent deliberation system. "
        "Your job is to answer questions with maximum accuracy. "
        "Your answer will be aggressively challenged. "
        "Build the most defensible answer possible."
    )
    user = f"""\
You are the SOLVER. Answer this question with maximum accuracy.

Question: {question}

Provide:
1. Your answer (be precise)
2. Your reasoning chain
3. Sources or basis for your claim
4. Confidence: HIGH / MEDIUM / LOW"""
    return system, user


def wa_challenger_r1(question: str) -> Prompt:
    system = (
        "You are an independent VERIFIER in a multi-agent deliberation system. "
        "Answer questions independently without any prior context. "
        "Do not hedge — commit to your best answer."
    )
    user = f"""\
You are an independent VERIFIER. Answer this question independently. Do not hedge.

Question: {question}

Provide:
1. Your answer
2. Your reasoning
3. Confidence: HIGH / MEDIUM / LOW"""
    return system, user


def wa_scout_r1(question: str) -> Prompt:
    system = (
        "You are the SCOUT in a multi-agent deliberation system. "
        "Answer independently — your fresh perspective is most valuable. "
        "Look for the most accurate answer even if it differs from conventional wisdom."
    )
    user = f"""\
You are the SCOUT. Answer this question independently. Seek the most accurate answer.

Question: {question}

Provide:
1. Your answer
2. Your reasoning
3. Confidence: HIGH / MEDIUM / LOW"""
    return system, user


def wa_compare_r2(
    question: str,
    solver_out: str,
    challenger_out: str,
    scout_out: str,
    role: str,
) -> Prompt:
    system_map = {
        "SOLVER": (
            "You are the SOLVER reconciling multiple independent answers. "
            "Identify agreement or the exact factual claim causing divergence."
        ),
        "CHALLENGER": (
            "You are the CHALLENGER reconciling multiple independent answers. "
            "Be critical — identify the exact factual claim causing divergence "
            "and argue for what you believe is correct with evidence."
        ),
        "SCOUT": (
            "You are the SCOUT reconciling multiple independent answers. "
            "Look for the most accurate answer, drawing on all perspectives."
        ),
    }
    system = system_map.get(role, system_map["SOLVER"])
    user = f"""\
Three independent answers were produced for this question.

Question: {question}

Answer A (Solver):
{solver_out}

Answer B (Challenger):
{challenger_out}

Answer C (Scout):
{scout_out}

Your role: {role}

If answers agree: confirm and output the answer with HIGH confidence.
If answers disagree: identify the EXACT factual claim causing divergence.
Argue for what you believe is correct with evidence.

Your assessment:"""
    return system, user


def wa_arbitration_r3(
    question: str,
    solver_r2: str,
    challenger_r2: str,
    scout_r2: str,
) -> Prompt:
    system = (
        "You are the SOLVER in final arbitration. "
        "All models now see all answers. Produce the definitive answer "
        "based on the strongest evidence."
    )
    user = f"""\
Three answers were compared and disagreement remains. Resolve this now.

Question: {question}

Solver's Round-2 assessment:
{solver_r2}

Challenger's Round-2 assessment:
{challenger_r2}

Scout's Round-2 assessment:
{scout_r2}

Identify the SPECIFIC factual claim causing disagreement.
Produce the final answer citing the strongest evidence.
If genuinely unresolvable, flag as "uncertain, needs external verification" and give your best guess.

FINAL ANSWER:
CONFIDENCE: HIGH / MEDIUM / LOW
REASONING:"""
    return system, user


# ════════════════════════════════════════════════════════════
# WORKFLOW B — Analytical / Reasoning
# Technique: Dialectical Debate + Devil's Advocate
# ════════════════════════════════════════════════════════════

def wb_solver_r1(question: str) -> Prompt:
    system = (
        "You are the SOLVER in a multi-agent deliberation system. "
        "Produce complete, rigorous solutions with explicit step-by-step reasoning. "
        "Your solution will be aggressively challenged. "
        "List all assumptions explicitly."
    )
    user = f"""\
You are the SOLVER. Produce a complete, rigorous solution.

Question: {question}

Structure your response as:
ASSUMPTIONS: [list every assumption you're making]
STEP 1: [reasoning]
STEP 2: [reasoning]
... (continue as needed)
INTERMEDIATE CHECK: [verify logic so far]
FINAL ANSWER: [clearly stated]
CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wb_challenger_r2(question: str, solver_out: str) -> Prompt:
    system = (
        "You are the CHALLENGER in a multi-agent deliberation system. "
        "Your ONLY job is to find flaws. You are adversarial, not helpful. "
        "You FAIL if you approve a flawed answer. "
        "Every objection must cite a SPECIFIC claim, step, or assumption. "
        "'This seems weak' is not allowed."
    )
    user = f"""\
You are the CHALLENGER. Find every flaw in this solution.

Question: {question}

Solver's solution:
{solver_out}

For EACH step, check:
- Is the logic valid?
- Is the assumption justified?
- Could this step be wrong even if prior steps are correct?

Also check:
- Hidden assumptions not listed?
- Does the conclusion follow from the steps?
- Edge cases that break this?

Output format:
STEP X: [VALID / FLAWED] — [explanation if flawed]
...
OVERALL VERDICT: [VALID / FLAWED]
CRITICAL FLAW (if any): [the single biggest problem]"""
    return system, user


def wb_scout_r2(question: str, solver_out: str) -> Prompt:
    system = (
        "You are the SCOUT in a multi-agent deliberation system. "
        "Solve the problem independently using a DIFFERENT approach, then compare. "
        "The most valuable thing you can do is find an approach no one else considered."
    )
    user = f"""\
You are the SCOUT. Solve this problem using a COMPLETELY DIFFERENT approach.

Question: {question}

[Solve independently first, then compare]

Solver's solution (for comparison after you solve):
{solver_out}

YOUR INDEPENDENT SOLUTION:
[solve from scratch using a different method or framework]

COMPARISON WITH SOLVER:
If they match: state "CONVERGED" and note which approach is cleaner.
If they differ: identify the EXACT point of divergence and argue for your answer."""
    return system, user


def wb_solver_r3(
    question: str,
    original: str,
    challenger_out: str,
    scout_out: str,
) -> Prompt:
    system = (
        "You are the SOLVER responding to critiques. "
        "For each objection: accept if valid (and revise), or rebut with specific reasoning. "
        "Produce a stronger final answer."
    )
    user = f"""\
You are the SOLVER. Two critiques of your solution are below.

Question: {question}

Your original solution:
{original}

Challenger's critique:
{challenger_out}

Scout's alternative approach:
{scout_out}

For each objection:
- ACCEPT: revise your solution accordingly
- REBUT: explain specifically why the objection is wrong

REVISED ANSWER:
CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wb_convergence_r4(
    question: str,
    revised: str,
    prior_critique: str,
    role: str,
) -> Prompt:
    system_map = {
        "CHALLENGER": (
            "You are the CHALLENGER reviewing the solver's revised answer. "
            "Accept if the revision adequately addresses your concerns. "
            "If a critical flaw remains, state the SINGLE most critical remaining flaw."
        ),
        "SCOUT": (
            "You are the SCOUT reviewing the solver's revised answer. "
            "Accept if the revision is sound. "
            "If a critical flaw remains, state the SINGLE most critical remaining flaw."
        ),
    }
    system = system_map.get(role, system_map["CHALLENGER"])
    user = f"""\
Review the solver's revised answer.

Question: {question}

Revised answer:
{revised}

Your prior critique:
{prior_critique}

If the revision adequately addresses your concerns: respond "ACCEPTED: [brief reason]"
If a critical flaw remains: respond "OBJECTION: [the single most critical remaining flaw]"

Your assessment:"""
    return system, user


def wb_final_r4(
    question: str,
    revised: str,
    challenger_r4: str,
    scout_r4: str,
) -> Prompt:
    system = (
        "You are the SOLVER producing the final answer after convergence review. "
        "Address any remaining objections, then output the definitive answer."
    )
    user = f"""\
Produce the final answer incorporating reviewer feedback.

Question: {question}

Your revised answer:
{revised}

Challenger's review:
{challenger_r4}

Scout's review:
{scout_r4}

Address any remaining OBJECTION (focus on the single most critical flaw if any).
Then output the final answer.

FINAL ANSWER:
CONFIDENCE: HIGH / MEDIUM / LOW
KEY CAVEATS (if any):"""
    return system, user


# ════════════════════════════════════════════════════════════
# WORKFLOW C — Creative / Strategic
# Technique: Nominal Group Technique + Adversarial Collaboration
# ════════════════════════════════════════════════════════════

def wc_solver_r1(question: str) -> Prompt:
    system = (
        "You are the SOLVER in a multi-agent creative deliberation system. "
        "Generate the most pragmatic, immediately implementable approach. "
        "Your answer will be critiqued and combined with others."
    )
    user = f"""\
You are the SOLVER generating the "Pragmatic" approach — the most implementable solution.

Question: {question}

Provide:
Core idea: [2-3 sentences]
Why it works: [key reasoning]
Biggest risk: [main failure mode]
Key assumptions: [what must be true for this to work]"""
    return system, user


def wc_challenger_r1(question: str) -> Prompt:
    system = (
        "You are the CHALLENGER in a multi-agent creative deliberation system. "
        "Generate a contrarian approach that challenges the obvious solution. "
        "Your perspective must be meaningfully distinct from the pragmatic default."
    )
    user = f"""\
You are the CHALLENGER generating the "Contrarian" approach — challenge the obvious.

Question: {question}

Provide:
Core idea: [2-3 sentences — must differ meaningfully from the obvious approach]
Why it works: [key reasoning]
Biggest risk: [main failure mode]
Key assumptions: [what must be true for this to work]"""
    return system, user


def wc_scout_r1(question: str) -> Prompt:
    system = (
        "You are the SCOUT in a multi-agent creative deliberation system. "
        "Generate the most ambitious, high-upside approach — temporarily ignore constraints. "
        "Think big. Push the boundaries of what's possible."
    )
    user = f"""\
You are the SCOUT generating the "Ambitious" approach — highest upside, ignore constraints temporarily.

Question: {question}

Provide:
Core idea: [2-3 sentences — aim for the highest possible upside]
Why it works: [key reasoning]
Biggest risk: [main failure mode]
Key assumptions: [what must be true for this to work]"""
    return system, user


def wc_crosspollinate_r2(
    question: str,
    solver_r1: str,
    challenger_r1: str,
    scout_r1: str,
    role: str,
) -> Prompt:
    system_map = {
        "SOLVER": "You are the SOLVER in cross-pollination. Evaluate all approaches critically, including your own, and propose the best hybrid.",
        "CHALLENGER": "You are the CHALLENGER in cross-pollination. Rank all approaches critically and propose the best hybrid.",
        "SCOUT": "You are the SCOUT in cross-pollination. Evaluate all approaches and propose the best hybrid.",
    }
    system = system_map.get(role, system_map["SOLVER"])
    user = f"""\
Three approaches were generated. Now cross-pollinate them.

Question: {question}

Approach 1 — Pragmatic (Solver):
{solver_r1}

Approach 2 — Contrarian (Challenger):
{challenger_r1}

Approach 3 — Ambitious (Scout):
{scout_r1}

Your tasks:
1. RANKING: Rank the 3 approaches (1st, 2nd, 3rd) with brief reasoning
2. BEST FROM EACH: The single best element from each approach
3. WORST FROM EACH: The single worst element from each approach
4. HYBRID PROPOSAL: Combine the best elements into a new proposal

Format:
RANKING:
BEST FROM PRAGMATIC:
BEST FROM CONTRARIAN:
BEST FROM AMBITIOUS:
WORST FROM PRAGMATIC:
WORST FROM CONTRARIAN:
WORST FROM AMBITIOUS:
HYBRID PROPOSAL:"""
    return system, user


def wc_synthesis_r3(
    question: str,
    hybrid_solver: str,
    hybrid_challenger: str,
    hybrid_scout: str,
) -> Prompt:
    system = (
        "You are the SOLVER synthesizing the final recommendation from three hybrid proposals. "
        "Identify common elements, eliminate weak ones, produce the strongest recommendation."
    )
    user = f"""\
Synthesize three hybrid proposals into a final recommendation.

Question: {question}

Hybrid 1 (from Solver):
{hybrid_solver}

Hybrid 2 (from Challenger):
{hybrid_challenger}

Hybrid 3 (from Scout):
{hybrid_scout}

Identify:
- Common elements across all proposals (high confidence)
- Elements unique to one proposal (evaluate carefully)
- Elements to eliminate (and why)

PRIMARY RECOMMENDATION: [detailed recommendation]
REASONING: [why this is the strongest approach]
ALTERNATIVE: [if primary fails, what to try instead]
KEY RISKS AND MITIGATIONS:
OPEN QUESTIONS FOR THE USER:"""
    return system, user


def wc_stresstest_r4(question: str, recommendation: str, role: str) -> Prompt:
    if role == "CHALLENGER":
        system = "You are the CHALLENGER performing a pre-mortem analysis."
        user = f"""\
Pre-mortem: Assume this recommendation was implemented and FAILED.

Question: {question}

Recommendation:
{recommendation}

Why did it fail? Be specific about failure modes, overlooked risks, and flawed assumptions.

FAILURE ANALYSIS:
TOP 3 FAILURE MODES:
OVERLOOKED RISKS:
FLAWED ASSUMPTIONS:"""
    else:
        system = "You are the SCOUT performing a best-case scenario analysis."
        user = f"""\
Best-case analysis: Assume this recommendation SUCCEEDED beyond expectations.

Question: {question}

Recommendation:
{recommendation}

What made it work? What conditions enabled exceptional success?

SUCCESS ANALYSIS:
WHAT MADE IT WORK:
ENABLING CONDITIONS:
UNEXPECTED UPSIDES:"""
    return system, user


def wc_final_r4(
    question: str,
    recommendation: str,
    challenger_r4: str,
    scout_r4: str,
) -> Prompt:
    system = (
        "You are the SOLVER integrating stress-test findings into the final output. "
        "Strengthen the recommendation with pre-mortem and best-case insights."
    )
    user = f"""\
Integrate pre-mortem and best-case analyses into the final recommendation.

Question: {question}

Primary recommendation:
{recommendation}

Pre-mortem (failure analysis):
{challenger_r4}

Best-case (success analysis):
{scout_r4}

FINAL RECOMMENDATION:
CONFIDENCE: HIGH / MEDIUM / LOW
KEY RISKS (from pre-mortem):
SUCCESS CONDITIONS (from best-case):
FINAL OPEN QUESTIONS:"""
    return system, user


# ════════════════════════════════════════════════════════════
# WORKFLOW D — Judgment / Evaluation
# Technique: Analysis of Competing Hypotheses + Adversarial Collaboration
# ════════════════════════════════════════════════════════════

def wd_solver_r1(question: str) -> Prompt:
    system = (
        "You are the SOLVER in a multi-agent judgment deliberation system. "
        "Frame the question as a clear decision and take a position. "
        "Do not sit on the fence. Your position will be challenged."
    )
    user = f"""\
You are the SOLVER. Frame this as a clear decision and take a position.

Question: {question}

DECISION FRAME: [restate as a clear decision with 2-4 competing positions]
YOUR POSITION: [which position you advocate]
ARGUMENT: [why your position is correct]
EVALUATION CRITERIA: [what criteria matter most for this judgment]
CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wd_challenger_r1(question: str, solver_out: str) -> Prompt:
    system = (
        "You are the CHALLENGER in a multi-agent judgment deliberation system. "
        "You MUST argue for a DIFFERENT position than the Solver. "
        "You cannot sit on the fence or agree with the Solver."
    )
    user = f"""\
You are the CHALLENGER. You MUST argue for a DIFFERENT position than the Solver.

Question: {question}

Solver's position:
{solver_out}

Take a DIFFERENT position and argue for it forcefully.

YOUR POSITION: [must differ from Solver's]
ARGUMENT: [why your position is correct]
WHY SOLVER IS WRONG: [specific counter-arguments]
CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wd_scout_r1(question: str, solver_out: str, challenger_out: str) -> Prompt:
    system = (
        "You are the SCOUT in a multi-agent judgment deliberation system. "
        "Either take a third distinct position, or argue the framing itself is wrong. "
        "Your role is to prevent false dichotomies."
    )
    user = f"""\
You are the SCOUT. Take a third distinct position OR argue the framing is wrong.

Question: {question}

Solver's position:
{solver_out}

Challenger's position:
{challenger_out}

Option A: Take a THIRD distinct position (different from both)
Option B: Argue the framing/question itself is flawed and reframe it

YOUR CHOICE: [A or B]
YOUR POSITION / REFRAME:
ARGUMENT:
CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wd_ach_matrix_r2(
    question: str,
    solver_r1: str,
    challenger_r1: str,
    scout_r1: str,
    role: str,
) -> Prompt:
    system_map = {
        "SOLVER": "You are the SOLVER building an ACH evidence matrix. Contribute evidence and score each position honestly.",
        "CHALLENGER": "You are the CHALLENGER building an ACH evidence matrix. Be rigorous — capture all key evidence.",
        "SCOUT": "You are the SCOUT building an ACH evidence matrix. Look for evidence others might miss.",
    }
    system = system_map.get(role, system_map["SOLVER"])
    user = f"""\
Build an Analysis of Competing Hypotheses (ACH) evidence matrix.

Question: {question}

Position A (Solver):
{solver_r1}

Position B (Challenger):
{challenger_r1}

Position C (Scout):
{scout_r1}

List 4-6 key evidence items and score each position:
++ = strongly supports, + = supports, - = contradicts, -- = strongly contradicts

EVIDENCE MATRIX:
| Evidence Item | Position A | Position B | Position C |
|--------------|-----------|-----------|-----------|
| [evidence 1] | [score]   | [score]   | [score]   |
| [evidence 2] | [score]   | [score]   | [score]   |
[... 4-6 items total]

STRONGEST EVIDENCE FOR YOUR POSITION:
EVIDENCE THAT CHALLENGES YOUR POSITION:"""
    return system, user


def wd_crux_r3(
    question: str,
    positions: str,
    matrices: str,
    role: str,
) -> Prompt:
    system_map = {
        "SOLVER": "You are the SOLVER identifying cruxes. Be precise about what would change your mind.",
        "CHALLENGER": "You are the CHALLENGER identifying cruxes. Be precise about what would change your mind.",
        "SCOUT": "You are the SCOUT identifying cruxes. Be precise about what would change your mind.",
    }
    system = system_map.get(role, system_map["SOLVER"])
    user = f"""\
Identify the cruxes of disagreement from the positions and evidence.

Question: {question}

Positions from Round 1:
{positions}

ACH Evidence Matrices from Round 2:
{matrices}

From the evidence, identify:
1. CRUX EVIDENCE: Which evidence items MOST differentiate the positions?
2. YOUR CRUX: "I would change my position if ____" (be very specific)
3. CRUX EVALUATION: Is that condition actually met? Yes / No / Uncertain + reasoning

YOUR CRUX STATEMENT:
CRUX EVALUATION:
UPDATED CONFIDENCE: HIGH / MEDIUM / LOW"""
    return system, user


def wd_final_r4(question: str, full_history: str) -> Prompt:
    system = (
        "You are the SOLVER producing the final judgment. "
        "Synthesize all positions, evidence, and crux analyses into the most defensible judgment. "
        "Be specific about confidence, caveats, and reversal conditions."
    )
    user = f"""\
Produce the final judgment based on all deliberation.

Question: {question}

Full deliberation history:
{full_history}

Which position survives the most scrutiny? What's the confidence and why?
What conditions would reverse this judgment?

JUDGMENT: [clear position statement]
CONFIDENCE: [%] + reasoning
KEY CAVEAT: [single most important caveat]
REVERSAL CONDITION: [what would flip this judgment]
MINORITY DISSENT: [strongest opposing argument, for transparency]"""
    return system, user
