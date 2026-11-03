"""Name normalisation shared by the sampling, inventory and structure code.

Names are folded (camelCase and separators split, lowercased), abbreviations
are expanded from the manual's own list (evaluate/abbreviations.json), tokens
are lightly singularised, and a few function words are dropped. Two names
normalise to the same key when the resulting token bags are equal, in any
order. For classes, the document's own labels for its sixteen items
('milestone', 'event', and the 'M<n>' numbering) are ignored, so 'OffBlock',
'OffBlockMilestone', and 'M15OffBlock' are one class.

  python src/evaluate/match.py "TobtFeasibilityCheck" "Target Off-Block Time"   # print the keys
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
ABBREVIATIONS = SRC / "evaluate" / "abbreviations.json"

STOPWORDS = {"of", "the", "a", "an", "and"}
CLASS_AFFIXES = {"milestone", "event"}                # the manual's labels for its sixteen items
MILESTONE_NUMBER = re.compile(r"m\d{1,2}")            # 'M9', 'M15'
TIME_PREFIXES = {"scheduled", "estimated", "target", "actual", "calculated"}   # the five prefixes scaffold.md names
TEXT_STOPWORDS = STOPWORDS | {"to", "in", "on", "for", "by", "at", "is", "are", "be", "as", "or", "with",
                              "from", "that", "this", "it", "its", "which", "when", "if", "not", "used"}


def _load_abbreviations() -> dict[str, str]:
    """Upper-cased keys, each also indexed without its hyphen ('T-DPI' and 'TDPI')."""
    d = json.loads(ABBREVIATIONS.read_text(encoding="utf-8"))
    out = {}
    for k, v in (d["abbreviations"] | d["document_defined"]).items():
        out[k.upper()] = v
        out.setdefault(k.upper().replace("-", ""), v)
    return out


ABBR = _load_abbreviations()


def _split(name: str) -> list[str]:
    """'TobtFeasibilityCheck' -> ['Tobt','Feasibility','Check']; 'A-SMGCS' -> ['A','SMGCS']."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)          # camelCase boundary
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)           # 'CDMPlatform' -> 'CDM Platform'
    return [t for t in re.split(r"[^A-Za-z0-9]+", s) if t]


def _singular(tok: str) -> str:
    if len(tok) <= 3 or not tok.endswith("s") or tok.endswith(("ss", "us", "is")):
        return tok
    if tok.endswith("ies"):
        return tok[:-3] + "y"
    if tok.endswith(("sses", "uses", "xes", "ches", "shes")):
        return tok[:-2]
    return tok[:-1]


def tokens(text: str) -> list[str]:
    """Folded, abbreviation-expanded, singularised tokens of a name or a sentence."""
    raw = text.strip()
    if raw.upper() in ABBR:                                       # whole name is an abbreviation
        return tokens(ABBR[raw.upper()])
    toks = _split(raw)
    out: list[str] = []
    i = 0
    while i < len(toks):
        t = toks[i]
        two = f"{t}-{toks[i + 1]}".upper() if i + 1 < len(toks) else None
        if two in ABBR:                                           # 'E', 'Dpi' -> E-DPI
            out.extend(_split(ABBR[two])); i += 2; continue
        one = t.upper() if t.upper() in ABBR else _singular(t).upper()   # 'Eldts' -> ELDT
        if one in ABBR:
            out.extend(_split(ABBR[one])); i += 1; continue
        out.append(t); i += 1
    return [_singular(w.lower()) for w in out]


def normalise(name: str, kind: str = "member") -> str:
    """The matching key for a name; equal keys mean a match. Tokens are sorted, so
    word order does not matter. For kind 'class' the document's item labels are
    dropped ('OffBlockMilestone' -> 'block off'); a name made only of those labels
    ('Milestone', 'MilestoneEvent') keys on 'milestone' so the superclass matches."""
    toks = [w for w in tokens(name) if w not in STOPWORDS]
    if kind == "class":
        core = [w for w in toks if w not in CLASS_AFFIXES and not MILESTONE_NUMBER.fullmatch(w)]
        toks = core or ([w for w in toks if w == "milestone"] or toks)
    return " ".join(sorted(toks))


def content_words(text: str) -> set[str]:
    return {w for w in tokens(text) if w not in TEXT_STOPWORDS and not w.isdigit()}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0


def main():
    for n in sys.argv[1:]:
        print(f"{n!r:40} -> class {normalise(n, 'class')!r}   member {normalise(n)!r}")


if __name__ == "__main__":
    main()
