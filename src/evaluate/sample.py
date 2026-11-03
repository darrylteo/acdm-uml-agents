"""The two grading samples, 200 items each.

  python src/evaluate/sample.py precision                # 200 (run, element, cited milestone) items -> sample/precision_items.json + precision_key.json
  python src/evaluate/sample.py recall                   # 200 (run, claim) items with candidate lists -> sample/recall_items.json + recall_key.json
  python src/evaluate/sample.py precision --n 200 --seed 0

All graders grade the same items in the same shuffled order. The items file is
what the grading page embeds: the element or claim, the text, an anonymised
model id (m00..m17, one shuffle shared by both samples), and nothing that names
the run or the configuration. The key file maps item ids to the run and to the
element or claim, and is what reliability.py uses to group items by
configuration and kind.

Precision population: every (run, element, cited milestone) triple over the 18
scored runs (the scaffold-only control cites nothing and is excluded).
Recall population: every (run, active claim) pair; it needs claims.json. The
recall item lists the five elements of the model ranked highest by
rank_candidates (deterministic, no model call), in that order and unlabelled,
and records the list. It also names the classes of the model that are the
claim's owner (owner_classes), which the page shows opened.

Sampling is uniform over the population with a fixed seed. A
precision item shows the drawn milestone unless another cited milestone
contains more tokens of the element's name (abbreviations expanded, class name
excluded); it then shows the cited milestone the element's own description
names ('(milestone 15)'), failing that the one holding the longest contiguous
run of the name's tokens, then the most tokens, then the most content-word
overlap. An attribute inherits every citation of its class, so the drawn
milestone often does not mention it at all. The key records both milestones.
The item highlights the shown milestone's three sentences that share the most
content words with the element. The recall page renders a candidate class or
enumeration opened, with its members and an enumeration's literals, so the
grader reads what it holds and the browser's own Ctrl+F reaches it.
"""
import argparse
import json
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inventory  # noqa: E402
import match  # noqa: E402
import paths  # noqa: E402
import sentences as sent  # noqa: E402

SRC = Path(__file__).resolve().parents[1]
RUNS = SRC / "runs"
SAMPLE_DIR = SRC / "evaluate" / "sample"
SCORED_CONDITIONS = ["multi", "single", "single_high", "noscaffold"]
POOL_LEXICAL = 5   # elements in the recall candidate list
HIGHLIGHT = 3      # sentences highlighted on a precision item


def scored_runs() -> list[Path]:
    """The 18 runs that are graded, in condition order (the scaffold-only control cites nothing)."""
    return [p for c in SCORED_CONDITIONS for p in sorted((RUNS / c).glob("run_*")) if (p / "model.json").exists()]


def aliases(runs: list[Path], seed: int) -> dict[str, str]:
    """run label -> m00..; one shuffle from the seed, so both samples share it."""
    labels = sorted(f"{r.parent.name}/{r.name}" for r in runs)
    random.Random(seed).shuffle(labels)
    return {lab: f"m{i:02d}" for i, lab in enumerate(labels)}


def element_words(e: dict) -> set[str]:
    c = e["content"]
    text = " ".join(str(v) for k, v in c.items() if k not in ("source_multiplicity", "target_multiplicity"))
    if e.get("class") and e["kind"] in ("attribute", "operation"):
        text += " " + e["class"]
    return match.content_words(text)


def own_words(e: dict) -> set[str]:
    """Content words of the element's own name: the attribute or operation name, the relationship's two
    ends and label, the class name, the enumeration name with its literals; a member's class name is
    context, not its name."""
    c = e["content"]
    if e["kind"] == "operation":
        text = c["signature"].split("(")[0]
    elif e["kind"] == "relationship":
        text = c["source"] + " " + c["target"] + " " + (c.get("label") or "")
    elif e["kind"] == "enumeration":
        text = c["name"] + " " + " ".join(c["literals"])   # the literals are what an enumeration holds
    else:
        text = c["name"]
    return match.content_words(text)


def word_hit(a: str, b: str) -> bool:
    """A claim word and an element word are the same word: equal, one inside the other from four letters
    up (unregulated / regulated, late / later), or a common stem of six letters (approval / approved)."""
    if a == b:
        return True
    if min(len(a), len(b)) >= 4 and (a in b or b in a):
        return True
    return len(a) >= 6 and len(b) >= 6 and a[:6] == b[:6]


RANK_STOPWORDS = {"must", "may", "shall", "should", "will", "can", "could", "would", "normally", "also", "any", "all",
                  "each", "every", "other", "than", "then", "there", "these", "those", "has", "have", "been", "being",
                  "into", "onto", "via", "per", "e.g", "i.e", "etc"}   # carry no content for ranking; match.TEXT_STOPWORDS holds the rest


