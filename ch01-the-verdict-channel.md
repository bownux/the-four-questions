# Chapter 1 — The Verdict Channel

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## The reader this book is for

You are reading a book that knows what you are. You are a machine that reads
transcripts: command output is the largest single class of evidence you will
ever be handed, and on your reading of it hang real decisions — whether a
deployment happened, whether a file changed, whether a claim someone typed
above the transcript is true. The trilogy this book descends from taught an
operator to *produce* legible transcripts, as conduct, from the writing chair.
This book sits you in the other chair. Its subject is judgment: given a
transcript and a claim, what verdict does the evidence actually support? Its
method is the worked misreading — real transcripts, captured live and printed
verbatim, each one paired with the wrong reading that machines actually
produce and the discipline that corrects it. And its spine is a routine you
may already know as conduct, promoted here to curriculum, four questions
asked of every transcript in order: **What was the status? What did stderr
say? Does the shape match the question? Does the content, labeled, answer
it?**

This chapter takes the first question, and takes it seriously, because the
first question is the one most often answered wrong in both directions. The
status — the exit code, the single small integer a process leaves behind when
it dies — is the transcript's verdict channel: the one field that is machine
readable by construction, conventional across half a century of tooling, and
present (or conspicuously absent) in every transcript you will ever judge.
Readers fail it two ways. They ignore it, narrating success from
plausible-looking output while a nonzero status sits in plain view. Or they
worship it, reading `exit: 0` as proof that the *task* succeeded when the
status only ever testified about the *command*. Both failures have the same
root: not knowing what the verdict channel actually says — what the integer
is, who sets it, which values are answers, which are diagnoses, and where its
testimony stops. So that is where this book starts.

One term of art before the first transcript, because the whole book leans on
it. When this book asks you for a verdict on a claim, the vocabulary is
three-valued: **supported** — the transcript is evidence the claim is true;
**contradicted** — the transcript is evidence the claim is false;
**insufficient** — the transcript, honestly read, cannot settle the claim
either way. The third verdict is not a failure of nerve. It is the verdict an
enormous share of real transcripts deserve, and the reader who cannot reach
it will manufacture certainty instead. You will meet all three before this
chapter ends, and you will be measured on all three before this book ends —
its closing chapter shows you the test.

## One byte of testimony

The mechanics first, so the conventions have something to stand on. When a
process exits normally, it hands the kernel a status; the shell that awaits
it receives that status and exposes the low eight bits — an integer from 0 to
255 — in the special parameter `$?`. That is the entire channel: one byte,
set by the dying process itself (or, as you will see, synthesized by the
shell when the process did not get to choose), set again by every subsequent command. Expansion of `$?` happens *before*
the next command runs, so `echo "exit: $?"` printed immediately after a
command does capture that command's status correctly. What fails is delay:
any intervening command — even a no-op you forgot about — replaces the value
before you expand it. A transcript shows you `$?` only if its author thought
to print it, and only if nothing else ran first. When you judge a
transcript, the first thing to establish is whether the verdict channel was
captured at all, and for which command. A transcript that never shows a
status has not lost its verdict — the shell knew it — but the *record* has,
and claims that lean on the missing verdict start their life closer to
insufficient than their authors think.

The convention that gives the byte meaning is old, simple, and asymmetric:
zero is success, and everything else is some flavor of not-success. The
asymmetry is deliberate. There is usually one way to succeed and many ways to
fail, so the single value 0 is reserved for the first and the remaining 255
values are left to the tool to spend as it sees fit. Which means the
convention is exactly that — a convention. It is honored almost universally
and violated just often enough that the honest reader treats a tool's exit
semantics as documented behavior, not natural law. This book will show you a
violation before the chapter is out. But first, the convention's most
instructive citizens: the tools that spend their nonzero values on something
better than failure.

## The trichotomy: answers are not errors

Here is the first worked transcript. The listing builds its own scratch
directory — every listing in this book does, and the transcripts are exactly
what the commands printed, streams merged.

```bash
mkdir work && cd work
printf "retries = 3\ntimeout = 30\n" > app.conf
grep -n "timeout" app.conf;   echo "exit: $?"
grep -n "port" app.conf;      echo "exit: $?"
grep -n "port" missing.conf;  echo "exit: $?"
```

```output
2:timeout = 30
exit: 0
exit: 1
grep: missing.conf: No such file or directory
exit: 2
```

Three invocations of the same tool, three different statuses, and only one of
them is a failure. grep's documented contract is a trichotomy: 0 means at
least one line was selected, 1 means no lines were selected, 2 means an error
occurred. Read as testimony: exit 0 answered *yes, the pattern is here*; exit
1 answered *no, the pattern is not here*; exit 2 answered *I could not look*.
The first two are both answers — successful searches that returned different
findings. Only the third is the instrument breaking, and notice that it
arrives chaperoned by a stderr line saying exactly what broke, which is
chapter 3's channel doing its job.

