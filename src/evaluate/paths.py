"""Element paths: the one naming convention shared by the model-grader prompts,
the sample, and the grading pages.

  Class                       a class or an enumeration
  Class.attribute             an attribute
  Class.operation()           an operation
  Source->Target [type]       a relationship
"""

def rel_path(r: dict) -> str:
    return f"{r['source']}->{r['target']} [{r['type']}]"


def elements(model: dict) -> list[dict]:
    """Every gradable element with its path, kind, citations, and display content.
    Attributes and operations inherit their class's citations."""
    out = []
    for c in model.get("classes", []):
        cites = list(c.get("source_milestones", []))
        out.append({"path": c["name"], "kind": "class", "cites": cites, "class": c["name"],
                    "content": {"name": c["name"], "stereotype": c["stereotype"], "package": c["package"],
                                "definition": c["definition"]}})
        for a in c.get("attributes", []):
            out.append({"path": f"{c['name']}.{a['name']}", "kind": "attribute", "cites": cites, "class": c["name"],
                        "content": {"name": a["name"], "type": a["type"], "description": a["description"]}})
        for o in c.get("operations", []):
            params = ", ".join(f"{p['name']}: {p['type']}" for p in o.get("parameters", []))
            out.append({"path": f"{c['name']}.{o['name']}()", "kind": "operation", "cites": cites, "class": c["name"],
                        "content": {"signature": f"{o['name']}({params}): {o['returns']}", "description": o["description"]}})
    for e in model.get("enumerations", []):
        out.append({"path": e["name"], "kind": "enumeration", "cites": list(e.get("source_milestones", [])), "class": e["name"],
                    "content": {"name": e["name"], "package": e["package"], "literals": list(e["literals"])}})
    for r in model.get("relationships", []):
        out.append({"path": rel_path(r), "kind": "relationship", "cites": list(r.get("source_milestones", [])), "class": None,
                    "content": {"type": r["type"], "source": r["source"], "target": r["target"], "label": r["label"],
                                "source_multiplicity": r["source_multiplicity"], "target_multiplicity": r["target_multiplicity"]}})
    return out


def index(model: dict) -> dict[str, dict]:
    """path -> element."""
    return {e["path"]: e for e in elements(model)}
