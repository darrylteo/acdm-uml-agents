"""Extract the 16 A-CDM milestone tables from the source PDF into structured JSON
and a canonical plain-text document for the agents.

Usage: python src/ingest/parse_milestones.py [pdf_path]
Writes src/data/milestones.json and src/data/document.txt.
"""
import json
import re
import sys
from pathlib import Path

import pdfplumber

SRC = Path(__file__).resolve().parents[1]
PDF = SRC / "data" / "acdm milestone only.pdf"
OUT_JSON = SRC / "data" / "milestones.json"
OUT_TXT = SRC / "data" / "document.txt"

# Field labels in the order they appear in every milestone table. The regex
# tolerates line breaks inside multi-word labels.
FIELDS = [
    ("definition", r"Definition"),
    ("origin_and_priority", r"Origin\s+and\s+priority"),
    ("timing", r"Timing"),
    ("data_quality", r"Data\s+Quality"),
    ("effect", r"Effect"),
    ("procedures", r"Procedures"),
    # The last two labels span two table rows and interleave with the content
    # column in extracted text, so anchor on the first line and strip the rest.
    ("operational_status", r"Operational\s+Status"),
    ("action_on_cdm", r"Action\s+on\s+CDM"),
]
LABEL_REMNANTS = {
    "operational_status": [r"\(changes\s+to\)"],
    "action_on_cdm": [r"Operation\s*\(ACISP\)"],
}
LABELS = {
    "definition": "Definition",
    "origin_and_priority": "Origin and priority",
    "timing": "Timing",
    "data_quality": "Data Quality",
    "effect": "Effect",
    "procedures": "Procedures",
    "operational_status": "Operational Status (changes to)",
    "action_on_cdm": "Action on CDM Operation (ACISP)",
}

KEEP_HYPHEN = {"off", "in", "pre", "turn", "push", "non", "start", "re", "air", "take", "up", "t", "e", "a", "c"}

HEADER = re.compile(r"MILESTONE\s+(\d+)\s+(.+)")
PAGE_FOOTER = re.compile(r"^\s*3-\d+\s*$", re.M)
SECTION_HEADER = re.compile(r"^\s*3\.\s*IMPLEMENTATION\s*$", re.M)


def clean(text: str) -> str:
    text = PAGE_FOOTER.sub("", text)
    text = SECTION_HEADER.sub("", text)
    text = text.replace("–", "-").replace("�", "-").replace("’", "'")
    text = text.replace("“", '"').replace("”", '"')
    # The PDF's square bullet glyph extracts as a bare "n", at line start or
    # mid-line after "by" / ":".
    text = re.sub(r"^n (?=[A-Za-z])", "- ", text, flags=re.M)
    text = re.sub(r"(\bby|:) n (?=[A-Za-z])", r"\1 - ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_fields(body: str) -> dict:
    """Split the table body into fields by locating each label in order."""
    positions = []
    for key, pattern in FIELDS:
        m = re.search(pattern, body)
        if not m:
            raise ValueError(f"label not found: {key}")
        positions.append((key, m.start(), m.end()))
    positions.sort(key=lambda p: p[1])
    fields = {}
    for i, (key, start, end) in enumerate(positions):
        stop = positions[i + 1][1] if i + 1 < len(positions) else len(body)
        content = body[end:stop]
        for remnant in LABEL_REMNANTS.get(key, []):
            content = re.sub(remnant, "", content)
        # Keep bullets on their own lines; join ordinary wrapped lines with a space.
        # Re-join words the PDF hyphenated at line ends, but keep the hyphen in
        # the document's own compound terms (off-block, turn-round, push-back...).
        content = re.sub(
            r"(\w+)-\n(?=[a-z])",
            lambda m: m.group(1) + ("-" if m.group(1).lower() in KEEP_HYPHEN else ""),
            content)
        content = re.sub(r"\n(?!- )", " ", content)
        fields[key] = re.sub(r"[ \t]+", " ", content).strip()
    return fields


def parse(pdf_path: Path) -> list:
    milestones = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = clean(page.extract_text() or "")
            m = HEADER.search(text)
            if not m:
                continue
            number = int(m.group(1))
            name = m.group(2).strip()
            body = text[m.end():]
            fields = split_fields(body)
            milestones.append({"number": number, "name": name, "page": page_no, "fields": fields})
    milestones.sort(key=lambda x: x["number"])
    return milestones


def to_document(milestones: list) -> str:
    blocks = []
    for ms in milestones:
        lines = [f"MILESTONE {ms['number']}: {ms['name']}"]
        for key, _ in FIELDS:
            lines.append(f"{LABELS[key]}: {ms['fields'][key]}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF
    milestones = parse(pdf_path)
    numbers = [m["number"] for m in milestones]
    assert numbers == list(range(1, 17)), f"expected milestones 1-16, got {numbers}"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(milestones, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT_TXT.write_text(to_document(milestones), encoding="utf-8")
    print(f"wrote {OUT_JSON} ({len(milestones)} milestones) and {OUT_TXT}")


if __name__ == "__main__":
    main()