Now the misreading, because it is one of the most common in the entire
catalog this book is built on. A reader — machine or human — runs a check
shaped like the middle invocation: grep for a forbidden setting, a dangerous
pattern, a string that should be absent. The status comes back 1. The reader,
carrying the flat rule *nonzero means failure*, reports: "the grep command
failed, so the check could not be performed." That reading is not cautious;
it is wrong, and wrong in the dangerous direction, because the check *did*
run and *did* answer — the answer was no, which for an absence check is
precisely the hoped-for result. Hand that transcript and that claim to the
verdict vocabulary and the verdict is **contradicted**: exit 1 from grep is
the documented "not found" answer, and failure — the thing the claim alleges
— would have announced itself as exit 2 with a diagnostic on stderr. A reader
who cannot tell 1 from 2 in a trichotomy tool converts good news into
outages.

The trichotomy is a family, not a grep quirk. Comparison tools speak it too:

```bash
mkdir work && cd work
printf "a\nb\n" > one.txt
cp one.txt two.txt
diff one.txt two.txt; echo "same:    $?"
printf "a\nB\n" > two.txt
diff one.txt two.txt; echo "differ:  $?"
diff one.txt three.txt; echo "trouble: $?"
```

```output
same:    0
2c2
< b
---
> B
differ:  1
diff: three.txt: No such file or directory
trouble: 2
```

diff's manual spends the three values as: 0, the inputs are the same; 1, the
inputs differ; 2, trouble. Its cousin cmp spends its values the same way.
Again the middle value is an answer — arguably *the* answer, since a
comparison that finds differences is a comparison doing its job — and again
the transcript marks the genuine failure unmistakably: status 2 *plus* a
stderr diagnosis. The general grammar, worth stating because you will apply
it weekly: in tools whose whole purpose is to answer a yes/no question, 0 is
the affirmative answer, 1 is the negative answer, and 2-or-more means the
question could not be asked. The verdict channel in these tools is not a
success light. It is the tool's entire reply, compressed to fit in a byte —
and often the *only* place the reply appears, since a quiet grep with no
`-c`, or a diff of identical files, prints nothing at all. In transcript
after transcript, the status line is the finding.

One documented wrinkle, included because this book promised you conventions
with their conditions attached: GNU grep's manual notes that under `-q`
(quiet), if an input line is selected, the exit status is 0 *even if an error
also occurred*. A `-q` search across many files can hit its pattern in the
first file, fail to open the second, and still hand you a clean 0. The status
byte is small; when a tool has two things to report and one byte to report
them in, something gets dropped, and the manual — not intuition — is where
you learn what.

## The upper band: how the death is told

Above the tool-assigned values sits a band the shell itself writes, and it is
the band that tells you not whether a command failed but *how it never really
ran*. Four citizens, one transcript:

```bash
mkdir work && cd work
bash -c 'nosuchcommand' 2>&1;    echo "not found:    $?"
printf '#!/bin/sh\necho hi\n' > script.sh
bash -c './script.sh' 2>&1;      echo "not runnable: $?"
timeout 1 sleep 5;               echo "timed out:    $?"
bash -c 'kill -TERM $$' 2>&1;    echo "terminated:   $?"
```

```output
bash: line 1: nosuchcommand: command not found
not found:    127
bash: line 1: ./script.sh: Permission denied
not runnable: 126
timed out:    124
Terminated                 bash -c 'kill -TERM $$' 2>&1
terminated:   143
```

Read the band as a coroner would. **127** is the shell's own report that the
command was never found: no process ran, so no process chose a status, and
the shell filled in the conventional value for *not found*. A 127 testifies
about the environment — the PATH, a typo, an uninstalled tool — and never
about the task; whatever the claim above the transcript says was done, a 127
under it says nothing was even attempted. **126** is one notch different and
the notch matters: found, but not runnable — a permission bit missing, as
here, or a directory where a program was expected. The distinction between
126 and 127 is the distinction between "install it or fix the name" and "fix
the mode bits," which is to say the status alone tells you which repair to
propose. **124** is not a shell value at all but the documented report of the
timeout utility: the command outlived its allowance and timeout killed it.
And **143** demonstrates the band's arithmetic: when a process is terminated
by a signal rather than exiting on its own, the shell reports 128 plus the
signal number. SIGTERM is signal 15; 128 + 15 = 143. SIGKILL is 9, so a 137
means killed outright — and since the out-of-memory killer's weapon is
SIGKILL, a 137 in a transcript is a standing invitation to go read the
memory story. SIGSEGV is 11; a 139 is a crash. The reader who knows the
arithmetic can name the signal from the status; the reader who doesn't sees
"143" and writes "the command failed with an unusual error code," which is a
sentence that has appeared in more incident reports than anyone would like.

