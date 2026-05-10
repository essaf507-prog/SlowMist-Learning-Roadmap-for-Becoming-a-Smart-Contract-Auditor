"""Semantic-friendly text chunking for long academic PDFs."""

from __future__ import annotations

import re
from dataclasses import dataclass


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(])")


@dataclass(frozen=True)
class TextChunk:
    """A chunk that can be sent to an LLM for semantic style analysis."""

    chunk_id: int
    text: str
    token_estimate: int


def estimate_tokens(text: str) -> int:
    """Estimate tokens without a tokenizer; English prose averages about 4 chars/token."""
    return max(1, len(text) // 4)


def split_into_chunks(text: str, max_tokens: int = 900, overlap_tokens: int = 120) -> list[TextChunk]:
    """Split text into overlapping chunks while preserving sentence boundaries."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if overlap_tokens < 0 or overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be non-negative and smaller than max_tokens")

    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n{2,}", text) if paragraph.strip()]
    units: list[str] = []
    for paragraph in paragraphs:
        sentences = _SENTENCE_SPLIT_RE.split(paragraph)
        units.extend(sentence.strip() for sentence in sentences if sentence.strip())

    chunks: list[TextChunk] = []
    current: list[str] = []
    current_tokens = 0

    for unit in units:
        unit_tokens = estimate_tokens(unit)
        if current and current_tokens + unit_tokens > max_tokens:
            chunk_text = " ".join(current).strip()
            chunks.append(TextChunk(len(chunks) + 1, chunk_text, estimate_tokens(chunk_text)))
            current = _tail_overlap(current, overlap_tokens)
            current_tokens = estimate_tokens(" ".join(current)) if current else 0
        current.append(unit)
        current_tokens += unit_tokens

    if current:
        chunk_text = " ".join(current).strip()
        chunks.append(TextChunk(len(chunks) + 1, chunk_text, estimate_tokens(chunk_text)))

    return chunks


def _tail_overlap(units: list[str], overlap_tokens: int) -> list[str]:
    if overlap_tokens == 0:
        return []
    selected: list[str] = []
    total = 0
    for unit in reversed(units):
        total += estimate_tokens(unit)
        selected.append(unit)
        if total >= overlap_tokens:
            break
    return list(reversed(selected))
