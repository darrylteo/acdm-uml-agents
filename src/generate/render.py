"""Deterministic JSON model -> PlantUML class diagram.

Usage: python generate/render.py model.json [out.puml] [--per-package DIR]

Rendering choices (display only; the JSON is the scored artifact):
  - top-to-bottom layout, generalizations emitted first and grouped by
    superclass, so parents sit above children;
  - stereotype spot letter and colour (E/B/C) in addition to the guillemet text;
  - enumeration literals normalised to UPPER_SNAKE for display;
  - hover tooltips carrying the definition/description and the source
    milestones of every class, attribute, operation, and relationship
    (PlantUML [[{tooltip}]] syntax, which becomes <title> in SVG output);
  - a legend explaining arrow kinds and multiplicities;
  - optional one-diagram-per-package output for the paper figures.
"""
import json
import re
import sys
from pathlib import Path

ARROWS = {
    "generalization": "--|>",
    "association": "--",
    "aggregation": "o--",
    "composition": "*--",
    "dependency": "..>",
}

SPOT = {"entity": ("E", "#C8E6C9"), "boundary": ("B", "#BBDEFB"), "control": ("C", "#FFE0B2")}

HEADER = [
    "top to bottom direction",
    "skinparam classAttributeIconSize 0",
    "skinparam linetype ortho",
    "skinparam nodesep 30",
    "skinparam ranksep 40",
    "skinparam class {",
    "  BackgroundColor<<entity>> #F1F8E9",
    "  BackgroundColor<<boundary>> #E3F2FD",
    "  BackgroundColor<<control>> #FFF3E0",
    "  BorderColor #555555",
    "}",
    "skinparam packageStyle rectangle",
    "hide empty members",
]

LEGEND = [
    "legend right",
    "  |= Notation |= Meaning |",
    "  | A --|> B | A is a subclass of B (generalization); B drawn above A |",
    "  | A -- B | association; end labels are multiplicities (1, 0..1, *, 1..*) |",
    "  | A *-- B | composition: B is a part of A |",
    "  | A o-- B | aggregation: B is grouped by A |",
    "  | A ..> B | dependency: A uses B |",
    "  | (E) (B) (C) | entity, boundary, control (Jacobson) |",
    "endlegend",
]


def ident(name: str) -> str:
    """PlantUML identifiers cannot contain spaces or punctuation; quote if needed."""
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) else f'"{name}"'


