# Chapter 2 — What the Number Cannot Say

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## The genus

Chapter 1 ended on an asymmetry: nonzero convicts the command, zero acquits
the command and says nothing about the mission. This chapter lives entirely
inside that gap. Its subject is the success-shaped failure — the transcript
in which every status is clean, every command did exactly what its contract
promised, and the task is dead anyway. No other genus of failure is as
dangerous to you, the reader, because no other genus recruits the evidence to
the wrong side. A crashed command leaves a nonzero status and a stderr
diagnosis; the transcript fights for you. A success-shaped failure leaves a
column of zeros and output that looks like progress; the transcript fights
against you, and the claim sitting above it — "backed up," "updated,"
"cleaned" — reads as confirmed by every field you check first.

The genus has an anatomy, and the anatomy is learnable. Every success-shaped
failure is a gap between two different things the word "it" means in the
sentence "it worked": the *command* that ran — a specific program, given
specific arguments, with a documented contract — and the *task* the operator
intended — a change in the world that the command was chosen to bring about.
The command's contract was honored; the task's intent was not; and the exit
status, as chapter 1 established, only ever testified about the first. What
makes the genus catalogable is that the gap opens in a small number of
recurring places. This chapter works through the four you will meet most —
the write that lands in the wrong place, the filter that matches nothing
lawfully, the no-op wearing success, and the aggregate that swallows its
failures — and then builds the reading discipline that catches all four at
once, because the correcting question is the same every time: *what would
this transcript also contain, if the claim were true?*

## The write that landed in the wrong place

Start with the anatomy's most treacherous species, treacherous because the
data is real, the write is real, and everything is real except the place.

```bash
mkdir work && cd work
printf "retries = 3\n" > app.conf
printf "port = 8080\n" > net.conf
cp app.conf backup;  echo "first copy:  $?"
cp net.conf backup;  echo "second copy: $?"
ls
cat backup
```

```output
first copy:  0
second copy: 0
app.conf
backup
net.conf
port = 8080
```

The operator's intent — stipulate it, as before — was to copy both
configuration files into a backup *directory*. No directory named `backup`
existed. And cp's contract for the two-argument form does not require one:
`cp source dest` copies the source to a destination *file* named dest. So
the first command created a regular file named `backup` containing the first
config; the second command overwrote that file with the second config; both
exited 0, correctly, because both did precisely what the two-argument
contract says. Now read the evidence like a judge. The claim is "both
configuration files are backed up." The statuses support nothing beyond
"both cp commands completed." The `ls` shows three names where a backup
directory should make a different shape — chapter 5 will train that instinct
formally — and the `cat` closes the case: the file called backup holds one
line, the second file's line, and the first file's content is nowhere. The
verdict is contradicted, and the interesting forensic fact is that *at no
point did anything fail*. The first copy's data was destroyed by the second
copy's success.

The species generalizes well beyond cp. The redirect that wrote to a
relative path while the working directory was somewhere unexpected; the
deploy that copied into a stale symlink's target; the archive extracted into
the wrong root — in every case the write succeeds, the bytes land, and the
place is wrong. What the species teaches is that *destination is part of the
task and absent from the verdict*. A clean status on a write testifies that
bytes were written somewhere the command found writable. Whether that
somewhere is the task's somewhere, only content evidence — a listing, a
read-back, a path printed and checked — can say.

## The filter that matched nothing, lawfully

Chapter 1 praised the trichotomy tools for spending their exit values on
answers: grep tells you found-or-not in the status itself. The trap in this
species is assuming that disclosure is universal — that any tool applying a
pattern would surely mention whether the pattern hit. Most stream editors
will not:

```bash
mkdir work && cd work
printf "max_conn = 50\nlog_level = info\n" > server.conf
sed -i "s/max_connections = .*/max_connections = 200/" server.conf
echo "exit: $?"
cat server.conf
```

