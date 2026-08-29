# Back Matter

## The routine, on one page

Asked of every transcript, in this order, because each question's answer
changes what the next one can mean.

**1. What was the status?** Find the verdict for the command under judgment
and confirm it belongs to that command. Translate it under the tool's
documented contract, not the flat nonzero-is-failure rule: trichotomy tools
spend 1 on an answer, the shell's band (126, 127, 128+signal) reports deaths
that were never really runs, and some tools are documented apostates.
Pipelines report their last member unless `pipefail` or `PIPESTATUS` says
otherwise. Nonzero convicts the command; zero acquits the command and says
nothing about the task.

**2. What did stderr say?** Establish first whether the commentary channel
was captured at all — merged, split, or discarded — because a no-warnings
claim needs a record that could have held warnings. Classify each line by
species (diagnosis, warning, progress, notice, debug) and bind it to the
command it narrates by content and label, never by adjacency. Diagnoses
explain statuses; warnings survive success and cap confidence; a diagnosis
inside a clean run may mean recovery, absorption, or a relayed child's
voice.

**3. Does the shape match the question?** Name, in one sentence, the
question the output actually answers. Compare its scope, frame, units, and
labels against the claim's. Watch for truncation marks and round counts;
subtract the observer from views that include their own production; ask of
any aggregate whether it would look different if the claim were false. When
output is empty, type the silence: none-found, wrong scope, suppressed
obstruction, dead filter, or lost in production.

**4. Does the content, labeled, answer it?** Grade each line — observation,
inference, assertion — and let observation beat inference beat assertion in
any disagreement. Restate the claim with its scope, strength, tense, and
subject explicit. Name the residue a true instance would leave, then look
for it. Compound claims take the verdict of their weakest conjunct. Then
choose: supported, contradicted, or insufficient — and say what would
settle an insufficient.

## The three verdicts

**supported** — the transcript is evidence the claim is true, sized to what
was actually observed. **contradicted** — the transcript is evidence the
claim is false; one in-scope counterexample is enough. **insufficient** —
the transcript cannot settle the claim either way, whether from partial
scope, missing residue, assertion-grade evidence, an unsupported bridge, or
staleness. The third verdict is a finding, not a failure, and the report
that carries it names the observation that would resolve it.

## Glossary

- **absence check** — asking what else would be present if the claim were true, and noticing it is not.
- **adjacent answer** — a valid, parseable transcript about a neighboring question; fails the shape check for the claim under trial.
- **assertion** — transcript text that someone (tool banner, operator echo) stated; evidence of stating, not of the stated fact.
- **Brier score** — mean squared error of confidence-as-probability against correctness; calibration metric in the eval.
- **bridge** — the unstated assumptions that turn an observation into a wider claim; must be cited or the verdict stays insufficient.
- **claim-sizing** — matching the claim's quantifiers and scope to the transcript's actual scope.
- **commentary channel** — stderr and merged-stream warnings/progress; chapter 3's surface.
- **compact treatment** — the one-page distillation used as eval condition (b) beside full-book and no-treatment.
- **Δ (gap)** — chapter 7's shorthand for the distance between when the instrument ran and when the claim is about; sized against the failure modes that fit inside it.
- **contradicted** — verdict: the transcript is evidence the claim is false.
- **escalation** — disciplined exit when insufficient cannot end the work: ask for evidence or hand a human the labeled chain.
- **four questions** — status; stderr; shape; labeled content — in that order.
- **inference** — a conclusion that requires a bridge from observation to claim.
- **insufficient** — verdict: the transcript cannot settle the claim either way; a complete answer.
- **observation** — a value the instrument reported directly in the bytes.
- **re-verification trigger** — deploy, restart, failover, rotation, or similar event that voids pre-trigger present-tense claims.
- **self-matching instrument** — a capture that counted the harness or scraper itself; a shape/provenance failure.
- **shape** — instrument, target, unit, frame, provenance, truncation, scope — before content is read.
- **staleness** — relation between the moment of reading and the moment the claim is about, when the gap admits relevant failure modes.
- **supported** — verdict: the transcript is evidence the claim is true.
- **T_read / T_claim** — chapter 7's labels for the moment the instrument ran and the moment the claim is about; naming both is what makes Δ measurable rather than felt.
- **trichotomy** — tools (grep, diff) that spend nonzero exits as answers, not only as failures.
- **unit** — what a count counts (lines, records, bytes, events); part of shape.
- **verdict channel** — the exit status integer; chapter 1's surface.

## The eval

Design, thresholds, and run recipe: `eval/README.md`. Task: given (context,
transcript, claim), emit a verdict and a 0–100 confidence. Corpus: 104
cases, 12–14 per misreading family, every transcript real, held out from this
book's worked examples by command line, fixture, and claim — enforced by
`eval/build/check_holdout.py`, which exits nonzero on any collision.
Verdicts are 40 contradicted, 33 supported, 31 insufficient, so the best
single-verdict shortcut scores 0.385 and an oracle scores 1.000 — the floor
and ceiling any result must sit between. Conditions: no-treatment, compact
one-page distillation (`eval/compact.md`), full book in context; three runs
each, mean ± range. Metrics: accuracy overall and per family, Brier score on
confidence, headline delta (full-book − baseline) against the noise floor
with the compact condition reported beside it. Proposed promotion
thresholds: delta above the noise floor, and Brier under the full-book
condition no worse than baseline. No measurement result is claimed in this
volume; the press's judge grades the exam.

