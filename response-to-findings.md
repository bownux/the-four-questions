# Response to Pass-2 findings — rogerai-labs--the-four-questions v1 → v2

Panel: SALVAGEABLE × 3 (xiaomi/mimo, muse, tencent/hy3). Every blocking finding
below is answered as **fixed** (with the substance of the diff) or **rebutted**
(with evidence). Suggestions are acknowledged; only blocking debts were required.

## Critic A (mimo-v2.5-free · xiaomi)

| # | Status | Answer |
|---|---|---|
| A1 | **Fixed** (paired with B1) | Front matter Introduction no longer states the curriculum “measurably improves” as a demonstrated fact. It now says the improvement is **proposed and testable, not yet measured**, and that the judge grades the exam. Provenance already said this; the intro is aligned. |
| A2 | **Fixed** | ch07 “gap between checking and using” now carries a **worked TOCTOU** with live transcripts: (1) atomic `noclobber` exclusive create (A wins, B refused); (2) stale check-then-act that writes on an old “absent” observation after a concurrent create. |
| A3 | **Fixed** | ch01 `$?` prose rewritten: expansion happens *before* the next command runs; `echo "exit: $?"` immediately after a command is correct; what fails is an intervening command, not inherent corruption. |
| A4 | **Accepted as non-blocking** (critic downgraded) | Still addressed under B5: swallowed-failure demos now state the `set -e` / `pipefail` off precondition explicitly. |

## Critic B (muse-spark-1.2-contributor-free · muse)

| # | Status | Answer |
|---|---|---|
| B1 | **Fixed** | Same intro qualification as A1 (high severity). |
| B2 | **Fixed** | ch01 upper band: new **Disambiguation rule** — 126/127/128+N are conventional, tools may exit the same integers voluntarily; `143` alone cannot prove SIGTERM; cap confidence without a bridge; prefer insufficient on specific-signal/OOM claims. |
| B3 | **Fixed** | ch04 vault/`chmod 000` demo: comment in listing + prose **Replication condition: non-root** (root traversal would contradict the lesson). |
| B4 | **Fixed** | ch05: **Operational requirement for process-table listings** — harness must not carry the pattern in its own `args=`; assemble at runtime / self-avoiding patterns. Listings pinned to `ps -eo args=` (procps). |
| B5 | **Fixed** | ch02: **Precondition for swallowed-failure demos** — `errexit`/`pipefail` off (bash defaults); claims that “exit 0 means the aggregate was fine” must size against option state. |
| B6 | **Fixed** | ch03: **CPython note** — `print` under a pipe is interpreter-buffered; not fully described by `setvbuf(3)`; use `python3 -u` / `PYTHONUNBUFFERED=1`; listing assumes default CPython pipe. |
| B7 | **Fixed** | `ps ax -o` → `ps -eo args=` throughout; back matter **Portability pin (process table)** documents procps/GNU, not pure POSIX. |

## Critic C (hy3-free · tencent)

| # | Status | Answer |
|---|---|---|
| C1 | **Fixed + partial rebuttal** | Provenance now states zero mismatches as the result of an **author-run** of in-tree `.listings/verify.py` at this SHA, and that third parties re-run the harness rather than take the sentence on faith. Back matter adds **Harness custody**: paths are in the repo; a review packet that omits the tree has deferred verification, not falsified it. **Rebuttal piece:** the critic packet’s omission of harness files is not evidence the harnesses are absent from the submission SHA — they are at `.listings/` and `eval/build/` in https://github.com/bownux/the-four-questions. |
| C2 | **Fixed** | Reference 21 no longer cites only `https://oailly.com/`. It lists the three trilogy reader URLs on oailly.com that carry the writing-side contract this volume reads against. |

## Gate

Local Pass-1 at this revision: **PASS 0/0**, measured body words updated in
`manifest.json` / `pass1-report.json`.

## Not done in this cycle (by design)

- Running the promotion eval (none/compact/book) and publishing accuracy/Brier
  numbers — still the judge’s exam; the book continues to refuse author-graded
  results.
- Non-blocking suggestions (TOC entry polish, denser commentary examples, etc.)
  unless they fell out of a blocking fix.
