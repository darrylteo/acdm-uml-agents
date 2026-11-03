"""Control: the model implied by the scaffold alone, with no LLM call.

Emits exactly what a reader could produce from src/prompts/scaffold.md and the
manual's abbreviation table without modelling anything: the six packages, one
class per abbreviation placed by the crude rule its expansion suggests, a
default stereotype, no attributes, no operations, no relationships. It holds no
member and no link, so its recall is bounded by the share of the inventory's
claims that are classes or enumerations (paper_numbers.py computes that bound).

  python src/evaluate/scaffold_only.py
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC / "generate"))
from common import MODEL_SCHEMA, SCAFFOLD, validate  # noqa: E402
from render import render  # noqa: E402

OUT = SRC / "runs" / "control_scaffold_only"

# Placement rule: crude and stated, not tuned. Time quantities to Timings,
# message-like terms to Messages, systems to Systems, parties to Stakeholders,
# everything else to Flights.
TIME_WORDS = ("Time", "Turn-round")
MESSAGE_WORDS = ("message", "Message", "Information message")
SYSTEM_WORDS = ("System", "Platform", "Centre", "Radar", "Display")
PARTY_WORDS = ("Operator", "Handler", "Control", "Provider", "Tower", "Unit", "Committee")


def packages_from_scaffold() -> list[dict]:
    """Read the six package names and one-liners straight out of the scaffold."""
    text = SCAFFOLD.read_text(encoding="utf-8")
    block = text.split("## Packages", 1)[1].split("##", 1)[0]
    out = []
    for m in re.finditer(r"^- `([A-Za-z]+)`: (.+)$", block, re.M):
        out.append({"name": m.group(1), "description": m.group(2).strip()})
    return out


def classify(expansion: str) -> tuple[str, str]:
    if any(w in expansion for w in MESSAGE_WORDS):
        return "Messages", "boundary"
    if any(w in expansion for w in SYSTEM_WORDS):
        return "Systems", "boundary"
    if any(w in expansion for w in PARTY_WORDS):
        return "Stakeholders", "entity"
    if any(w in expansion for w in TIME_WORDS):
        return "Timings", "entity"
    return "Flights", "entity"


def build() -> dict:
    abbr = json.loads((SRC / "evaluate" / "abbreviations.json").read_text(encoding="utf-8"))
    terms = dict(abbr["abbreviations"]) | dict(abbr["document_defined"])
    classes = []
    for acronym, expansion in sorted(terms.items()):
        package, stereotype = classify(expansion)
        classes.append({
            "name": "".join(w for w in re.sub(r"[^A-Za-z ]", " ", expansion).title().split()),
            "package": package,
            "stereotype": stereotype,
            "definition": expansion,
            "source_milestones": [],
            "attributes": [],
            "operations": [],
        })
    return {"packages": packages_from_scaffold(), "classes": classes,
            "enumerations": [], "relationships": [], "unmodelled": []}


def main() -> None:
    model = build()
    errs = validate(model, MODEL_SCHEMA)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "model.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
    (OUT / "model.puml").write_text(render(model), encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps({
        "condition": "control_scaffold_only", "ok": not errs, "validation_errors": errs,
        "note": "Deterministic. No LLM call, no cost, no latency.",
        "total_input_tokens": 0, "total_output_tokens": 0, "total_cost_usd": 0.0,
        "total_duration_ms": 0}, indent=2), encoding="utf-8")
    print(f"{len(model['classes'])} classes, validation {'ok' if not errs else errs[:3]} -> {OUT}")


if __name__ == "__main__":
    main()