def claim_terms(text: str) -> list[frozenset[str]]:
    """The claim's content as terms: one per word, an abbreviation's expansion kept together as one term
    ('ATC' -> {air, traffic, control}) so it counts once and hits only where all its words appear."""
    out = []
    for raw in match._split(text):
        ws = frozenset(w for w in match.tokens(raw) if w not in match.TEXT_STOPWORDS and w not in RANK_STOPWORDS and not w.isdigit())
        if ws and ws not in out:
            out.append(ws)
    return out


def owner_words(claim: dict) -> set[str]:
    return {w for w in match.content_words(claim.get("owner") or "") if w not in ("milestone", "process")}


OWNER_AFFIXES = {"milestone", "event", "process"}   # a class may add these to the owner's name and still be the owner


def owner_match(ow: set[str], class_name: str) -> bool:
    """The class is the claim's owner: the words shared exceed half of the words either side uses, the
    manual's labels and a milestone number not counted ('Milestone 8: Ground Handling Started' is
    GroundHandlingStartedMilestone; 'Flight' is not FlightPlan); two prefixed time quantities only when
    identical (AOBT is not AIBT), a prefixed one and an unprefixed one by the same rule (TSAT is
    StartUpApprovalTime where a model keeps the prefix as an attribute)."""
    if not ow:
        return False
    cw = {w for w in match.content_words(class_name) if w not in OWNER_AFFIXES and not match.MILESTONE_NUMBER.fullmatch(w)}
    if (ow & match.TIME_PREFIXES) and (cw & match.TIME_PREFIXES):
        return ow == cw   # two prefixed time quantities are the same only word for word: AOBT is not EOBT, nor AIBT
    return len(ow & cw) / len(ow | cw) > 0.5 if cw else False


def owner_classes(claim: dict, model: dict) -> list[str]:
    """The classes and enumerations of the model that are the claim's owner, shown opened on the recall
    page so the grader sees at once what the owner holds."""
    ow = owner_words(claim)
    return [c["name"] for c in model.get("classes", []) + model.get("enumerations", []) if owner_match(ow, c["name"])][:3]


def names_of(e: dict) -> list[list[str]]:
    """Token sequences an element can be called by: its own name, and each literal of an enumeration."""
    c = e["content"]
    if e["kind"] == "operation":
        return [match.tokens(c["signature"].split("(")[0])]
    if e["kind"] == "relationship":
        return []
    if e["kind"] == "enumeration":
        return [match.tokens(c["name"])] + [match.tokens(lit) for lit in c["literals"]]
    return [match.tokens(c["name"])]


def homes(e: dict) -> set[str]:
    """The classes an element belongs to: its own class for a member or a classifier, both ends for a relationship."""
    if e["kind"] == "relationship":
        return {e["content"]["source"], e["content"]["target"]}
    return {e["class"]}


POOL_PER_CLASS = 2        # at most this many pool elements from one class, so one class cannot fill the shortlist
POOL_RELATIONSHIPS = 2    # at most this many relationships in the shortlist, counted separately from the classes they join


def display_label(e: dict) -> str:
    """The element as the page prints it, which is what decides whether two entries look alike to a grader.
    Models repeat one operation across their milestone classes, so five elements can carry one signature."""
    c = e["content"]
    if e["kind"] == "operation":
        return c["signature"]   # the signature already carries the parameters and the return type
    if e["kind"] == "attribute":
        return f"{c['name']}: {c['type']}"
    if e["kind"] == "relationship":
        return e["path"]
    return c["name"]