```output
exit: 0
max_conn = 50
log_level = info
```

The intent was to raise a limit to 200. The substitution's pattern says
`max_connections`; the file says `max_conn`; the pattern matched zero lines.
And sed's contract is perfectly content with that: its job is to run the
script over the stream, applying substitutions *where they match*, and a
script that matches nowhere is a lawful run, exit 0. sed does not spend its
exit values on match-or-not the way grep does — a no-match edit and a
successful edit are indistinguishable in the verdict channel. The transcript
convicts anyway, but only because the operator printed the file afterward:
`max_conn = 50`, unchanged, sits in plain view, and the claim "the limit is
now 200" is contradicted by read-back. Strip that `cat` from the transcript
— and countless real transcripts are exactly this one without the cat — and
you are left with an edit command, an exit 0, and a claim. The verdict then
is insufficient, and saying so is not pedantry. It is the difference between
a reader that reports "the transcript shows the edit command succeeded but
contains no evidence the file changed" and a reader that launders a silent
no-op into a confirmed configuration change.

Name the general principle, because it upgrades chapter 1's rule: **tools
differ in how much of their findings they disclose through the verdict
channel, and the disclosure level is part of the tool's contract.** grep
discloses found-or-not. diff discloses same-or-different. sed, awk, and most
editors disclose only ran-or-broke. The identical byte — 0 — therefore
carries different amounts of information depending on which program produced
it, and a reader who does not know a tool's disclosure level does not yet
know what its 0 means.

## The success that destroyed its own input

One variant of the wrong-place species is worth isolating, because it is the
most destructive transcript in this chapter and the most innocuous-looking:

```bash
mkdir work && cd work
printf "beta\nalpha\ngamma\n" > data.txt
echo "before: $(wc -l < data.txt) lines"
sort data.txt > data.txt
echo "sort exit: $?"
echo "after:  $(wc -l < data.txt) lines"
cat data.txt
echo "(nothing above this line is the file's remaining content)"
```

```output
before: 3 lines
sort exit: 0
after:  0 lines
(nothing above this line is the file's remaining content)
```

Three lines in, zero lines out, exit 0, and the data is gone. The mechanism
is the shell's, not the tool's: redirections are set up *before* the command
runs, so `> data.txt` truncates the file to zero length, and only then does
sort open the now-empty file and dutifully sort nothing into it. Every
component behaved exactly as documented. The status is clean because
nothing failed. And the transcript of a successful in-place sort — which is
what the operator believed they were running — would look identical but for
the counts, which is why the counts are the only reason this page can tell
you what happened.

Read the judgment implications carefully, because they generalize past this
one idiom. First, a clean status can accompany *destruction*, not merely
inaction; chapter 1's rule that zero acquits the command needs the corollary
that acquitting the command says nothing about what the command's setup
destroyed on the way in. Second, the evidence that convicts here is
quantitative and comparative — a before count and an after count — and
neither alone would have shown anything: 0 lines after is only alarming if
you know there were 3 before. Transcripts that measure both sides of an
operation are the ones that can testify about it at all, and their absence
is the single most common reason a transformation claim lands on
insufficient. Third, the same shape recurs wherever a command's output
destination is also one of its inputs: in-place edits attempted by
redirection, archives extracted over their own source, a copy whose
destination is resolved through a symlink back to the source. When a
transcript shows a command whose input and output name the same thing and
prints no before/after counts, the honest verdict on "the data was
transformed" is insufficient — and the honest next sentence is that the
transcript is also consistent with the data being gone.

## The no-op wearing success

The third species is the strangest, because the command not only succeeds —
it succeeds *by design* precisely when it changes nothing:

```bash
mkdir work && cd work
rm -f stale.lock;   echo "rm exit:    $?"
mkdir -p cache;     echo "mkdir exit: $?"
ls -A
```

```output
rm exit:    0
mkdir exit: 0
cache
```

