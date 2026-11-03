"""The typed claim inventory: every sentence of the document, drafted by a model and decided by two reviewers.

  python src/evaluate/inventory.py draft                 # 16 model calls (one per milestone) -> claims_draft.json (resumable)
  python src/evaluate/inventory.py draft --only 1        # one milestone
  python src/evaluate/inventory.py agreement A.json B.json   # agreement between two independent reviews; lists disagreements and near-miss pairs
  python src/evaluate/inventory.py freeze A.json B.json --consensus claims_consensus.json   # the meeting's consensus -> claims.json
  python src/evaluate/inventory.py freeze A.json B.json --merges merges.json   # without a consensus file (two exports that already agree)
  python src/evaluate/inventory.py stats                 # counts by kind for the draft or the frozen file

The draft is written to src/evaluate/inventory/ (one request, raw response,
and result per milestone) and assembled into src/evaluate/claims_draft.json.
The review files are exports of the claim-review page built by grade_ui.py.
Repeats: a class or enumeration claimed twice, within or
across milestones, is marked once by code on the set of its normalised tokens
(match.normalise, so 'estimated in-block time (EIBT)' and 'EIBT' are one key)
and removed from the review pages, so the reviewers decide each distinct thing
once. Two reviewers review independently; `agreement` reports their agreement on
keep/reject (raw, Gwet's AC1, kappa), kind, and owner, writes review_disagreements.md, and writes
review_near_misses.md, the pairs of kept class claims whose keys are nested
(one a subset of the other, sharing two or more tokens), which the reviewers
settle at the same meeting. Each corrects their own file and re-exports; the
agreed merges go in one committed JSON file {duplicate_id: canonical_id}, and
`freeze` merges the files and applies it: a claim decided by one reviewer takes
that decision; a claim decided by both must agree (kind, owner, text), and a claim
added on a shared milestone must be added by both, or freeze refuses.
The meeting itself uses the merge page (`grade_ui.py merge`): both
reviews side by side, one consensus decision per claim, the recurring sentence
families (FAMILIES below) shown together so one rule is applied to all of them,
the near-miss pairs decided in place; it exports one claims_consensus.json that
carries every final decision, the kept additions, the merges, and the rule agreed
per family. `freeze --consensus` takes the final decisions from that file and
stores the two independent exports beside them, with each claim's independent
decisions and whether the meeting changed it. claims.json
keeps the drafting model's proposal and the reviewers' decision for every claim; a claim
is *active* (graded) when its decision is accept, edit, or added and
its final duplicate_of is empty.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC / "generate"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from client import ClaudeCLI  # noqa: E402
import match  # noqa: E402
import sentences as sent  # noqa: E402

ROLE = SRC / "prompts" / "roles" / "inventory.md"
SCHEMA = SRC / "schema" / "inventory_schema.json"
LOG_DIR = SRC / "evaluate" / "inventory"
DRAFT = SRC / "evaluate" / "claims_draft.json"
FROZEN = SRC / "evaluate" / "claims.json"
JUDGE_MODEL = "claude-opus-5"
JUDGE_EFFORT = "medium"
KINDS = ["class", "attribute", "operation", "relationship", "enumeration"]


def user_message(milestone: int, rows: list[dict]) -> str:
    ms = next(m for m in json.loads(sent.MILESTONES.read_text(encoding="utf-8")) if m["number"] == milestone)
    lines = [f"# Milestone {milestone}: {ms['name']}", "",
             "The section, split into sentences. The field name precedes each field; the id precedes each sentence.", ""]
    field = None
    for r in rows:
        if r["field"] != field:
            field = r["field"]
            lines += ["", f"## {sent.FIELD_LABELS[field]}", ""]
        lines.append(f"[{r['id']}] {r['text']}")
    lines += ["", "# Task", "",
              "Return every sentence with keep or drop, a reason, and the claims of each kept sentence, "
              "as JSON conforming to the schema."]
    return "\n".join(lines) + "\n"


def draft(only: int | None, model: str, effort: str):
    rows_all = sent.load()
    client = ClaudeCLI(model=model, effort=effort)
    numbers = [only] if only else sorted({r["milestone"] for r in rows_all})
    for n in numbers:
        tag = f"M{n:02d}"
        if (LOG_DIR / f"{tag}.result.json").exists() and json.loads(
                (LOG_DIR / f"{tag}.result.json").read_text(encoding="utf-8")).get("meta", {}).get("ok"):
            print(f"[{tag}] exists, skipping")
            continue
        rows = [r for r in rows_all if r["milestone"] == n]
        res = client.call(ROLE, user_message(n, rows), SCHEMA, LOG_DIR, tag)
        status = "ok" if res.ok else f"FAILED: {res.error}"
        n_claims = sum(len(s["claims"]) for s in res.output["sentences"]) if res.ok else 0
        print(f"[{tag}] {status}  {len(rows)} sentences -> {n_claims} claims  "
              f"in={res.input_tokens} out={res.output_tokens} ${res.cost_usd:.3f} {res.duration_ms / 1000:.0f}s")
    assemble()


def thing_key(text: str) -> frozenset[str]:
    """The set of normalised tokens of a class or enumeration claim (abbreviations expanded
    from the manual's table, stopwords and the document's item labels dropped, singularised).
    A set, not a sequence, so 'estimated in-block time (EIBT)' and 'EIBT' are one key."""
    key = frozenset(match.normalise(text, "class").split())
    return key or frozenset(text.lower().split())


OWNER_ALIASES = {  # the drafting model's spellings -> one name each; the document's own terms
    "cdm platform": "Airport CDM Platform", "airport cdm platform": "Airport CDM Platform",
    "ao": "Aircraft Operator", "aircraft operator": "Aircraft Operator",
    "ao/gh": "Aircraft Operator / Ground Handler", "aogh": "Aircraft Operator / Ground Handler",
    "aircraft operator / ground handler": "Aircraft Operator / Ground Handler",
    "gh": "Ground Handler", "ground handler": "Ground Handler",
    "atc": "ATC", "atc system": "ATC system", "radar system": "Radar system", "flight": "Flight",
    "network operations": "Network Operations", "pilot": "Pilot", "aircraft": "Aircraft",
}


def canonical_owner(owner: str, milestone: int, names: dict[int, str]) -> str:
    """One spelling per owner. Any reference to a milestone (by number, by name, or
    'Milestone n: name' in any punctuation) becomes 'Milestone <n>: <name>'."""
    o = " ".join(owner.split())
    if not o:
        return ""
    low = o.lower().strip(" .:")
    if low in OWNER_ALIASES:
        return OWNER_ALIASES[low]
    m = re.fullmatch(r"(?:milestone\s*|m)\s*(\d{1,2})(?:\D.*)?", low)
    if m and int(m.group(1)) in names:
        return f"Milestone {int(m.group(1))}: {names[int(m.group(1))]}"
    for n, nm in names.items():
        if low == nm.lower():
            return f"Milestone {n}: {nm}"
    return o


def canonicalise_owners(sentences: list[dict]) -> int:
    names = {m["number"]: m["name"] for m in json.loads(sent.MILESTONES.read_text(encoding="utf-8"))}
    n = 0
    for s in sentences:
        for c in s["claims"]:
            new = canonical_owner(c["owner"], s["milestone"], names)
            if new != c["owner"]:
                c["owner_as_proposed"] = c["owner"]
                c["owner"] = new
                n += 1
    return n


def mark_repeats(sentences: list[dict]) -> int:
    """A class or enumeration claimed again, in the same or a later milestone, is marked
    duplicate_of the first claim with the same key and flagged `auto_duplicate`. Repeats are
    kept in the draft and left out of the review pages (grade_ui.build_claims), so each
    distinct thing is decided once. The drafting model's own within-milestone marks are kept."""
    first: dict[tuple[str, frozenset], str] = {}
    n = 0
    for s in sentences:
        for c in s["claims"]:
            if c["kind"] not in ("class", "enumeration") or c["duplicate_of"]:
                continue
            key = (c["kind"], thing_key(c["text"]))
            if key in first:
                c["duplicate_of"] = first[key]
                c["auto_duplicate"] = True
                n += 1
            else:
                first[key] = c["id"]
    return n


