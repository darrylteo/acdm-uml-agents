import json
from pathlib import Path

import jsonschema

SRC = Path(__file__).resolve().parents[1]
DOCUMENT = SRC / "data" / "document.txt"
SCAFFOLD = SRC / "prompts" / "scaffold.md"
MODEL_SCHEMA = SRC / "schema" / "schema.json"
ANALYST_SCHEMA = SRC / "schema" / "analyst_schema.json"
ATTRIBUTE_SCHEMA = SRC / "schema" / "attribute_delta.json"
OPERATION_SCHEMA = SRC / "schema" / "operation_delta.json"
RELATIONSHIP_SCHEMA = SRC / "schema" / "relationship_delta.json"
ROLES = SRC / "prompts" / "roles"


def load_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def build_user_message(brief: dict | None = None, model: dict | None = None,
                       task: str = "Return the full model as JSON conforming to the schema.",
                       scaffold: bool = True) -> str:
    parts = []
    if scaffold:
        parts.append("# Scaffold\n\n" + load_text(SCAFFOLD).strip())
    parts.append("# Document\n\n" + load_text(DOCUMENT).strip())
    if brief is not None:
        parts.append("# Analyst brief\n\n```json\n" + json.dumps(brief, separators=(",", ":")) + "\n```")
    if model is not None:
        parts.append("# Current model\n\n```json\n" + json.dumps(model, separators=(",", ":")) + "\n```")
    parts.append("# Task\n\n" + task)
    return "\n\n".join(parts) + "\n"


def validate(obj: dict, schema_path: Path) -> list[str]:
    schema = json.loads(load_text(schema_path))
    v = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(str(x) for x in e.path)}: {e.message}" for e in v.iter_errors(obj)]


def class_names(model: dict) -> set[str]:
    return {c["name"] for c in model.get("classes", [])}


def structural_checks(model: dict) -> list[str]:
    """Cheap semantic checks the schema cannot express."""
    problems = []
    names = [c["name"] for c in model.get("classes", [])]
    all_names = names + [e["name"] for e in model.get("enumerations", [])]
    dups = {n for n in all_names if all_names.count(n) > 1}
    if dups:
        problems.append(f"duplicate class/enumeration names: {sorted(dups)}")
    pkgs = {p["name"] for p in model.get("packages", [])}
    for c in model.get("classes", []):
        if c["package"] not in pkgs:
            problems.append(f"class {c['name']} in undeclared package {c['package']}")
    known = set(names) | {e["name"] for e in model.get("enumerations", [])}
    for r in model.get("relationships", []):
        for end in ("source", "target"):
            if r[end] not in known:
                problems.append(f"relationship {r['type']} {r['source']}->{r['target']}: unknown {end}")
    # generalization cycles
    parent = {}
    for r in model.get("relationships", []):
        if r["type"] == "generalization":
            parent.setdefault(r["source"], set()).add(r["target"])
    for start in parent:
        seen, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n == start and seen:
                problems.append(f"generalization cycle through {start}")
                break
            if n in seen:
                continue
            seen.add(n)
            stack.extend(parent.get(n, ()))
    return problems


# --- delta merging -------------------------------------------------------
# The attribute, operation, and relationship agents return only what they add.
# Merging is deterministic, so no intermediate agent can alter the class set.
# Anything addressed to a class that does not exist is dropped and reported.

def _index(model: dict) -> dict:
    return {c["name"]: c for c in model.get("classes", [])}


def merge_attributes(model: dict, delta: dict) -> list[str]:
    """Add attributes in place. Returns diagnostics."""
    problems, by_name = [], _index(model)
    for entry in delta.get("classes", []):
        cls = by_name.get(entry["name"])
        if cls is None:
            problems.append(f"attributes for unknown class {entry['name']!r} dropped")
            continue
        have = {a["name"] for a in cls["attributes"]}
        for a in entry.get("attributes", []):
            if a["name"] in have:
                problems.append(f"duplicate attribute {entry['name']}.{a['name']} dropped")
                continue
            cls["attributes"].append(a)
            have.add(a["name"])
    return problems


def merge_operations(model: dict, delta: dict) -> list[str]:
    problems, by_name = [], _index(model)
    for entry in delta.get("classes", []):
        cls = by_name.get(entry["name"])
        if cls is None:
            problems.append(f"operations for unknown class {entry['name']!r} dropped")
            continue
        have = {o["name"] for o in cls["operations"]}
        for o in entry.get("operations", []):
            if o["name"] in have:
                problems.append(f"duplicate operation {entry['name']}.{o['name']} dropped")
                continue
            cls["operations"].append(o)
            have.add(o["name"])
    return problems


def merge_relationships(model: dict, delta: dict) -> list[str]:
    problems = []
    known = class_names(model) | {e["name"] for e in model.get("enumerations", [])}
    seen = {(r["type"], r["source"], r["target"]) for r in model.get("relationships", [])}
    for r in delta.get("relationships", []):
        missing = [x for x in (r["source"], r["target"]) if x not in known]
        if missing:
            problems.append(f"relationship {r['source']}->{r['target']} references unknown {missing} dropped")
            continue
        key = (r["type"], r["source"], r["target"])
        if key in seen:
            problems.append(f"duplicate relationship {key} dropped")
            continue
        model["relationships"].append(r)
        seen.add(key)
    return problems