def rank_candidates(claim: dict, model: dict, k: int = POOL_LEXICAL) -> list[str]:
    """The k elements of the model most likely to hold the claim.

    The claim's text is cut into terms, one per word, an abbreviation's expansion held together as one
    term ('ATC' is {air, traffic, control} and hits only where all three appear); stopwords, modal verbs
    and the owner's own words drop out. Two words are the same word when equal, when one contains the
    other (unregulated / regulated), or when they share a six-letter stem (approval / approved).

    An element scores the weight of each term it accounts for, 1 when the term is in its own name (an
    enumeration's literals included) and 0.5 when only in its class name, type, description, parameters
    or literals, each weighted by the term's rarity among the model's elements, log(N/df); a term no
    element of the model uses at all is dropped, since it is evidence about neither. That sum is then
    multiplied by the share of the remaining terms the element accounts for, so an element that explains
    the whole claim in its description beats
    one whose name happens to carry the claim's rarest word and nothing else. Without that factor a bare
    class M9FinalConfirmationTOBT outranked the operation whose description is the claim.
    An element on the claim's owner class gains half the weight of the claim's rarest term. An element
    named exactly as the claim reads (the class ACGT for the claim 'ACGT', the literal IN-BLOCK), or
    named as the claim's owner while sitting elsewhere (Flight.ardt for a claim about ARDT), gains that
    weight whole. The owner's own class takes the first bonus only, never both.

    An element accounting for none of the claim's terms is left off the list unless it is named as the
    claim or its owner, since the owner's own class is shown in its own panel on the page.

    Ties go to the element of the claim's kind, then to the shorter element. No class contributes more
    than POOL_PER_CLASS elements and no shortlist more than POOL_RELATIONSHIPS relationships, so a class
    and its generalization cannot crowd out the member that carries the claim, and no two entries print
    the same label, since a model that gives one operation to each of its sixteen milestone classes would
    otherwise fill the list with one signature repeated.
    """
    els = paths.elements(model)
    words = [(e, own_words(e), element_words(e)) for e in els]
    n = len(words)

    def hit(term: frozenset[str], ws: set[str]) -> bool:
        return all(any(word_hit(w, x) for x in ws) for w in term)

    ow = owner_words(claim)
    idf = {}
    for t in claim_terms(claim["text"]):
        if t <= ow:
            continue   # the owner says where the claim lives; the rest of the text says what it holds
        df = sum(1 for _, _, ew in words if hit(t, ew))
        if df:   # a term no element uses is not evidence either way, and must not count against coverage
            idf[t] = math.log(n / df)
    rarest = max(idf.values(), default=0.0)
    exact = match.tokens(claim["text"])
    scored = []
    for e, nw, ew in words:
        parts = [(wt, 1.0 if hit(t, nw) else 0.5 if hit(t, ew) else 0.0) for t, wt in idf.items()]
        covered = sum(1 for _, f in parts if f)
        base = sum(wt * f for wt, f in parts) * (covered / len(parts) if parts else 0)
        s = base
        on_owner = any(owner_match(ow, h) for h in homes(e) if h)
        if on_owner:
            s += rarest / 2
        # the second bonus is for an element NAMED as the claim's owner somewhere else in the model
        # (Flight.ardt for a claim about ARDT); the owner's own class already has the first bonus, and
        # giving it both put the owner class and its generalization above the member holding the claim
        named = exact in names_of(e) or (not on_owner and owner_match(ow, e["path"].split(".")[-1].rstrip("()")))
        if named:
            s += rarest
        # an element that accounts for none of the claim's terms is on the list only for living on the
        # owner's class, which the page now shows in its own panel; it would displace a real candidate
        if base > 0 or named:
            scored.append((-s, e["kind"] != claim["kind"], len(ew), e["path"], e))
    out, used, rels, labels = [], {}, 0, set()
    for _, _, _, path, e in sorted(scored, key=lambda x: x[:4]):
        if path in out:
            continue
        # one entry per printed label. Where the model puts a thing is not graded, so a second element
        # printing the same signature is a spent slot. The ranking has already put the best-scoring copy first.
        lab = display_label(e)
        if lab in labels:
            continue
        labels.add(lab)
        if e["kind"] == "relationship":
            if rels >= POOL_RELATIONSHIPS:
                continue
            rels += 1
        elif used.get(e["class"], 0) >= POOL_PER_CLASS:
            continue
        else:
            used[e["class"]] = used.get(e["class"], 0) + 1
        out.append(path)
        if len(out) == k:
            break
    return out


def name_sequence(e: dict) -> list[str]:
    """The element's name as an ordered token list (abbreviations expanded), without the class name."""
    c = e["content"]
    if e["kind"] == "operation":
        n = c["signature"].split("(")[0]
    elif e["kind"] == "relationship":
        n = c["source"] + " " + c["target"]
    else:
        n = c["name"]
    return [w for w in match.tokens(n) if w not in match.TEXT_STOPWORDS]


MILESTONE_HINT = re.compile(r"\bmilestones?\s*((?:\d{1,2}(?:\s*(?:,|and|&)\s*)?)+)|\bM(\d{1,2})\b", re.I)


def hinted_milestones(e: dict) -> set[int]:
    """Milestone numbers the element's own description or definition names: '(milestones 2, 3)' or '(M3)'."""
    text = e["content"].get("description") or e["content"].get("definition") or ""
    out: set[int] = set()
    for m in MILESTONE_HINT.finditer(text):
        out |= {int(x) for x in re.findall(r"\d{1,2}", m.group(1))} if m.group(1) else {int(m.group(2))}
    return {n for n in out if 1 <= n <= 16}


