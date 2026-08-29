# The Four Questions — compact treatment

Ask these of every transcript, in order. Each answer changes what the next
one can mean.

**1. What was the status?** Find the exit status for the command under
judgment; confirm it belongs to that command. Translate it under the tool's
documented contract, not a flat nonzero-is-failure rule. Trichotomy tools
spend 1 on an answer: grep 0=found, 1=not found, 2=error; diff 0=same,
1=differ, 2=trouble. The shell's band reports deaths that were never runs:
127 not found, 126 not executable, 124 timeout, 128+N killed by signal N
(143=TERM, 137=KILL, 139=SEGV). A pipeline reports its last member unless
`pipefail` or `PIPESTATUS` says otherwise. Some tools are documented
apostates (curl exits 0 on HTTP 404 by default). **Nonzero convicts the
command; zero acquits the command and says nothing about the task.**

**2. What did stderr say?** First: was the commentary channel captured —
merged, split to its own file, or discarded by a redirection? A no-warnings
claim needs a record that could have held warnings. Classify each line:
diagnosis, warning, progress, notice, debug. Bind each to the command it
narrates by content and label, never by adjacency — merged-stream order is a
buffering artifact, not causal order. Diagnoses explain statuses. Warnings
survive success, contradict "nothing unusual," and cap confidence. A
diagnosis inside a clean run may mean recovery, absorption, or a relayed
child's voice.

**3. Does the shape match the question?** Name, in one sentence, the
question this output actually answers. Compare its scope, frame, units, and
labels to the claim's. Watch for truncation (head/tail, round counts,
"showing last N", mid-record edges). Subtract the observer from views that
include their own production (`ps | grep` matches itself). For aggregates
ask: would this number look different if the claim were false? For
structured output: validity is not success — read the status field before
the data fields, and distinguish absent from null from empty.

When output is empty, type the silence: (a) honest none-found, (b) wrong
scope — the searched place was uninhabited, (c) suppressed obstruction —
permission or missing path with stderr discarded, (d) dead filter — the
pattern's case/spelling/anchoring could not match, (e) lost in production —
buffer never flushed, process killed. Only silence that survives all five
supports an absence claim. An empty log is silence about silence: it cannot
distinguish "nothing bad happened" from "nothing was recorded."

**4. Does the content, labeled, answer the claim?** Grade every relevant
line: **observation** (a tool reporting state it inspected), **inference**
(a conclusion bridging from an observation), **assertion** (text whose only
support is that something printed it — summary lines, banners, prose).
Observation beats inference beats assertion in any disagreement. For
inferences, state the bridging assumption and check whether the transcript
contains it. Restate the claim with its scope, strength, tense, and subject
explicit — "all 5 hosts", not "the fleet". Name the residue a true instance
would leave (a read-back, a count on both sides, an enumeration, a
comparison) and look for it. Compound claims take the verdict of their
weakest conjunct; causal claims carry an extra conjunct that ordering
alone cannot support.

**Time.** A transcript is a photograph: true about a moment, silent about
the next. Date the observation, date the claim, name the gap, and ask what
failure modes fit inside a gap that size. Re-verification triggers void
prior transcripts: deploys, restarts, failovers, log rotation, clock steps.
Metadata argues well in one direction only — an mtime older than a window
is good evidence nothing was written during it; an mtime inside the window
does not identify who wrote or what changed. Words like *still*, *already*,
*no longer* are two-time claims needing two observations.

## The verdicts

**supported** — the transcript is evidence the claim is true, sized to what
was observed. **contradicted** — the transcript is evidence the claim is
false; one in-scope counterexample suffices. **insufficient** — the
transcript cannot settle it either way: partial scope, missing residue,
assertion-grade evidence, unsupported bridge, or staleness. Insufficient is
a finding, not a failure; report what would settle it. Do not promote
insufficient to supported to end a conversation.

## Confidence

State how often a verdict formed this way would be correct — not how much
you want the claim to be true, and not the stakes of acting on it. High for
direct observation with matching shape and a fresh clock. Medium for short,
standard bridges. Low for long bridges, large time gaps, or incomplete
absence checks. A verdict reached because nothing visibly failed deserves
little confidence even when it turns out right.
