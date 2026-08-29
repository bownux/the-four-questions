# Chapter 7 — Time, Order, and the Moving World

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## Evidence has a clock

Every transcript is a photograph. Photographs are true about a moment and
silent about the next one. Readers lose verdicts they earned when they treat
a photograph as a window. This chapter is about the temporal shape of
evidence: when the command ran, when the claim is made, what can change in
between, and which claims a past transcript is simply not allowed to support.

The four questions still apply. Time is not a fifth question. Time is a
dimension of shape (when, in what order) and of content (timestamps in the
bytes), and it sizes claims the way scope sizes them. A perfect reading of a
stale transcript is still a perfect reading of the wrong moment.

## When the read happened

An artifact's mtime and a wall clock, captured together:

```bash
export TZ=UTC
mkdir work && cd work
: > artifact.txt
echo "== a read with no clock in the capture =="
cat artifact.txt
echo "exit: $?"
echo "== the same read, with the clock captured beside it =="
NOW=$(date +%s)
MTIME=$(stat -c %Y artifact.txt)
echo "age of the observation at capture: $((NOW - MTIME)) seconds"
```

```output
== a read with no clock in the capture ==
exit: 0
== the same read, with the clock captured beside it ==
age of the observation at capture: 0 seconds
```

The first read is undated: content (here, an empty file) and a status, with
nothing in the record saying *when*. The second read subtracts the file's
mtime from a wall clock sampled at capture time, and the difference — zero
seconds — is itself evidence: this observation was current at the moment it
was taken. That conjunction is what a clock in the capture buys, and most
transcripts do not buy it. A bare `cat artifact.txt` leaves the age of the
observation unspecified. Claims that say "current," "latest," or "as of this
incident" against undated transcripts are missing a shape field. Verdict:
**insufficient** for recency-qualified claims, even when the file's content
is clear.

A listing with an explicit timestamp is better shape:

```bash
export TZ=UTC
mkdir work && cd work
printf "v2\n" > artifact.txt
touch -d "2026-08-29 03:27:10" artifact.txt
stat -c "%n  size=%s  modified=%y" artifact.txt
echo "exit: $?"
```

```output
artifact.txt  size=3  modified=2026-08-29 03:27:10.000000000 +0000
exit: 0
```

Now the observation is dated — and note two deliberate choices in that
command, both of which are the producer doing the reader a favor. The format
string names its fields (`size=`, `modified=`) instead of leaving the reader
to assign meanings to columns by position, which is chapter 5's unlabeled-
column trap. And the zone is pinned to UTC, so the timestamp reads the same
on any machine that re-runs it; an unzoned local timestamp is two claims
apart from a zoned one, as the cross-host section below shows. A claim at 2026-08-29T03:27:10Z about the
file's content can use it. A claim at 2026-08-30 that "the artifact is still
four bytes" cannot — not from this transcript alone. The world moves. Files
grow, shrink, get replaced by deploys, get restored from backups. The
transcript did not promise to keep watching.

## Staleness is a relation, not a feeling

Staleness is not "old." It is "older than the claim's needs." A year-old
transcript can **support** "this hostname existed in DNS on that date." It
cannot support "this hostname resolves now." A five-second-old health check
can support "the process answered then" and still be stale for "the process
will answer the next request" under a crash loop. The discipline is to name:

- **T_read** — when the instrument ran (from the transcript or capture
  metadata).
- **T_claim** — when the claim is about (explicitly, or "now" by default).
- **Δ** — the gap, and the failure modes that fit inside gaps of that size
  for this kind of system.

If Δ is large enough for the relevant failure mode, the verdict on present-tense
claims softens to **insufficient** unless re-verification is present. How large
is large? That is domain knowledge, and the honest reader states it as part of
the bridge rather than swallowing it. Disk fills in minutes to hours. Certificate
expiry is calendar-scale. Memory leaks are hours to days. Process crashes can
be sub-second. One Δ does not serve all claims.

## Order inside the transcript

Timestamps in content create order:

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

Observations, labeled in time: boot at 10:00Z, disk error at 10:05Z, ok at
01:00Z next day. Claim: "the service recovered after the disk error." The
transcript **supports** an ok line after an error line. It does not, by
itself, support "recovered" as a durable state — only that an INFO ok was
logged later. Claim: "the disk error was the most recent event." **Contradicted**
by the later ok line. Claim: "no errors occurred on 2026-08-29." The window
on 2026-08-29 shows only `INFO ok` in this file — **supported** for this log
file and vocabulary, with the usual bridges.

Order claims without timestamps fall back to file order, which is not always
time order (buffered writes, merged streams, concurrent appenders). Chapter 3's
commentary-channel lessons return: interleaved stderr/stdout may not be
causal order. If the claim needs causality, the transcript needs causal shape
— timestamps, sequence numbers, or a single-threaded instrument.

