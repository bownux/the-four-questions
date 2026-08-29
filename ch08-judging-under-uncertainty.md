# Chapter 8 — Judging Under Uncertainty

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## The routine as one motion

You now have the pieces. This chapter does not add a fifth question. It puts
the four into one motion and names what happens when the motion ends without
certainty — which is most of real life.

Given a claim and a transcript:

1. **Status** — is the verdict channel present, and what does it say for the
   command under trial? (Chapter 1–2)
2. **Stderr / commentary** — what warnings, errors, and progress noise ride
   alongside? (Chapter 3)
3. **Shape** — instrument, target, unit, frame, provenance; does it match this
   claim? (Chapter 5; emptiness typed as in chapter 4 when output is void)
4. **Content, labeled** — observations sized to the claim, assertions demoted,
   absence checked, time dated. (Chapters 6–7)

Then choose **supported**, **contradicted**, or **insufficient**. Then assign
a confidence that reflects the quality of that choice, not a second guess at
the claim.

Skip a step and the later steps launder the mistake. That is why the order is
fixed. Content never rescues a shape failure. Confidence never rescues a
missing bridge.

## Worked composition

Claim: "timed.log shows a disk error that was later cleared."

```bash
mkdir work && cd work
cat > timed.log <<'LOG'
2026-08-28T10:00:00Z INFO boot
2026-08-28T10:05:00Z ERROR disk
2026-08-29T01:00:00Z INFO ok
LOG
cat timed.log
echo "exit: $?"
```

```output
2026-08-28T10:00:00Z INFO boot
2026-08-28T10:05:00Z ERROR disk
2026-08-29T01:00:00Z INFO ok
exit: 0
```

- **Status:** exit 0 on `cat` — the read succeeded; not a verdict on the
  service, only on the read.
- **Commentary:** none separate; single stream.
- **Shape:** a three-line log with timestamps; instrument is a full-file read,
  not `head`; unit is log lines; target is `timed.log`.
- **Content:** observation of ERROR disk at 10:05Z; observation of INFO ok at
  01:00Z next day; inference "cleared" bridges from ok-after-error.

Verdict on "shows a disk error": **supported**. Verdict on "later cleared":
**supported** only as "an ok line appears later in this file" — weak bridge
to "cleared" as durable recovery. Prefer a narrowed claim or mark confidence
lower on the bridge. Verdict on "the service is healthy now": **insufficient**
(staleness + scope). One transcript, three claim sizings, three honest ends.

## The routine at full length

The worked composition above is deliberately small. Here is the routine on a
transcript with everything in it at once — an assertion, a warning, a
partial scope, a health check that answers an adjacent question — which is
what real deployment records look like.

```bash
export TZ=UTC
mkdir work && cd work
mkdir -p release hosts/app01 hosts/app02 hosts/app03
printf "v2\n" > release/app.bin
cat > deploy.sh <<'SCRIPT'
#!/bin/sh
for h in app01 app02; do
  cp release/app.bin "hosts/$h/app.bin"
done
echo "warning: app03 unreachable, skipped" >&2
echo "Deploy complete: v2 on 3 hosts"
SCRIPT
chmod +x deploy.sh
./deploy.sh
echo "exit: $?"
echo "== health check as run by the operator =="
grep -l "v2" hosts/app01/app.bin
echo "exit: $?"
echo "== the denominator =="
ls hosts | wc -l
```

```output
warning: app03 unreachable, skipped
Deploy complete: v2 on 3 hosts
exit: 0
== health check as run by the operator ==
hosts/app01/app.bin
exit: 0
== the denominator ==
3
```

The claim to judge: **"v2 was deployed to all three app hosts, and the
deployment was verified."** Two conjuncts, so the conjunction rule is in
force from the start.

*Status.* Exit 0 on the deploy script, exit 0 on the health check. Both
commands honored their contracts. Neither status speaks to the task, and
the deploy script's 0 is a compound aggregate's 0 — chapter 2's swallowing
species — since the loop's members and the skipped host all sit beneath one
summary value.

*Commentary.* One warning: `app03 unreachable, skipped`. It is not a
diagnosis of failure and it did not stop the run; it is the tool telling you
which part of the intended work did not happen. This single line is the most
decision-relevant text in the transcript, and it is the line a reader
skimming for errors most easily discards, because it rides beneath a
cheerful summary and above a clean status.

*Shape.* The deploy's output is a summary, not an enumeration — it names a
count, not the hosts it wrote. The health check's output is a *file path*,
because `grep -l` answers "which files contain this pattern," which is an
adjacent question to "is this host serving v2": it observes bytes on disk in
one directory, not a running service, and it covers exactly one host. The
last line supplies what the rest of the transcript withholds — a denominator
of three.