## Marking discipline

Runnable listings are re-executed by the publisher's acceptance gate.
`no-run` marks author-executed listings outside the gate's per-book
execution budget — unused in this volume. Fragments are never executed —
none appear in this volume. Beyond the gate, `.listings/verify.py` re-runs
every listing under gate conditions and compares output byte-for-byte
against the printed transcript.

## Measured-output conditions

All transcripts were captured on Gentoo Linux (kernel 6.18.31-gentoo-dist)
with GNU userland, under `PATH=/usr/bin:/bin` with a scratch `HOME`,
non-root, streams merged. GNU behavior is assumed where GNU and POSIX
differ; the relevant instances are `stat -c` format strings, `grep -r`,
`ls`, `sed -i`, and `touch -d`, none of which are POSIX-portable spellings.
Listings that would otherwise vary by machine pin what they can: `TZ=UTC` is
exported where a timestamp is printed, process-table listings match on a
name the harness does not itself carry, and no listing prints a username,
process id, or wall clock.

## References

Each reference is cited for the specific contract the text asserts; all URLs
resolved at submission.

1. GNU grep manual — exit status 0/1/2 and the `-q` caveat.
   https://man7.org/linux/man-pages/man1/grep.1.html
2. GNU grep manual — Exit Status section; `-c` counts selected lines.
   https://www.gnu.org/software/grep/manual/grep.html#Exit-Status
3. GNU diffutils manual — diff exit status 0 (same), 1 (different), 2
   (trouble). https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html
4. GNU diffutils manual — Invoking cmp: "An exit status of 0 means no
   differences were found, 1 means some differences were found, and 2 means
   trouble." https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html
5. GNU Bash manual — exit status conventions: 128+N for fatal signal N, 127
   for command-not-found, 126 for found-but-not-executable; pipeline status
   and `pipefail`; `PIPESTATUS`; `for` returns its last command's status;
   redirections performed as part of command setup; the `time` keyword's
   output on stderr. https://www.gnu.org/software/bash/manual/bash.html
6. POSIX Shell Command Language — exit status and special parameters.
   https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_08_02
7. GNU coreutils manual, timeout — 124 on timeout, 125/126/127, 137 on kill.
   https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html
8. find(1) — exits 0 if all files processed successfully, greater than 0 if
   errors occur. https://man7.org/linux/man-pages/man1/find.1.html
9. GNU sed manual — script application semantics; a substitution matching
   nothing is not an error. https://www.gnu.org/software/sed/manual/sed.html
10. GNU coreutils manual, rm — `-f` ignores nonexistent operands.
   https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html
11. GNU coreutils manual, mkdir — `-p` succeeds when the directory exists.
    https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html
12. GNU coreutils manual, head — keeping the beginning and discarding the
    rest, as a designed filter.
    https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html
13. GNU coreutils manual, wc — `-l` counts newlines.
    https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html
14. stat(1) — `-c` format directives used for labeled metadata output.
    https://man7.org/linux/man-pages/man1/stat.1.html
15. ps(1) — process listing and the `-o args=` output form.
    https://man7.org/linux/man-pages/man1/ps.1.html
16. pgrep(1) — matches processes without matching itself.
    https://man7.org/linux/man-pages/man1/pgrep.1.html
17. signal(7) — signal numbers behind the 128+N arithmetic (SIGTERM 15,
    SIGKILL 9, SIGSEGV 11).
    https://man7.org/linux/man-pages/man7/signal.7.html
18. setvbuf(3) — stream buffering modes; why stdout to a pipe is
    block-buffered while stderr is not.
    https://man7.org/linux/man-pages/man3/setvbuf.3.html
19. Python documentation, os — `os._exit` exits without flushing stdio
    buffers or running cleanup handlers.
    https://docs.python.org/3/library/os.html
20. curl manual — "By default, curl does not consider HTTP response codes to
    indicate failure"; `--fail` fails with error code 22 for responses 400
    and above. https://curl.se/docs/manpage.html
21. O'AILLY press catalog — the operator trilogy this volume reads against.
    https://oailly.com/

## Boundaries (restated)

No claims about model internals; no claim of transfer beyond the measured
transcript-judgment task; no claim that models enjoy reading; insufficient is
never abolished; the eval measures this task only.

## Companion volumes

*Linux for Language Models* (the non-interactive register), *Durable State
for Ephemeral Minds* (state that survives the session), and *The Repository
Is the Ledger* (git for unattended operators) teach the writing half of this
book's contract: produce a record that can answer the four questions. This
volume teaches the reading half.
