# Chapter 3 — The Commentary Channel

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## Misnamed from birth

The second question of the routine — *what did stderr say?* — is about the
most consistently misread channel in the transcript, and the misreading
starts with the name. "Standard error" suggests a stream that carries
errors, implying both that everything on it is an error and that errors are
all it carries. Neither is true, and a reader holding either half of the
name's implication will misjudge transcripts weekly. The design intent,
older than most tools you will read, is better captured by a different
name: stderr is the *commentary channel* — the stream a process uses to
talk *about* its work, kept separate from stdout precisely so that the
work's product stays clean enough for the next program to consume. Data on
one channel, narration on the other. Diagnoses go there, yes; so do
warnings, progress reports, deprecation notices, usage help, debug chatter,
and the occasional banner printed for no reason anyone remembers. A process
writing to stderr is not necessarily failing. It is *talking to you* — the
supervising reader — rather than to the pipeline, and question two exists
because what it says there routinely changes the verdict on claims the
status and stdout would happily support.

The first discipline is structural, before any line is interpreted: know
that the two streams exist, and know what the transcript you are holding
did with them. Every transcript is downstream of a capture decision —
merged, split, or partially discarded — and that decision determines what
silence means, the way a courtroom transcript's meaning depends on whether
the microphone was on.

```bash
mkdir work && cd work
cat > convert.sh <<'SCRIPT'
#!/bin/sh
echo "warning: input has no header row" >&2
echo "converted 14 records"
SCRIPT
chmod +x convert.sh
./convert.sh 2>/dev/null
echo "--- without the commentary channel: the line above is all you see"
./convert.sh 2>&1
echo "exit: $?"
```

```output
converted 14 records
--- without the commentary channel: the line above is all you see
warning: input has no header row
converted 14 records
exit: 0
```

One program, run twice. In the first run its commentary was discarded, and
the record shows a clean conversion: fourteen records, nothing else worth
saying. In the second, the same program, same input, same exit 0 — and a
warning that the input had no header row, which for a record-conversion
task is the kind of fact that decides whether those fourteen records are
fourteen truths or thirteen truths and a column header eaten as data. Now
place the claim this chapter's family is built on: *"the conversion ran
cleanly, with no warnings."* Against the merged transcript, contradicted —
the warning is right there, and "ran cleanly" in the claimant's sense is
false even though the run succeeded in the tool's sense. Against the first
transcript, the honest verdict is insufficient, not supported — and this
is the structural point. The first transcript does not show an absence of
warnings; it shows an absence of *evidence about* warnings, because the
channel warnings travel on was pointed at `/dev/null`. A no-warnings claim
can only ever be supported by a transcript whose capture provably included
the commentary channel. When the redirection is visible in the transcript,
as here, you can read the capture decision straight off the command line —
one more reason the command lines belong in transcripts. When it is not
visible, the capture configuration is an assumption, and your confidence
should price it.

## A taxonomy for the talk

Once captured, commentary has to be classified, because its species carry
different evidential weight and readers who treat the channel as
homogeneous either panic at noise or sleep through signal. Five species
cover nearly everything. **Diagnoses** — "No such file or directory,"
"Permission denied," "connection refused" — are testimony that a specific
operation failed; they usually travel with a nonzero status, and when they
do, they tell you *which* failure the number summarizes; chapter 1's
transcripts used them this way throughout. **Warnings** are the tool
saying it proceeded, but under protest: an assumption was made, a fallback
taken, an input odd. A warning does not contradict "it succeeded"; it
contradicts "it succeeded and nothing was unusual" — and it *predicts*.
Today's "input has no header row" is next week's corrupted import;
deprecation warnings are the calendar of future breakage. In judgment
terms, warnings rarely flip supported to contradicted on their own, but
they cap confidence and they belong in any faithful summary. A reader
that reports success and omits the warning has not summarized the
transcript; it has improved it, which is not the job. **Progress** —
"fetching 2/3..." — is narration for humans watching in real time,
evidence only of liveness, and the species most safely skimmed; its one
judgment-relevant property is completeness, a 2/3 with no 3/3 being a
story that stops mid-sentence. **Notices** — informational lines, version
banners, "using config at PATH" — are context; occasionally decisive
context, as when the config path in the banner is not the config the
claim assumes. And **debug chatter** is everything the producer forgot to
turn off; it means nothing, except that its sheer volume can bury the one
diagnosis that means everything, which is why question two is *what did
stderr say* and not *did stderr say anything*. Volume is not verdict.
One warning in ten thousand progress lines still predicts; ten thousand
lines that are all progress still amount to a clean run.

