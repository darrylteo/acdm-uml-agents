"""Multi-agent condition: six agents in sequence, then a deterministic render.

The class agent and the reviewer return whole models. The attribute, operation,
and relationship agents return only what they add, which is merged in code, so
no intermediate agent can alter the class set: the delta schemas give it no way
to express such a change. Every intermediate artifact is persisted.
"""
import json
from pathlib import Path

from client import ClaudeCLI
from common import (ANALYST_SCHEMA, ATTRIBUTE_SCHEMA, MODEL_SCHEMA, OPERATION_SCHEMA,
                    RELATIONSHIP_SCHEMA, ROLES, build_user_message, merge_attributes,
                    merge_operations, merge_relationships, structural_checks, validate)
from render import render
from viewer import write as write_viewer

# (step name, role file, schema, merge function; None means the step returns a whole model)
STEPS = [
    ("analyst", "analyst.md", ANALYST_SCHEMA, None),
    ("class", "class_agent.md", MODEL_SCHEMA, None),
    ("attribute", "attribute_agent.md", ATTRIBUTE_SCHEMA, merge_attributes),
    ("operation", "operation_agent.md", OPERATION_SCHEMA, merge_operations),
    ("relationship", "relationship_agent.md", RELATIONSHIP_SCHEMA, merge_relationships),
    ("reviewer", "reviewer.md", MODEL_SCHEMA, None),
]

TASKS = {
    "analyst": "Return the brief as JSON conforming to the schema, one entry per milestone, all sixteen.",
    "class": "Return the full model as JSON conforming to the schema, with classes and enumerations filled in and attributes, operations, and relationships left empty.",
    "attribute": "Return only the attributes to add, as JSON conforming to the schema.",
    "operation": "Return only the operations to add, as JSON conforming to the schema.",
    "relationship": "Return only the relationships to add, as JSON conforming to the schema.",
    "reviewer": "Return the full corrected model as JSON conforming to the schema.",
}


def run(run_dir: Path, client: ClaudeCLI, include_analyst: bool = True) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"condition": "multi", "model_alias": client.model, "effort": client.effort,
                "steps": [], "ok": True, "diagnostics": []}
    brief, model = None, None
    totals = {"input": 0, "output": 0, "cost": 0.0, "ms": 0}

    for i, (name, role_file, schema, merge) in enumerate(STEPS, start=1):
        if name == "analyst" and not include_analyst:
            continue
        tag = f"step{i}_{name}"
        msg = build_user_message(brief=brief, model=model, task=TASKS[name])
        res = client.call(ROLES / role_file, msg, schema, run_dir, tag)
        manifest["steps"].append(res.__dict__ | {"output": None, "step": name})
        for k, v in (("input", res.input_tokens), ("output", res.output_tokens),
                     ("cost", res.cost_usd), ("ms", res.duration_ms)):
            totals[k] += v
        if not res.ok:
            manifest["ok"] = False
            manifest["failed_step"] = name
            break

        errs = validate(res.output, schema)
        if errs:
            manifest["diagnostics"].append({"step": name, "validation_errors": errs[:20]})

        if name == "analyst":
            brief = res.output
            continue

        if merge is None:
            model = res.output
        else:
            problems = merge(model, res.output)
            if problems:
                manifest["diagnostics"].append({"step": name, "merge_problems": problems})
            (run_dir / f"{tag}.merged.json").write_text(json.dumps(model, indent=2), encoding="utf-8")

    if manifest["ok"] and model is not None:
        manifest["validation_errors"] = validate(model, MODEL_SCHEMA)
        manifest["structural_problems"] = structural_checks(model)
        manifest["unmodelled"] = model.get("unmodelled", [])
        (run_dir / "model.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
        (run_dir / "model.puml").write_text(render(model), encoding="utf-8")
        write_viewer(model, run_dir / "model.html", f"A-CDM class model ({run_dir.name})")

    manifest["total_input_tokens"] = totals["input"]
    manifest["total_output_tokens"] = totals["output"]
    manifest["total_cost_usd"] = totals["cost"]
    manifest["total_duration_ms"] = totals["ms"]
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
