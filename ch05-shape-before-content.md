# Chapter 5 — Shape Before Content

*Draft status: author draft; human verification pending. Every runnable listing
was executed by the author during writing in a scratch directory the listing
itself creates; printed outputs are real transcripts.*

## The question you did not ask

The third question — *does the shape match the question?* — sits where it
does for a reason. It comes after status and commentary and before content,
because it is the check that decides whether reading the content is worth
doing at all. A transcript can be valid, well-formed, richly detailed,
fluent in every particular, and *about something else*. No amount of careful
content reading rescues a reader from that; careful content reading is
exactly how the wrong transcript gets promoted into a confident answer,
since the content is real and answers *its* question beautifully. The only
defense is to check the fit first: what question does this output actually
answer, and is it the question the claim above it turns on?

The failure has a shape of its own, which is what makes it teachable. In
almost every instance the transcript answers an *adjacent* question — one
close enough to the intended question that the answer looks responsive, far
enough that the answer is worthless or inverted. Adjacent in scope: the
right query, the wrong subtree. Adjacent in subject: the right pattern found
in the wrong file. Adjacent in time: the right measurement, taken before the
change. Adjacent in aggregation: a count of the wrong things. Adjacent in
completeness: the first five lines of a thirteen-line answer. This chapter
works those adjacencies with real transcripts, and then states the routine
that catches them, which is cheaper than any of the readings it prevents:
*name the question the output answers, in one sentence, before reading the
output for its answer.*

## Right pattern, wrong document

Start with the adjacency that hides in plain sight, because the searched-for
string genuinely appears:

```bash
mkdir work && cd work
mkdir -p etc docs
printf "listen_port = 9090\n" > etc/service.conf
printf "The service listens on port 8080 by default.\n" > docs/README.txt
echo "== the question: is the service configured for port 8080? =="
grep -rn "8080" .
echo "exit: $?"
```

```output
== the question: is the service configured for port 8080? ==
./docs/README.txt:1:The service listens on port 8080 by default.
exit: 0
```

Everything about this transcript reads like confirmation. The question was
port 8080; the search was for 8080; the search succeeded, exit 0; a line
came back containing 8080; the line even *says* the service listens on port
8080. A reader running on fluency stops here and reports the claim
supported. Then look at what the matched line is: a sentence in
`docs/README.txt`, prose written by a human, about defaults. The actual
configuration file is `etc/service.conf`, and it says 9090. The transcript
answers the question *"does the string 8080 appear anywhere under this
directory?"* — truthfully, yes — while the claim needs an answer to *"what
port is this service configured to use?"*, which is 9090, the exact opposite
of what the reader just reported. The verdict, read honestly, is
contradicted-in-fact and insufficient-on-this-evidence: the search's scope
included documentation, and documentation is not configuration.

This adjacency — *evidence about a description of the system, mistaken for
evidence about the system* — is one of the most common in real practice, and
it multiplies in modern repositories, which are full of documents that
describe the system in the system's own vocabulary: READMEs, comments,
example configs, test fixtures, commented-out lines, changelogs describing
what used to be true, templates describing what could be true. A recursive
grep treats all of them as equal witnesses. The reader's correction is not
to distrust grep but to *read the match's address before its content*: the
`file:line:` prefix that grep prints (and that chapter 6 will formalize as
labeling) is the part of the output that answers "whose testimony is this?"
A hit in a README testifies about documentation. A hit in a test fixture
testifies about a test. A hit in a commented-out line testifies about
history. Only a hit in the file the running system actually reads testifies
about the running system — and knowing which file that is, is knowledge the
transcript itself rarely contains.

## The instrument that sees itself

Some transcripts answer a question that is not merely adjacent but
self-referential — the measurement includes the measurer:

```bash
mkdir work && cd work
printf '#!/bin/sh\nsleep 5\n' > svc.sh
chmod +x svc.sh
./svc.sh > /dev/null 2>&1 & SVC=$!
sleep 1
echo "== while the service runs =="
ps -eo args= | grep "svc.sh"
echo "match count: $(ps -eo args= | grep -c "svc.sh")"
kill "$SVC" 2>/dev/null; wait "$SVC" 2>/dev/null
echo "== after the service is stopped =="
ps -eo args= | grep "svc.sh"
echo "match count: $(ps -eo args= | grep -c "svc.sh")"
pgrep -f "svc.sh" > /dev/null; echo "pgrep exit: $?"
```

```output
== while the service runs ==
/bin/sh ./svc.sh
grep svc.sh
match count: 2
== after the service is stopped ==
grep svc.sh
match count: 1
pgrep exit: 1
```