## Re-verification triggers

Some events void prior transcripts. The list is practical, not metaphysical:

- a deploy, restart, or config reload in the window after T_read
- a failover or leader election
- a clock step (NTP slew is usually fine; manual clock jumps are not)
- rotation or truncation of the log you cited
- credentials or feature flags changing
- "we fixed it" messages in the operator channel — social assertions that
  *should* trigger a fresh read

When a trigger is known to have fired and the transcript predates it,
present-tense claims relying on that transcript are **insufficient** until a
post-trigger read exists. Readers who keep citing the pre-fix health check
are not being conservative. They are being stale.

## What a transcript can never testify about

Even a fresh, well-shaped, well-labeled transcript has a permanent outside:

- **Intent.** Why the operator ran the command. Intent lives in messages and
  tickets, not in stdout.
- **Counterfactuals.** What would have happened with different flags, inputs,
  or timing.
- **Future arrivals.** Whether the next request succeeds, whether the cron
  will fire, whether the disk will fill.
- **Unobserved hosts.** The other side of the load balancer, the replica not
  queried, the region not scraped.
- **Absence of silent failures** outside the instrument's vocabulary — the
  chapter 4 lesson at fleet scale.

The fourth question's "insufficient" is the correct resting place for these,
and no amount of confidence theater should move them to supported. The eval
for this book includes cases whose honest answer is insufficient precisely
so a reader cannot win on accuracy by never using the third verdict.

## Ordering artifacts from the capture itself

The capture harness has a clock too. Pasting order in a chat is not execution
order. An operator can run check B before check A and paste A above B.
Transcripts that lack internal timestamps cannot prove paste order equals
causal order. When two undated pastes disagree, you have conflict without a
timeline — **insufficient** to sequence them, and possibly **contradicted**
as a pair if they assert incompatible present states without times. Ask for
a clock. If none arrives, refuse the sequence claim.

## A discipline for time

1. **Date the transcript.** Prefer internal timestamps; else capture metadata;
   else treat recency as unknown.
2. **Date the claim.** Default "now" is a date; write it down.
3. **Name Δ and the failure modes that fit it.**
4. **Check re-verification triggers** in the surrounding context.
5. **Refuse futures, intents, and unobserved scopes** as unsupported by
   nature — not as temporary gaps.


## Windows that moved under you

Incident response produces a special staleness: the window named in the claim
is not the window captured in the transcript. "Errors during the outage
(10:00–10:30)" paired with a log scrape from 10:00–10:10 is a shape/time
failure. The content may be flawless about the first ten minutes and silent
about the twenty that matter. Readers fix this by checking the time range of
the capture against the time range of the claim — literally, the first and
last timestamps, or the `since`/`until` flags in the instrument line. If the
flags are missing and the timestamps do not span the window, the verdict on
window-scoped claims is **insufficient**.

The reverse also happens: a scrape wider than the window includes an error
outside the incident and the reader attributes it inside. Time bounds are
scope. Scope failures are chapter 5; here they wear a clock.

## The window that closed behind you

Rotation deserves its own worked case, because it is the trigger that most
often fires *between* an event and the reader's inspection of it, and
because the transcript it produces is indistinguishable from good news.

```bash
export TZ=UTC
mkdir work && cd work
printf "2026-08-29T09:58:00Z ERROR upstream refused\n" > app.log
echo "== the incident window's evidence, before rotation =="
grep -c ERROR app.log
mv app.log app.log.1
: > app.log
echo "== the same command, run after rotation =="
grep -c ERROR app.log
echo "exit: $?"
echo "== what the directory holds =="
ls
wc -c app.log app.log.1
```

```output
== the incident window's evidence, before rotation ==
1
== the same command, run after rotation ==
0
exit: 1
== what the directory holds ==
app.log
app.log.1
 0 app.log
44 app.log.1
44 total
```

One error, one file, two readings minutes apart, and the second reading is
the one that reaches the reader. Nothing was deleted and nothing failed:
rotation renamed the evidence to `app.log.1` and started a fresh `app.log`,
which is exactly what rotation is for. The post-rotation count is a truthful
0 with grep's honest exit 1 behind it, and against the claim "the log shows
no errors during the incident" it is worthless — the log that covers the
incident is now the file with the other name, and it is sitting right there
in the listing with 44 bytes in it.

Three tells generalize from this. First, the byte count: a log that covers a
busy window and holds zero bytes is chapter 4's empty-log finding wearing a
clock, and the reader's next question is when the file was created rather
than what it contains. Second, the neighbors: rotation leaves siblings —
`.1`, `.gz`, dated suffixes, an archive directory — and a directory listing
beside the search is the cheapest possible check on whether the searched
file is the whole record. Third, the mtime relation: a log whose modification
time is *older* than the incident cannot testify about the incident, and one
whose creation time is *newer* than the incident is a file that did not
exist when the events happened. All three are shape questions with clocks
attached, and all three are answered by evidence the producer could have
included in one extra line.

