# Chapter 6 — Claims Against Evidence

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## The fourth question, at judgment strength

The first three questions clear the ground. Status tells you whether the
commands honored their contracts; commentary tells you what the process said
about its own work; shape tells you whether the output is even about the
subject at hand. What remains is the question the whole routine exists to
answer: *does the content, labeled, answer the claim?* — and the two words
doing the heavy lifting there are "labeled" and "the claim."

Labeled, because content without attribution is not evidence. A line of
output means something only when you know which command produced it, over
what input, at what moment; strip the labels and you have text that resembles
evidence. Chapter 3 established this for merged streams and chapter 5 for
adjacent questions; here it becomes a judgment rule with three grades, since
the lines in a transcript are not all the same kind of thing.

The claim, because a verdict is not a temperature reading on a transcript's
general vibe. It is an assessment of a *specific sentence*, and the sentence
has a size: a scope (which things), a strength (all, most, some), a tense
(is, was, will be), and a subject (the world, the record, the command). Two
claims about the same transcript can land on opposite verdicts because their
sentences differ by one word. Readers who judge transcripts rather than
claims lose this entirely — they report the transcript "looks fine," which
is not a verdict about anything, and cannot be checked, and is how a
half-true summary becomes someone else's premise.

This chapter builds the machinery: evidence typing, claim sizing, the
absence check, and the composition of the three into a verdict with a
confidence attached.

## Three grades of evidence

Every line in a transcript is one of three things, and confusing them is the
most consequential error in this book — more consequential than any single
misread status, because it corrupts the reader's whole model of what a
transcript is.

An **observation** is a report by a tool about state it inspected: the bytes
`cat` printed, the entries `ls` enumerated, the size `stat` read from the
inode, the hit `grep` found and labeled with its file and line. Observations
are the load-bearing evidence in any transcript. They can still mislead —
chapter 5's whole catalog is observations that answer adjacent questions —
but they are, at least, the machine reporting on the world.

An **inference** is a conclusion drawn from an observation, whether by the
tool, the operator, or you. "The file was modified during the incident" is
an inference from an mtime; "the service is running" is an inference from a
line in a process table; "the deploy succeeded" is an inference from a
status. Inferences are legitimate and unavoidable — judgment is made of them
— but each one imports assumptions that the transcript does not carry, and
the reader owes those assumptions an inspection rather than a nod.

An **assertion** is a statement whose only support is that something printed
it. A script's `echo "Deploy complete"`, a tool's cheerful summary line, a
commit message, a comment, a claim in the prose above the transcript: these
are text about the world, produced by something that was *told* to produce
it, not by something that looked. Assertions are the weakest grade, and they
are typographically identical to the strongest.

```bash
mkdir work && cd work
mkdir -p src backup
printf "a\n" > src/one.txt
printf "b\n" > src/two.txt
printf "c\n" > src/three.txt
cat > backup.sh <<'SCRIPT'
#!/bin/sh
cp src/one.txt backup/
cp src/two.txt backup/
echo "Backup complete: 3 files copied to backup/"
SCRIPT
chmod +x backup.sh
./backup.sh
echo "exit: $?"
echo "--- what the directory holds ---"
ls backup
ls backup | wc -l
```

```output
Backup complete: 3 files copied to backup/
exit: 0
--- what the directory holds ---
one.txt
two.txt
2
```

The script says three files. Two files exist. Nothing failed: both copies
succeeded, the exit status is 0, and the summary line is exactly what the
script's author wrote into it — a hardcoded string that was never connected
to the loop it describes, which is how most such summaries are written. The
line "Backup complete: 3 files copied" is an assertion; the `ls` and the
count beneath it are observations; and where an assertion and an observation
disagree, the observation wins, always, without argument. Against the claim
"three files were backed up," the verdict is contradicted, and the
contradicting evidence is two lines of directory listing.

What makes this genus dangerous is that the assertion is usually *right*.
Summary lines mostly do reflect what happened, which trains a reader to
accept them, which is precisely the training that fails at the one moment it
matters. So the rule is not "distrust summaries" — it is **rank the grades
and let the ranking decide disagreements**: observation over inference over
assertion, and a claim supported only by assertion is supported only as
strongly as the claim "somebody typed this." When a transcript contains an
assertion and no observation to corroborate it, the verdict on the asserted
fact is insufficient no matter how specific the assertion is. Specificity is
not evidence. "3 files" is more specific than "files were copied" and no
better attested.

## Inference and its assumptions