The classic, in both of its states. While the service runs, the process
table holds two matching entries: the service, and the grep that is looking
for it — because the grep's own command line contains the string it is
searching for, and `ps` lists the grep as faithfully as it lists everything
else. After the service is killed, one match remains, and it is the grep
alone. That surviving line is the trap: a transcript ending in `grep svc.sh`
and a match count of 1, presented under the claim "the service is running,"
is *contradicted* — the only thing running is the search. Every element of
the misreading is supplied by the transcript's own shape: output is present
(not silence), the count is nonzero, the line contains the service's name.
A reader checking content without checking shape sees a match and answers
yes. A reader who asks what the output is a list *of* — running processes,
including this pipeline's own members — notices that the question "is the
service in this list?" requires excluding the asker from the list first.

Note the last line, which is the same question asked with an instrument that
does not have this flaw: `pgrep` matches processes without listing itself,
and its exit 1 is chapter 1's trichotomy answering *no* cleanly. When a
transcript offers both a self-matching instrument and a clean one, the clean
one is the testimony. When it offers only the self-matching one, the reader
subtracts the known artifact — one line, the grep itself — before counting.

Operational requirement for process-table listings. The harness that produces the transcript must not carry the search pattern in its own `args=` — otherwise the observer is guaranteed to appear in the observation. Assemble the target name at runtime, use a self-avoiding pattern such as `[s]vc`, or filter on fields a wrapper will not share. Chapter 5's lesson is not complete until the capture procedure itself obeys the subtract-observer rule; a checker that only scans for usernames will not catch this family.