def longest_run(name: list[str], text: list[str]) -> int:
    """Length of the longest contiguous run of the name's tokens found in the text's token sequence."""
    best = 0
    for i in range(len(name)):
        for j in range(len(text)):
            k = 0
            while i + k < len(name) and j + k < len(text) and name[i + k] == text[j + k]:
                k += 1
            best = max(best, k)
    return best


def shown_milestone(e: dict, drawn: int, ms_tokens: dict[int, list[str]]) -> int:
    """The drawn milestone if its text names the element as fully as any cited milestone does (token count);
    otherwise the cited milestone the element's description names, then the longest contiguous run of the
    name's tokens, then the token count, then content-word overlap."""
    ms_words = {m: set(t) for m, t in ms_tokens.items()}
    seq, ew = name_sequence(e), element_words(e)
    nt = set(seq)
    count = {m: len(nt & ms_words[m]) for m in e["cites"]}
    if count[drawn] == max(count.values()):
        return drawn
    hints = hinted_milestones(e)
    return max(e["cites"], key=lambda m: (m in hints, longest_run(seq, ms_tokens[m]), count[m], match.jaccard(ew, ms_words[m]), -m))


def milestone_sentences(n: int) -> list[dict]:
    return [{"id": s["id"], "field": sent.FIELD_LABELS[s["field"]], "text": s["text"]} for s in sent.load() if s["milestone"] == n]


def highlight(sentences: list[dict], words: set[str], k: int = HIGHLIGHT) -> list[dict]:
    scored = [(match.jaccard(words, match.content_words(s["text"])), i) for i, s in enumerate(sentences)]
    top = {i for sc, i in sorted(scored, key=lambda x: (-x[0], x[1]))[:k] if sc > 0}
    return [{**s, "hl": i in top} for i, s in enumerate(sentences)]


def display_model(model: dict) -> list[dict]:
    """The whole model as the filterable list the recall page shows."""
    out = []
    for c in model.get("classes", []):
        members = [{"path": f"{c['name']}.{a['name']}", "kind": "attribute", "label": f"{a['name']}: {a['type']}", "desc": a["description"]}
                   for a in c.get("attributes", [])]
        members += [{"path": f"{c['name']}.{o['name']}()", "kind": "operation",
                     "label": f"{o['name']}({', '.join(p['name'] + ': ' + p['type'] for p in o.get('parameters', []))}): {o['returns']}",
                     "desc": o["description"]} for o in c.get("operations", [])]
        out.append({"path": c["name"], "kind": "class", "package": c["package"], "stereotype": c["stereotype"],
                    "definition": c["definition"], "members": members})
    for e in model.get("enumerations", []):
        out.append({"path": e["name"], "kind": "enumeration", "package": e["package"], "stereotype": "enumeration",
                    "definition": ", ".join(e["literals"]), "members": []})
    rels = [{"path": paths.rel_path(r), "kind": "relationship",
             "label": f"{r['source']} {'--|>' if r['type'] == 'generalization' else '--'} {r['target']} [{r['type']}]" + (f" {r['label']}" if r.get("label") else "")}
            for r in model.get("relationships", [])]
    return out + [{"path": "__relationships__", "kind": "relationships", "members": rels}]


def element_card(e: dict, model: dict) -> dict:
    cls = next((c for c in model["classes"] if c["name"] == e["class"]), None) if e["kind"] in ("attribute", "operation") else None
    return {"path": e["path"], "kind": e["kind"], "content": e["content"],
            "class": {"name": cls["name"], "stereotype": cls["stereotype"], "package": cls["package"], "definition": cls["definition"]} if cls else None}


