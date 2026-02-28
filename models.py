import os
from typing import Optional
import anthropic

_client: Optional[anthropic.Anthropic] = None
MODEL = "claude-sonnet-4-6"


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def call_model(system_prompt: str, user_prompt: str) -> str:
    """Call the Anthropic API with the given system and user prompts."""
    client = get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text.strip()
