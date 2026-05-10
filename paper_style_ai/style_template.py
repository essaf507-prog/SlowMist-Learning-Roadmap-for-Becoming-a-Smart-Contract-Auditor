"""Load and render reusable academic style templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_template(path: Path) -> dict[str, Any]:
    """Load the template section from an analysis JSON file or a template-only JSON file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("template", data)


def render_template_for_prompt(template: dict[str, Any]) -> str:
    """Convert a structured template into prompt-ready guidance."""
    return json.dumps(template, ensure_ascii=False, indent=2)