def near_misses(claims: list[dict]) -> list[tuple[dict, dict]]:
    """Pairs of distinct class or enumeration claims whose keys are nested, one a subset of the
    other with two or more shared tokens ('flight plan' in 'ATC flight plan'). An upper bound on
    the repeats the key misses; the reviewers settle each pair by discussion."""
    things = [(c, thing_key(c["text"])) for c in claims if c["kind"] in ("class", "enumeration") and not c.get("duplicate_of")]
    out = []
    for i, (a, ka) in enumerate(things):
        for b, kb in things[i + 1:]:
            if ka != kb and (ka <= kb or kb <= ka) and len(ka & kb) >= 2:
                out.append((a, b))
    return out


# Recurring sentence families: the same kind of sentence
# recurs in most milestones, so the reviewers, each on their own milestones, could treat it
# more than one way. The merge page shows each family together so the meeting agrees one rule
# and applies it everywhere. Membership is by the drafting model's proposal (field, kind, text), not by
# the reviewers' decisions, so the list is the same whoever reviewed the milestone.
FAMILIES = [
    ("A", "Origin statements",
     "Under Origin and priority, who provides the time. Proposed as an attribute of the time or the milestone "
     "and, where a party is named, as a relationship. Decide one rule for the three readings (attribute, "
     "relationship, operation owned by the provider).",
     lambda c, s: s["field"] == "origin_and_priority" and c["kind"] in ("attribute", "relationship")
     and re.search(r"provid|available from|issued by|input|automatic|\bATC\b|ACARS|outstation|Aircraft Operator|"
                   r"Ground Handler|Network Operations|submitted by|distributed by", c["text"], re.I)
     and not re.search(r"priority", c["text"], re.I)),
    ("B", "Directly available after occurrence of the milestone",
     "The same Timing sentence in ten milestones, proposed as an attribute of the milestone or the time. "
     "Decide once whether availability is a claim.",
     lambda c, s: re.search(r"directly available.*after occurrence", c["text"], re.I)),
    ("C", "Local parameters",
     "A locally agreed value that an operation uses ('t is a parameter agreed locally', 'a predefined time "
     "(local parameter)', 'accuracy is agreed locally'). Decide whether the parameter is an attribute claim "
     "in its own right beside the operation.",
     lambda c, s: re.search(r"local parameter|agreed locally|parameter set by ATC|parameter time", c["text"], re.I)),
    ("D", "Network Operations is informed",
     "Under Procedures, the tolerance rule is proposed as an operation and the clause 'Network Operations is "
     "informed' as a relationship beside it. Decide whether the receiving relationship is a separate claim.",
     lambda c, s: re.search(r"Network Operations is informed", c["text"], re.I)),
    ("E", "Sequences as classes",
     "'pre-departure sequence', 'push back / pre-departure sequence', 'departure sequence' proposed as classes. "
     "Decide whether the sequence is a thing that persists across the process.",
     lambda c, s: c["kind"] == "class" and re.search(r"sequence", c["text"], re.I)),
    ("F", "ACARS and 'equivalent to'",
     "Each actual time is 'equivalent to' an ATA/ATD with an ACARS event, proposed as a relationship; the ACARS "
     "state as a class, attribute, or enumeration; ACARS as a source. Decide the reading of each.",
     lambda c, s: re.search(r"ACARS|Equivalent to", c["text"], re.I)),
    ("G", "'in the Airport CDM Platform' as a relationship",
     "Under Procedures, 'inform all relevant Airport CDM Partners of <time> in the Airport CDM Platform' is "
     "proposed as an operation plus a relationship for the platform holding the time. Confirm one reading.",
     lambda c, s: c["kind"] == "relationship" and re.search(r"in the Airport CDM Platform|input to the Airport CDM Platform", c["text"], re.I)),
]