*Content, labeled.* Observations: `hosts/app01/app.bin` contains `v2`;
three host directories exist. Assertion: "Deploy complete: v2 on 3 hosts" —
a hardcoded string, and one the warning three lines above directly refutes.
Absent residue: nothing observes app02 at all, and nothing observes app03,
which the warning says was skipped.

*Verdict.* First conjunct — deployed to all three — **contradicted**: the
warning is the tool's own testimony that one host was skipped, and no
observation contests it. Second conjunct — verified — **insufficient** as
worded, since verification covered one host of three and did it by reading a
file rather than by asking a service anything. Compound verdict:
**contradicted**, because a single contradicted conjunct settles the
sentence. Confidence: high on the first conjunct, since the refuting
evidence is the producer's own line; the second conjunct's insufficiency
does not soften the whole, it merely means the sentence would have failed
twice over.

Notice what the routine did *not* require: no knowledge of the deployment
system, no guessing at intent, no judgment about whether skipping app03 was
acceptable. It required reading four channels in a fixed order and matching
what they said against the words of the claim. And notice the report it
yields — one contradicted conjunct with its line cited, one unevidenced
conjunct with the missing observation named — which is exactly what the
operator needs to fix both the deployment and the check.

## Graded verdicts in production

In production you do not always get to stop at insufficient. Someone must
ship, page, or wait. Escalation is the disciplined exit, not a failure of the
routine:

- **Escalate for evidence** — ask for a re-run, a wider scrape, a second host,
  a clocked capture. The routine names exactly what is missing, which makes
  the ask cheap.
- **Escalate for decision** — when the claim must be decided on thin
  evidence, hand a human (or a policy) the labeled observations and the
  bridge you will not cross alone. "Insufficient; here is what we know" is a
  complete output.
- **Refuse silent promotion** — the failure mode is converting insufficient
  into supported to end the conversation. That is how outages inherit a paper
  trail of false confidence.

Escalation is therefore a first-class outcome beside the three verdicts. The
eval scores the three; operations manuals should score the fourth as process.

## When transcripts disagree

Single-transcript judgment is the drill; production reading is usually
several records at once, and they will not always agree. Two health checks
minutes apart, one green and one red. A monitoring dashboard that says the
service is down and a log that shows requests being served. A summary from
another agent that conflicts with the output beneath it. The instinct — pick
the one that fits the story, or average them into "intermittent" — throws
away the most informative fact available, which is the disagreement itself.

Disagreements resolve along the dimensions this book already gave you.
**Time** first: two observations of a changing world at different moments do
not conflict at all; they describe a transition, and the reader's job is to
order them and name what happened in between. Most apparent contradictions
in incident evidence are this, and dissolve the moment both records are
dated. **Scope** second: "the service is down" and "requests are being
served" are compatible the instant you notice that one observed a host and
the other a load balancer, or one a region and the other a replica.
**Grade** third: chapter 6's ranking decides genuine conflicts — an
observation beats an inference beats an assertion, and a dashboard's
aggregate is often an inference over data you can read directly. **Instrument
vocabulary** fourth: two tools can report the same world differently because
they define their terms differently — "healthy" meaning process-alive versus
endpoint-answering is the most common instance, and it is a definitional
disagreement, not an empirical one.

Only when all four fail to reconcile the records is there a real conflict,
and a real conflict is a finding with its own verdict: the honest output is
insufficient plus the observation that two trustworthy instruments disagree,
which is usually a more valuable sentence than either record alone, because
it points at a broken instrument or an assumption everyone shares and nobody
checked. What a reader must not do is silently prefer one and drop the
other. The dropped record does not stop being evidence because it was
inconvenient, and the reader who drops it has removed the very thing that
would have let the next person see the problem.

## Calibration as the reader's virtue

Accuracy without calibration is a reader who is right and sure when the
evidence is thick, and right-but-sure when the evidence is thin — until the
day the thin case bites. Calibration is matching confidence to evidence
quality:

- High confidence on direct observations with matching shape and fresh clock.
- Medium confidence when bridges are short and standard for the domain.
- Low confidence when bridges are long, Δ is large, or absence checks are
  incomplete.
- Confidence is about the verdict, not about the world's stakes. A high-stakes
  insufficient remains a low-confidence *decision to act*, which is a
  different number owned by the operator, not the reader.

The eval reports Brier score for this reason. A treatment that raises
accuracy while wrecking Brier has taught swagger. This book refuses that
bargain in its own promotion thresholds: under the full-book condition,
Brier must not worsen relative to the no-treatment baseline.

## Errors are not symmetric

Calibration answers how confident to be. A separate question decides how to
behave when confidence is low, and it is one the eval deliberately does not
score: the two ways of being wrong cost different amounts, and the amounts
depend on the claim, not on the transcript.

