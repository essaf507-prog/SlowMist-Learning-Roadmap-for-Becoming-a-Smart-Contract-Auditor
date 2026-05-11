"""Runtime configuration for OpenAI-compatible API access."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiConfig:
    """Configuration required by the chat-completion API client."""

    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    timeout_seconds: int = 120

    @classmethod
    def from_env(cls) -> "ApiConfig":
        """Build configuration from environment variables."""
        api_key = os.getenv("AI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("AI_API_KEY is required. Copy .env.example and export the variables first.")

        return cls(
            api_key=api_key,
            base_url=os.getenv("AI_API_BASE_URL", cls.base_url).rstrip("/"),
            model=os.getenv("AI_MODEL", cls.model),
            timeout_seconds=int(os.getenv("AI_TIMEOUT_SECONDS", str(cls.timeout_seconds))),
        )