def families(sentences: list[dict]) -> list[dict]:
    """The recurring families as {key, title, question, ids} over the claims on the review pages."""
    out = []
    for key, title, question, rule in FAMILIES:
        ids = [c["id"] for s in sentences for c in s["claims"] if not c["duplicate_of"] and rule(c, s)]
        out.append({"key": key, "title": title, "question": question, "ids": ids})
    return out


def consensus_seed(draft: dict, reviews: list[dict], names: list[str]) -> dict:
    """The merge page's starting state. Per claim: the reviewers' final views, and a consensus
    decision when they need no discussion (one reviewer decided it, or both decided it the same
    way); null where they differ. Per sentence: the union of the reviewers' additions, keyed by
    (kind, text), kept when both added it or when it is on one reviewer's own milestone, undecided
    when one reviewer added it on a shared milestone."""
    shared = set.intersection(*(set(r.get("assigned", [])) for r in reviews)) if len(reviews) > 1 else set()
    claims, added = {}, {}
    for s in draft["sentences"]:
        for c in s["claims"]:
            if c["duplicate_of"]:
                continue
            views = {}
            for name, rev in zip(names, reviews):
                r = rev.get("claims", {}).get(c["id"])
                if r and r.get("decision") in ("accept", "edit", "reject"):
                    views[name] = {"decision": r["decision"], "note": r.get("note", ""), **(_final(c, r) or {})}
            finals = [(v["decision"] != "reject", {k: v.get(k) for k in ("kind", "owner", "text", "rel_type")}) for v in views.values()]
            agree = len(finals) >= 1 and all(f == finals[0] for f in finals[1:])
            cons = None
            if agree:
                v = next(iter(views.values()))
                cons = {k: v[k] for k in ("decision", "kind", "owner", "text", "rel_type") if k in v}
                cons["note"] = " | ".join(x["note"] for x in views.values() if x.get("note"))
            claims[c["id"]] = {"views": views, "consensus": cons}
        union: list[dict] = []
        for name, rev in zip(names, reviews):
            for a in rev.get("added", {}).get(s["id"], []):
                if not a.get("text", "").strip():
                    continue
                sig = _added_sig(a)
                hit = next((u for u in union if _added_sig(u) == sig), None)
                if hit:
                    hit["by"].append(name)
                else:
                    union.append({"kind": a["kind"], "owner": a.get("owner", ""), "text": a["text"],
                                  "rel_type": a.get("rel_type", ""), "note": a.get("note", ""), "by": [name]})
        for u in union:
            u["keep"] = True if len(u["by"]) == len(reviews) or s["milestone"] not in shared else None
        if union:
            added[s["id"]] = union
    return {"claims": claims, "added": added}