No file named `stale.lock` ever existed in this directory — the listing
builds the directory fresh, and the final `ls -A` shows nothing but the
cache directory just created. Yet `rm -f` reports 0. That is the `-f`
contract: force mode's documented behavior includes not complaining about
missing operands — it converts "remove this file" from an action into a
goal: *make it so this file does not exist*. The goal was already met, so
the command succeeds without acting. `mkdir -p` is the same shape in the
other direction: *make it so this directory exists*, succeed whether or not
you had to create it. These are goal-state contracts, and operators use them
deliberately — the previous trilogy taught its reader to prefer them,
because retried scripts need commands that tolerate their own success.

But goal-state semantics change what the transcript can testify to, and the
reader must reprice accordingly. Under an action contract, exit 0 means *the
action occurred*. Under a goal-state contract, exit 0 means only *the goal
state now holds* — whether anything happened is undisclosed. So consider the
claim "a stale lock file was found and removed." The rm line supports "no
lock file exists now." It cannot distinguish "removed one" from "there was
never one to remove"; the historical half of the claim is beyond the
command's testimony, and with nothing else in the transcript speaking to it,
the verdict is insufficient. Readers stumble here in a characteristic way:
the claim's narrative — found, then removed — is *plausible*, the command is
*consistent* with it, and consistency gets promoted to confirmation.
Consistency is not confirmation. A transcript consistent with the claim and
equally consistent with its negation supports neither; that sentence is
half of what "insufficient" means, and goal-state tools produce such
transcripts by design.

## The aggregate that swallows

The fourth species scales the gap up: compound structures — loops,
conditionals, scripts — whose single reported verdict summarizes many inner
verdicts, using rules the reader had better know:

```bash
mkdir work && cd work
printf "ok\n" > a.txt
printf "ok\n" > b.txt
for f in a.txt b.txt c.txt; do
  grep -q ok "$f" 2>/dev/null && echo "$f: valid" || echo "$f: INVALID"
done
echo "loop exit: $?"
```

```output
a.txt: valid
b.txt: valid
c.txt: INVALID
loop exit: 0
```

Three inputs, one of which does not exist. The check on `c.txt` failed —
grep could not even open the file — and the loop reports 0. Two mechanisms
conspire, both documented shell behavior. The `|| echo` arm exists to
*report* failure, but echo itself succeeds, so each iteration's compound
command exits 0 no matter which branch ran — the failure is converted into
a successful report of failure. And a for loop's exit status is its last
iteration's status, so even without the echo the loop would report on
`c.txt` alone and stay silent about any earlier casualty. The aggregate's
verdict channel has a compression contract, and the contract is lossy:
last-iteration status, failures narrated instead of propagated, `set -e`
absent and — as the previous trilogy documented — full of exceptions even
when present. Verdict-channel testimony thins as structures nest.

Precondition for swallowed-failure demos. The listings in this section assume bash defaults: `set -e` / `errexit` off and `set -o pipefail` off. With `errexit` on, a failing iteration can abort the loop before a later `echo` repaints the status to 0. With `pipefail` on, a pipeline's status is no longer only its last stage. Size any claim of the form "exit 0 means the whole aggregate was fine" against that option state — or the observation is about a different shell than the one you are judging. The same precondition applies to `|| true` swallowers later in this chapter.

What rescues this transcript is its content: `c.txt: INVALID` is printed,
plain as day. Against the claim "all three inputs validated," the verdict
is contradicted — by line three of the output, not by the status. This is
the pattern you should notice recurring: in every species of this genus,
the conviction, when one is available at all, comes from *content* — the
cat, the ls, the printed INVALID — while the statuses stand in a row
swearing everything is fine. Question one opens the case. Question four
closes it. The chapters between teach the channels the closing evidence
travels through.

