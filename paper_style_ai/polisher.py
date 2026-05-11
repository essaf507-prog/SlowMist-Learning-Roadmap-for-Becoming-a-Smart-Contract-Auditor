"""Polish user writing with a learned academic style template."""

from __future__ import annotations

import json


from paper_style_ai.config import ApiConfig
from paper_style_ai.style_template import render_template_for_prompt


POLISH_SYSTEM_PROMPT = """You are an academic writing editor.
Rewrite the user's draft in English using the supplied learned paper-style template.
Preserve the user's meaning, claims, and uncertainty. Do not invent citations, data, or results.
Return JSON with keys: polished_text, revision_notes, retained_claims, missing_evidence_warnings.
"""


class PaperPolisher:
    """Apply a learned template to a user draft through an OpenAI-compatible API."""

    def __init__(self, config: ApiConfig):
        self.config = config

    def polish(self, draft: str, template: dict) -> dict:
        """Return a polished document and revision notes."""
        prompt = f"""Learned style template:
{render_template_for_prompt(template)}

User draft to polish:
{draft}
"""
        try:
            import requests
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "requests is required for API calls. Install dependencies with: "
                "python -m pip install -r requirements.txt"
            ) from exc

        response = requests.post(
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": POLISH_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.15,
                "response_format": {"type": "json_object"},
            },
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"polished_text": content, "revision_notes": [], "retained_claims": [], "missing_evidence_warnings": []}