def assemble():
    rows_all = sent.load()
    out, missing = [], []
    for r in rows_all:
        r = dict(r)
        p = LOG_DIR / f"M{r['milestone']:02d}.result.json"
        r["judge"], r["claims"] = None, []
        if p.exists():
            res = json.loads(p.read_text(encoding="utf-8"))
            if res.get("meta", {}).get("ok"):
                by_id = {s["id"]: s for s in res["output"]["sentences"]}
                s = by_id.get(r["id"])
                if s is None:
                    missing.append(r["id"])
                else:
                    r["judge"] = {"decision": s["decision"], "reason": s["reason"]}
                    for k, c in enumerate(s["claims"], start=1):
                        r["claims"].append({"id": f"{r['id']}.c{k}", **c})
        out.append(r)
    auto = mark_repeats(out)
    owners = canonicalise_owners(out)
    metas = {}
    for p in sorted(LOG_DIR.glob("M*.result.json")):
        m = json.loads(p.read_text(encoding="utf-8")).get("meta", {})
        if m.get("ok"):
            metas[p.stem.split(".")[0]] = {k: m[k] for k in ("model", "input_tokens", "output_tokens", "cost_usd", "duration_ms", "num_turns")}
    DRAFT.write_text(json.dumps({"generated": dt.datetime.now().isoformat(timespec="seconds"),
                                 "role": str(ROLE.relative_to(SRC.parent)), "calls": metas,
                                 "sentences": out}, indent=1, ensure_ascii=False), encoding="utf-8")
    done = sum(1 for r in out if r["judge"])
    claims = sum(len(r["claims"]) for r in out)
    print(f"draft: {done}/{len(out)} sentences judged, {claims} claims ({auto} repeated classes and enumerations marked, {owners} owner spellings canonicalised), "
          f"{len(metas)}/16 milestones -> {DRAFT.name}")
    if missing:
        print(f"WARNING: {len(missing)} sentences absent from the drafting model's output: {missing[:10]}")


