"""LLM-backed semantic style analysis for academic writing chunks."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


from paper_style_ai.chunker import TextChunk
from paper_style_ai.config import ApiConfig


SYSTEM_PROMPT = """You are an academic writing style analyst.
Analyze elite English-language university paper excerpts. Focus on reusable writing conventions, not topic facts.
Return concise JSON with keys: rhetorical_moves, sentence_patterns, hedging_patterns, transition_patterns,
argumentation_style, citation_style, vocabulary_profile, reusable_templates, cautions.
"""


class SemanticAnalyzer:
    """Analyze chunk style through an OpenAI-compatible chat-completion API."""

    def __init__(self, config: ApiConfig):
        self.config = config

    def analyze_chunk(self, chunk: TextChunk) -> dict[str, Any]:
        """Analyze one text chunk and return structured style observations."""
        user_prompt = f"""Chunk ID: {chunk.chunk_id}
Estimated tokens: {chunk.token_estimate}

Text:
{chunk.text}
"""
        content = self._chat(user_prompt)
        return _parse_json(content, fallback={"chunk_id": chunk.chunk_id, "raw_analysis": content})

    def analyze_chunks(self, chunks: list[TextChunk], limit: int | None = None) -> list[dict[str, Any]]:
        """Analyze multiple chunks, optionally limiting calls for budget control."""
        selected = chunks[:limit] if limit else chunks
        return [self.analyze_chunk(chunk) for chunk in selected]

    def synthesize_style_template(self, analyses: list[dict[str, Any]]) -> dict[str, Any]:
        """Condense chunk-level analyses into a reusable polishing template."""
        prompt = f"""Synthesize the following style analyses into one reusable academic polishing template.
Return JSON with keys: style_name, global_principles, paragraph_structure, sentence_templates,
transition_bank, hedging_bank, evidence_integration, revision_checklist.

Analyses:
{json.dumps(analyses, ensure_ascii=False, indent=2)}
"""
        content = self._chat(prompt)
        return _parse_json(content, fallback={"raw_template": content})

    def _chat(self, user_prompt: str) -> str:
        url = f"{self.config.base_url}/chat/completions"
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        try:
            import requests
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "requests is required for API calls. Install dependencies with: "
                "python -m pip install -r requirements.txt"
            ) from exc

        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


def save_analysis(path: Path, chunks: list[TextChunk], analyses: list[dict[str, Any]], template: dict[str, Any]) -> None:
    """Persist chunk metadata, analyses, and final template as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "chunks": [asdict(chunk) for chunk in chunks],
        "analyses": analyses,
        "template": template,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _parse_json(content: str, fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return fallback
