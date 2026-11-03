"""Reference-free structural lint of generated models.

Usage: python src/evaluate/lint.py src/runs/multi/run_*/model.json src/runs/single/run_*/model.json --md

Reports, per model, what can be checked without a reference model: schema-level
consistency and the shape of the model. It is a sanity check, not a quality measure.

Columns
  classes, enums, attrs, ops, rels   counts
  dup      names used by both a class and an enumeration, or twice
  dangling attribute, parameter, or return types naming no class, enum, or primitive
  badend   relationship endpoints naming no class or enumeration
  orphan   classes with no relationship at all
  empty    classes with neither attributes nor operations (typically leaf subclasses)
  gen/assoc/aggr/comp/dep   relationship type mix
  unmod    length of the unmodelled list
"""
import collections
import json
import re
import sys
from pathlib import Path

PRIMITIVES = {"string", "boolean", "bool", "datetime", "date", "time", "duration", "integer",
              "int", "float", "double", "real", "void", "number", "timestamp"}
COLS = ["classes", "enums", "attrs", "ops", "rels", "dup", "dangling", "badend", "orphan",
        "empty", "gen", "assoc", "aggr", "comp", "dep", "unmod"]


def base_type(t: str) -> str:
    """'List<Flight>' -> 'Flight', 'Flight[]' -> 'Flight', 'Flight[0..*]' -> 'Flight'."""
    m = re.fullmatch(r"(?:List|Set|Collection|Array)\s*<\s*(.+?)\s*>", t.strip())
    if m:
        return m.group(1)
    return re.sub(r"\[.*\]$", "", t.strip())


def lint(model: dict) -> dict:
    classes = model.get("classes", [])
    enums = model.get("enumerations", [])
    rels = model.get("relationships", [])
    cn = [c["name"] for c in classes]
    en = [e["name"] for e in enums]
    known = set(cn) | set(en)
    counts = collections.Counter(cn + en)
    types = ([a["type"] for c in classes for a in c["attributes"]]
             + [o["returns"] for c in classes for o in c["operations"]]
             + [p["type"] for c in classes for o in c["operations"] for p in o["parameters"]])
    dangling = sorted({t for t in types if base_type(t) not in known and base_type(t).lower() not in PRIMITIVES})
    ends = {r["source"] for r in rels} | {r["target"] for r in rels}
    kinds = collections.Counter(r["type"] for r in rels)
    return {
        "classes": len(cn), "enums": len(en),
        "attrs": sum(len(c["attributes"]) for c in classes),
        "ops": sum(len(c["operations"]) for c in classes),
        "rels": len(rels),
        "dup": sorted(n for n, k in counts.items() if k > 1),
        "dangling": dangling,
        "badend": sorted(ends - known),
        "orphan": sorted(n for n in cn if n not in ends),
        "empty": sum(1 for c in classes if not c["attributes"] and not c["operations"]),
        "gen": kinds["generalization"], "assoc": kinds["association"], "aggr": kinds["aggregation"],
        "comp": kinds["composition"], "dep": kinds["dependency"],
        "unmod": len(model.get("unmodelled", [])),
    }


def cell(v):
    return str(len(v)) if isinstance(v, list) else str(v)


def main():
    paths = [Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    md = "--md" in sys.argv
    rows = [(p, lint(json.loads(p.read_text(encoding="utf-8")))) for p in paths]
    label = lambda p: p.parent.name if p.name == "model.json" else p.stem
    if md:
        print("| run | " + " | ".join(COLS) + " |")
        print("|---|" + "---|" * len(COLS))
        for p, r in rows:
            print(f"| {label(p)} | " + " | ".join(cell(r[c]) for c in COLS) + " |")
    else:
        w = max(len(label(p)) for p, _ in rows) if rows else 4
        print(f"{'run':<{w}} " + " ".join(f"{c:>8}" for c in COLS))
        for p, r in rows:
            print(f"{label(p):<{w}} " + " ".join(f"{cell(r[c]):>8}" for c in COLS))
    for p, r in rows:
        for k in ("dup", "dangling", "badend", "orphan"):
            if r[k]:
                print(f"  {label(p)} {k}: {', '.join(r[k])}")


if __name__ == "__main__":
    main()