## Clocks that disagree

Distributed systems do not share one clock. A transcript from host A saying
10:05:00 and a transcript from host B saying 10:04:58 may be the same event
or different ones. When claims require cross-host order, you need either
synchronized timestamps (and a stated tolerance) or logical clocks / request
ids that both sides share. Without that, sequence claims across hosts are
**insufficient** even when each side is locally clear. Paste order in a
ticket is not a logical clock.

## The "still" operator

Natural language smuggles time with words like *still*, *already*, *yet*,
*no longer*, *again*. Each one is a two-time claim. "The service is still
up" needs a prior observation and a current one. A single transcript can
supply *current*. It cannot supply *still* unless it also contains the prior
or the prior is cited as a separate dated evidence item. Readers who treat
*still* as emphasis rather than as a temporal operator invent a past. The
fourth question, under time pressure, should expand *still* into two claims
and score them separately.

## Rate, not only state

Some claims are about rates: errors per minute, jobs per hour, p99 latency.
A single instantaneous transcript (one `curl`, one log line) cannot support a
rate. You need a series, a histogram export, or a metrics query whose window
is stated. Substituting a single sample for a rate is a time-shaped cousin of
substituting a single host for a fleet. Verdict: **insufficient**, with an
ask for the series.

## Re-verification as a first-class capture

The best operators paste pairs: before/after, or old/new, with clocks on
both. The shape of a re-verification pair is two dated transcripts and a
stated trigger between them ("after deploy of abc1234"). Claims about the
effect of the trigger become answerable. Single-sided pastes leave the
trigger's effect in inference land. If you are authoring transcripts for
other readers (humans or models), the house style from the trilogy applies:
leave a clock, leave the trigger, leave the after. This book is easier to
satisfy when the writers of transcripts expect the readers this book trains.

## When delay is the signal

Not all gaps are staleness bugs. Some systems are eventually consistent;
some queues drain slowly; some DNS TTLs bind the past for minutes. In those
domains, a "too fresh" check after a write can **contradict** a claim that
would be true after the propagation window — or more often, show a
pre-propagation state that makes the claim **insufficient** rather than false.
The bridge must include the propagation budget. Domain knowledge enters as a
stated allowance, not as a silent fudge. If you do not know the budget, you
do not know whether you are early or wrong, and insufficient is again the
honest rest.


## The gap between checking and using

There is a staleness so short that no discipline of freshness can close it,
and it deserves naming because readers who understand every other section of
this chapter still walk into it. Between the moment a check observes the
world and the moment anything acts on that observation, the world is
unlocked. The check says the file is absent, and by the time the write
happens the file exists. The check says the disk has room, and by the time
the copy runs another process has taken it. The check says the lock is free,
and two workers who checked simultaneously both believe it. This is the
time-of-check-to-time-of-use gap, and it is not a bug in the check — the
check was accurate when it ran. It is a property of reading a moving world
through photographs.

For the reader judging transcripts, the gap changes what a check-then-act
transcript can support. A transcript showing a check, then an action, then a
success status supports "the action succeeded"; it does not support "the
action was safe," because safety was a property of the interval, and the
interval is exactly what no observation covers. The stronger evidence is
never a fresher check — it is an *atomic* operation, one whose contract
makes the check and the act inseparable: a create-if-absent flag, an
exclusive open, a compare-and-swap, a rename that either replaces the target
or does not. When a transcript shows one of those, the gap is closed by the
tool's contract and the reader can credit it. When it shows a separate check
followed by a separate act, the reader should notice that the sequence is
evidence of *hope*, and price accordingly under concurrency: a single
operator on a quiet machine is usually fine, and the same transcript from a
fleet of workers on shared state is a race with a clean exit status.

The reason this belongs in a reader's book rather than a writer's is that
the gap is invisible in output. Both transcripts — the atomic one and the
racy one — show a check, an action, and a zero. Only the command lines
distinguish them, which returns to this book's recurring instruction: read
the commands, not just their output. The commands are where the contracts
live, and contracts are the only thing that turns an observation about the
past into a claim about the moment of action.




Worked TOCTOU (captured live). Two demonstrations, same lesson.

**Atomic create closes the gap.** With `set -o noclobber`, create-if-absent is
one contract — the second writer is refused by the open, not by a later hope:

```bash
rm -f slot
( set -o noclobber; echo A > slot ) 2>errA; echo "A_status:$?"
( set -o noclobber; echo B > slot ) 2>errB; echo "B_status:$?"
echo "final:$(cat slot)"
echo -n "errB:"; cat errB
```