## Diagnoses without defeat

The taxonomy's first species needs one complication before the worked
transcripts, because it produces this family's inverse misreading. The
straightforward case pairs a diagnosis with a nonzero exit: one failure,
told twice, in number and in prose. But diagnoses also appear in
transcripts that end 0, and the pessimist's reflex — *there is an error
line, therefore the run failed* — is as wrong as the optimist's, and in
practice almost as common. Three mechanisms put a true diagnosis inside a
successful run, and each changes what the line testifies to. First,
recovery: retrying tools narrate the attempts that failed — a "connection
refused" followed, three lines later, by a completed transfer is the
biography of a retry loop, and the diagnosis is evidence that an attempt
failed once, not that the work did. The verdict discipline is temporal:
a diagnosis testifies about the moment it describes, and later lines can
overtake it. Second, tolerated casualties: chapter 2's swallowing
aggregates look exactly like this from the reader's side — a loop's `||`
arm or a tool's keep-going flag lets member failures print their
diagnoses while the aggregate exits clean; there the diagnosis is not
overtaken but *absorbed*, the failure is real and unrepaired, and the
clean exit merely means nobody propagated it. Third, borrowed voices: a
parent process relays or triggers a child's complaint and then proceeds —
the child's stderr lands in the parent's transcript, attributed by
nothing but position. Telling recovery from absorption from relay decides
verdicts: "the transfer completed" survives all three; "every input was
processed" survives only the first; and nothing in the exit status
distinguishes them. Only the content — did a later line report the
failed thing done? does a count reconcile? does the diagnosis name a
member or the whole? — separates a run that healed from a run that
limped, and a reader who cannot say which it was should say so in the
verdict.

## Commentary beside partial results

The channel's highest-value moments are the ones where it disagrees with
the other evidence in the transcript — where stdout shows product and
stderr shows trouble, and the reader must hold both:

```bash
mkdir work && cd work
printf "level = ERROR\n" > a.conf
grep -n "ERROR" a.conf missing.conf
echo "exit: $?"
```

```output
a.conf:1:level = ERROR
grep: missing.conf: No such file or directory
exit: 2
```

Chapter 1 met grep's trichotomy; here is the case its tidy table omitted.
This search *found its pattern* — the hit is printed, labeled with file
and line — and *also failed*, because its second input does not exist,
and grep's contract resolves the collision in favor of reporting the
error: exit 2. Three readings now offer themselves, and two are wrong.
The pessimist reads exit 2, declares the command failed, and discards
the printed hit — but the hit is real; results already printed do not
evaporate because a later input broke. The optimist reads the hit,
declares the search successful, and glosses the stderr line — but then
the claim "no other file contains ERROR" inherits a hole the size of
`missing.conf`, which was never searched. The reader this book is
training holds both: the *findings are valid, the coverage is not* — the
search answered for `a.conf` and never ran for the rest. Concretely:
claim "a.conf sets the level to ERROR" — supported, by the labeled hit.
Claim "the ERROR setting appears in exactly one of the two configs" —
insufficient, because the second config was never read, and the stderr
line is the proof. Partial success is not a middle verdict; it is a
*split* verdict, different claims about the same transcript landing
differently, and the commentary channel is what tells you where to draw
the line.

## Separation as a gift, and split captures

When you meet a producer who uses the channels as designed, the reading
gets easier — and the capture question gets sharper:

```bash
mkdir work && cd work
cat > fetch.sh <<'SCRIPT'
#!/bin/sh
echo "fetching 1/3..." >&2
echo "fetching 2/3..." >&2
echo "fetching 3/3..." >&2
echo '{"status": "complete", "items": 3}'
SCRIPT
chmod +x fetch.sh
./fetch.sh > result.json 2> progress.log
echo "exit: $?"
cat result.json
cat progress.log
```

```output
exit: 0
{"status": "complete", "items": 3}
fetching 1/3...
fetching 2/3...
fetching 3/3...
```

