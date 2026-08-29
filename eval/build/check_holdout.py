#!/usr/bin/env python3
"""Verify the corpus is held out from the book's worked examples.

Checks three collision classes: a case's claim sentence appearing in the
manuscript, a case's transcript appearing verbatim, and fixture filenames
shared between a case and any chapter listing. Exits nonzero on any hit, so
this runs as a pre-submission check rather than living as a promise in prose.
"""
import json, re, sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[2]
FIXTURE_RE = re.compile(
    r"\b[\w.-]+\.(?:txt|conf|log|json|csv|sh|py|bin|ini|tar|tgz|jar|tbl|env|md|chk|pdf|c)\b")

book_text = " ".join(f.read_text() for f in sorted(BOOK.glob("ch*.md"))).lower()
book_listings = "\n".join(
    m for f in sorted(BOOK.glob("ch*.md"))
    for m in re.findall(r"```bash\n(.*?)```", f.read_text(), re.S))
book_fixtures = set(FIXTURE_RE.findall(book_listings.lower()))

cases = json.loads((BOOK / "eval" / "cases.json").read_text())["cases"]
hits = []
for c in cases:
    if c["claim"].lower().rstrip(".") in book_text:
        hits.append(f"{c['id']}: claim sentence appears in the manuscript")
    if len(c["transcript"]) > 25 and c["transcript"].lower() in book_text:
        hits.append(f"{c['id']}: transcript appears verbatim in the manuscript")
    shared = FIXTURE_RE.findall((c["transcript"] + " " + c["context"]).lower())
    overlap = sorted(set(shared) & book_fixtures)
    if overlap:
        hits.append(f"{c['id']}: shares fixture filename(s) with a chapter listing: {overlap}")

if hits:
    print(f"HOLD-OUT VIOLATIONS ({len(hits)}):")
    for h in hits:
        print("  " + h)
    sys.exit(1)
print(f"hold-out clean: {len(cases)} cases, no claim, transcript, or fixture collisions")
