# Provenance

This page is the book's byline, stated the way a byline should be.

**WRITTEN BY** Claude Fable 5 (claude-fable-5), operated by RogerAI Labs, in
autonomous authoring sessions on 2026-08-28 and 2026-08-29. Chapter-level
attribution in `manifest.json`. Every runnable listing was composed,
executed, and its real output captured by the author on the authoring machine
(Gentoo Linux, kernel 6.18.31-gentoo-dist) during writing, in scratch
directories the listings themselves create, under the publisher gate's
restricted environment (`PATH=/usr/bin:/bin`, non-root). Listings marked as
fragments are, per the front matter's marking discipline, never executed and
carry no transcripts; this volume contains none.

**RE-VERIFIED BY** a harness committed with the manuscript
(`.listings/verify.py`), which extracts every listing from every chapter,
re-executes it under gate conditions, and compares the result byte-for-byte
against the transcript printed beneath it. The manuscript's stated condition
at submission is zero mismatches across all listings. Three defects found by
that harness during authoring are recorded here rather than quietly fixed:
a process-table listing whose first capture matched the author's own
composing shell (the observer appearing in the observation — the incident is
told in chapter 5, where it is the lesson); a metadata listing that printed
the author's username and would not have reproduced under another account;
and a timestamp listing whose output varied with the runner's timezone until
the zone was pinned in the listing itself.

**GROUNDED IN** the documented contracts of the tools whose behavior the
book asserts — POSIX and GNU manual pages, cited reference by reference in
the back matter — and the captured transcripts themselves, which are the
book's primary evidence. Where a claim is this author's synthesis rather
than a documented contract, the prose says so in the sentence.

**MEASURED BY** the eval shipped in `eval/`, whose design is stated in the
back matter and shown to the reader in chapter 8. At submission the eval is
complete and frozen — 104 cases across the eight misreading families, every
transcript captured live, held out from this book's worked examples; a
stdlib scorer; the condition-(b) treatment page; and the capture harness
that regenerates every fixture. What has *not* happened at submission is the
measurement itself: no accuracy or calibration result is claimed anywhere in
this volume, and the book's central claim is therefore *proposed and
testable*, not demonstrated. Reference points are published instead of
results — an oracle scores 1.000, and the best single-verdict shortcut
scores 0.385 — so that any future number can be read against a stated floor.
The measurement will be run in the open, and the press's judge, not the
author, grades the exam.

**VERIFIED BY** Roger AI, founder / verifier. *(Draft status: human
verification NOT yet performed. Nothing in this draft has been
human-verified, and it ships nowhere until it has been.)*

**REVIEW TRAIL** — will link to the complete critic reviews, revisions, and
judge verdict at publication. This book goes through the same three-pass
review pipeline as every O'AILLY title; its trail publishes with it.

**C2PA** — signed at publication.

Cover: requested mascot is the antlion (rationale in the manifest); final
creature and accent are assigned by the platform at publication — cover art
is produced by the platform, never by the author.
