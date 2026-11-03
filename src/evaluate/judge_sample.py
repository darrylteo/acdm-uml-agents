"""The model graders on the two samples: the same 200 + 200 items the two researchers grade.

  python src/evaluate/judge_sample.py precision --model claude-opus-5 --effort high
  python src/evaluate/judge_sample.py precision --model claude-sonnet-5 --effort high
  python src/evaluate/judge_sample.py precision --model claude-opus-5 --effort high --dry-run    # one run only
  python src/evaluate/judge_sample.py recall --model claude-opus-5 --effort high [--runs multi/run_03 ...]
  python src/evaluate/judge_sample.py recall --model claude-sonnet-5 --effort high --role judge_recall_sonnet.md

One call per run (18 per model). The message opens with the whole document,
identical in every call so the CLI's prompt cache serves it, followed, for
precision, by the run's sampled elements (graded against the document) and, for
recall, by the run's whole model and then its sampled claims (graded against
the model, under the rubric of graders/GRADERS.md Task 2). Output goes to sample/judge_<task>_<model>_<effort>.json
in the same shape as a grader's export (grader, grades{id: credit, ...}), so
reliability.py takes it as one more grader; every request and raw response is
kept under sample/judge_logs/. A run already in the output file is skipped, and
the script stops at the first rate-limit error (the subscription's weekly window
resets a day later, not in minutes): rerun the same command after the reset.

The supporting sentence id is kept per item so a grade can be checked;
the element's citations are neither graded nor reported.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC / "generate"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from client import RATE_LIMIT_MARKERS, ClaudeCLI  # noqa: E402
import paths  # noqa: E402
import sentences as sent  # noqa: E402

SAMPLE_DIR = SRC / "evaluate" / "sample"
ROLES = {"precision": SRC / "prompts" / "roles" / "judge_grounding.md", "recall": SRC / "prompts" / "roles" / "judge_recall.md"}
SCHEMAS = {"precision": SRC / "schema" / "grounding_sample_schema.json", "recall": SRC / "schema" / "recall_sample_schema.json"}
META_KEYS = ("model", "input_tokens", "output_tokens", "thinking_tokens", "cache_read_tokens", "cost_usd", "duration_ms", "attempts")


def document_text() -> str:
    names = {m["number"]: m["name"] for m in json.loads(sent.MILESTONES.read_text(encoding="utf-8"))}
    lines, ms, field = ["# The document: sixteen A-CDM milestones, sentences numbered", ""], None, None
    for s in sent.load():
        if s["milestone"] != ms:
            ms, field = s["milestone"], None
            lines += [f"## Milestone {ms}: {names[ms]}", ""]
        if s["field"] != field:
            field = s["field"]
            lines += [f"### {sent.FIELD_LABELS[field]}", ""]
        lines.append(f"[{s['id']}] {s['text']}")
    return "\n".join(lines) + "\n"


def element_line(item: dict, el: dict) -> str:
    e, c = item["element"], item["element"]["content"]
    cites = ", ".join(str(m) for m in el["cites"])
    if e["kind"] in ("attribute", "operation"):
        body = f"{e['path']}: {c.get('type') or c.get('signature')}; description: {c.get('description') or ''}"
        cls = e["class"]
        body += f"\n    on class {cls['name']} «{cls['stereotype']}» in {cls['package']}: {cls['definition']}"
    elif e["kind"] == "relationship":
        body = f"{c['source']} -> {c['target']} [{c['type']}]" + (f" label: {c['label']}" if c.get("label") else "")
    elif e["kind"] == "enumeration":
        body = f"{c['name']} in {c['package']}: literals {', '.join(c['literals'])}"
    else:
        body = f"{c['name']} «{c['stereotype']}» in {c['package']}: {c['definition']}"
    return f"[{item['id']}] {e['kind']}, cites milestones {cites}\n    {body}"


def message(doc: str, items: list[dict], idx: dict) -> str:
    lines = [doc, "# Elements to grade", ""]
    for it in items:
        lines.append(element_line(it, idx[it["element"]["path"]]))
        lines.append("")
    lines += ["# Task", "", "For every element return the grade, the supporting sentence id, and a note if needed, as JSON conforming to the schema."]
    return "\n".join(lines) + "\n"


def model_text(model: dict) -> str:
    """The whole model as the recall page's tree shows it: package, definition, members with types and descriptions;
    stereotypes are left out, as on the page (neither is graded)."""
    lines = ["# The model", ""]
    for c in model["classes"]:
        lines.append(f"class {c['name']} (package {c['package']}): {c.get('definition') or ''}")
        for a in c.get("attributes", []):
            lines.append(f"  attribute {a['name']}: {a.get('type') or ''}; {a.get('description') or ''}")
        for o in c.get("operations", []):
            ps = ", ".join(f"{p['name']}: {p.get('type') or ''}" for p in o.get("parameters", []))
            lines.append(f"  operation {o['name']}({ps}): {o.get('returns') or ''}; {o.get('description') or ''}")
        lines.append("")
    for e in model.get("enumerations", []):
        lines.append(f"enumeration {e['name']} (package {e['package']}): {', '.join(e['literals'])}")
    lines.append("")
    for r in model.get("relationships", []):
        lines.append(f"relationship {r['source']} -> {r['target']} [{r['type']}]" + (f" {r['label']}" if r.get("label") else ""))
    return "\n".join(lines) + "\n"


def recall_message(doc: str, model: dict, items: list[dict]) -> str:
    lines = [doc, model_text(model), "# Claims to grade", ""]
    for it in items:
        c = it["claim"]
        sid = c["id"].rsplit(".", 1)[0]
        lines.append(f"[{it['id']}] {c['kind']}, owner {c['owner'] or '-'}, from sentence {sid}\n    {c['text']}")
        lines.append("")
    lines += ["# Task", "", "For every claim return the grade, the elements that carry it, and a note if needed, as JSON conforming to the schema."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task", choices=["precision", "recall"])
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort", default="high")
    ap.add_argument("--dry-run", action="store_true", help="one run only")
    ap.add_argument("--runs", nargs="*", help="only these runs, e.g. multi/run_03")
    ap.add_argument("--role", help="a role prompt other than the task's default, by file name under prompts/roles "
                                   "(recall with claude-sonnet-5 uses judge_recall_sonnet.md)")
    args = ap.parse_args()

    role = SRC / "prompts" / "roles" / args.role if args.role else ROLES[args.task]
    key = json.loads((SAMPLE_DIR / f"{args.task}_key.json").read_text(encoding="utf-8"))
    items = {i["id"]: i for i in json.loads((SAMPLE_DIR / f"{args.task}_items.json").read_text(encoding="utf-8"))["items"]}
    out_path = SAMPLE_DIR / f"judge_{args.task}_{args.model}_{args.effort}.json"
    out = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else \
        {"grader": f"{args.model}/{args.effort}", "task": args.task, "seed": key["seed"], "prompt": role.name, "calls": {}, "grades": {}}
    by_run: dict[str, list[str]] = {}
    for iid, k in key["items"].items():
        by_run.setdefault(k["run"], []).append(iid)
    doc = document_text()
    sid_ms = {s["id"]: s["milestone"] for s in sent.load()}
    client = ClaudeCLI(model=args.model, effort=args.effort, rate_limit_max_s=0)  # do not wait out a weekly limit
    log_dir = SAMPLE_DIR / "judge_logs" / f"{args.model}_{args.effort}"
    runs = [r for r in sorted(by_run) if r in args.runs] if args.runs else sorted(by_run)
    runs = runs[:1] if args.dry_run else runs
    print(f"{args.task}: {len(runs)} runs, {sum(len(by_run[r]) for r in runs)} items, {client.model}/{client.effort}", flush=True)
    for run in runs:
        if out["calls"].get(run, {}).get("ok"):
            continue
        model = json.loads((SRC / "runs" / run / "model.json").read_text(encoding="utf-8"))
        idx = paths.index(model)
        ids = sorted(by_run[run])
        msg = message(doc, [items[i] for i in ids], idx) if args.task == "precision" else recall_message(doc, model, [items[i] for i in ids])
        res = client.call(role, msg, SCHEMAS[args.task], log_dir, f"{role.stem}_{run.replace('/', '_')}")
        entry = {"ok": res.ok, "error": res.error, "meta": {k: getattr(res, k) for k in META_KEYS},
                 "judged": dt.datetime.now().isoformat(timespec="seconds")}
        if res.ok:
            got = {it["id"]: it for it in res.output["items"]}
            entry["missing"] = sorted(set(ids) - set(got))
            for iid, it in got.items():
                if iid not in ids or it["grade"] not in (0, 0.5, 1):
                    continue
                if args.task == "recall":
                    out["grades"][iid] = {"credit": it["grade"], "elements": it["elements"], "note": it["note"]}
                    continue
                out["grades"][iid] = {"credit": it["grade"], "sentence": it["sentence"], "note": it["note"],
                                      "sentence_known": (it["sentence"] in sid_ms) if it["sentence"] else None}
        out["calls"][run] = entry
        out["exported"] = dt.datetime.now().isoformat(timespec="seconds")
        out_path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        m = entry["meta"]
        print(f"[{run}] {'ok' if res.ok else 'FAILED ' + str(res.error)[:80]} {len(ids)} items in={m['input_tokens']} "
              f"cached={m['cache_read_tokens']} out={m['output_tokens']} ${m['cost_usd']:.3f} {m['duration_ms'] / 1000:.0f}s"
              + (f" missing={entry['missing']}" if res.ok and entry["missing"] else ""), flush=True)
        if not res.ok and any(k in str(res.error).lower() for k in RATE_LIMIT_MARKERS):
            print("rate limited; stopping. Rerun the same command after the window resets to continue.", flush=True)
            break
    g = out["grades"]
    if g:
        print(f"{len(g)} graded; mean {sum(v['credit'] for v in g.values()) / len(g):.3f}"
              + (f"; unknown sentence ids: {sum(1 for v in g.values() if v.get('sentence_known') is False)}" if args.task == "precision" else ""))


if __name__ == "__main__":
    main()
