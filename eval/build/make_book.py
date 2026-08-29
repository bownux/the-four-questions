#!/usr/bin/env python3
"""Produce eval/book.md, the condition-(c) treatment, from the chapters.

Generated rather than committed so the manuscript stays the single source:
a committed copy would be a second text that drifts from the chapters the
moment either is edited, which is the failure this book spends chapter 6
calling an assertion.
"""
from pathlib import Path

EVAL = Path(__file__).resolve().parent.parent
BOOK = EVAL.parent
chapters = sorted(BOOK.glob("ch0*.md"))
if not chapters:
    raise SystemExit("no chapters found next to eval/")
text = "\n\n".join(c.read_text() for c in chapters)
(EVAL / "book.md").write_text(text)
print(f"wrote eval/book.md from {len(chapters)} chapters: {len(text)} chars")
