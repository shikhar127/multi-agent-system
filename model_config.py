"""
Model catalogue, preset configurations, and config loader.

Tiers
-----
free   — Open-source models served through Groq's free API tier.
         Requires a free Groq account: https://console.groq.com
paid   — Proprietary models from Anthropic and OpenAI.
         Requires a paid API key from the respective provider.

Presets
-------
free      Solver = Llama 3.3 70B  |  Challenger = Mixtral 8x7B  |  Scout = Gemma 2 9B
paid      All roles → Claude Sonnet 4.6
premium   Solver = Claude Opus 4.6  |  Challenger & Scout → Claude Sonnet 4.6

Configuration (via .env or shell environment)
---------------------------------------------
MODEL_PRESET     — "free" | "paid" | "premium"   (default: paid)
SOLVER_MODEL     — override model for the Solver role
CHALLENGER_MODEL — override model for the Challenger role
SCOUT_MODEL      — override model for the Scout role

API keys (set whichever providers you use)
GROQ_API_KEY       — from https://console.groq.com          (free)
ANTHROPIC_API_KEY  — from https://console.anthropic.com     (paid)
OPENAI_API_KEY     — from https://platform.openai.com       (paid)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


# ════════════════════════════════════════════════════════════
# Data types
# ════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ModelInfo:
    model_id: str       # exact ID passed to litellm
    display_name: str
    provider: str
    tier: str           # "free" | "paid"
    description: str
    api_key_env: str    # environment variable name for the required API key
    api_key_url: str    # where to get the key


@dataclass
class ModelConfig:
    solver: str
    challenger: str
    scout: str

    def roles(self) -> Dict[str, str]:
        return {"SOLVER": self.solver, "CHALLENGER": self.challenger, "SCOUT": self.scout}


# ════════════════════════════════════════════════════════════
# Model catalogue
# ════════════════════════════════════════════════════════════

AVAILABLE_MODELS: Dict[str, ModelInfo] = {

    # ── Free / Open-source  (Groq free tier) ────────────────
    "groq/llama-3.3-70b-versatile": ModelInfo(
        model_id="groq/llama-3.3-70b-versatile",
        display_name="Llama 3.3 70B",
        provider="Groq",
        tier="free",
        description="Meta's latest 70B — best open-source general-purpose model",
        api_key_env="GROQ_API_KEY",
        api_key_url="https://console.groq.com",
    ),
    "groq/llama-3.1-8b-instant": ModelInfo(
        model_id="groq/llama-3.1-8b-instant",
        display_name="Llama 3.1 8B Instant",
        provider="Groq",
        tier="free",
        description="Smallest and fastest — ideal when speed matters most",
        api_key_env="GROQ_API_KEY",
        api_key_url="https://console.groq.com",
    ),
    "groq/mixtral-8x7b-32768": ModelInfo(
        model_id="groq/mixtral-8x7b-32768",
        display_name="Mixtral 8x7B",
        provider="Groq",
        tier="free",
        description="Mistral's mixture-of-experts — strong structured reasoning",
        api_key_env="GROQ_API_KEY",
        api_key_url="https://console.groq.com",
    ),
    "groq/gemma2-9b-it": ModelInfo(
        model_id="groq/gemma2-9b-it",
        display_name="Gemma 2 9B",
        provider="Groq",
        tier="free",
        description="Google's Gemma 2 — distinct architecture for the Scout role",
        api_key_env="GROQ_API_KEY",
        api_key_url="https://console.groq.com",
    ),

    # ── Paid — Anthropic ────────────────────────────────────
    "claude-opus-4-6": ModelInfo(
        model_id="claude-opus-4-6",
        display_name="Claude Opus 4.6",
        provider="Anthropic",
        tier="paid",
        description="Most capable Claude — best for deep, complex reasoning",
        api_key_env="ANTHROPIC_API_KEY",
        api_key_url="https://console.anthropic.com",
    ),
    "claude-sonnet-4-6": ModelInfo(
        model_id="claude-sonnet-4-6",
        display_name="Claude Sonnet 4.6",
        provider="Anthropic",
        tier="paid",
        description="Balanced performance and speed — excellent across all roles",
        api_key_env="ANTHROPIC_API_KEY",
        api_key_url="https://console.anthropic.com",
    ),
    "claude-haiku-4-5": ModelInfo(
        model_id="claude-haiku-4-5-20251001",
        display_name="Claude Haiku 4.5",
        provider="Anthropic",
        tier="paid",
        description="Fastest and most cost-efficient Claude model",
        api_key_env="ANTHROPIC_API_KEY",
        api_key_url="https://console.anthropic.com",
    ),

    # ── Paid — OpenAI ───────────────────────────────────────
    "gpt-4o": ModelInfo(
        model_id="gpt-4o",
        display_name="GPT-4o",
        provider="OpenAI",
        tier="paid",
        description="OpenAI flagship — strong reasoning and instruction following",
        api_key_env="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com",
    ),
    "gpt-4o-mini": ModelInfo(
        model_id="gpt-4o-mini",
        display_name="GPT-4o Mini",
        provider="OpenAI",
        tier="paid",
        description="Efficient OpenAI model — good balance of quality and cost",
        api_key_env="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com",
    ),
}

# Convenience lookups: model_id → ModelInfo
_BY_MODEL_ID: Dict[str, ModelInfo] = {
    info.model_id: info for info in AVAILABLE_MODELS.values()
}


def get_info(model_id: str) -> ModelInfo | None:
    """Return ModelInfo for a model_id, or None if not in catalogue."""
    return _BY_MODEL_ID.get(model_id) or AVAILABLE_MODELS.get(model_id)


# ════════════════════════════════════════════════════════════
# Presets
# ════════════════════════════════════════════════════════════

FREE_PRESET = ModelConfig(
    solver="groq/llama-3.3-70b-versatile",
    challenger="groq/mixtral-8x7b-32768",
    scout="groq/gemma2-9b-it",
)

PAID_PRESET = ModelConfig(
    solver="claude-sonnet-4-6",
    challenger="claude-sonnet-4-6",
    scout="claude-sonnet-4-6",
)

PREMIUM_PRESET = ModelConfig(
    solver="claude-opus-4-6",
    challenger="claude-sonnet-4-6",
    scout="claude-sonnet-4-6",
)

PRESETS: Dict[str, ModelConfig] = {
    "free": FREE_PRESET,
    "paid": PAID_PRESET,
    "premium": PREMIUM_PRESET,
}


# ════════════════════════════════════════════════════════════
# Config loader
# ════════════════════════════════════════════════════════════

def load_config() -> ModelConfig:
    """
    Load model configuration from environment variables.

    Priority (highest → lowest):
      1. Individual role vars: SOLVER_MODEL, CHALLENGER_MODEL, SCOUT_MODEL
      2. MODEL_PRESET=free|paid|premium
      3. Default: paid preset
    """
    preset_name = os.environ.get("MODEL_PRESET", "paid").lower()
    base = PRESETS.get(preset_name, PAID_PRESET)

    return ModelConfig(
        solver=os.environ.get("SOLVER_MODEL", base.solver),
        challenger=os.environ.get("CHALLENGER_MODEL", base.challenger),
        scout=os.environ.get("SCOUT_MODEL", base.scout),
    )


# ════════════════════════════════════════════════════════════
# Display helpers
# ════════════════════════════════════════════════════════════

def print_catalogue() -> None:
    """Print the full model catalogue with tier grouping."""
    free = [m for m in AVAILABLE_MODELS.values() if m.tier == "free"]
    paid = [m for m in AVAILABLE_MODELS.values() if m.tier == "paid"]

    print("\n┌─────────────────────────────────────────────────────────────────────┐")
    print("│                     AVAILABLE MODELS                               │")
    print("├─────────────────────────────────────────────────────────────────────┤")

    print("│  FREE  (Groq — get a free key at https://console.groq.com)         │")
    print("│                                                                     │")
    for m in free:
        key = next(k for k, v in AVAILABLE_MODELS.items() if v.model_id == m.model_id)
        print(f"│  {key:<40} {m.display_name:<22}│")
        print(f"│    {m.description:<67}│")
    print("│                                                                     │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│  PAID  (Anthropic / OpenAI — requires paid API key)                │")
    print("│                                                                     │")
    for m in paid:
        key = next(k for k, v in AVAILABLE_MODELS.items() if v.model_id == m.model_id)
        print(f"│  {key:<40} {m.display_name:<22}│")
        print(f"│    {m.description:<67}│")
    print("│                                                                     │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│  PRESETS  (set MODEL_PRESET=<name> in .env)                        │")
    print("│                                                                     │")
    for name, cfg in PRESETS.items():
        print(f"│  {name:<10}  Solver={cfg.solver:<30}                │")
        print(f"│             Challenger={cfg.challenger:<27}                │")
        print(f"│             Scout={cfg.scout:<32}                │")
        print("│                                                                     │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│  CUSTOM  — override individual roles in .env:                      │")
    print("│    SOLVER_MODEL=...  CHALLENGER_MODEL=...  SCOUT_MODEL=...         │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")


def print_active_config(config: ModelConfig) -> None:
    """Print the currently active model assignments."""
    def label(model_id: str) -> str:
        info = get_info(model_id)
        return f"{model_id}  ({info.provider}, {info.tier})" if info else model_id

    print(f"\n  Active model configuration:")
    print(f"    Solver     → {label(config.solver)}")
    print(f"    Challenger → {label(config.challenger)}")
    print(f"    Scout      → {label(config.scout)}")


def validate_config(config: ModelConfig) -> list[str]:
    """
    Check that required API keys are set for the configured models.
    Returns a list of warning strings (empty = all good).
    """
    warnings = []
    checked_envs: set[str] = set()

    for role, model_id in config.roles().items():
        info = get_info(model_id)
        if info and info.api_key_env not in checked_envs:
            if not os.environ.get(info.api_key_env):
                warnings.append(
                    f"  Missing {info.api_key_env} (needed for {model_id}). "
                    f"Get it at {info.api_key_url}"
                )
            checked_envs.add(info.api_key_env)

    return warnings
