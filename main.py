import os
from dotenv import load_dotenv

load_dotenv()

from orchestrator import run_deliberation


def run(question: str) -> str:
    """
    Run the multi-agent deliberation pipeline on a question.

    The pipeline:
      1. Classifies the question (FACTUAL / ANALYTICAL / CREATIVE / JUDGMENT)
      2. Detects ambiguities (skipped in non-interactive mode)
      3. Runs the matching workflow (A / B / C / D) with Solver, Challenger, Scout
      4. Returns the final synthesized answer as a string

    This entry point runs non-interactively (no user prompts for clarification).
    Use run_deliberation(question, interactive=True) for the interactive version.
    """
    result = run_deliberation(question, interactive=False)
    return result["answer"]


if __name__ == "__main__":
    question = input("Ask a question: ")
    answer = run_deliberation(question, interactive=True)["answer"]
    print(answer)