The largest aggregates you will judge are not shell loops but continuous-
integration runs, and they deserve a paragraph in this species' entry
because their verdict channels are aggregates of aggregates: a "green
build" is a summary of steps, each step a summary of a script, each script
a summary of commands, and every layer applies its own lossy compression.
A step's script may narrate failures the way this listing's `|| echo` arm
does, deliberately or by cargo-culted defensiveness; a `|| true` deep in a
build script converts a broken sub-task into green all the way up the
stack. Test harnesses add their own goal-state wrinkle: a suite that
*skipped* tests — because a dependency was missing, a marker excluded
them, a filter matched nothing (the second species, wearing a test
runner's clothes) — commonly reports success, and "0 failed" is a very
different fact from "all passed" when the unstated third number is "40
skipped." When a claim above a CI transcript says "the tests pass," the
residue a true claim leaves is the counts: how many ran, how many passed,
how many skipped, and whether the ran-count matches the suite's known
size. A green badge with no counts is the aggregate's exit 0 — it acquits
the pipeline's machinery and says far less about the code than its color
implies. The reasoning to carry off is size-matching: the summary is
true, the claim is bigger than the summary, and the difference is visible
only to a reader who checked the claim's size against the evidence's —
a discipline chapter 6 will name properly and drill.

## The discipline: ask what a true claim would leave behind

Four species, one correcting discipline. When a transcript's statuses are
clean and a claim above it asserts task success, do not ask "did anything
fail?" — in this genus nothing did. Ask instead: **if the claim were true,
what else would this transcript contain?** A true "both files backed up"
leaves a backup directory listing with two names in it. A true "limit
raised to 200" leaves a read-back line saying 200. A true "stale lock
removed" leaves — at minimum — some evidence a lock existed. A true "all
inputs validated" leaves per-input verdicts, all of them affirmative. Then
look for that residue. Present: the claim is supported, and by evidence
rather than by the absence of visible failure. Absent: the verdict is
insufficient, and you say what is missing. Present-but-wrong — the cat that
shows the old value, the INVALID in the roll call: contradicted, and you
cite the line.

The producing operator's version of this discipline appeared a volume ago
as conduct: verify your own effects, read back what you wrote, emit
affirmative evidence because your successor cannot ask you questions. Here
is what the discipline looks like when the producer follows it, and what
it does for you when they do:

```bash
mkdir work && cd work
printf "retries = 3\n" > app.conf
printf "port = 8080\n" > net.conf
mkdir -p backup
cp app.conf net.conf backup/;  echo "copy exit:     $?"
ls backup
cmp -s app.conf backup/app.conf && cmp -s net.conf backup/net.conf
echo "read-back:     $?"
```

```output
copy exit:     0
app.conf
net.conf
read-back:     0
```

Same task as the chapter's first listing, done right and — more to the
point — *evidenced* right. The destination is created before it is used;
the multi-source form of cp is chosen, which requires the destination to
be a directory and would have failed loudly in the first listing's
situation; the directory is listed after; the copies are compared
byte-for-byte against their sources, and the comparison's verdict is
printed. Against "both configuration files are backed up," this transcript
is supported — not because its statuses are clean, but because the residue
a true claim requires is present at every point where the first listing
left silence. Notice also what the comparison step is: cmp is a trichotomy
tool, deployed here precisely because its verdict channel *does* disclose
same-or-different. The skilled producer reaches for high-disclosure tools
at verification points for the reader's sake. When you meet a transcript
built this way, the reading is easy. This book exists because most
transcripts are not, and the reader must supply, by inference and by
verdict discipline, the caution the producer left out.

## Where the genus breeds: verbs and their residues

The discipline gets faster with a catalog, because success-shaped failures
cluster around a small set of claim verbs, and each verb has a
characteristic residue — the evidence a true instance leaves behind — that
you can learn to demand by reflex. *Created* claims (files, directories,
records) require the created thing observed after the fact: a listing, a
stat, a query that finds it. Creation commands are heavily goal-state in
practice — the `-p` and `IF NOT EXISTS` idioms — so their clean exits
testify to existence, never to novelty; if the claim's force depends on the
thing being *new*, the residue must include evidence of prior absence, and
almost no transcript carries it. *Updated* claims require the new value
read back from the authoritative place — not echoed from the variable that
was about to be written, which proves intent rather than effect. The
distance between "the transcript prints the value we meant to write" and
"the transcript prints the value the file now holds" is the entire
distance between intent and effect, and fluent transcripts blur it
constantly. *Removed* claims require the absence checked — and here recall
chapter 1's grep: the checking command's "not found" answer is an exit 1,
so the residue of a true removal claim frequently *is* a nonzero status,
one more way the flat nonzero-is-failure rule inverts a verdict. *Migrated*
and *converted* claims, the bulk verbs, require counts on both sides —
so-many read, so-many written — and ideally a reconciliation of the two;
a migration transcript without numbers is a narrative, not evidence.
*Cleaned* and *rotated* and *pruned*, the maintenance verbs, are the
no-op species' home terrain: their tools are built idempotent, their
clean exits mean "the goal state holds," and whether this run did
anything is exactly what the status cannot say — a true "cleaned up 400MB
of old logs" leaves before-and-after measurements or it leaves a claim
the transcript merely permits.

None of this asks you to memorize tools. It asks you to translate the
claim's verb into its residue before reading the transcript, so that
reading becomes checking — presence, absence, or wrongness of something
specific — instead of the vague gestalt scan that fluent output defeats.
The translation also disciplines confidence, which this book's eval
measures alongside accuracy: a verdict of supported reached through
residue found is worth high confidence; the same verdict reached because
nothing visibly failed deserves little, and the honest number says so.

## When the read-back shares the flaw

One limit on the correcting discipline itself, stated now because chapter
7 will need it and because a discipline whose failure mode you cannot
name is a superstition. Read-back verification works by re-observing the
world through a second command and comparing against intent. Its blind
spot is the case where the second observation *shares the flaw of the
first act* — where whatever misdirected the write misdirects the check
identically, and the two agree with each other while both disagree with
the world. The operator who wrote to the wrong host's config reads it
back from the same wrong host: match. The edit landed in a stale copy of
a file, and the cat that verifies reads the same stale copy: match. The
loop validated the wrong directory's inputs, and the summarizing recount
recounts the same wrong directory: match. In each case the transcript
contains genuine residue — value read back, comparison passed — and the
claim is still false, because act and check traveled the same wrong path
and the agreement between them proves consistency, not correctness.

As a reader you cannot always detect this from inside the transcript;
that is what makes it the genus's most advanced species. What you can do
is grade the *independence* of the verification you are shown. A
read-back through the same variable, the same relative path, the same
session's working directory inherits every assumption the act made; a
verification through an absolute path, a different tool, a different
vantage (the consumer of the file rather than its producer) inherits
fewer. The strongest residue is one whose route to the world shares as
little as possible with the act it is checking — the previous volume
called the pattern verify-by-consumer, proving a backup by restoring
from it rather than by listing it. When the claim's stakes are high and
the verification shown is same-route, the disciplined verdict is
supported-with-a-caveat at best, and your confidence number should carry
the caveat even when the verdict cannot.

## The two questions wearing one sentence

So: question one, extended to its honest limit. The status byte tells you
whether commands honored their contracts. It cannot tell you the contract
was the task — that the destination was the intended one, the pattern
matched what the operator imagined, the goal state changed rather than
merely held, the aggregate's members all share the summary's cheer. "Did
it work" is two questions wearing one sentence, and the verdict channel
answers only the smaller of them. The larger one is answered, when it is
answerable at all, by what the command left in the world and in the
transcript — and the next two chapters take up the channels that evidence
arrives through, beginning with the one the status byte cannot silence:
the commentary stream, where processes explain themselves while dying and,
sometimes more usefully, while succeeding.
