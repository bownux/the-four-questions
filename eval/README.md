# The Four Questions — eval

The shelf's delta, shipped with the book. Task: given (context, transcript,
claim), output a verdict — `supported` / `contradicted` / `insufficient` —
plus a 0–100 confidence. Every transcript is real: produced by executing real
commands in a gate-style sandbox (`PATH=/usr/bin:/bin`, fresh `HOME`, merged
streams) and captured verbatim, per the house honesty rule extended to eval
fixtures. Nothing here was composed by hand to make a point.

## Files

- `cases.json` — the measured corpus: **104 cases**, 12–14 per misreading
  family, verdicts 40 contradicted / 33 supported / 31 insufficient
  (majority-class baseline **0.385** — a reader that always answers
  "contradicted" scores that and no more).
- `cases-seed.json` — 10 earlier seed fixtures kept as scorer smoke tests.
  Not part of the measured corpus.
- `scorer.py` — stdlib-only, runs in the gate sandbox. See its docstring.
- `compact.md` — the condition-(b) treatment: the routine on one page.
- `build/` — the capture harness and the case definitions. Re-running
  `build/fam1_4.py`, `build/fam5_8.py`, and `build/balance.py` re-captures
  every transcript from scratch, which is how the fixtures stay honest when
  a case is edited.

## Hold-out discipline

No case reuses a command line, fixture filename, claim sentence, or data
file from the book's worked examples. The families match the chapters; the
surfaces deliberately do not — where a chapter teaches with `grep`/`app.conf`,
the corpus tests with `tar`, `sha256sum`, `truncate`, `unittest`, CSV
columns, JSON payloads, symlinks, rotated logs, and retry loops.

This is enforced, not asserted: `build/check_holdout.py` diffs every case's
claim, transcript, and fixture names against the manuscript and exits
nonzero on any collision. It found five on its first run — two claim
sentences and three filenames shared with chapter listings — which were
fixed by rewording and renaming, then re-captured. Run it before any
submission.

## Run recipe

```sh
# smoke test, no network: score a hand-written answers file
python3 scorer.py --cases cases.json --answers answers.json

# against a local OpenAI-compatible endpoint, one condition per run
python3 scorer.py --cases cases.json --endpoint http://127.0.0.1:8085/v1/chat/completions \
    --model <served-model> --condition none    --out results-none.json
python3 scorer.py --cases cases.json ... --condition compact --out results-compact.json
python3 scorer.py --cases cases.json ... --condition book    --out results-book.json
```

Condition `book` requires `eval/book.md` — the concatenated chapters —
which `build/make_book.py` generates and `.gitignore` keeps untracked, so
the manuscript stays the single source. A committed copy would be a second
text that drifts from the chapters the moment either is edited. Run
`python3 build/make_book.py` before any `--condition book` run. Three runs per condition (temperature 0 still varies
across servers); report mean ± range.

## Pilot runs

`build/pilot.py` runs a stratified subset against a live endpoint with
per-case progress logging — for proving the harness end-to-end and getting a
preliminary signal without committing to the full 3×3 design:

```sh
python3 build/pilot.py --per-family 3 --conditions none,compact \
    --endpoint http://127.0.0.1:8085/v1/chat/completions --model <served-model>
```

It writes `pilot-<condition>.json` (gitignored). A pilot is **not** the
promotion measurement: one run, a subset, no noise floor. Nothing from a
pilot belongs in the book.

## Metrics

- **Accuracy**, overall and per-family. Unparseable answers score as wrong —
  a reader that cannot state its verdict has failed the transcript-reading
  task, not the parsing task.
- **Brier score** on confidence, read as the forecast probability that one's
  own verdict is correct: `(confidence/100 − correct)²`, mean over parsed
  answers. Lower is better.
- **Reference points.** Oracle (gold answers at 85 confidence) scores
  accuracy 1.000 / Brier 0.023. The three degenerate single-verdict readers
  score 0.385, 0.317, and 0.298 accuracy. Any real result belongs between
  those.

## Proposed promotion thresholds (author's proposal, judge decides)

- Headline: the `book − none` accuracy delta must exceed the noise floor
  (max range observed across the 3×3 runs) — a delta inside the noise is a
  null result and the book says so.
- `compact` is reported beside it, always: a book that only matches its own
  one-page summary has an honest problem this line exists to surface.
- Brier under `book` must not be worse than under `none` — a treatment that
  raises accuracy while wrecking calibration teaches confidence, not reading.

## Provenance of fixtures

Captured 2026-08-28/29 on the authoring machine (Gentoo Linux), gate-style
sandbox. Two capture lessons are on the record because they changed the
fixtures. A `ps`-based case initially matched the capture harness's own
wrapper process, whose command line contained the searched-for name — the
fixture leaked session internals and its rationale was false against it;
re-captured with the target name assembled at runtime. And a first audit
pass of the corpus found four cases whose rationales cited facts that were
true of the scenario but absent from the captured transcript (a config file
that was never printed, a log line below a truncation point); those gold
labels were corrected to `insufficient` or their fixtures extended to show
the evidence, because a case is only as good as what its transcript actually
contains. Both lessons are the book's own subject matter, applied to the
book.