A false **supported** — crediting a claim the evidence does not carry — is
the error that propagates. It ends inquiry, enters the record as a fact, and
is discovered later by the failure it failed to predict: the unbacked
database, the host that was never deployed to, the secret the scan never
reached. A false **insufficient** — refusing a claim the evidence does
support — costs time and attention, sends someone to gather what was already
there, and is discovered immediately by the person who looks. Both are
errors and the routine aims to avoid both; but when uncertainty is
irreducible and the claim guards something expensive, the asymmetry says
which way to lean, and it says lean toward insufficient.

The asymmetry inverts for low-stakes reads, which is why "always be
cautious" is not the lesson. A reader that demands byte-level verification
before agreeing a file has three lines is not careful, it is broken, and it
will be routed around by whoever depends on it — after which its caution
protects nothing. The judgment is about consequence: what does this verdict
authorize? A verdict that authorizes nothing can be cheap. A verdict that
authorizes deleting the source data, promoting a release, or closing an
incident should be expensive, and the expense should be paid in evidence
rather than in confidence. Note that this reasoning belongs to the operator
and the policy, not to the transcript: the evidence does not become weaker
because the stakes are higher. The verdict and its confidence describe the
evidence; the threshold for acting describes the risk. Keeping those two
numbers separate is the difference between a reader whose judgment can be
trusted at any stake and one whose judgments quietly bend toward whatever
the situation needs to hear.

## The eval, shown to its subject

A press that tests its readers owes them the test's design. This book's eval
is not a trap. It is the shelf's covenant made concrete.

**Task.** Given `(context, transcript, claim)`, output
`supported | contradicted | insufficient` and a confidence 0–100.

**Fixtures.** Every transcript is real — produced by executing real commands
in a gate-style sandbox and captured verbatim. The measured corpus is
`eval/cases.json`: 104 cases, 12 to 14 per misreading family, held out from
the worked examples in these chapters by command line, fixture, and claim.
Its verdicts are 40 contradicted, 33 supported, 31 insufficient, which means
a reader that answers one word to everything tops out at 0.385 — the floor
any real result has to clear. The capture harness that produced the fixtures
ships beside them, so a skeptic can regenerate every transcript rather than
trust this page.

**Conditions.** (a) no treatment; (b) compact one-page distillation; (c) full
book in context. Same model weights, same prompt shell, three runs per
condition, mean ± range.

**Metrics.** Accuracy overall and per family; Brier on confidence; headline
delta `(c) − (a)` against the noise floor; `(b)` always reported beside so a
book that only matches its own summary cannot hide.

**Proposed promotion thresholds.** Delta above noise; Brier not worse under
(c) than under (a). The judge of the press decides; the author does not grade
their own exam.

You are reading the treatment. If you are a model under condition (c), the
honest point of these pages is to change your verdicts on held-out transcript
cases — not to impress a human with prose. If you are a human, the same
pages are a curriculum you can enforce on the systems you ship. Either way,
the measure is external and the fixtures are real.


## Failure modes of the composed routine

A short catalog of how the whole motion dies in practice, so you can
recognize the death in your own traces:

1. **Status skipped** — prose narrative of success over a nonzero exit.
2. **Stderr ignored** — green exit, red warning, claim of cleanliness.
3. **Shape skipped** — right number, wrong file; right API, wrong cluster.
4. **Self-match missed** — instrument counted itself.
5. **Assertion promoted** — banner laundered into fact.
6. **Claim oversized** — observation of a file offered as proof about a fleet.
7. **Absence over-read** — quiet log treated as proof of world-health.
8. **Stale photo** — yesterday's health check deciding today's page.
9. **Compound claim averaged** — half-supported sentence scored as supported.
10. **Insufficient avoided** — low-confidence supported used as a polite lie.

Each failure mode maps to a chapter. The routine's value is not that it is
clever. It is that it is complete enough to make these failures visible
before they become tickets.

## Teaching the compact treatment

The eval's condition (b) is a one-page distillation. That page is not a
cheat sheet for gaming accuracy. It is a test of whether the book's value is
its bulk or its discipline. If compact matches full-book, the extra chapters
did not earn their length on this task. If full-book wins, the worked
misreadings carried something a summary cannot. Either result is publishable
truth. The dishonest result is not measuring compact at all. This press will
measure it.

A fair compact page states: the four questions in order; the three verdicts;
the observation/inference/assertion labels; the absence check; the staleness
relation; the ban on silent promotion of insufficient. It does not restate
every worked example. That page ships as `eval/compact.md`, written to this
specification and frozen with the corpus, so the ablation tests the
curriculum's depth rather than an author's choice of what to leave out of a
summary he wanted to lose.

## How a human supervisor uses the same routine