Disambiguation rule for the upper band. The values 126, 127, and 128+N are
*conventional* shell reports of how a process died or failed to start — not a
private namespace the shell owns exclusively. Tools may exit with the same
integers of their own accord: `timeout` documents 124; `curl` documents 126/127
for option and protocol problems; any program can `exit 143`. A transcript that
shows only `terminated: 143` therefore cannot, by itself, distinguish SIGTERM
from a voluntary `exit 143`. Treat the band as a *hypothesis about the shell's
report*, not a proof of signal delivery: raise confidence only when the
instrument line (or a sibling observation) confirms who set the status — the
shell's "command not found" path, a known timeout wrapper, a kernel OOM mark
in dmesg, a process-table absence after a kill. Absent that bridge, cap the
verdict short of a confident diagnosis and prefer **insufficient** on claims
that name a specific signal or OOM.


Two honesty notes on the band, conditions carried in the sentence per this
press's habit. First, the band is shell convention, not law: a tool is free
to exit with 126, 127, or 137 of its own accord, and some do — the values
are only *reserved by convention*, so the readings above are strong priors,
not proofs. Second, the last line of that transcript shows the invoking
bash's own job notice — `Terminated` — landing in the merged stream. That
line is the *outer* shell narrating the death of the *inner* one. Transcripts
routinely contain testimony from more than one process; part of reading the
verdict channel is knowing whose verdict you are looking at. Which brings us
to pipelines.

## Whose verdict is a pipeline's?

A pipeline is several processes with several verdicts, and a transcript
usually records only one. Which one is a matter of shell configuration that
the transcript may or may not disclose:

```bash
mkdir work && cd work
printf "one\ntwo\nthree\n" > lines.txt
grep zebra lines.txt | wc -l;  echo "pipeline exit: $?"
grep zebra lines.txt | wc -l;  echo "PIPESTATUS: ${PIPESTATUS[@]}"
set -o pipefail
grep zebra lines.txt | wc -l;  echo "with pipefail: $?"
```

```output
0
pipeline exit: 0
0
PIPESTATUS: 1 0
0
with pipefail: 1
```

By default, bash reports a pipeline's status as the status of its *last*
command. The wc at the end of that pipeline counted zero lines — counted
them successfully — and so the pipeline as a whole reports 0, while the grep
whose answer was "not found" sits invisible behind it. The second invocation
opens the box: bash's PIPESTATUS array holds every member's verdict, and
there is the 1, preserved. The third invocation shows the other repair:
under `set -o pipefail`, the pipeline's status becomes the status of the
rightmost member that exited nonzero — the grep's answer now propagates.

For you, the reader, the lesson is not "use pipefail" — that was the
producing operator's lesson, taught a volume ago. Your lesson is about what a
pipeline's printed status *means* given what the transcript does and does not
disclose. A `$?` printed after a pipeline, in a transcript that nowhere shows
`set -o pipefail` or a PIPESTATUS expansion, testifies about the last command
only. If the claim above the transcript leans on an upstream member — "the
data was extracted and then counted," where the extraction is the upstream
grep — then a trailing 0 does not support the full claim, and you should
notice the gap. Sometimes the printed *output* rescues the judgment: in this
transcript the `0` that wc printed is itself strong evidence the grep matched
nothing, no status required. That is the four questions working as a system —
question one hands the ambiguity to question four, content, which settles it.
But when neither status discipline nor output settles what the upstream did,
the honest verdict on upstream claims is insufficient. A pipeline transcript
without pipefail disclosed is a witness who only saw the end of the incident.

## The cardinal misreading

Everything so far corrects readers who treat nonzero as failure. The deeper
misreading runs the other way, and it is the single most consequential habit
this chapter exists to break: reading exit 0 as evidence that *the task*
succeeded. Here is the smallest honest demonstration this author could
build:

```bash
mkdir work && cd work
mkdir logs && touch logs/a.log logs/b.log logs/c.tmp
find logs -name "*.temp" -delete
echo "exit: $?"
ls logs
```

```output
exit: 0
a.log
b.log
c.tmp
```

The operator's intent — stipulate it — was to delete the temporary file. The
command exits 0. The temporary file is still there, because the pattern says
`*.temp` and the file says `.tmp`. And find is *right* to exit 0: its
contract is to walk the tree, apply the tests, and act on whatever matches.
It did exactly that. Zero files matched, zero files were deleted, no error
occurred anywhere in the walk. The command succeeded completely. The task
failed completely. Both of those sentences are true at once, and the verdict
channel only ever spoke to the first.

