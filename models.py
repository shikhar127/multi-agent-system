"""
Thin wrapper around litellm that provides a single call_model() function.

litellm gives us a unified interface across Anthropic, OpenAI, Groq, and
100+ other providers — the caller just passes the right model ID string.

Provider routing is automatic based on the model ID prefix:
  claude-*         → Anthropic  (uses ANTHROPIC_API_KEY)
  groq/*           → Groq       (uses GROQ_API_KEY)
  gpt-* / openai/* → OpenAI     (uses OPENAI_API_KEY)
"""

import logging
import litellm

# Silence litellm's verbose request/response logging; keep only errors
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Drop provider-specific params silently when a model doesn't support them
litellm.drop_params = True


def call_model(system_prompt: str, user_prompt: str, model: str) -> str:
    """
    Call any LLM via litellm.

    Parameters
    ----------
    system_prompt : Role / persona instructions for the model.
    user_prompt   : The actual content for this turn.
    model         : litellm model ID, e.g. "claude-sonnet-4-6",
                    "groq/llama-3.3-70b-versatile", "gpt-4o".

    Returns
    -------
    str — the model's text response, stripped of leading/trailing whitespace.
    """
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=2048,
    )
    return response.choices[0].message.content.strip()
