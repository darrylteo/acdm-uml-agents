"""Deterministic JSON model -> Python class stubs.

Usage: python generate/render_code.py model.json [out.py]
       python generate/render_code.py --all      (every scored run and the scaffold-only control; writes model.py
                                                   beside each model.json, then compiles, imports, and instantiates it)

Rendering choices (a demonstration that the model is a code skeleton, never scored):
  - enumerations become Enum classes, literals normalised to UPPER_SNAKE with the document's spelling as the value;
  - classes become dataclasses, defined after their superclasses, generalizations as Python bases;
  - every attribute becomes a typed field defaulting to None; UML primitives map to Python types
    (String str, DateTime datetime, Duration timedelta, Boolean bool, Integer int, Real float),
    any other type is the class or enumeration of that name, as a postponed annotation;
  - every operation becomes a typed method whose docstring is the model's description (the rule or formula
    the document gives) and whose body raises NotImplementedError;
  - associations, aggregations, compositions, and dependencies are listed in the class docstring, since the
    scaffold already requires a typed attribute for every reference that holds information.
Anything the output cannot express is reported, never repaired in the model: a generalization cycle or a
base that would give no consistent method resolution order drops that base; a repeated member name is
suffixed; an identifier that is not valid Python is rewritten.
"""
import json
import keyword
import re
import sys
from pathlib import Path

PRIMITIVES = {
    "string": "str", "str": "str", "text": "str", "char": "str",
    "datetime": "datetime", "date": "date", "time": "time", "timestamp": "datetime",
    "duration": "timedelta", "timedelta": "timedelta",
    "boolean": "bool", "bool": "bool",
    "integer": "int", "int": "int", "long": "int", "natural": "int",
    "real": "float", "float": "float", "double": "float", "decimal": "float", "number": "float",
    "void": "None", "none": "None", "": "None",
}
LIST_RE = re.compile(r"^(?:List|Set|Collection|Sequence|Array)\s*[<\[]\s*(.+?)\s*[>\]]$|^(.+?)\s*\[\s*(?:\*|\d*\.\.\*|)\s*\]$", re.I)


def ident(name: str, upper: bool = False) -> str:
    s = re.sub(r"\W+", "_", str(name).strip()).strip("_") or "_"
    if upper:
        s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s).upper()
    if s[0].isdigit():
        s = "_" + s
    return s + "_" if keyword.iskeyword(s) or s in ("None", "True", "False") else s


def pytype(t: str | None, known: set[str]) -> str:
    t = (t or "").strip()
    m = LIST_RE.match(t)
    if m:
        return f"list[{pytype(m.group(1) or m.group(2), known)}]"
    if t.lower() in PRIMITIVES:
        return PRIMITIVES[t.lower()]
    return ident(t)


def order_classes(classes: dict[str, dict], parents: dict[str, list[str]], notes: list[str]) -> list[str]:
    """Superclasses first; a base that would close a cycle is dropped and reported."""
    done, out = set(), []

    def visit(c: str, path: tuple[str, ...]):
        if c in done:
            return
        for p in list(parents.get(c, [])):
            if p in path or p == c:
                parents[c].remove(p)
                notes.append(f"generalization cycle: dropped base {p} of {c}")
            else:
                visit(p, path + (c,))
        done.add(c)
        out.append(c)

    for c in sorted(classes):
        visit(c, ())
    return out


def consistent_bases(bases: list[str], parents: dict[str, list[str]]) -> list[str]:
    """Drop a base that is already an ancestor of another listed base (Python rejects that MRO)."""
    def ancestors(c, seen=None):
        seen = set() if seen is None else seen
        for p in parents.get(c, []):
            if p not in seen:
                seen.add(p)
                ancestors(p, seen)
        return seen
    return [b for b in bases if not any(b in ancestors(o) for o in bases if o != b)]