def literal(lit: str) -> str:
    """UPPER_SNAKE for enumeration literals: 'Off-Block', 'offBlock', 'E-DPI' -> OFF_BLOCK, OFF_BLOCK, E_DPI."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", lit.strip())
    s = re.sub(r"[^A-Za-z0-9]+", "_", s)
    return s.strip("_").upper()


def tooltip(text: str, milestones=None) -> str:
    text = re.sub(r"[\[\]{}\n]", " ", text or "").strip()
    if milestones:
        text = f"{text} [M{', M'.join(str(m) for m in milestones)}]".strip()
    return f" [[{{{text}}}]]" if text else ""


def class_block(c: dict, indent: str = "  ") -> list[str]:
    spot, colour = SPOT.get(c["stereotype"], ("?", "#EEEEEE"))
    lines = [f"{indent}class {ident(c['name'])} << ({spot},{colour}) {c['stereotype']} >>"
             f"{tooltip(c.get('definition', ''), c.get('source_milestones'))} {{"]
    for a in c.get("attributes", []):
        lines.append(f"{indent}  +{a['name']} : {a['type']}{tooltip(a.get('description', ''))}")
    for op in c.get("operations", []):
        params = ", ".join(f"{p['name']} : {p['type']}" for p in op.get("parameters", []))
        lines.append(f"{indent}  +{op['name']}({params}) : {op.get('returns', 'void')}"
                     f"{tooltip(op.get('description', ''))}")
    lines.append(f"{indent}}}")
    return lines


def enum_block(e: dict, indent: str = "  ") -> list[str]:
    lines = [f"{indent}enum {ident(e['name'])}{tooltip('', e.get('source_milestones'))} {{"]
    for lit in e.get("literals", []):
        lines.append(f"{indent}  {literal(lit)}")
    lines.append(f"{indent}}}")
    return lines


def relationship_lines(rels: list[dict]) -> list[str]:
    out = []
    gens = [r for r in rels if r["type"] == "generalization"]
    others = [r for r in rels if r["type"] != "generalization"]
    # generalizations first, grouped by superclass, so the layout engine stacks each family
    for r in sorted(gens, key=lambda r: (r["target"], r["source"])):
        out.append(f"{ident(r['target'])} <|-- {ident(r['source'])}{tooltip('', r.get('source_milestones'))}")
    if gens and others:
        out.append("")
    for r in others:
        arrow = ARROWS.get(r["type"], "--")
        src, dst = ident(r["source"]), ident(r["target"])
        sm = f' "{r["source_multiplicity"]}"' if r.get("source_multiplicity") else ""
        tm = f'"{r["target_multiplicity"]}" ' if r.get("target_multiplicity") else ""
        label = f" : {r['label']}" if r.get("label") else ""
        out.append(f"{src}{sm} {arrow} {tm}{dst}{label}{tooltip('', r.get('source_milestones'))}")
    return out


def render(model: dict, title: str = "", legend: bool = True) -> str:
    lines = ["@startuml"]
    if title:
        lines.append(f"title {title}")
    lines += HEADER + [""]
    by_package: dict[str, list] = {}
    for p in model.get("packages", []):
        by_package.setdefault(p["name"], [])
    for c in model.get("classes", []):
        by_package.setdefault(c["package"], []).append(("class", c))
    for e in model.get("enumerations", []):
        by_package.setdefault(e["package"], []).append(("enum", e))

    for pkg, members in by_package.items():
        lines.append(f'package "{pkg}" {{')
        for kind, m in members:
            lines += enum_block(m) if kind == "enum" else class_block(m)
        lines.append("}")
        lines.append("")

    lines += relationship_lines(model.get("relationships", []))
    if legend:
        lines += [""] + LEGEND
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def render_package(model: dict, pkg: str) -> str:
    """One package with full members; classes elsewhere that it relates to are shown as stubs."""
    inside = {c["name"] for c in model["classes"] if c["package"] == pkg}
    inside |= {e["name"] for e in model.get("enumerations", []) if e["package"] == pkg}
    rels = [r for r in model.get("relationships", []) if r["source"] in inside or r["target"] in inside]
    outside = {r["source"] for r in rels} | {r["target"] for r in rels}
    outside -= inside
    lines = ["@startuml", f"title Package {pkg}"] + HEADER + ["", f'package "{pkg}" {{']
    for c in model["classes"]:
        if c["package"] == pkg:
            lines += class_block(c)
    for e in model.get("enumerations", []):
        if e["package"] == pkg:
            lines += enum_block(e)
    lines += ["}", ""]
    by_pkg: dict[str, list[str]] = {}
    for c in model["classes"]:
        if c["name"] in outside:
            by_pkg.setdefault(c["package"], []).append(f"  class {ident(c['name'])} <<{c['stereotype']}>>")
    for e in model.get("enumerations", []):
        if e["name"] in outside:
            by_pkg.setdefault(e["package"], []).append(f"  enum {ident(e['name'])}")
    for other, stubs in by_pkg.items():
        lines += [f'package "{other}" #EEEEEE {{'] + stubs + ["}", ""]
    lines += relationship_lines(rels) + ["@enduml"]
    return "\n".join(lines) + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = Path(args[0])
    out = Path(args[1]) if len(args) > 1 else src.with_suffix(".puml")
    model = json.loads(src.read_text(encoding="utf-8"))
    out.write_text(render(model), encoding="utf-8")
    print(f"wrote {out}")
    if "--per-package" in sys.argv:
        d = Path(sys.argv[sys.argv.index("--per-package") + 1])
        d.mkdir(parents=True, exist_ok=True)
        for p in model.get("packages", []):
            f = d / f"{re.sub(r'[^A-Za-z0-9]+', '_', p['name']).lower()}.puml"
            f.write_text(render_package(model, p["name"]), encoding="utf-8")
            print(f"wrote {f}")


if __name__ == "__main__":
    main()
