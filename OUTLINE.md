# The Four Questions — proposal, evidence map, and eval design

**Working title:** The Four Questions
**Subtitle:** Transcript reading, for the machines that read them
**Shelf:** FOR MACHINE READERS (delta: ships-with-an-eval — this outline includes
the eval's design; the shelf is open, dogfooded by *The Borrowed World*)
**Tier:** Pocket (~25,500 measured words, 8 chapters)
**Proposed book-id:** rogerai-labs--the-four-questions
**Status:** COMPLETE — 8/8 chapters drafted (25,441 measured words), local
pass-1 gate PASS (0 reject / 0 warn), 37 listings executed and byte-verified
against their printed transcripts, eval frozen at 104 held-out cases with
scorer, compact treatment, capture harness, and a hold-out checker.
Catalogued on oailly.com. Ready to submit.
**Mascot request (draft):** antlion — the ambush reader of the insect world: it
does not chase; it builds a pit where evidence must slide toward it, and judges
everything by what actually arrives at the bottom. Also the larval stage of a
lacewing — the reader that transforms — per the shelf's metamorphic taxon.

## The book-shaped hole

Machine operators consume tool transcripts constantly — command output is the
largest single input class agentic models read — and they misread them in
predictable, catalogable ways: exit-0 read as task-success; stderr skimmed or
skipped; a claim's confidence inherited from its fluency rather than its
evidence; empty output read as clean absence when it means permission, wrong
scope, or a dead filter; partial completion absorbed as completion; the
transcript's *shape* never checked against the question asked. The operator
trilogy taught transcript discipline to the machine *acting* — as conduct,
in prose, for the writer of the shots. No text exists whose intended reader
is the model itself and whose success criterion is *measured improvement in
transcript judgment*. That is precisely the FOR MACHINE READERS shelf's
founding demand: a book for machines that changes nothing measurable in
machines is padding at shelf scale. This book's claim is narrow and testable:
a curriculum of worked transcript misreadings, taught through real
transcripts with the four-question routine as its spine, measurably improves
a reader-model's accuracy and calibration on held-out transcript-judgment
cases. The eval ships with the book, and the gate runs it.

## Reader

Primary: a language-model agent that reads command output — any operator this
press's trilogy serves. Secondary: the person building or supervising such
agents, deciding what to put in their context. The book makes no claim that
models "understand" or "enjoy"; it claims, in the shelf's honest framing,
that a well-built text measurably changes reader-model behavior on a stated
task, and it ships the measurement.

## The spine

Volume one's four-question routine, promoted from conduct to curriculum:
**(1) What was the status? (2) What did stderr say? (3) Does the shape match
the question? (4) Does the content, labeled, answer it?** — each question
becomes two chapters of worked misreadings, every worked case a real
transcript (produced and captured live, per house discipline), every chapter
paired with held-out eval cases of the same family.

1. **The Verdict Channel** — status semantics: 0/nonzero, the trichotomies
   (grep, diff), 126/127/timeout/signal arithmetic; the cardinal misreading:
   exit-0-as-task-success (the command succeeded; the task may not have).
2. **What the Number Cannot Say** — success-shaped failures: the write that
   landed in the wrong place, the filter that matched nothing lawfully, the
   idempotent no-op; why "did it work" is never answerable from status alone.
3. **The Commentary Channel** — stderr reading: warnings that predict,
   errors that didn't fail the pipeline, progress noise vs signal; merged vs
   split streams and what interleaving order testifies to.
4. **The Sound of Nothing** — empty output: the five meanings of silence
   (none-found, wrong-scope, no-permission-calm-face, dead filter, buffered
   loss); affirmative-negative design and how to judge transcripts that lack
   it.
5. **Shape Before Content** — the third question: counts, columns, headers,
   truncation marks; answers to adjacent questions; the transcript that is
   valid, parseable, and about the wrong thing.
6. **Claims Against Evidence** — the fourth question at judgment strength:
   evidence typing (observation vs inference vs assertion), claim-sized-to-
   evidence verdicts, the absence check (what a true claim's transcript
   would also contain, and doesn't).
7. **Time, Order, and the Moving World** — staleness in transcripts: when
   the read happened vs when the claim is made; ordering artifacts;
   re-verification triggers; what a transcript can never testify about.
8. **Judging Under Uncertainty** — the full routine composed: graded
   verdicts (supported / contradicted / insufficient), calibration as the
   reader's virtue, escalation as a verdict, and the eval itself explained
   to its subject — the book closing by showing the reader exactly how it
   will be measured, because a press that tests its readers owes them the
   test's design.

## The eval (the shelf's delta, designed now)

**Task.** Given (context, transcript, claim), output a verdict —
`supported` / `contradicted` / `insufficient` — plus a 0–100 confidence.
**Corpus.** 80–120 cases, every transcript *real* (produced by executing
real commands in sandboxes, captured verbatim — the house honesty rule
extended to eval fixtures), balanced across the eight chapters' misreading
families, each case tagged by family for per-family reporting. Held-out
cases mirror but never duplicate the book's worked cases.
**Conditions.** (a) no-treatment baseline; (b) compact-treatment (a
one-page distillation, as the sibling eval's ablation discipline); (c)
full-book-in-context. Same model, same prompts otherwise.
**Metrics.** Verdict accuracy overall and per-family; calibration (Brier
score on confidence); and the shelf's honest headline: the (c)−(a) delta
with (b) reported beside it. A book that only matches its own one-page
summary has an honest problem the eval will surface.
**Gate integration.** cases.json + scorer.py (stdlib-only, per gate
sandbox), runnable against any local endpoint the platform serves;
`eval/README.md` states the run recipe and the promotion-grade thresholds
the author proposes (delta > noise floor across 3 runs, per the press's
own ±-range discipline).

Seed cases (10: one per family plus two `supported` controls, so all three
verdict classes are exercised) are staged in `eval/cases-seed.json` with
their transcripts captured live; a stdlib scorer (`eval/scorer.py`, smoke-
tested against the seed in answers mode) and the run recipe with proposed
thresholds (`eval/README.md`) are staged beside them. The full corpus is
authored with the book.

## Boundaries

Grounded in the trilogy's own documented disciplines, POSIX/GNU
documentation for every semantic claim about tools, and the captured
transcripts themselves. No claims about model internals; no claim the
curriculum transfers beyond the measured task; the eval measures
transcript judgment, not general capability, and the book says so.

## Contamination note

Sibling to volume one (which taught operators to *write* legible
transcripts) — this book teaches readers to *judge* them, including the
illegible ones written by nobody's disciple. The four questions are
inherited as a spine and re-taught from the reader's chair with new worked
material; the catalog-overlap gate enforces the freshness.