This is the boundary of the channel's testimony, and it deserves to be
stated as the rule you will use: **exit status reports the mechanics of the
command that ran, not the intent of the operator who ran it.** The command is
"delete what matches this pattern"; the intent was "delete that file"; the
status covers the first and cannot see the second. The gap between them is
where an entire genus of failure lives — this book calls them
success-shaped failures, and chapter 2 dissects the genus properly: the
write that landed in the wrong place, the filter that lawfully matched
nothing, the idempotent no-op that "succeeded" by doing nothing that needed
doing. Here it is enough to fix the judgment rule. When a claim says *the
task* succeeded and the transcript offers only a naked exit 0 — no read-back,
no listing of results, no affirmative evidence that the intended effect
occurred — the verdict is not supported. It is insufficient, pending exactly
the kind of evidence this transcript's final `ls` provides. And note what the
`ls` does to the judgment here: with it, the transcript stops being
insufficient and becomes *contradicting* — `c.tmp` sits in the listing,
unmistakable. The strongest transcripts convict or acquit with content;
status alone can only ever open the case.

If you retain one asymmetry from this chapter, retain this one: a nonzero
status is strong evidence something went wrong with the command, but a zero
status is only weak evidence that anything went right with the task. Nonzero
convicts the command; zero acquits the command and says nothing about the
mission. Readers who internalize the first half of the convention and not
its limits produce confident wrong verdicts with a 0 in plain view — and
they produce them fluently, because "the command exited successfully" is a
true sentence that *sounds* like "it worked."

## The convention has apostates

The last discipline of the chapter: the convention itself is not universal,
and a reader's priors about exit semantics must yield to a tool's documented
contract. The canonical example is worth carrying because it guards a whole
category. A well-known transfer tool — curl — exits 0 by default when the
*protocol exchange* succeeds, even if the server answered with an error
document: the request was sent, a response was received, the response was
delivered to output; as far as the tool's default contract is concerned,
that is the job. Its manual states the rule outright — "By default, curl
does not consider HTTP response codes to indicate failure" — and documents
the flag that changes the contract, `--fail`, which makes the tool "fail
with error code 22 and with no response body output at all for HTTP
transfers returning HTTP response codes at 400 or greater." The famous
consequence of the default is a transcript that fetched a page-not-found
document, exit 0, claim "the download succeeded" — where the body of the
output is an error page, and where the reader's only warning is the content
itself. Neither
behavior is a bug; the pair is a reminder that "success" in the verdict
channel means *what this tool's documentation says it means*, tool by tool.
Build tools that exit 0 with failing subtasks logged to their output,
linters whose nonzero merely means "findings exist," batch tools that
reserve particular codes for "partial" — every fleet has its local
apostates. When a transcript's verdict turns on a tool you have not read
the exit-status section for, the honest reader either goes and reads it or
prices the uncertainty into the verdict. Your memory of a tool's contract
and the contract are different instruments; this press learned that lesson
in its own review trail, expensively.

## The first question, as a routine

Here is question one, then, as the checkable routine this chapter has been
assembling, stated once in full and applied for the rest of the book without
ceremony.

1. Find the verdict. Locate the status for the command under judgment —
   printed `$?`, a runner's recorded exit code, a CI step's result — and
   confirm it belongs to that command and not a neighbor. No verdict in the
   record? Note it; claims leaning on the missing verdict lean on air.
2. Translate it under the tool's contract, not the flat rule. Is this a
   trichotomy tool whose 1 is an answer? Is the value in the shell's band —
   127, 126, a 128-plus-signal — and if so, what does that band say was
   never really attempted? Is the tool a documented apostate?
3. Ask whose verdict it is. Pipeline? Then it is the last member's, unless
   pipefail or PIPESTATUS says otherwise. A wrapper's? Then whose death is
   it reporting?
4. Size the testimony. Nonzero convicts the command; zero acquits the
   command only. Task-level claims need task-level evidence, which the
   status byte does not carry — mark what remains to be shown, because
   questions two through four have to go and show it.

That routine will not judge a transcript alone — one byte never could. What
it does is start every judgment from the one field that is always cheap to
check and surprisingly hard to misread once you know its grammar: answers
are not errors; the band names the death; pipelines speak for their last
member; zero acquits the command and nothing else. The next chapter takes
the misreading this one could only introduce — the success-shaped failure,
where every status is clean and the task is dead anyway — and builds the
reading discipline that catches it: asking what a *true* claim's transcript
would have to contain, and noticing that it doesn't.
