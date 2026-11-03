"""Build the human-grading pages: claim review, the reviewers' meeting page, and the two sample pages.

  python src/evaluate/grade_ui.py claims                    # -> src/evaluate/graders/claims_review.html (from claims_draft.json)
  python src/evaluate/grade_ui.py claims --reviewer grader_A --milestones 1-9   # one reviewer's assignment
  python src/evaluate/grade_ui.py merge src/evaluate/graders/claims_review_grader_A.json src/evaluate/graders/claims_review_grader_B.json   # -> graders/claims_merge.html, the reviewers' meeting page
  python src/evaluate/grade_ui.py sample --task precision --grader grader_A   # -> src/evaluate/graders/grade_precision_grader_A.html
  python src/evaluate/grade_ui.py sample --task recall --grader grader_A      # (from sample/<task>_items.json, drawn by sample.py)

Each page is one self-contained HTML file with the data embedded: open it in
any browser, no server or install. Decisions autosave in that browser's
localStorage and are exported as JSON with the Export button; the export is
what inventory.py freeze (claim review) and reliability.py (sample grades)
read. The sample pages never contain the run, the configuration, or any model
grader's grade; models are shown under anonymised ids.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
UI = SRC / "evaluate" / "ui"
DRAFT = SRC / "evaluate" / "claims_draft.json"
SAMPLE_DIR = SRC / "evaluate" / "sample"
MILESTONES = SRC / "data" / "milestones.json"
OUT_DIR = SRC / "evaluate" / "graders"   # everything that is sent to the graders


def embed(template: Path, data: dict, **subs: str) -> str:
    html = template.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__DATA__", payload)
    for k, v in subs.items():
        html = html.replace(f"__{k.upper()}__", v)
    return html


def parse_milestones(spec: str | None) -> list[int]:
    """'1-7,9' -> [1, 2, ..., 7, 9]."""
    out = []
    for part in (spec or "").split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


EXTRA_OWNERS = ["Airport"]  # owner names the reviewers added that the drafting model never used,
                            # so they appear in the preset dropdown


def build_claims(reviewer: str | None = None, milestones: list[int] | None = None, seed: Path | None = None) -> Path:
    d = json.loads(DRAFT.read_text(encoding="utf-8"))
    names = {m["number"]: m["name"] for m in json.loads(MILESTONES.read_text(encoding="utf-8"))}
    ms_owners = [f"Milestone {n}: {nm}" for n, nm in sorted(names.items())]
    other_owners = sorted({c["owner"] for s in d["sentences"] for c in s["claims"] if c["owner"]} | set(EXTRA_OWNERS)
                           - set(ms_owners), key=str.lower)
    data = {"generated": d["generated"], "names": names, "reviewer": reviewer or "", "assigned": milestones or [],
            "owners": other_owners + ms_owners,
            # a starting state (claims + added) baked into the page itself, so the reviewer opens straight
            # into it instead of an extra Import step; still just their own local state, edited freely from there
            "seed": json.loads(seed.read_text(encoding="utf-8")) if seed else None,
            # repeats (duplicate_of set by the drafting model within a milestone, or by inventory.mark_repeats) stay in the
            # draft and off the page, so each distinct thing is decided once; the page shows only how many were left out
            "sentences": [{"id": s["id"], "milestone": s["milestone"], "field": s["field"], "text": s["text"],
                           "judge": s["judge"], "claims": [c for c in s["claims"] if not c["duplicate_of"]],
                           "repeats": [c["duplicate_of"] for c in s["claims"] if c["duplicate_of"]]} for s in d["sentences"]]}
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / (f"claims_review_{reviewer}.html" if reviewer else "claims_review.html")
    out.write_text(embed(UI / "claims_review.html", data), encoding="utf-8")
    return out


def build_merge(review_paths: list[Path]) -> Path:
    """The reviewers' meeting page: both independent reviews side by side, one consensus decision per
    claim, the recurring families (inventory.FAMILIES) shown together, the union of the additions, and
    the near-miss pairs to settle. Its export is what `inventory.py freeze --consensus` reads."""
    import inventory as inv
    d = json.loads(DRAFT.read_text(encoding="utf-8"))
    reviews = [json.loads(p.read_text(encoding="utf-8")) for p in review_paths]
    names = [r.get("reviewer") or p.stem for r, p in zip(reviews, review_paths)]
    seed = inv.consensus_seed(d, reviews, names)
    # candidate near-miss pairs over everything either reviewer kept plus every addition, in freeze order
    # (a sentence's claims, then its additions); the page shows a pair while both members are still kept
    things, kept_keys = [], {}
    for s in d["sentences"]:
        for c in s["claims"]:
            e = seed["claims"].get(c["id"])
            if c["duplicate_of"] or not e or c["kind"] not in ("class", "enumeration"):
                continue
            views = [v for v in e["views"].values() if v["decision"] != "reject"]
            if not views:
                continue
            text = (e["consensus"] or views[0])["text"]
            things.append({"id": c["id"], "kind": (e["consensus"] or views[0])["kind"], "text": text, "duplicate_of": ""})
            kept_keys.setdefault((c["kind"], inv.thing_key(text)), c["id"])
        for i, a in enumerate(seed["added"].get(s["id"], [])):
            if a["kind"] in ("class", "enumeration"):
                a["repeat_of"] = kept_keys.get((a["kind"], inv.thing_key(a["text"])), "")
                things.append({"id": f"{s['id']}.add.{i}", "kind": a["kind"], "text": a["text"], "duplicate_of": ""})
    pairs = [{"a": a["id"], "b": b["id"], "shared": sorted(inv.thing_key(a["text"]) & inv.thing_key(b["text"]))}
             for a, b in inv.near_misses(things)]
    names_ms = {m["number"]: m["name"] for m in json.loads(MILESTONES.read_text(encoding="utf-8"))}
    ms_owners = [f"Milestone {n}: {nm}" for n, nm in sorted(names_ms.items())]
    other_owners = sorted({c["owner"] for s in d["sentences"] for c in s["claims"] if c["owner"]} | set(EXTRA_OWNERS)
                          - set(ms_owners), key=str.lower)
    data = {"generated": d["generated"], "names": names_ms, "reviewers": names,
            "assigned": {n: r.get("assigned", []) for n, r in zip(names, reviews)},
            "exported": {n: r.get("exported", "") for n, r in zip(names, reviews)},
            "state": None, "state_from": "", "final": None,
            "owners": other_owners + ms_owners, "seed": seed, "families": inv.families(d["sentences"]), "pairs": pairs,
            "sentences": [{"id": s["id"], "milestone": s["milestone"], "field": s["field"], "text": s["text"],
                           "judge": s["judge"], "claims": [c for c in s["claims"] if not c["duplicate_of"]],
                           "repeats": [c["duplicate_of"] for c in s["claims"] if c["duplicate_of"]]} for s in d["sentences"]]}
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "claims_merge.html"
    out.write_text(embed(UI / "claims_merge.html", data), encoding="utf-8")
    return out


def build_sample(task: str, grader: str, start: Path | None = None) -> Path:
    d = json.loads((SAMPLE_DIR / f"{task}_items.json").read_text(encoding="utf-8"))
    d["grader"] = grader
    # what the grader sees per item, hashed, so the page's local state cannot outlive a change to the sample
    d["fingerprint"] = hashlib.sha1(json.dumps([(i["id"], i.get("milestone"), i.get("candidates"), i["element"]["path"] if "element" in i else i["claim"]["id"])
                                               for i in d["items"]], sort_keys=True).encode()).hexdigest()[:10]
    d["start"] = json.loads(start.read_text(encoding="utf-8")) if start else None
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"grade_{task}_{grader}.html"
    out.write_text(embed(UI / "grade_sample.html", d, task=task), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", choices=["claims", "sample", "merge"])
    ap.add_argument("reviews", nargs="*", type=Path, help="merge: the two reviewers' claims_review_*.json exports")
    ap.add_argument("--grader", help="grader's name (as in the output file name), for the sample page")
    ap.add_argument("--task", choices=["precision", "recall"], help="which sample page to build")
    ap.add_argument("--reviewer", help="reviewer's name (as in the output file name), for a claim-review assignment")
    ap.add_argument("--milestones", help="assigned milestones for the claim review, e.g. 1-7,9")
    ap.add_argument("--seed", type=Path, help="a claims_review_*.json export whose claims/added state the page starts from")
    ap.add_argument("--start", type=Path, help="a grades_*.json export the sample page starts from (grades carried over from an earlier pass)")
    args = ap.parse_args()
    if args.page == "claims":
        out = build_claims(args.reviewer, parse_milestones(args.milestones), args.seed)
    elif args.page == "merge":
        if len(args.reviews) < 2:
            sys.exit("merge needs the two review exports")
        out = build_merge(args.reviews)
    else:
        if not args.grader or not args.task:
            sys.exit("--task and --grader are required")
        out = build_sample(args.task, args.grader, args.start)
    print(f"written {out.relative_to(SRC.parent)} ({out.stat().st_size // 1024} kB); open it in a browser")


if __name__ == "__main__":
    main()
