"""OpenAI Chat Completions wrapper for message generation."""

from __future__ import annotations

import os

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"


def get_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def generate_message(prompt: str, model: str | None = None) -> tuple[str | None, str | None]:
    """
    Returns (message, error). error is None on success.
    """
    client = get_client()
    if client is None:
        return None, "Missing OPENAI_API_KEY in environment or .env file."

    model_name = model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write heartfelt wedding thank-you messages for Nigerian couples. "
                        "Output only the message body, no quotes or labels."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        text = (response.choices[0].message.content or "").strip()
        if not text:
            return None, "OpenAI returned an empty message."
        return text, None
    except Exception as exc:  # noqa: BLE001 — surface API errors in UI
        return None, str(exc)
