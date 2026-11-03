"""Split the document into sentences.

Each field of each milestone is split into sentences. A bullet line is a
sentence. Sentence ids are M<n>.<field>.<k>, with <field> one of the eight
field keys of milestones.json and <k> counting from 1. The split is
deterministic and is the only preprocessing the claim inventory receives.

  python src/evaluate/sentences.py              # rewrites src/evaluate/sentences.json, prints counts
  python src/evaluate/sentences.py --show 1     # prints the sentences of milestone 1 (rewrites sentences.json too)

The committed sentences.json is the frozen split that the claim inventory and both samples refer to.
"""
import argparse
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
MILESTONES = SRC / "data" / "milestones.json"
OUT = SRC / "evaluate" / "sentences.json"

FIELDS = ["definition", "origin_and_priority", "timing", "data_quality", "effect",
          "procedures", "operational_status", "action_on_cdm"]
FIELD_LABELS = {"definition": "Definition", "origin_and_priority": "Origin and priority", "timing": "Timing",
                "data_quality": "Data Quality", "effect": "Effect", "procedures": "Procedures",
                "operational_status": "Operational Status (changes to)", "action_on_cdm": "Action on CDM Operation (ACISP)"}

# Abbreviations in the document whose full stop must not end a sentence.
PROTECT = ["e.g.", "i.e.", "N. A.", "N.A.", "etc.", "approx.", "hr.", "min."]
_PLACEHOLDER = "․"  # one dot leader, never in the document


def _protect(text: str) -> str:
    for a in PROTECT:
        text = text.replace(a, a.replace(".", _PLACEHOLDER))
    # section numbers such as 3.7.3 and decimals such as 0.5
    text = re.sub(r"(?<=\d)\.(?=\d)", _PLACEHOLDER, text)
    return text


def _restore(text: str) -> str:
    return text.replace(_PLACEHOLDER, ".")


def split_field(text: str) -> list[str]:
    """Sentences of one field, in order, whitespace-normalised."""
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("-"):           # a bullet is one sentence
            out.append(line)
            continue
        line = _protect(line)
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"'])", line)
        out.extend(_restore(p).strip() for p in parts if p.strip())
    return out


def build() -> list[dict]:
    milestones = json.loads(MILESTONES.read_text(encoding="utf-8"))
    sentences = []
    for ms in milestones:
        n = ms["number"]
        for field in FIELDS:
            for k, s in enumerate(split_field(ms["fields"][field]), start=1):
                sentences.append({"id": f"M{n}.{field}.{k}", "milestone": n, "field": field, "k": k, "text": s})
    return sentences


def load() -> list[dict]:
    if not OUT.exists():
        OUT.write_text(json.dumps(build(), indent=1, ensure_ascii=False), encoding="utf-8")
    return json.loads(OUT.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=None)
    args = ap.parse_args()
    sentences = build()
    OUT.write_text(json.dumps(sentences, indent=1, ensure_ascii=False), encoding="utf-8")
    if args.show:
        for s in sentences:
            if s["milestone"] == args.show:
                print(f"{s['id']:34} {s['text']}")
        return
    per_ms = {}
    for s in sentences:
        per_ms[s["milestone"]] = per_ms.get(s["milestone"], 0) + 1
    print(f"{len(sentences)} sentences, {sum(len(s['text'].split()) for s in sentences)} words")
    print("per milestone:", " ".join(f"M{k}={v}" for k, v in sorted(per_ms.items())))
    print(f"written {OUT.relative_to(SRC.parent)}")


if __name__ == "__main__":
    main()