def freeze(review_paths: list[Path], merges_path: Path | None = None, consensus_path: Path | None = None):
    """Merge the reviewers' exports into claims.json (split-with-overlap design). `merges_path`
    is the committed {duplicate_id: canonical_id} file agreed at the reviewers' meeting.
    `consensus_path` is the merge page's export (grade_ui.py merge): when given, every final
    decision, addition, and merge comes from it, and the independent exports are stored beside
    them with each claim's independent decisions and whether the meeting changed it."""
    d = json.loads(DRAFT.read_text(encoding="utf-8"))
    reviews = [json.loads(p.read_text(encoding="utf-8")) for p in review_paths]
    names = [r.get("reviewer") or p.stem for r, p in zip(reviews, review_paths)]
    C = json.loads(consensus_path.read_text(encoding="utf-8")) if consensus_path else None
    merges = dict(C.get("merges", {})) if C else {}
    if merges_path:
        merges.update(json.loads(merges_path.read_text(encoding="utf-8")))
    seed = consensus_seed(d, reviews, names) if C else None  # what needed no discussion, to record what the meeting changed
    claims, undecided, conflicts = [], [], []
    for s in d["sentences"]:
        for c in s["claims"]:
            proposal = {k: c[k] for k in ("text", "kind", "owner", "rel_type", "duplicate_of")}
            if C and c["id"] in C.get("claims", {}) and C["claims"][c["id"]].get("decision") in ("accept", "edit", "reject"):
                r = C["claims"][c["id"]]
                final = _final(c, r)
                independent = {n: rv["claims"][c["id"]]["decision"] for n, rv in zip(names, reviews)
                               if rv.get("claims", {}).get(c["id"], {}).get("decision") in ("accept", "edit", "reject")}
                agreed = seed["claims"].get(c["id"], {}).get("consensus")
                changed = agreed is None or (agreed["decision"] != "reject") != (final is not None) or bool(
                    final and any(agreed.get(k) != final.get(k) for k in ("kind", "owner", "text", "rel_type")))
                claims.append({"id": c["id"], "milestone": s["milestone"], "field": s["field"], "sentence_id": s["id"],
                               **(final or proposal), "decision": r["decision"], "reviewers": list(independent) or ["meeting"],
                               "independent": independent, "changed_at_meeting": changed,
                               "note": r.get("note", ""), "proposal": proposal})
                continue
            views = []
            for name, rev in zip(names, reviews):
                r = rev.get("claims", {}).get(c["id"])
                if r and r.get("decision") in ("accept", "edit", "reject"):
                    final = _final(c, r)
                    views.append((name, r, final))
            if not views:
                if c["duplicate_of"]:  # a repeat: not on the review pages, excluded from scoring either way
                    views = [("(repeat, not reviewed)", {"decision": "accept", "note": "repeat of an earlier claim; not reviewed"}, dict(proposal))]
                else:  # a reviewer may leave a claim blank when unsure; it is kept on file and not scored
                    undecided.append(c["id"])
                    views = [("(undecided)", {"decision": "undecided", "note": ""}, dict(proposal))]
            finals = [v[2] for v in views]
            if len(views) > 1 and any(f != finals[0] for f in finals[1:]):
                conflicts.append((c["id"], [(v[0], v[1]["decision"], v[2]) for v in views]))
                continue
            name, r, final = views[0]
            final = final or proposal  # rejected: keep the proposal's fields on file
            claims.append({"id": c["id"], "milestone": s["milestone"], "field": s["field"], "sentence_id": s["id"],
                           **final, "decision": r["decision"], "reviewers": [v[0] for v in views],
                           "note": " | ".join(v[1].get("note", "") for v in views if v[1].get("note")), "proposal": proposal})
        if C:
            for k, a in enumerate([a for a in C.get("added", {}).get(s["id"], []) if a.get("text", "").strip()], start=1):
                claims.append({"id": f"{s['id']}.a{k}", "milestone": s["milestone"], "field": s["field"], "sentence_id": s["id"],
                               "text": a["text"], "kind": a["kind"], "owner": a.get("owner", ""),
                               "rel_type": a.get("rel_type", ""), "duplicate_of": "", "decision": "added",
                               "reviewers": a.get("by") or ["meeting"], "note": a.get("note", ""), "proposal": None})
            continue
        seen_added = set()
        k = 0
        for name, rev in zip(names, reviews):
            for a in rev.get("added", {}).get(s["id"], []):
                if not a.get("text", "").strip():
                    continue
                sig = _added_sig(a)
                if sig in seen_added:
                    continue
                seen_added.add(sig)
                k += 1
                claims.append({"id": f"{s['id']}.a{k}", "milestone": s["milestone"], "field": s["field"], "sentence_id": s["id"],
                               "text": a["text"], "kind": a["kind"], "owner": a.get("owner", ""),
                               "rel_type": a.get("rel_type", ""), "duplicate_of": "", "decision": "added",
                               "reviewers": [name], "note": a.get("note", ""), "proposal": None})
    if undecided:
        print(f"{len(undecided)} claims left undecided by the reviewers (kept on file, not scored): {undecided[:8]}{' ...' if len(undecided) > 8 else ''}")
    if conflicts:
        print(f"NOT FROZEN: {len(conflicts)} shared claims still differ between the reviewers:")
        for cid, views in conflicts[:40]:
            print(f"  {cid}: " + "; ".join(f"{n} {dec} {f and {kk: f[kk] for kk in ('kind', 'owner', 'text', 'duplicate_of')}}" for n, dec, f in views))
    one_sided = one_sided_additions(reviews, names) if not C else []  # the consensus file settles them
    if one_sided:
        print(f"NOT FROZEN: {len(one_sided)} claims added on a shared milestone by one reviewer only:")
        for name, sid, a in one_sided[:40]:
            print(f"  {sid} {name}: {a['kind']} {a['text'][:80]!r}")
    if conflicts or one_sided:
        sys.exit(1)
    ids = {c["id"] for c in claims}
    for dup, canon in merges.items():  # the meeting's decisions on near-miss pairs
        if dup not in ids or canon not in ids:
            sys.exit(f"NOT FROZEN: merge {dup} -> {canon} names a claim that does not exist")
        while canon in merges and merges[canon] != dup:  # a chain (a -> b -> c) points at its root
            canon = merges[canon]
        next(c for c in claims if c["id"] == dup)["duplicate_of"] = canon
    seen: dict[tuple[str, frozenset], str] = {}  # an added or edited class that repeats a kept one
    n_rep = 0
    for c in claims:
        if c["kind"] in ("class", "enumeration") and c["decision"] in ("accept", "edit", "added") and not c["duplicate_of"]:
            key = (c["kind"], thing_key(c["text"]))
            if key in seen:
                c["duplicate_of"], n_rep = seen[key], n_rep + 1
            else:
                seen[key] = c["id"]
    if n_rep:
        print(f"{n_rep} kept or added claims repeat an earlier kept claim after review; marked")
    for c in claims:
        if c["duplicate_of"] and c["duplicate_of"] not in ids:
            print(f"WARNING: {c['id']} duplicate_of {c['duplicate_of']} does not exist; cleared")
            c["duplicate_of"] = ""
    for c in claims:
        c["active"] = c["decision"] in ("accept", "edit", "added") and not c["duplicate_of"]
    for c in claims:  # the key pass above can re-create chains; every repeat points at its root
        seen_ids, root = set(), c["duplicate_of"]
        while root and root in ids and next(x for x in claims if x["id"] == root)["duplicate_of"] and root not in seen_ids:
            seen_ids.add(root)
            root = next(x for x in claims if x["id"] == root)["duplicate_of"]
        c["duplicate_of"] = root
    for c in claims:
        c["active"] = c["decision"] in ("accept", "edit", "added") and not c["duplicate_of"]
    # pairs the meeting called two things; the merge page keys additions by their page id
    # (<sid>.add.<i>, the index in the union list), so translate those to the frozen ids
    uid_to_id = {}
    for sid, lst in (C.get("state", {}).get("added", {}) if C else {}).items():
        k = 0
        for i, a in enumerate(lst):
            if a.get("keep") is True and a.get("text", "").strip():
                k += 1
                uid_to_id[f"{sid}.add.{i}"] = f"{sid}.a{k}"
    tr = lambda x: uid_to_id.get(x, x)
    distinct = {"|".join(tr(x) for x in k.split("|")) for k, v in (C.get("pairs", {}) if C else {}).items() if v == "distinct"}
    left = [(a, b) for a, b in near_misses([c for c in claims if c["active"]]) if f"{a['id']}|{b['id']}" not in distinct]
    if left:
        print(f"{len(left)} near-miss pairs remain among active claims that the meeting did not decide: "
              + "; ".join(f"{a['id']}~{b['id']}" for a, b in left[:6]))
    sentences = [{"id": s["id"], "milestone": s["milestone"], "field": s["field"], "text": s["text"], "judge": s["judge"]}
                 for s in d["sentences"]]
    FROZEN.write_text(json.dumps({"frozen": dt.datetime.now().isoformat(timespec="seconds"),
                                  "reviewers": names, "draft_generated": d["generated"],
                                  "assignments": {n: r.get("assigned", []) for n, r in zip(names, reviews)},
                                  "reviews_exported": [r.get("exported", "") for r in reviews],
                                  "consensus_exported": C.get("exported", "") if C else "",
                                  "family_rules": C.get("families", {}) if C else {},
                                  "changed_at_meeting": sum(1 for c in claims if c.get("changed_at_meeting")),
                                  "merges": merges,
                                  "independent_reviews": reviews,
                                  "sentences": sentences, "claims": claims}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"frozen {FROZEN.name}: {len(claims)} claims, {sum(c['active'] for c in claims)} active")
    stats(FROZEN)


def _final(c: dict, r: dict | None) -> dict | None:
    """A reviewer's final view of a claim: None if rejected or undecided."""
    if r is None or r.get("decision") not in ("accept", "edit"):
        return None
    out = {k: c[k] for k in ("text", "kind", "owner", "rel_type", "duplicate_of")}
    if r["decision"] == "edit":
        for k in out:
            if k in r and r[k] is not None:
                out[k] = r[k]
    return out


def _norm_owner(s: str) -> str:
    return " ".join(s.lower().replace("-", " ").split())


def _added_sig(a: dict) -> tuple[str, str]:
    return (a["kind"], " ".join(a["text"].lower().split()))


def one_sided_additions(reviews: list[dict], names: list[str]) -> list[tuple[str, str, dict]]:
    """Claims added on a shared milestone by one reviewer and not the other, as (reviewer,
    sentence id, added claim). An addition is a decision like any other: on the shared
    milestones both reviewers must make it, or neither."""
    if len(reviews) < 2:
        return []
    shared = set.intersection(*(set(r.get("assigned", [])) for r in reviews))
    out = []
    for i, (name, rev) in enumerate(zip(names, reviews)):
        others = [r for j, r in enumerate(reviews) if j != i]
        for sid, adds in rev.get("added", {}).items():
            if int(sid.split(".")[0][1:]) not in shared:
                continue
            for a in adds:
                if not a.get("text", "").strip():
                    continue
                if not all(any(_added_sig(b) == _added_sig(a) for b in o.get("added", {}).get(sid, [])) for o in others):
                    out.append((name, sid, a))
    return out


def agreement(path_a: Path, path_b: Path):
    """Agreement between two independent reviews of the draft; writes review_disagreements.md."""
    from stats import gwet_ac2, weighted_kappa
    d = json.loads(DRAFT.read_text(encoding="utf-8"))
    A, B = (json.loads(p.read_text(encoding="utf-8")) for p in (path_a, path_b))
    na, nb = A.get("reviewer") or path_a.stem, B.get("reviewer") or path_b.stem
    keep_a, keep_b, kind_agree, kind_n, owner_agree, owner_n, single = [], [], 0, 0, 0, 0, 0
    rows = []
    for s in d["sentences"]:
        for c in s["claims"]:
            ra, rb = A.get("claims", {}).get(c["id"]), B.get("claims", {}).get(c["id"])
            if not ra or not rb or not ra.get("decision") or not rb.get("decision"):
                single += 1  # outside the overlap, or not yet decided: counted, not listed
                continue
            fa, fb = _final(c, ra), _final(c, rb)
            keep_a.append(1.0 if fa else 0.0)
            keep_b.append(1.0 if fb else 0.0)
            if (fa is None) != (fb is None):
                rows.append((c["id"], f"{na}: {ra['decision']}; {nb}: {rb['decision']}", c))
                continue
            if fa and fb:
                kind_n += 1
                if fa["kind"] == fb["kind"]:
                    kind_agree += 1
                else:
                    rows.append((c["id"], f"kind {na}={fa['kind']} {nb}={fb['kind']}", c))
                if {fa["kind"], fb["kind"]} & {"attribute", "operation", "enumeration"}:
                    owner_n += 1
                    if _norm_owner(fa["owner"]) == _norm_owner(fb["owner"]):
                        owner_agree += 1
                    else:
                        rows.append((c["id"], f"owner {na}={fa['owner']!r} {nb}={fb['owner']!r}", c))
                if bool(fa["duplicate_of"]) != bool(fb["duplicate_of"]):
                    rows.append((c["id"], f"duplicate {na}={fa['duplicate_of']!r} {nb}={fb['duplicate_of']!r}", c))
                if fa["text"] != fb["text"]:
                    rows.append((c["id"], f"text {na}={fa['text']!r} {nb}={fb['text']!r}", c))
    kept = []  # every claim kept by any reviewer, in its final form, plus the added ones; for the near-miss list
    for s in d["sentences"]:
        for c in s["claims"]:
            for rev in (A, B):
                f = _final(c, rev.get("claims", {}).get(c["id"]))
                if f and not c.get("duplicate_of"):
                    kept.append({"id": c["id"], **f})
                    break
        for rev in (A, B):
            for k, a in enumerate(rev.get("added", {}).get(s["id"], []), start=1):
                if a.get("text", "").strip():
                    kept.append({"id": f"{s['id']}.a{k}", "text": a["text"], "kind": a["kind"], "duplicate_of": ""})
    pairs = near_misses(kept)
    added_a = sum(len(v) for v in A.get("added", {}).values())
    added_b = sum(len(v) for v in B.get("added", {}).values())
    one_sided = one_sided_additions([A, B], [na, nb])
    n = len(keep_a)
    keep_agree = sum(x == y for x, y in zip(keep_a, keep_b)) / n if n else 0
    kappa = weighted_kappa(keep_a, keep_b, levels=(0.0, 1.0)) if n else 0
    ac1, ac1_se = gwet_ac2(keep_a, keep_b, levels=(0.0, 1.0)) if n else (0, 0)
    print(f"{n} claims decided by both, {single} by one or neither; keep/reject agreement {keep_agree:.3f}, "
          f"Gwet's AC1 {ac1:.3f} (se {ac1_se:.3f}), Cohen's kappa {kappa:.3f}")
    print(f"kind agreement on claims both kept: {kind_agree}/{kind_n} = {kind_agree / kind_n if kind_n else 0:.3f}")
    print(f"owner agreement (attribute/operation/enumeration both kept): {owner_agree}/{owner_n} = {owner_agree / owner_n if owner_n else 0:.3f}")
    print(f"claims added: {na} {added_a}, {nb} {added_b}; {len(one_sided)} added on a shared milestone by one reviewer only")
    print(f"{len(rows)} items to resolve by discussion -> src/evaluate/review_disagreements.md")
    print(f"{len(pairs)} near-miss pairs of class claims to settle -> src/evaluate/review_near_misses.md")
    out = SRC / "evaluate" / "review_disagreements.md"
    lines = [f"# Review disagreements: {na} vs {nb}", "",
             f"{n} claims decided by both. Keep/reject agreement {keep_agree:.3f} (Gwet's AC1 {ac1:.3f}, kappa {kappa:.3f}); "
             f"kind agreement {kind_agree}/{kind_n}; owner agreement {owner_agree}/{owner_n}; added {na} {added_a}, {nb} {added_b}.", "",
             "Resolve each item by discussion, then one reviewer exports the consensus from the review page "
             "(Import their own file, apply the agreed changes, Export). Added claims are reconciled the same way.", "",
             "| claim | disagreement | drafting model's proposal |", "|---|---|---|"]
    for cid, why, c in rows:
        lines.append(f"| {cid} | {why} | {c['kind']}, owner={c['owner']!r}: {c['text']} |")
    if one_sided:
        lines += ["", f"## Added on a shared milestone by one reviewer only: {len(one_sided)}", "",
                  "Freeze refuses while any remains. Either both reviewers add it (same kind and text) or the one who added it removes it.", "",
                  "| sentence | added by | claim |", "|---|---|---|"]
        for name, sid, a in one_sided:
            lines.append(f"| {sid} | {name} | {a['kind']}, owner={a.get('owner', '')!r}: {a['text']} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    nm = [f"# Near-miss pairs: {len(pairs)}", "",
          "Pairs of kept class or enumeration claims whose normalised names are nested (one inside the other, "
          "sharing two or more words). For each pair decide together whether they name one thing or two. "
          "Record every 'one thing' decision in merges.json as {\"<later id>\": \"<earlier id>\"}; freeze applies it.", "",
          "| a | b | decision |", "|---|---|---|"]
    for a, b in pairs:
        nm.append(f"| {a['id']} ({a['kind']}): {a['text']} | {b['id']} ({b['kind']}): {b['text']} | |")
    (SRC / "evaluate" / "review_near_misses.md").write_text("\n".join(nm) + "\n", encoding="utf-8")
    (SRC / "evaluate" / "review_agreement.json").write_text(json.dumps({
        "reviewers": [na, nb], "claims_both_decided": n, "keep_agreement": keep_agree, "keep_ac1": ac1, "keep_ac1_se": ac1_se, "keep_kappa": kappa,
        "kind_agreement": [kind_agree, kind_n], "owner_agreement": [owner_agree, owner_n],
        "added": {na: added_a, nb: added_b}, "added_one_sided_on_shared": len(one_sided),
        "disagreements": len(rows), "near_miss_pairs": len(pairs)}, indent=1), encoding="utf-8")


def load_frozen() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def active_claims() -> list[dict]:
    return [c for c in load_frozen()["claims"] if c["active"]]


def stats(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    if "claims" in d:
        cs = [c for c in d["claims"] if c.get("active", True)]
        dec = {}
        for c in d["claims"]:
            dec[c["decision"]] = dec.get(c["decision"], 0) + 1
        print("decisions:", dec)
    else:
        cs = [c for s in d["sentences"] for c in s["claims"]]
        kept = sum(1 for s in d["sentences"] if s["judge"] and s["judge"]["decision"] == "keep")
        print(f"sentences kept {kept}/{len(d['sentences'])}")
    by_kind = {k: sum(1 for c in cs if c["kind"] == k) for k in KINDS}
    dups = sum(1 for c in cs if c.get("duplicate_of"))
    print(f"{len(cs)} claims ({dups} marked duplicate):", by_kind)
    by_ms = {}
    for c in cs:
        m = c.get("milestone") or int(c["id"].split(".")[0][1:])
        by_ms[m] = by_ms.get(m, 0) + 1
    print("per milestone:", " ".join(f"M{k}={v}" for k, v in sorted(by_ms.items())))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["draft", "assemble", "agreement", "freeze", "stats"])
    ap.add_argument("review", nargs="*", help="review exports: two for agreement, all of them for freeze")
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--model", default=JUDGE_MODEL)
    ap.add_argument("--effort", default=JUDGE_EFFORT)
    ap.add_argument("--merges", type=Path, default=None, help="freeze: the agreed {duplicate_id: canonical_id} file")
    ap.add_argument("--consensus", type=Path, default=None, help="freeze: the merge page's export (final decisions, additions, merges)")
    args = ap.parse_args()
    if args.cmd == "draft":
        draft(args.only, args.model, args.effort)
    elif args.cmd == "assemble":
        assemble()
    elif args.cmd == "agreement":
        if len(args.review) != 2:
            sys.exit("agreement needs two review exports")
        agreement(Path(args.review[0]), Path(args.review[1]))
    elif args.cmd == "freeze":
        if not args.review:
            sys.exit("freeze needs the review exports")
        freeze([Path(p) for p in args.review], args.merges, args.consensus)
    else:
        stats(FROZEN if FROZEN.exists() else DRAFT)


if __name__ == "__main__":
    main()
