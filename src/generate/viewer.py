"""Deterministic JSON model -> standalone interactive HTML class diagram.

Usage: python generate/viewer.py model.json [out.html] [--title "..."]

The page follows the Visual Studio class-designer presentation: each class has a
collapsible body and separate collapsible Attributes and Operations compartments,
associations carry role labels and end multiplicities, and generalizations are
drawn with the superclass above the subclass. Clicking a class, a relationship,
or a package opens a side panel with the definition or description and the
source milestones recorded in the JSON. No network access; one file.

Layout is computed in the page from the model alone, so the same JSON always
gives the same picture. Nothing here touches the JSON or the scoring.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "viewer_template.html"
MILESTONES = HERE.parent / "data" / "milestones.json"


def milestone_names() -> dict:
    if not MILESTONES.exists():
        return {}
    return {str(m["number"]): m["name"] for m in json.loads(MILESTONES.read_text(encoding="utf-8"))}


def build(model: dict, title: str) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    # "</script" inside a string would end the script block; escape it
    dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return (html.replace("__TITLE__", title)
                .replace("__MODEL_JSON__", dump(model))
                .replace("__MILESTONES_JSON__", dump(milestone_names()))
                .replace("__TITLE_JSON__", dump(title)))


def write(model: dict, out: Path, title: str) -> None:
    out.write_text(build(model, title), encoding="utf-8")


def main():
    args = sys.argv[1:]
    title = "A-CDM class model"
    if "--title" in args:
        i = args.index("--title")
        title = args[i + 1]
        del args[i:i + 2]
    src = Path(args[0])
    out = Path(args[1]) if len(args) > 1 else src.with_suffix(".html")
    write(json.loads(src.read_text(encoding="utf-8")), out, title)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