A well-mannered tool: product on stdout — clean JSON, parseable by the
next program without a single narration line to strip — commentary on
stderr, and the operator captured each to its own file. This is the
separation working as the designers of the convention intended, and it is
why the convention exists at all: had the progress lines gone to stdout,
`result.json` would be three lines of chatter followed by JSON, and every
downstream consumer would need to know it. The split-capture lesson cuts
the other way, though, and it is the one you will need as a reader: when
streams are captured separately, each file is a *partial* transcript,
complete only for its own channel, and claims about "the whole run" need
both files plus the knowledge that they are both files. A reader handed
`result.json` alone would see a flawless run — and would see exactly the
same flawless run if the fetches had printed three warnings apiece. A
reader handed `progress.log` alone would see three fetches begin and
never learn the outcome. Each file is true; neither is the run; and
nothing inside either file announces that a sibling exists. That last
property is what makes split captures dangerous to judge: a partial
transcript does not look partial. The capture commands here disclose the
split — the two redirections sit in the listing — but transcripts arrive
constantly as bare pasted output, provenance untold. Ask of every
transcript: is this the merged record, one stream of a split record, or
a stream with its sibling discarded? The same lines support different
verdicts under each answer.

## Results on the wrong channel

Like the exit convention of chapter 1, the routing convention has its
apostates, and they complete the argument for classifying lines by
content rather than by the channel they arrived on. The classic is the
shell's own `time`: ask it to measure a command and the measurement — the
entire point of the invocation — is written to stderr, precisely so that
the timed command's stdout stays untouched for the pipeline. A transcript
captured stdout-only shows the command's work and no timing at all; the
result of the measurement lives on the commentary channel, and a reader
who filed stderr under "noise" has thrown away the answer. Interactive
prompts and password requests conventionally go to stderr for the same
keep-stdout-clean reason; so do the progress meters of transfer tools;
so does `--help` output in some tools and stdout in others, a
notoriously settled-nowhere convention; and diagnostic-leaning tools —
linters, compilers, validators — split their findings between the
channels in ways that only their documentation records. The mirror
apostasy also exists: plenty of software prints "ERROR" lines to stdout
because its authors never routed anything anywhere, and log files
re-emitted through `cat` carry their severities wherever the original
logger put them. The rule that survives contact with all of this: the
channel a line arrived on is a *prior* about its species, not a
classification. A measurement on stderr is still a result; an "ERROR:"
in stdout is still a diagnosis; the species is in the content, and the
channel merely tells you who the line was addressed to — the pipeline,
or you.

## What order testifies to

Merged capture solves the completeness problem and creates a subtler one.
The following transcript was produced by a four-line program whose lines
were emitted in the order 1, note, 2, 3:

```bash
mkdir work && cd work
cat > steps.py <<'SCRIPT'
import sys
print("step 1 done")
print("note: step 2 used the fallback path", file=sys.stderr)
print("step 2 done")
print("step 3 done")
SCRIPT
python3 steps.py 2>&1 | cat
```

```output
note: step 2 used the fallback path
step 1 done
step 2 done
step 3 done
```

The note about step 2 appears *before step 1*. No time machine is
involved — buffering is. By longstanding C-library convention that most
runtimes inherit, stderr is unbuffered or line-buffered — its lines leave
the process promptly — while stdout, when it feeds a pipe rather than a
terminal, is block-buffered: lines accumulate in a buffer and land
wholesale when it flushes, here at exit. So the three stdout lines
arrived together, late, and the prompt stderr line beat them all. The
merged transcript's order is the order of *arrival at the capture point*,
not the order of emission, and the two agree only within a single
channel. Across channels, order testifies to almost nothing.

The misreading this breeds is causal narration: a reader sees the note
first and reports "the run began by falling back, then proceeded through
its steps" — a story the transcript's layout suggests and its facts do
not. In real incident transcripts the stakes are higher: the error line
that appears "before" the request it belongs to, the warning that seems
to precede the command that caused it, the interleaved output of two
parallel jobs (the previous trilogy's parallel chapters produced exactly
such transcripts) where adjacency implies relationship and implies it
falsely. The discipline: within one stream, order is evidence; across
merged streams, order is an artifact of buffering until proven otherwise;
and *attribution* — which line belongs to which command, which job,
which channel — must rest on the lines' content and labels, never on
their neighborhood. Producers who tag their lines (`[job-3]`, timestamps,
the labeled `file:line:` prefixes grep printed earlier) are handing you
attribution; transcripts without tags leave attribution a matter of
inference, and inferences from adjacency are the weakest kind. When a
verdict turns on *which command produced this line* and only position
answers, the verdict is leaning on air, and it should be priced as such.