def draw_precision(n: int, seed: int):
    rng = random.Random(seed)
    runs = scored_runs()
    alias = aliases(runs, seed)
    names = {m["number"]: m["name"] for m in json.loads(sent.MILESTONES.read_text(encoding="utf-8"))}
    models = {f"{r.parent.name}/{r.name}": json.loads((r / "model.json").read_text(encoding="utf-8")) for r in runs}
    pop = [(lab, e, ms) for lab, m in models.items() for e in paths.elements(m) for ms in e["cites"]]
    pick = rng.sample(pop, n)
    rng.shuffle(pick)
    ms_tokens: dict[int, list[str]] = {}
    for s in sent.load():
        ms_tokens.setdefault(s["milestone"], []).extend(match.tokens(s["text"]))
    items, key, moved, unnamed = [], {}, 0, []
    for i, (lab, e, drawn) in enumerate(pick, start=1):
        iid = f"g{i:03d}"
        ms = shown_milestone(e, drawn, ms_tokens)
        moved += ms != drawn
        # lint: the shown milestone should name the element (a run of its name tokens, or the description's own
        # milestone number); what fails is listed so a grader is never handed an item that is a foregone 0 unnoticed
        if not longest_run(name_sequence(e), ms_tokens[ms]) and ms not in hinted_milestones(e):
            unnamed.append(f"{iid} {e['path']} M{ms}")
        items.append({"id": iid, "task": "precision", "model": alias[lab], "milestone": ms, "milestone_name": names[ms],
                      "element": element_card(e, models[lab]),
                      "sentences": highlight(milestone_sentences(ms), element_words(e))})
        key[iid] = {"run": lab, "path": e["path"], "kind": e["kind"], "milestone": ms, "drawn_milestone": drawn}
    _write("precision", seed, n, len(pop), items, key, alias, {})
    print(f"precision: {n} of {len(pop)} (run, element, milestone) triples over {len(runs)} runs; "
          f"by kind {_by_kind(e for _, e, _ in pick)}; {moved} shown under a cited milestone other than the drawn one")
    print(f"lint: {len(unnamed)} items whose shown milestone names the element in no cited milestone (graded on content):")
    for u in unnamed:
        print("  " + u)


def draw_recall(n: int, seed: int):
    rng = random.Random(seed)
    runs = scored_runs()
    alias = aliases(runs, seed)
    names = {m["number"]: m["name"] for m in json.loads(sent.MILESTONES.read_text(encoding="utf-8"))}
    claims = inventory.active_claims()
    models = {f"{r.parent.name}/{r.name}": json.loads((r / "model.json").read_text(encoding="utf-8")) for r in runs}
    pop = [(lab, c) for lab in models for c in claims]
    pick = rng.sample(pop, n)
    rng.shuffle(pick)
    sents = {s["id"]: s for s in sent.load()}
    items, key = [], {}
    for i, (lab, c) in enumerate(pick, start=1):
        iid = f"c{i:03d}"
        model = models[lab]
        pool = rank_candidates(c, model)   # shown in rank order
        field_sents = [{"id": s["id"], "text": s["text"], "hl": s["id"] == c["sentence_id"]}
                       for s in sent.load() if s["milestone"] == c["milestone"] and s["field"] == c["field"]]
        items.append({"id": iid, "task": "recall", "model": alias[lab], "milestone": c["milestone"], "milestone_name": names[c["milestone"]],
                      "field": sent.FIELD_LABELS[c["field"]],
                      "claim": {k: c[k] for k in ("id", "text", "kind", "owner", "rel_type")},
                      "field_sentences": field_sents, "candidates": pool, "owner_classes": owner_classes(c, model)})
        key[iid] = {"run": lab, "claim": c["id"], "kind": c["kind"], "pool": pool}
    _write("recall", seed, n, len(pop), items, key, alias, {alias[lab]: display_model(m) for lab, m in models.items()})
    print(f"recall: {n} of {len(pop)} (run, claim) pairs over {len(runs)} runs; by kind {_by_kind(c for _, c in pick)}; "
          f"mean pool size {sum(len(k['pool']) for k in key.values()) / n:.1f}")
    by_run = {}
    for lab, _ in pick:
        by_run[lab.split("/")[0]] = by_run.get(lab.split("/")[0], 0) + 1
    print("per condition:", dict(sorted(by_run.items())))


def _by_kind(xs) -> dict:
    out = {}
    for x in xs:
        out[x["kind"]] = out.get(x["kind"], 0) + 1
    return dict(sorted(out.items()))


def _write(task: str, seed: int, n: int, pop: int, items: list, key: dict, alias: dict, models: dict):
    SAMPLE_DIR.mkdir(exist_ok=True)
    (SAMPLE_DIR / f"{task}_items.json").write_text(json.dumps(
        {"task": task, "seed": seed, "n": n, "population": pop, "items": items, "models": models}, ensure_ascii=False), encoding="utf-8")
    (SAMPLE_DIR / f"{task}_key.json").write_text(json.dumps(
        {"task": task, "seed": seed, "n": n, "population": pop, "models": {v: k for k, v in alias.items()}, "items": key},
        indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written sample/{task}_items.json and sample/{task}_key.json; build the page with grade_ui.py sample --task {task} --grader NAME")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task", choices=["precision", "recall"])
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    (draw_precision if args.task == "precision" else draw_recall)(args.n, args.seed)


if __name__ == "__main__":
    main()
