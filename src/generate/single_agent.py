"""Single-agent condition: one invocation with the union of the role prompts.

With scaffold=False this is the no-scaffold control: the same document and the
same schema, with the scaffold and the single-agent role prompt both replaced by
the three-sentence no_scaffold.md.
"""
import json
from pathlib import Path

from client import ClaudeCLI
from common import MODEL_SCHEMA, ROLES, build_user_message, structural_checks, validate
from render import render
from viewer import write as write_viewer


def run(run_dir: Path, client: ClaudeCLI, scaffold: bool = True) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    role = "single_agent.md" if scaffold else "no_scaffold.md"
    msg = build_user_message(scaffold=scaffold)
    res = client.call(ROLES / role, msg, MODEL_SCHEMA, run_dir, "step1_single")
    manifest = {"condition": "single" if scaffold else "noscaffold",
                "model_alias": client.model, "effort": client.effort,
                "steps": [res.__dict__ | {"output": None}], "ok": res.ok}
    if res.ok:
        model = res.output
        manifest["validation_errors"] = validate(model, MODEL_SCHEMA)
        manifest["structural_problems"] = structural_checks(model)
        manifest["unmodelled"] = model.get("unmodelled", [])
        (run_dir / "model.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
        (run_dir / "model.puml").write_text(render(model), encoding="utf-8")
        write_viewer(model, run_dir / "model.html", f"A-CDM class model ({run_dir.name})")
    manifest["total_input_tokens"] = res.input_tokens
    manifest["total_output_tokens"] = res.output_tokens
    manifest["total_cost_usd"] = res.cost_usd
    manifest["total_duration_ms"] = res.duration_ms
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