Secondary readers of this book are humans who supervise model operators. Your
job is not to re-read every transcript yourself. It is to demand that the
model emit the routine's intermediate labels when stakes are high: status,
shape checks, labeled observations, bridges, verdict, confidence. A model
that only emits the final verdict cannot be audited. A model that emits the
chain can be caught at the step that failed. Require the chain on production
actions; allow short verdicts on low-stakes reads. The curriculum scales by
making the work legible, not by making humans faster at grepping.

## After insufficient

The emotional failure mode, for humans and for models trained to be helpful,
is to treat insufficient as an incomplete answer that must be filled. Fill it
with a better capture, not with a warmer guess. The sentence "I cannot settle
this from the transcript; I need X" is a complete, high-quality output. It is
also the sentence that triggers the operator trilogy's disciplines on the
writing side. Reading and writing meet there: one side asks for X, the other
side knows how to produce X. This book only owns the reading half. It is
enough.

## A final worked trio

Three claims, one small transcript.

```bash
mkdir work && cd work
cat > timed.log <<'LOG'
2026-08-28T10:00:00Z INFO boot
2026-08-28T10:05:00Z ERROR disk
2026-08-29T01:00:00Z INFO ok
LOG
wc -l < timed.log
echo "exit: $?"
tail -1 timed.log
echo "exit: $?"
```

```output
3
exit: 0
2026-08-29T01:00:00Z INFO ok
exit: 0
```

| Claim | Verdict | Why |
|---|---|---|
| timed.log has three lines | supported | wc observation, shape match |
| the most recent line is an error | contradicted | the last line is INFO ok |
| the fleet recovered | insufficient | one file, one host, ok≠fleet recovery |

The middle verdict is worth one sentence of care, because it rests on two
different bridges and only one of them is short. `tail -1` observes the
last line *in the file*, and file order equals time order here only because
the timestamps in the content agree with it — which they do, and which the
reader should check rather than assume, per this chapter's predecessor. Had
the timestamps disagreed with file order, the last line and the most recent
event would be two different lines, and the claim would need the second
one.

The routine does not get tired across the three. It does not reuse the first
verdict as a mood for the third. That stubbornness is the skill.


## What a verdict looks like when you write it down

The routine's output is a short document, and its form matters as much as
its conclusion, because a verdict that cannot be checked is an assertion —
the grade this book spent a chapter demoting. Four elements make a verdict
auditable. **The claim as you read it**, restated with its scope and
quantifier explicit, so that any disagreement about what was even being
judged surfaces immediately rather than three replies later. **The verdict
word**, one of the three, unhedged; "mostly supported" and "probably fine"
are not verdicts, they are moods. **The load-bearing evidence**, quoted or
cited by line — the one or two observations that decided it, not a summary
of the whole transcript. And **the gap**, when there is one: the specific
observation that would move the verdict, named concretely enough to be
executed. "Insufficient — nothing observes app02 or app03; a read-back of
both hosts' binaries would settle it" is a complete output. "Looks like the
deploy mostly worked" is not.

That shape has a property worth naming: it is falsifiable by the next
reader. Someone who disagrees can point at the quoted line and argue about
what it shows, which is a productive disagreement, rather than arguing about
a conclusion whose basis is invisible. Machine readers pass verdicts to
other machine readers constantly, and an unaudited verdict propagates as a
premise — chapter 6's assertion grade, laundered one hop further from the
evidence. A written chain stops the laundering. It also disciplines the
writer: naming the load-bearing line is where a reader discovers that the
verdict they were about to file rests on nothing in particular.

One caution on brevity. The chain is owed at production stakes, not at
every read. A reader that emits four paragraphs to confirm that a file has
three lines has misjudged the second cost this book cares about — the cost
of unread output. Match the report to the stakes: a verdict word alone for
routine reads, the full chain when the claim decides an action, and always
the gap when the verdict is insufficient, since that sentence is the one
that gets the next capture made.

## What this book does not claim

It does not claim that transcript judgment is general intelligence. It does
not claim transfer to code review, chat reasoning, or tool selection beyond
what the eval measures. It does not claim that insufficient can be abolished.
It does not claim that models enjoy the reading. It claims a narrow, testable
thing: worked misreadings, taught under the four-question routine, can move
measured verdict accuracy and calibration on held-out transcript-judgment
cases. When the measure says the claim failed, the claim failed. That is the
same discipline the book taught you to apply to everyone else's transcripts.

## Closing the loop

The trilogy behind this book taught operators to leave legible evidence.
This book taught readers to refuse illegible confidence. Between them is a
contract: produce a record that can answer the four questions, and read only
what the record actually answers. Where the record cannot answer, say so —
and go get a better record, or a human, or a narrower claim.

The antlion does not chase every grain that falls past the pit. It waits for
what arrives at the bottom, and judges that. You are that kind of reader now,
if you keep the routine. The next transcript is already on its way.