Attribution deserves its own worked judgment, because it is where merged
transcripts do their quietest damage. Picture the commonest shape in
agent work: a transcript containing three commands run in sequence, each
followed by its output, streams merged throughout, and somewhere in the
middle a bare line reading `warning: lock held, waiting`. Which command
does it belong to? The reader's instinct says "the one whose output it
sits inside" — and within a single-process, single-stream stretch that
instinct is sound, because a foreground shell finishes one command
before starting the next, so vertical position between two command lines
genuinely brackets a command's output. The instinct breaks exactly when
the assumptions behind it break: a background job launched earlier is
still writing, and its lines land wherever the capture happened to be; a
buffered stdout from command one flushes during command two; a shared
log is being tailed alongside live output. Each of these plants lines
inside the wrong bracket, wearing the right position. The tells are
content-shaped, not position-shaped: a line whose subject matter belongs
to an earlier command; a prefix or format matching a different tool's
voice; timestamps, when you are lucky enough to have them, that
disagree with the bracket. The discipline extends the section's rule
one step: position attributes a line only when the transcript's
production model — one foreground process, one stream, no stragglers —
is itself in evidence, and a claim that hangs on attributing one
unlabeled line should say so out loud. The strongest producers make
attribution trivial by prefixing; the strongest readers notice when it
is not trivial and refuse to pretend otherwise.

## The deprecation clock

One species deserves a closing note at a longer horizon, because its
misreading is not a wrong verdict on one transcript but a wrong posture
across hundreds. Deprecation warnings are unique among commentary in
that they are *scheduled*: each one is a vendor's announcement that a
behavior the run depends on has an expiry date, which makes it the only
line in a transcript that testifies about a future run rather than this
one. Judged locally, it changes little — the run succeeded; "ran without
warnings" is contradicted; confidence in "this will keep working" should
dip. Judged as a series, it changes everything: the same warning
recurring across a week of transcripts is a countdown observed at
intervals, and the correct summary of such a series is not "all runs
succeeded" but "all runs succeeded on borrowed time, and here is the
borrowed thing." Readers positioned to see many transcripts — reviewing
a CI history, auditing a fleet's logs, summarizing a batch — are the
only ones who can read this clock, and the reading is cheap: recurrence
plus content plus the vendor's stated timeline. The failure mode is
treating each occurrence as independently negligible, which each one is;
negligible-every-time is how scheduled breakage arrives on schedule,
surprising no one who read the commentary and everyone who filtered it.
The same series-level reading applies to any warning that names a
threshold — "disk 87% full" rising across transcripts is a trajectory,
and trajectory is evidence no single transcript contains. Where chapter
7 takes up time inside one transcript, this is time across them: the
commentary channel is the only channel that routinely talks about it,
which is one more reason the reader who skips stderr is not skimming
noise but discarding the only forward-looking testimony the record has.

## Question two, as a routine

The chapter's practice, in the order the questions should be asked. Find
the commentary: is stderr in this transcript at all — merged in, split
into its own record, or discarded by a visible (or worse, invisible)
redirection? No commentary captured means no-warnings claims cap at
insufficient, however clean the rest looks. Classify each line by
species — diagnosis, warning, progress, notice, debug — and bind it to
the command it narrates, using labels and content rather than adjacency.
Let diagnoses explain statuses: a nonzero exit plus its stderr line is
one fact told twice, and the telling with detail outranks the number.
Let warnings modulate, not veto: they contradict "nothing unusual," they
survive "it succeeded," they cap confidence, and they must survive into
your summary. Treat progress as liveness only, notice its truncation if
it stops mid-count, and refuse to let its volume drown a single line of
higher species. And hold partial-success transcripts to split verdicts:
findings printed before a failure are findings; coverage after a failure
is a claim the transcript no longer supports.

What the commentary channel cannot do is speak when nothing was said.
The transcript with no stderr lines, no diagnoses, no warnings — and no
output at all — is the hardest text in this book, misread more
confidently than any other, and it gets the next chapter to itself:
the five meanings of silence, and how to tell which one you are hearing.