The middle grade needs its own worked case, because inferences are where
careful readers go wrong — the careless ones never get past assertions.

```bash
export TZ=UTC
mkdir work && cd work
mkdir -p srv
printf "version 1.9\n" > srv/app.txt
touch -d "2026-08-29 03:00:00" srv/app.txt
echo "== the evidence the operator showed =="
stat -c "%n  size=%s  modified=%y" srv/app.txt
echo "== the evidence the operator did not show =="
cat srv/app.txt
```

```output
== the evidence the operator showed ==
srv/app.txt  size=12  modified=2026-08-29 03:00:00.000000000 +0000
== the evidence the operator did not show ==
version 1.9
```

Suppose the claim is "the 2.1 release was deployed at 03:00." The first
observation is genuine and precise: this path has that size and that
modification time. The inference the operator wants you to draw is that the
deploy wrote this file at 03:00, and therefore the file now holds 2.1. Every
step of that inference is an assumption the observation does not carry.
That an mtime marks *this* deploy rather than any other write. That a write
happened at all — `touch` sets mtime with no content change, and so do
several ordinary operations. That the thing written was the intended
version. The second command settles it: the file says version 1.9. Same
file, same instant, and the claim is contradicted by content while being
consistent with metadata.

The general discipline for inference-grade evidence is to **state the
assumption bridging observation and conclusion, then ask whether the
transcript contains it.** Timestamp-to-authorship ("this mtime means the
deploy wrote it") assumes exclusivity. Presence-to-function ("the process is
listed, so the service works") assumes a running process serves traffic — an
assumption that dies routinely on wedged processes, wrong config, closed
ports. Name-to-content ("the file is called `app-2.1.jar`, so it is 2.1")
assumes naming discipline. Count-to-completeness ("500 rows loaded, so the
load finished") assumes the expected total was 500, which is a number from
somewhere else. In each pair, the observation is fine and the bridge is what
is being asked to bear the claim's weight. A reader who names the bridge can
usually see whether it is present in the transcript; a reader who never
names it credits the conclusion to the observation's strength.

## Sizing the claim

Now the second half of the question: the claim's own dimensions. Consider a
check and a fleet.

```bash
mkdir work && cd work
mkdir -p hosts
for h in web01 web02 web03 db01 db02; do
  printf "service: running\n" > "hosts/$h.status"
done
printf "service: stopped\n" > hosts/db02.status
echo "== the check that was run =="
for h in web01 web02; do
  printf "%s: " "$h"; cat "hosts/$h.status"
done
echo "== the fleet the claim covers =="
ls hosts | wc -l
```

```output
== the check that was run ==
web01: service: running
web02: service: running
== the fleet the claim covers ==
5
```

Two observations, both true, both clean: web01 running, web02 running. Now
size three claims against them. *"web01 and web02 are running"* — supported;
the evidence matches the claim exactly. *"The web tier is running"* — the
web tier has three members and one was not checked; insufficient, and the
gap is nameable: web03. *"The fleet is healthy"* — five hosts, two checked,
and the transcript's last line is the reader's cue that the denominator
exists at all; insufficient, and in fact false, since db02 is stopped — a
fact this transcript never shows and a wider check would have. One evidence
set, three verdicts, differing only in the words of the claims.

This is claim sizing, and it decomposes into four dimensions worth checking
one at a time. **Scope**: how many things does the claim quantify over, and
how many did the evidence touch? The denominator is the question most
transcripts leave to the reader, and the reader must go find it — from a
listing, an inventory, a count, or an explicit statement — before any
universal claim can be graded. **Strength**: "all" needs every member;
"some" needs one; "most" needs a majority *and* a denominator; and unhedged
plurals ("the services are running") read as universals in every language
this book's readers speak. **Tense**: "is running" is a present-tense claim
supported by a past-tense observation, which chapter 7 takes up as its whole
subject. **Subject**: is the claim about the world ("the service is up"),
the record ("the log shows no errors"), or the command ("the check
succeeded")? These are three different claims with three different evidence
requirements, and sliding between them is the commonest rhetorical move in
incident summaries — usually unconsciously, since the sentence that starts
as a statement about a log ends as a statement about a system.

The productive habit is to restate the claim with its quantifier and
denominator made explicit before judging it: not "the fleet is healthy" but
"all 5 hosts have their service running," at which point the transcript's
2-of-5 coverage is visible without any cleverness at all. Most
overclaiming survives only in the unrestated sentence.

## The absence check

The three grades and the four dimensions cover claims the transcript speaks
to. The sharpest instrument in the chapter covers the rest: **ask what a
transcript of a *true* claim would also contain, and look for it.** Chapter
2 introduced this as the discipline for success-shaped failures; at judgment
strength it becomes a general test, and it is the one move that reliably
turns "I have no reason to doubt this" into a decidable question.

```bash
mkdir work && cd work
mkdir -p src backup
printf "a\n" > src/one.txt
printf "b\n" > src/two.txt
cp src/one.txt src/two.txt backup/
echo "copy exit: $?"
echo "== residue a true backup claim leaves =="
ls backup
echo "files in src:    $(ls src | wc -l)"
echo "files in backup: $(ls backup | wc -l)"
diff -r src backup > /dev/null; echo "trees identical (diff exit): $?"
```

```output
copy exit: 0
== residue a true backup claim leaves ==
one.txt
two.txt
files in src:    2
files in backup: 2
trees identical (diff exit): 0
```

Compare this transcript against the chapter's first one. Same task, and the
claim "every file in src is backed up" now arrives with the residue a true
instance requires: the destination enumerated, both sides counted so the
denominator is in evidence, and a recursive comparison whose trichotomy exit
0 means the trees match — an observation, not a summary. Nothing here is
asserted; everything is observed; the counts make the scope explicit; the
comparison closes the gap between "files exist with the right names" and
"files have the right contents." The verdict is supported, at high
confidence, and a reader can say *why* in one sentence — which is the test
of whether a verdict was reached or merely felt.

The absence check runs the same way on transcripts that lack the residue.
For "the config was updated": a true instance leaves a read-back showing the
new value. For "the migration completed": counts on both sides, ideally
reconciled. For "the certificate was renewed": the new expiry date observed
from the certificate, not the renewal tool's summary. For "no secrets in the
repository": evidence the scan reached every file, which is chapter 4's
coverage problem. Name the residue first, look second. When it is missing,
the verdict is insufficient and your report says exactly what would settle
it — a habit that converts a passive verdict into an actionable one, and
which the next chapter's escalation discipline builds on.

## Compound claims and the conjunction rule

Most real claims are compounds, and compounds fail in a way that averages
cannot express. "The migration ran, all records transferred, and the old
table was dropped" is three claims wearing one sentence, and a transcript
can support the first, leave the second insufficient, and contradict the
third. There is no honest single verdict on that sentence except the one
the conjunction rule gives: **a compound claim is supported only if every
conjunct is supported, and contradicted if any conjunct is contradicted.**
The middle case — some supported, none contradicted, at least one
insufficient — is insufficient overall, however impressive the supported
portion looks.

The temptation is to grade compounds proportionally: two of three
conjuncts confirmed feels like mostly-supported, and "mostly" is a word
that reads as yes. It is the same arithmetic error as reporting a green
build for a suite that skipped half its tests. What the reader owes
instead is a decomposition: state the conjuncts, grade each, and let the
weakest one set the verdict on the whole while the report preserves the
detail. That decomposition is also the most useful thing a reader can
hand back to whoever wrote the claim, because it converts "I'm not
convinced" into "conjunct two is unevidenced; here is what would settle
it." The same rule extends to claims joined by causal language, which
smuggle in a conjunct that transcripts almost never carry: "the restart
fixed the latency" asserts that latency improved *and* that the restart
caused it, and post-hoc ordering is the weakest possible bridge for a
causal conjunct. Grade the improvement from the measurements; grade the
causation as insufficient unless something in the record isolates it.

## When the transcript itself is the claim

Everything so far has treated the transcript as ground truth and the
claim as the thing on trial. Sometimes that is backwards. A transcript
arrives pasted into an issue, quoted in a summary, or relayed by another
agent, and its own provenance is exactly as unattested as any assertion:
text that looks like output, produced by something that may or may not
have run a command. The grades apply recursively. Output you executed
yourself, in this session, is observation. Output captured by tooling you
trust — a CI log, a gate's recorded transcript, a run's archived stdout —
is observation with a chain of custody worth checking once. Output pasted
into prose by an author who says it is from the run is, strictly, an
assertion *about* a transcript, and it carries the author's honesty and
memory as assumptions.

This is not paranoia; it is the ordinary condition of reading in a
pipeline of agents, and it has cheap tells. Real transcripts carry
incidental noise — exact paths, unrounded numbers, warning lines nobody
would invent, the odd interleaving that chapter 3 explained. Reconstructed
ones are suspiciously clean: round counts, tidy alignment, no stderr, no
irrelevant lines, and — the strongest tell — output that is *exactly* what
the claim needs and nothing else. Edited transcripts show seams: an
elision marker, a line whose format differs from its neighbors, a
timestamp out of sequence, a prompt that changes shape mid-record.
Fabricated ones tend to contain output that the named command does not
actually produce, which a reader who knows the tool spots immediately —
one reason this book keeps returning to documented contracts. When
provenance is doubtful and the stakes are real, the correct verdict is
insufficient with a stated remedy — re-run it, or point me at the
recorded log — and the remedy is usually cheap. This press's own house
rules exist for exactly this reason: every printed output in this book is
a real transcript, re-captured whenever its listing changes, because a
book that taught this discipline while quietly inventing its own
transcripts would be teaching the opposite.

## The claims you write yourself

The procedure below is usually pointed outward, at someone else's sentence.
It has to be pointed inward too, and this is the least comfortable paragraph
in the book. Every summary you produce is a claim, and it enters someone
else's evidence chain at the assertion grade — the weakest one — unless you
carry the observations with it. A reader who judges a transcript correctly
and then writes "the deploy looks fine" has performed the judgment and
discarded it: the sentence that travels onward is unfalsifiable, unsized,
and indistinguishable from the fluent guess of a reader who did none of the
work. This matters more in a pipeline of machine readers than it ever did on
a human team, because each hop compounds. A transcript becomes a summary
becomes a status line becomes a decision, and if the grade is lost at hop
one, hop four is acting on assertion with the confidence of observation.

The remedy is mechanical: when you report, carry the load-bearing
observation with the verdict, size the claim to what you actually checked,
and mark the gaps you did not close. "Two of five hosts confirmed running;
the other three were not checked" is barely longer than "the fleet is
healthy" and belongs to a different epistemic universe. The same discipline
governs the confidence number: it is not a politeness marker or a hedge
against embarrassment, it is your own estimate of how often a verdict formed
this way is correct, and it is only worth anything if you would accept being
scored on it. This book's eval scores exactly that, on its author's own
readers, which is the press's way of insisting that a text about honest
judgment be subject to one.

## Composing the verdict

The pieces assemble into a procedure that can be run on any (transcript,
claim) pair, and it is the procedure the eval at the end of this book
measures.

Restate the claim with its scope, strength, tense, and subject explicit.
Name the residue a true instance would leave. Walk the transcript grading
each relevant line — observation, inference, assertion — and bind each to
the command that produced it. Then compare. If observations match the
restated claim across its full scope: **supported**. If observations
contradict it anywhere in scope — the two-file listing under a three-file
assertion, the 1.9 under a 2.1 claim, the stopped host inside "the fleet" —
**contradicted**, and one observation is enough, since a universal claim
dies on a single counterexample. If the observations neither match nor
contradict — because the scope was partial, the residue is absent, the
evidence is assertion-grade, or the bridge from observation to conclusion
is unsupported — **insufficient**, and the report names the missing piece.

Two failure modes bracket this procedure, and it is worth naming both since
readers tend to have a characteristic one. The first is the fluency trap:
crediting a claim because the transcript is detailed, technical, and
consistent with it. Consistency is not confirmation — chapter 2's no-op
proved that — and detail is not evidence, as the hardcoded "3 files" showed.
The second is the paranoia trap: refusing to credit any claim because some
assumption is always unproven. Every verdict rests on assumptions —
that the tools behaved as documented, that the transcript is genuine, that
the clock was roughly right. The discipline is not to eliminate assumptions
but to keep them *ordinary*: standard tool behavior is a reasonable
assumption; exclusive authorship of an mtime is not. A reader who marks
everything insufficient is as useless as one who marks everything supported,
and is wrong exactly as often — it merely feels more responsible.

Which is why the verdict travels with a number. Confidence is not decoration
on the verdict; it is where the residual uncertainty is recorded. Two
supported verdicts — one from a byte-for-byte comparison, one from a
plausible inference over a same-route read-back — are the same word carrying
different weights, and the number is the only place that difference can be
said. The book's last chapter takes up calibration as a discipline in its
own right, since a reader whose confidence tracks its accuracy is more
useful than a reader who is merely often right. Before that, one dimension
of claim sizing still owes an accounting: tense. Every observation in this
chapter was in the past by the time it was printed, every claim it graded
was in the present, and nothing so far has priced the distance between
them.