def render_code(model: dict, title: str = "") -> tuple[str, list[str]]:
    notes: list[str] = []
    classes = {c["name"]: c for c in model.get("classes", [])}
    enums = {e["name"]: e for e in model.get("enumerations", []) if e["name"] not in classes}
    known = set(classes) | set(enums)
    parents: dict[str, list[str]] = {c: [] for c in classes}
    links: dict[str, list[str]] = {c: [] for c in classes}
    for r in model.get("relationships", []):
        s, t = r.get("source"), r.get("target")
        if r.get("type") == "generalization":
            if s in classes and t in classes:
                if t not in parents[s]:
                    parents[s].append(t)
            else:
                notes.append(f"generalization to or from an undeclared class: {s} -> {t}")
        elif s in links:
            label = f" '{r['label']}'" if r.get("label") else ""
            mult = f" [{r.get('target_multiplicity')}]" if r.get("target_multiplicity") else ""
            links[s].append(f"{r.get('type')}{label} -> {t}{mult}")

    lines = [f'"""Class stubs rendered from {title or "model.json"} by src/generate/render_code.py; do not edit by hand."""',
             "from __future__ import annotations", "",
             "from dataclasses import dataclass", "from datetime import date, datetime, time, timedelta",
             "from enum import Enum", "", ""]
    for name in sorted(enums):
        e = enums[name]
        lines.append(f"class {ident(name)}(Enum):")
        seen = set()
        for lit in e.get("literals", []) or []:
            k = ident(lit, upper=True)
            while k in seen:
                k += "_"
            seen.add(k)
            lines.append(f"    {k} = {json.dumps(str(lit), ensure_ascii=False)}")
        if not seen:
            lines.append("    pass")
        lines += ["", ""]

    for name in order_classes(classes, parents, notes):
        c = classes[name]
        bases = consistent_bases(parents[name], parents)
        for dropped in set(parents[name]) - set(bases):
            notes.append(f"redundant base dropped for a consistent MRO: {dropped} of {name}")
        head = f"({', '.join(ident(b) for b in bases)})" if bases else ""
        lines += ["@dataclass", f"class {ident(name)}{head}:"]
        doc = [c.get("definition", "").strip() or name,
               f"Package {c.get('package', '')}, stereotype {c.get('stereotype', '')}, milestones {c.get('source_milestones', [])}."]
        doc += [f"Relationship: {x}" for x in links[name]]
        lines.append('    """' + "\n\n    ".join(d.replace('"""', "'''").replace("\\", "\\\\") for d in doc) + '\n    """')
        used: set[str] = set()
        for a in c.get("attributes", []):
            n = ident(a["name"])
            if n in used:
                notes.append(f"repeated attribute {a['name']} on {name}")
                n += "_2"
            used.add(n)
            lines.append(f"    {n}: {pytype(a.get('type'), known)} | None = None")
        for o in c.get("operations", []):
            n = ident(o["name"])
            if n in used:
                notes.append(f"repeated member name {o['name']} on {name}")
                n += "_2"
            used.add(n)
            params = ["self"] + [f"{ident(p['name'])}: {pytype(p.get('type'), known)}" for p in o.get("parameters", [])]
            ret = pytype(o.get("returns"), known)
            desc = (o.get("description") or "").replace("\\", "\\\\").replace('"""', "'''")
            lines += ["", f"    def {n}({', '.join(params)}) -> {ret}:", f'        """{desc}"""', "        raise NotImplementedError"]
        if not c.get("attributes") and not c.get("operations"):
            lines.append("    pass")
        lines += ["", ""]
    undeclared = sorted({t for c in classes.values() for t in
                         [a.get("type") for a in c.get("attributes", [])] +
                         [p.get("type") for o in c.get("operations", []) for p in o.get("parameters", [])] +
                         [o.get("returns") for o in c.get("operations", [])]
                         if t and not LIST_RE.match(t.strip()) and t.strip().lower() not in PRIMITIVES and t.strip() not in known})
    if undeclared:
        notes.append(f"types used but not declared ({len(undeclared)}): {', '.join(undeclared)}")
    return "\n".join(lines).rstrip() + "\n", notes


def check(py: Path) -> str:
    """Compile, import, and instantiate every dataclass with no arguments; returns '' when all succeed."""
    import dataclasses
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"stubs_{abs(hash(str(py)))}", py)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # dataclasses resolves the module through sys.modules
    try:
        spec.loader.exec_module(mod)
        n = 0
        for obj in vars(mod).values():
            if isinstance(obj, type) and dataclasses.is_dataclass(obj) and obj.__module__ == mod.__name__:
                obj()
                n += 1
        return "" if n else "no classes"
    except Exception as e:  # noqa: BLE001 - report any failure as the check's result
        return f"{type(e).__name__}: {e}"


def main():
    src = Path(__file__).resolve().parents[1]
    if sys.argv[1:] == ["--all"]:
        paths = sorted(src.glob("runs/*/run_*/model.json")) + sorted(src.glob("runs/control_scaffold_only/model.json"))
        ok = 0
        for p in paths:
            code, notes = render_code(json.loads(p.read_text(encoding="utf-8")), str(p.relative_to(src)).replace("\\", "/"))
            out = p.with_name("model.py")
            out.write_text(code, encoding="utf-8")
            err = check(out)
            ok += not err
            print(f"{str(p.parent.relative_to(src)):32} {code.count(chr(10) + 'class '):3} classes  "
                  f"{'ok' if not err else 'FAIL ' + err}" + (f"  ({len(notes)} notes)" if notes else ""))
            for n in notes:
                print(f"    note: {n}")
        print(f"{ok} of {len(paths)} models compile, import, and instantiate")
        sys.exit(0 if ok == len(paths) else 1)
    model = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    code, notes = render_code(model, Path(sys.argv[1]).name)
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(code, encoding="utf-8")
    else:
        sys.stdout.write(code)
    for n in notes:
        print(f"note: {n}", file=sys.stderr)


if __name__ == "__main__":
    main()