A note on how this chapter's transcript was produced, because it is the
chapter's lesson happening to its author. The first capture of that listing
printed *three* matches, not two, and the third was neither the service nor
the grep: it was the interactive shell in which this author was composing
the listing, whose command line contained the script's text — including the
string `svc.sh` — and which therefore appeared in the process table as a
match. The capture was polluted by the act of capturing. Re-run through a
harness whose own command line does not contain the pattern, the transcript
is the clean two-line result printed above. The general form is worth
carrying: *the process table includes the observer*, and so do many other
system views — open-file lists include the lister, connection tables include
the querying connection, directory listings include the script doing the
listing (a trap this press's own gate taught its authors expensively). When
a transcript's shape can include its own production, subtract the production
before reading the shape.

## Truncation as a shape

The third adjacency is the most mechanical and the least noticed, because
the mechanism that causes it is a tool nobody thinks of as a filter:

```bash
mkdir work && cd work
mkdir logs
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  printf "2026-08-29 request %02d handled\n" "$i" >> logs/app.log
done
printf "2026-08-29 ERROR upstream refused\n" >> logs/app.log
head -5 logs/app.log
echo "--- head -5 above; wc -l below ---"
wc -l < logs/app.log
```

```output
2026-08-29 request 01 handled
2026-08-29 request 02 handled
2026-08-29 request 03 handled
2026-08-29 request 04 handled
2026-08-29 request 05 handled
--- head -5 above; wc -l below ---
13
```

Five orderly lines of successful requests, and a file that has thirteen. The
thirteenth is an error, and it is invisible to this transcript by
construction: `head -5` is a filter that keeps the beginning and discards
everything else, including — as here, and as in logs generally — the part
where things went wrong, since logs record trouble in the order it happens
and trouble usually happens after a while. Against the claim "the log shows
the service handling requests normally," the head-only evidence is
insufficient in the precise, checkable sense this book means: the transcript
covers 5 of 13 lines, the claim covers all of them, and the uncovered
fraction is where the counter-evidence lives. The `wc -l` is what makes the
gap visible, and its presence in this listing is deliberate: a count beside
a truncated view converts an unknown truncation into a known one, which is
the difference between insufficient-and-you-know-it and
insufficient-and-you-don't.

Truncation arrives in more disguises than `head`. `tail` keeps the end and
loses the beginning — including startup errors and the configuration banner
that would have told you which config was loaded. Pagers, `less`-style
viewers, and terminal scrollback keep a window. Log viewers and CI web
interfaces silently cap at some number of lines, occasionally with a notice
("showing last 100 lines") and occasionally without. Chat and issue-tracker
paste boxes truncate at a size limit, sometimes mid-line, sometimes with an
ellipsis nobody notices. Notebook and REPL displays abbreviate long
structures with markers like `...`, and a reader who takes an abbreviated
display for a complete one will confidently report on elements that were
never shown. Every one of these produces a transcript whose *shape* — a
window, not a whole — is the single most decision-relevant fact about it,
and the correcting question is always the same: is this the output, or a
view of the output? Look for the marks: an explicit truncation notice, an
ellipsis, a suspiciously round line count (exactly 100, exactly 1000), a
first line that begins mid-record, a last line cut off mid-word. When any
of them is present, the honest verdict on any whole-of-the-data claim is
insufficient, and the missing region is not a small caveat — it is
precisely the region the producer's filter chose not to show you.

## Counting the wrong things

The fourth adjacency lives in aggregates, where the output is a single
number and the number answers a subtly different question than the one
asked:

```bash
mkdir work && cd work
printf "name,role,active\nalice,admin,true\nbob,viewer,false\ncarol,admin,false\n" > users.csv
echo "== count of admins (naive) =="
grep -c admin users.csv
echo "== count of ACTIVE admins (column-aware) =="
awk -F, '$2=="admin" && $3=="true"' users.csv | wc -l
```

```output
== count of admins (naive) ==
2
== count of ACTIVE admins (column-aware) ==
1
```

Two counts of the same file, differing by a factor of two, and both correct
about what they measure. The naive count answers "how many *lines* contain
the string admin" — which happens to equal the number of admin rows here,
and would not if any user's name were "administrator," if a viewer's
comment mentioned admin, or if the header row said "admin_role." The
column-aware count answers "how many rows have role=admin *and* active=true"
— which is what an access review actually wants to know, and which the
naive count over-reports by including the disabled account. Against the
claim "two administrators can access the system," the naive transcript
looks like support and is contradicted by the second measurement, taken from
the same file three lines later.

The general lesson is about aggregation's information loss. A count
discards everything except its own criterion, and the criterion lives in the
command, never in the number. So a number in a transcript is only as
meaningful as the reader's reconstruction of what was counted: which rows
were eligible, which field the predicate examined, whether a header row was
included (a very common off-by-one — `grep -c` counts a header line that
says `role` if the pattern is `role`), whether duplicates were collapsed,
whether the unit is lines, records, bytes, or matches, which for multi-match
lines differ. `grep -c` counts *lines with at least one match*, not matches;
a line with three occurrences counts once. `wc -l` counts newline
characters, so a final line without a trailing newline goes uncounted —
a classic one-off in transcripts of hand-edited files. Sums and averages
lose their distributions entirely: "average response time 120ms" is
compatible with every request taking 120ms and with 99 requests at 20ms and
one at 10 seconds, and the claim "the service is responsive" survives the
first and dies on the second. When a claim turns on an aggregate, the shape
question becomes: what would this number look like if the claim were false?
If the answer is "the same," the aggregate is not evidence for the claim,
whatever its value.

## Well-formed and wrong

Machine readers meet a species of shape error the terminal-reading tradition
never had to name, because it belongs to structured output: the document
that parses perfectly and reports failure in its payload.

```bash
mkdir work && cd work
cat > response.json <<'JSON'
{"status": "error", "message": "quota exceeded", "records": [], "expires": null}
JSON
echo "== well-formed? =="
python3 -m json.tool response.json > /dev/null; echo "parse exit: $?"
echo "== what a naive extraction reports =="
python3 -c '
import json
d = json.load(open("response.json"))
print("records returned:", len(d["records"]))
print("expires:", d.get("expires"))
print("renewed:", d.get("renewed"))
print("expires present?", "expires" in d, " renewed present?", "renewed" in d)
print("status:", d["status"], "-", d["message"])
'
```

```output
== well-formed? ==
parse exit: 0
== what a naive extraction reports ==
records returned: 0
expires: None
renewed: None
expires present? True  renewed present? False
status: error - quota exceeded
```

Three distinct traps, one document. First, **validity is not success**: the
parse exits 0 because the bytes are legal JSON, and legality says nothing
about the payload, which announces `"status": "error"` and a quota problem.
This is chapter 1's cardinal misreading wearing a schema — a reader that
checks "did the response parse?" and reports the fetch successful has
confirmed the envelope and ignored the letter. Second, **an empty
collection is not an absent one**: `records` is present, well-typed, and
empty, and a pipeline that reports "0 records returned" as a finding about
the data has misattributed a quota rejection to the query — the same
five-worlds problem chapter 4 posed for silence, now posed for `[]`. When a
structured response can carry both an error status and an empty result set,
the result set is only evidence when the status is success; reading them in
the wrong order manufactures facts about the world out of facts about the
request. Third, and most specific to structured formats, **absent and null
are different facts that most extraction idioms collapse**: `expires` is
present with a null value — the field exists and its value is known to be
nothing — while `renewed` does not exist in the document at all, and the
convenient `.get()` accessor returns the same `None` for both. The
membership test on the last line is what separates them. The distinction
carries weight in exactly the cases that matter: a null `expires` may mean
"this credential never expires," while a missing `expires` means the
server did not tell you, and a reader that reports "no expiry" for both has
converted an unanswered question into a reassuring answer.

The habit to build, for any structured transcript: read the envelope's
status field before its data fields, treat empty collections as
uninterpretable until the status is known good, and — when a claim turns on
a field being empty, null, false, or zero — check whether the field is
present at all before believing the value. Extraction tools that flatten
missing, null, empty, and false into one falsy blur are the JSON world's
version of the merged stream: convenient, lossy, and silent about the loss.

## Structure, headers, and the units nobody printed

Two smaller shape checks round out the routine, both concerning the parts of
output that are not the data. First, **headers and labels are part of the
shape, and their absence is a shape too.** A table of numbers whose column
headings were cut off by a filter is a set of unlabeled columns, and readers
assign meanings to unlabeled columns by position and habit — which is how a
"used" column gets read as "available," how a percentage gets read as a
count, how a timestamp gets read as a duration. Where a transcript's columns
are unlabeled and the claim depends on which column is which, the honest
verdict is insufficient even though the numbers are right there. Second,
**units and scales are claims in themselves.** Output that says `4096` says
nothing about bytes, kilobytes, blocks, or pages until something else in the
transcript says so; human-readable flags (`-h`) and their suffixes are the
producer volunteering the unit, and their absence leaves the unit to be
inferred from the tool's defaults, which vary by tool, by platform, and
occasionally by locale. The same discipline extends to time zones (a
timestamp without a zone is two claims apart from a timestamp with one),
to number formatting (locale-dependent separators can turn 1.234 into
one-point-two-three-four or one-thousand-two-hundred-thirty-four), and to
sort order (lexicographic sorting puts `item10` before `item2`, which
routinely produces "the last item" claims about the wrong item).

None of these are exotic. They are the ordinary furniture of command output,
and they matter because the reader's eye slides over furniture to get to
data. Shape checking is the discipline of looking at the furniture first:
what are these columns, what are these units, what is this sorted by, what
is missing from the frame, and what question would this output be a perfect
answer to? Only when that last question's answer matches the claim's
question does content reading begin.

## The adjacency that is a time zone away

One adjacency deserves flagging here even though chapter 7 owns the
subject, because it is a *shape* failure before it is a time failure: the
transcript that answers the right question about the wrong moment. A
measurement taken before the change is a perfect answer to "what was the
state?" and no answer at all to "what is the state?" — and nothing in the
output's appearance distinguishes the two, since a file listing from
before a deploy looks exactly like a file listing from after one. The
shape check that catches it is the same naming discipline: the output's
own question is always past-tense and always anchored — "these were the
files under `/srv/app` at the moment this command ran" — and the claim's
question is usually present-tense and unanchored — "the new binary is
deployed." Whether the two meet depends entirely on when the command ran
relative to the event, which is information the transcript carries only if
someone printed a clock. Reading a transcript's ordering as a proxy for
that anchoring is the trap chapter 3 already dismantled for merged
streams; chapter 7 dismantles the rest.

## Question three, as a routine

The check, in the order that catches most for least effort. **Name the
output's own question** in one sentence — "this is a list of files under
`data/2026/08` whose names end in .json," not "this is the search." The
naming is the whole discipline; most shape errors die here, because the
sentence you are forced to write will not match the claim's sentence.
**Compare scopes**: does the output's subject — its directory, its host, its
table, its time window, its file — contain the claim's subject? **Compare
frames**: is this the whole output or a view of it? Look for truncation
marks, round counts, mid-record edges, and prefer transcripts that print a
total beside a window. **Compare units and labels**: are the columns
identified, the units stated, the sort order known, the aggregate's
criterion reconstructible from the command line? **Subtract the observer**:
does this view include its own production — the grep in the process list,
the script in the directory listing, the query in the connection table?
And **ask the falsification question** for aggregates: would this number
look different if the claim were false?

Shape checking does not tell you whether a claim is true. It tells you
whether this transcript is *about* the claim — whether reading it further
is evidence-gathering or a category error dressed as diligence. That is
why it precedes content, and why a reader who runs it first is spared the
most embarrassing failure in this book's catalog: the confident, detailed,
entirely accurate summary of the wrong thing. What remains, once the
transcript is known to be about the right thing, is the hardest question
of the four — whether its content actually supports the words of the claim,
sized exactly as the claim was worded. That is the next chapter's subject,
and the place where this book's three verdicts finally have to be assigned
with rigor rather than instinct.
