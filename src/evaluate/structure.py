"""Reference-free structural properties of generated models.

Each property operationalises one structural rule of the scaffold, whose own
provenance is Larman, Fowler, or the manual, so the check needs no reference
model and no grader. A property must vary within a configuration, and it must be
invariant across the designs the scaffold permits (one class per abbreviation,
one per event with a prefix attribute, or a single TimeQuantity; the flight
reaching the quantity by typed attribute or by association).

Columns
  hoist      S1  shared members declared once on the parent / members shared by
                 two or more siblings (scaffold line 11; Camara et al. 2023 F17,
                 "does not factor out the common attributes of subclasses")
  redecl     S2  members declared on both a parent and one of its children
                 (line 11)
  leak       S3  the manual's time quantities (abbreviation table, expansions
                 ending in "Time") held as datetime or duration primitives on a
                 class outside Timings (rule 44: each time quantity is a class).
                 A tolerance or offset applied to a quantity is a rule parameter,
                 not the quantity, and is not counted
  complete   S4  Timings classes carrying value, originator, and time of update,
                 own or inherited / Timings classes (rule 44 names the three)
  history    S5  links from a non-Timings class to a Timings class whose
                 Timings end is many / all such links (rule 44: every successive
                 value is kept; an update appends)

Usage: python src/evaluate/structure.py src/runs/multi/run_*/model.json src/runs/single/run_*/model.json [--md] [--json PATH]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from match import ABBR, normalise, tokens  # noqa: E402

TIME_PRIMITIVES = {"datetime", "date", "time", "timestamp", "localdatetime", "instant", "duration"}
TIME_QUANTITIES = {k: set(tokens(v)) for k, v in ABBR.items() if v.lower().endswith("time")}
VALUE_WORDS = {"value", "time"}                                    # rule 44: "every successive value"
ORIGIN_WORDS = {"originator", "origin", "source", "provider", "partner", "by"}   # "with its originator"
UPDATE_WORDS = {"update", "updated", "recorded", "timestamp", "logged", "set"}   # "and time of update"
PARAMETER_WORDS = {"tolerance", "offset", "window", "threshold", "margin", "deviation"}  # a rule's parameter about a quantity, not its value
COLS = ["classes", "attrs", "ops", "hoist", "redecl", "leak", "complete", "history"]


def base_type(t: str) -> str:
    m = re.fullmatch(r"(?:List|Set|Collection|Array)\s*<\s*(.+?)\s*>", t.strip())
    return m.group(1) if m else re.sub(r"\[.*\]$", "", t.strip())


def is_time_quantity(name: str) -> str | None:
    """The abbreviation whose expansion the attribute name contains, if any."""
    bag = set(tokens(name))
    if bag & PARAMETER_WORDS:
        return None
    for abbr, words in TIME_QUANTITIES.items():
        if words <= bag:
            return abbr
    return None


def _members(c: dict) -> set[tuple[str, str]]:
    return ({("a", normalise(a["name"], "attribute")) for a in c["attributes"]}
            | {("o", normalise(o["name"], "operation")) for o in c["operations"]})


def structure(model: dict) -> dict:
    cls = {c["name"]: c for c in model["classes"]}
    parent = {r["source"]: r["target"] for r in model["relationships"] if r["type"] == "generalization"}
    children: dict[str, list[str]] = {}
    for s, t in parent.items():
        children.setdefault(t, []).append(s)

    # S1, S2
    hoisted = unhoisted = redeclared = 0
    for p, kids in children.items():
        if len(kids) < 2 or p not in cls:
            continue
        pm = _members(cls[p])
        seen: dict[tuple[str, str], int] = {}
        for k in kids:
            for m in _members(cls.get(k, {"attributes": [], "operations": []})):
                seen[m] = seen.get(m, 0) + 1
                redeclared += m in pm
        unhoisted += sum(1 for m, n in seen.items() if n >= 2 and m not in pm)
        hoisted += len(pm)

    # S3
    leaks = []
    for c in model["classes"]:
        if c["package"] == "Timings":
            continue
        for a in c["attributes"]:
            if base_type(a["type"]).lower() in TIME_PRIMITIVES and is_time_quantity(a["name"]):
                leaks.append(f'{c["name"]}.{a["name"]}')

    # S4
    def inherited_attrs(n: str) -> list[dict]:
        out, seen_n = [], set()
        while n in cls and n not in seen_n:
            seen_n.add(n)
            out += cls[n]["attributes"]
            n = parent.get(n, "")
        return out

    def has(attrs: list[dict], words: set[str]) -> bool:
        return any(set(tokens(a["name"])) & words for a in attrs)

    timings = [c["name"] for c in model["classes"] if c["package"] == "Timings"]
    complete = sum(1 for n in timings
                   if (at := inherited_attrs(n)) and has(at, VALUE_WORDS) and has(at, ORIGIN_WORDS) and has(at, UPDATE_WORDS))

    # S5
    many = links = 0
    for r in model["relationships"]:
        if r["type"] == "generalization":
            continue
        s, t = r["source"], r["target"]
        if s in cls and t in cls and (cls[s]["package"] == "Timings") != (cls[t]["package"] == "Timings"):
            end = r["target_multiplicity"] if cls[t]["package"] == "Timings" else r["source_multiplicity"]
            links += 1
            many += "*" in end

    return {
        "classes": len(cls),
        "attrs": sum(len(c["attributes"]) for c in model["classes"]),
        "ops": sum(len(c["operations"]) for c in model["classes"]),
        "hoist": (hoisted, hoisted + unhoisted),
        "redecl": redeclared,
        "leak": leaks,
        "complete": (complete, len(timings)),
        "history": (many, links),
    }


def cell(v) -> str:
    if isinstance(v, tuple):
        n, d = v
        return f"{n}/{d}" + (f" ({n / d:.2f})" if d else "")
    return str(len(v)) if isinstance(v, list) else str(v)


def main():
    md = "--md" in sys.argv
    out = Path(sys.argv[sys.argv.index("--json") + 1]) if "--json" in sys.argv else None
    paths = [Path(a) for a in sys.argv[1:] if not a.startswith("--") and (out is None or Path(a) != out)]
    rows = [(p, structure(json.loads(p.read_text(encoding="utf-8")))) for p in paths]
    label = lambda p: f"{p.parent.parent.name}/{p.parent.name}" if p.name == "model.json" else p.stem
    if md:
        print("| run | " + " | ".join(COLS) + " |")
        print("|---|" + "---|" * len(COLS))
        for p, r in rows:
            print(f"| {label(p)} | " + " | ".join(cell(r[c]) for c in COLS) + " |")
    else:
        w = max(len(label(p)) for p, _ in rows) if rows else 4
        print(f"{'run':<{w}} " + " ".join(f"{c:>12}" for c in COLS))
        for p, r in rows:
            print(f"{label(p):<{w}} " + " ".join(f"{cell(r[c]):>12}" for c in COLS))
    for p, r in rows:
        if r["leak"]:
            print(f"  {label(p)} leak: {', '.join(r['leak'])}")
    if out:
        out.write_text(json.dumps({label(p): r for p, r in rows}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
