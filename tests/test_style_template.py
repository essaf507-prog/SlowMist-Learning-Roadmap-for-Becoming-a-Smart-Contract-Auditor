import json

from paper_style_ai.style_template import load_template, render_template_for_prompt


def test_load_template_accepts_analysis_payload(tmp_path):
    template = {"style_name": "test", "global_principles": ["clear claims"]}
    path = tmp_path / "analysis.json"
    path.write_text(json.dumps({"template": template}), encoding="utf-8")

    loaded = load_template(path)

    assert loaded == template
    assert "clear claims" in render_template_for_prompt(loaded)
