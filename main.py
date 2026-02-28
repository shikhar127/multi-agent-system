import os
from dotenv import load_dotenv

load_dotenv()

from model_config import (
    ModelConfig, AVAILABLE_MODELS, PRESETS,
    load_config, print_catalogue, print_active_config, validate_config,
)
from orchestrator import run_deliberation


def run(question: str, config: ModelConfig | None = None) -> str:
    """
    Programmatic entry point — runs the deliberation pipeline non-interactively.

    Parameters
    ----------
    question : The question to deliberate on.
    config   : Optional ModelConfig. Defaults to load_config() which reads
               MODEL_PRESET / SOLVER_MODEL / CHALLENGER_MODEL / SCOUT_MODEL
               from the environment (or .env file).

    Returns
    -------
    str — the final synthesized answer.
    """
    result = run_deliberation(question, config=config, interactive=False)
    return result["answer"]


def _pick_preset_interactively() -> ModelConfig:
    """Let the user choose a preset or custom model IDs at the prompt."""
    print_catalogue()

    preset_names = list(PRESETS.keys())
    print("Choose a preset (or type 'custom' to set models individually):")
    for i, name in enumerate(preset_names, 1):
        cfg = PRESETS[name]
        print(f"  {i}. {name:<10}  Solver={cfg.solver}")
        print(f"             Challenger={cfg.challenger}")
        print(f"             Scout={cfg.scout}")
    print()

    choice = input("Enter preset name or number [default: paid]: ").strip().lower()

    if not choice:
        return PRESETS["paid"]

    # Numeric choice
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(preset_names):
            selected = PRESETS[preset_names[idx]]
            print(f"  → Using '{preset_names[idx]}' preset.")
            return selected
        print("  Invalid number, defaulting to 'paid'.")
        return PRESETS["paid"]

    # Named preset
    if choice in PRESETS:
        return PRESETS[choice]

    # Custom
    if choice == "custom":
        model_ids = [m.model_id for m in AVAILABLE_MODELS.values()]
        print("\nAvailable model IDs:")
        for mid in model_ids:
            print(f"  {mid}")
        print()

        def pick(role: str, default: str) -> str:
            val = input(f"  {role} model [default: {default}]: ").strip()
            return val if val else default

        return ModelConfig(
            solver=pick("Solver", PRESETS["paid"].solver),
            challenger=pick("Challenger", PRESETS["paid"].challenger),
            scout=pick("Scout", PRESETS["paid"].scout),
        )

    print("  Unrecognised choice, defaulting to 'paid'.")
    return PRESETS["paid"]


if __name__ == "__main__":
    # Check if a preset is already set in the environment
    env_preset = os.environ.get("MODEL_PRESET", "")
    env_custom = any(
        os.environ.get(v) for v in ["SOLVER_MODEL", "CHALLENGER_MODEL", "SCOUT_MODEL"]
    )

    if env_preset or env_custom:
        # Use whatever is in the environment — no interactive prompt
        config = load_config()
        print("\n[Using model configuration from environment]")
        print_active_config(config)
    else:
        # Nothing pre-configured — let the user choose
        config = _pick_preset_interactively()

    # Validate API keys before asking for the question
    warnings = validate_config(config)
    if warnings:
        print("\n[Warning] The following API keys are missing:")
        for w in warnings:
            print(w)
        print("\nSet the missing keys in your .env file and restart, or choose a different preset.\n")

    question = input("\nAsk a question: ").strip()
    if not question:
        print("No question provided. Exiting.")
    else:
        run_deliberation(question, config=config, interactive=True)