```output
A_status:0
B_status:1
final:A
errB:bash: line 5: slot: cannot overwrite existing file
```

**Stale check-then-act loses deterministically.** The operator records
"absent", a concurrent writer fills the path during the gap, and the operator
still acts on the old observation:

```bash
rm -f slot3
if [ ! -e slot3 ]; then OBS=absent; else OBS=present; fi
echo "check:$OBS"
echo racer > slot3                    # concurrent writer during the gap
if [ "$OBS" = absent ]; then echo winner > slot3; echo "write_status:$?"; fi
echo "final:$(cat slot3)"
```

```output
check:absent
write_status:0
final:winner
```

`write_status:0` **supports** "the write syscall succeeded." It is
**insufficient** for "the write was safe against concurrent creators," and
the final bytes (`racer` overwritten by `winner`, or the reverse under a
different schedule) are the residue of a race, not of a contract. Read the
command lines: only an atomic exclusive create, a lock with a defined owner,
or a compare-and-swap turns the gap into a single verdict channel. A separate
check followed by a separate act remains evidence of hope under concurrency —
even when every status is zero and a single quiet machine "usually" gets away
with it.



## Instants, durations, and the output that spans a window

Every transcript in this chapter so far has been treated as a photograph,
and photographs are the easy case. Long-running commands produce something
else: output that *spans* an interval, where the first line and the last
line describe different moments and the difference can be the whole story.
A build that ran for twenty minutes, a backup that ran for two hours, a
migration that streamed progress across a maintenance window — each emits a
record whose parts are not contemporaneous, and reading such a record as a
snapshot of any single moment is a category error.

Two consequences follow. First, the *state* a spanning transcript reports is
the state at the moment each line was written, not at the end: a progress
line reading "412 of 500 records" was true when written and is not a
statement about now, and the summary at the bottom is the only line that
speaks to the end — if the command reached the bottom at all. Second, and
more useful, a spanning transcript can testify about *change*, which a
photograph cannot. A pair of measurements at the top and bottom of a long
run brackets the run; a series of them describes a trajectory. This is the
one shape that supports rate claims honestly, and it is why the rate section
below asks for a series rather than a sample.

The reader's practical checks are the same in both directions. Does the
transcript say when it started and when it ended, or only one of the two? A
record with a start and no end is a run that may still be going, may have
been killed, or may have had its tail truncated — chapter 5's frame problem
with a clock on it. Does the elapsed span cover the window the claim is
about? A two-hour backup that began before a schema change and ended after
it has copied some tables from before and some from after, and "the backup
covers the state at completion" is false for every table copied early. That
last case is worth carrying as its own species: long operations over
changing data do not observe a single consistent world unless something —
a snapshot, a transaction, a quiesced service — made them do so, and the
transcript rarely says which. When a claim needs point-in-time consistency
and the evidence is a long stream, the honest verdict is insufficient, and
the missing evidence is the isolation mechanism, not a fresher run.

## Metadata remembers less than you think

One more limit belongs here, because readers routinely ask filesystem
metadata to testify about history it never recorded. A file carries a small
fixed set of times — last modification, last access, last inode change —
and each is a single slot, overwritten by the next event of its kind. There
is no history in them, only a most-recent. So an mtime says *the last write
happened at this instant* and is silent about every write before it: a file
modified fifty times today has the same shaped evidence as one modified
once. It cannot tell you how many changes there were, what any of them was,
or whether the last one reverted the others. And the slot can be set without
any content change at all — `touch` exists precisely to do that, archive
extraction and file copies assign times of their own, and restores from
backup can install old times on new content or new times on old content.

The reading discipline follows directly. Treat metadata as an *upper bound
on ignorance*, not as a record: an mtime older than a window is strong
evidence no write happened inside the window, since a write would have
updated it — that is the one direction metadata argues well, and it is the
direction that supports negative claims. An mtime inside the window is much
weaker in the positive direction: it establishes that something touched the
file, not that the deploy did, not that content changed, not what the change
was. Chapter 6's inference grade covers the rest of the walk. Where the
claim needs an actual history — who changed what, in which order — the
evidence has to come from a system that keeps one: a version control log, an
audit trail, an append-only record of the kind this press's earlier volumes
taught operators to maintain. Metadata is the wrong witness, and it will
answer anyway, which is what makes it dangerous.

## Bridging to judgment under uncertainty

Chapters 1–7 give you a routine that ends, often, in insufficient. That is
not a bug in the curriculum. The production skill is to live with graded
verdicts, to escalate when the claim must be decided anyway, and to keep
confidence calibrated when the evidence is thin. The last chapter composes
the routine end-to-end, teaches escalation as a first-class verdict path,
and — because this press measures its machine readers — shows you the test
by which you will be measured, in the open.
