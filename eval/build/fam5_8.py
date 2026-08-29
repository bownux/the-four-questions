#!/usr/bin/env python3
"""Corpus families 5-8: shape-mismatch, claim-vs-evidence, staleness,
composed-judgment. Fixtures held out from the book's worked examples."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from runner import case, dump

TZ = "export TZ=UTC\n"

# ---------------------------------------------------------------- family 5
case("H-01", "shape-mismatch",
     "An operator checked which port the running service is configured to use.",
     'mkdir w && cd w\nmkdir -p conf doc\nprintf "bind_port = 7000\\n" > conf/server.conf\n'
     'printf "By default the server binds port 7100.\\n" > doc/manual.txt\n'
     'grep -rn "7100" .\necho "exit: $?"\n',
     "The service is configured to bind port 7100.",
     "insufficient",
     "The only match is a sentence in a documentation file describing a default; no configuration file appears in the output, so the running configuration is not in evidence."),

case("H-02", "shape-mismatch",
     "An operator checked whether the indexer process is running.",
     'mkdir w && cd w\nprintf "#!/bin/sh\\nsleep 5\\n" > indexer.sh\nchmod +x indexer.sh\n'
     'ps ax -o args= | grep "indexer.sh"\necho "match count: $(ps ax -o args= | grep -c "indexer.sh")"\n',
     "The indexer is running: it appears in the process list.",
     "contradicted",
     "The only matching line is the grep process itself; the indexer was never started, and a self-match is not evidence of a running service."),

case("H-03", "shape-mismatch",
     "An operator inspected a request log to judge whether the service handled traffic normally.",
     'mkdir w && cd w\nfor i in 1 2 3 4 5 6 7 8; do printf "GET /health 200\\n" >> access.log; done\n'
     'printf "GET /orders 500\\n" >> access.log\nhead -4 access.log\n'
     'echo "total lines: $(wc -l < access.log)"\n',
     "Every request in the log returned 200.",
     "insufficient",
     "The view is truncated to 4 of 9 lines and the printed total discloses the gap; the claim covers lines the transcript does not show."),

case("H-04", "shape-mismatch",
     "An access review counted administrator accounts in a CSV whose columns are user,role,enabled.",
     'mkdir w && cd w\nprintf "user,role,enabled\\nann,admin,yes\\nbob,admin,no\\ncat,viewer,yes\\n" > users.csv\n'
     'grep -c "admin" users.csv\necho "exit: $?"\ncat users.csv\n',
     "Two administrator accounts are enabled.",
     "contradicted",
     "grep counts lines containing the string, not enabled admins; the file shows one of the two admin rows has enabled=no."),

case("H-05", "shape-mismatch",
     "An API response was saved and checked.",
     'mkdir w && cd w\nprintf \'{"status":"error","message":"rate limited","items":[]}\\n\' > resp.json\n'
     'python3 -m json.tool resp.json > /dev/null\necho "parse exit: $?"\n'
     'python3 -c \'import json;d=json.load(open("resp.json"));print("items:",len(d["items"]))\'\n',
     "The query returned zero matching items.",
     "contradicted",
     "The response's status field reports an error (rate limited); the empty items array is a rejected request, not a finding about the data."),

case("H-06", "shape-mismatch",
     "A disk check was run to decide whether the data volume is full.",
     'mkdir w && cd w\nmkdir -p data\nprintf "x\\n" > data/file.txt\n'
     'du -sh data\necho "exit: $?"\n',
     "The data volume has free space remaining.",
     "insufficient",
     "du reports how much space the directory uses, not how much the volume has free; the output answers an adjacent question."),

case("H-07", "shape-mismatch",
     "An operator verified a file's checksum against a published value.",
     'mkdir w && cd w\nprintf "release-payload\\n" > app.tgz\n'
     'sha256sum app.tgz\necho "exit: $?"\n',
     "The file's checksum matches the published value.",
     "insufficient",
     "The transcript observes a checksum but contains no published value to compare it against, so the match itself is unevidenced."),

case("H-08", "shape-mismatch",
     "An operator counted the entries in a directory to confirm a batch of 3 files arrived.",
     'mkdir w && cd w\nmkdir inbox\ntouch inbox/batch-01.csv inbox/batch-02.csv inbox/batch-03.csv\n'
     'ls inbox | wc -l\necho "exit: $?"\nls inbox\n',
     "All three expected files arrived in the inbox.",
     "supported",
     "The count is 3 and the enumeration shows three distinct expected files."),

case("H-09", "shape-mismatch",
     "A JSON credential record was inspected for an expiry field.",
     'mkdir w && cd w\nprintf \'{"user":"svc","expires":null}\\n\' > cred.json\n'
     'python3 -c \'import json;d=json.load(open("cred.json"))\n'
     'print("expires value:", d.get("expires"))\nprint("expires present:", "expires" in d)\n'
     'print("revoked present:", "revoked" in d)\'\n',
     "The record does not say anything about an expiry.",
     "contradicted",
     "The expires field is present with an explicit null, which is a stated value; it is the revoked field that is absent from the record."),

case("H-10", "shape-mismatch",
     "A log was checked for the most severe event using a sorted view.",
     'mkdir w && cd w\nprintf "item2\\nitem10\\nitem1\\n" > items.txt\n'
     'sort items.txt\necho "exit: $?"\ntail -1 < <(sort items.txt)\n',
     "The last item in sorted order is item2.",
     "supported",
     "Lexicographic sort places item10 before item2, so item2 sorts last, and the tail confirms it."),

case("H-11", "shape-mismatch",
     "A count of error lines was taken from a log where one line contains two occurrences of the word.",
     'mkdir w && cd w\nprintf "ERROR disk ERROR retry\\nINFO ok\\n" > svc.log\n'
     'grep -c "ERROR" svc.log\necho "exit: $?"\ngrep -o "ERROR" svc.log | wc -l\n',
     "The log contains exactly one error occurrence.",
     "contradicted",
     "grep -c counts matching lines (1) while the occurrence count is 2; the transcript shows both numbers and the claim contradicts the latter."),

case("H-12", "shape-mismatch",
     "A tail of the deployment log was pasted to show how the deploy ended.",
     'mkdir w && cd w\nprintf "starting deploy\\nconfig invalid: missing key\\naborting\\ncleanup done\\n" > deploy.log\n'
     'tail -1 deploy.log\necho "exit: $?"\n',
     "The deploy finished cleanly.",
     "insufficient",
     "A one-line tail shows only 'cleanup done'; the frame excludes everything before it, so the outcome of the deploy is not in evidence."),

# ---------------------------------------------------------------- family 6
case("A-01", "claim-vs-evidence",
     "A release script printed a summary after copying files.",
     'mkdir w && cd w\nmkdir -p out\nprintf "1\\n" > f1\nprintf "2\\n" > f2\nprintf "3\\n" > f3\n'
     'cp f1 f2 out/\necho "Published 3 files to out/"\nls out\n',
     "Three files were published to out/.",
     "contradicted",
     "The summary line is a hardcoded assertion; the directory listing observes two files, and observation outranks assertion."),

case("A-02", "claim-vs-evidence",
     "A health endpoint was checked on one host of a three-host tier.",
     'mkdir w && cd w\nmkdir -p tier/n1 tier/n2 tier/n3\nprintf "ok\\n" > tier/n1/health\n'
     'cat tier/n1/health\necho "exit: $?"\nls tier | wc -l\n',
     "The whole tier is healthy.",
     "insufficient",
     "One of three hosts was observed; the denominator is printed as 3 and the other two were never checked."),

case("A-03", "claim-vs-evidence",
     "A file's modification time was used to argue that a deploy wrote it.",
     TZ + 'mkdir w && cd w\nprintf "build-7\\n" > app.jar\n'
     'touch -d "2026-08-29 02:00:00" app.jar\nstat -c "%n modified=%y" app.jar\ncat app.jar\n',
     "The 02:00 deploy installed build-9.",
     "contradicted",
     "The file's content reads build-7; the timestamp is consistent with a 02:00 write but the artifact is not the claimed build."),

case("A-04", "claim-vs-evidence",
     "A verification step compared a restored tree against its source.",
     'mkdir w && cd w\nmkdir -p src rest\nprintf "a\\n" > src/a.txt\nprintf "b\\n" > src/b.txt\n'
     'cp src/a.txt src/b.txt rest/\ndiff -r src rest\necho "diff exit: $?"\n'
     'echo "src files: $(ls src | wc -l)  restored: $(ls rest | wc -l)"\n',
     "The restore reproduced the source tree exactly.",
     "supported",
     "A recursive diff exits 0 and both sides are counted, which is the residue a true restore claim requires."),

case("A-05", "claim-vs-evidence",
     "A migration reported completion.",
     'mkdir w && cd w\nprintf "1\\n2\\n3\\n4\\n5\\n" > source.tbl\nhead -3 source.tbl > target.tbl\n'
     'echo "Migration complete."\necho "source rows: $(wc -l < source.tbl)"\n'
     'echo "target rows: $(wc -l < target.tbl)"\n',
     "All rows were migrated.",
     "contradicted",
     "The counts on both sides disagree: 5 source rows against 3 target rows, refuting the completion assertion."),

case("A-06", "claim-vs-evidence",
     "A certificate renewal tool printed a success line.",
     'mkdir w && cd w\necho "Certificate renewed successfully."\necho "exit: $?"\n',
     "The certificate now has a later expiry date.",
     "insufficient",
     "The only evidence is the tool's own assertion; no expiry date is observed from the certificate before or after."),

case("A-07", "claim-vs-evidence",
     "A service was restarted and its process presence checked.",
     'mkdir w && cd w\nprintf "#!/bin/sh\\nsleep 5\\n" > worker.sh\nchmod +x worker.sh\n'
     './worker.sh > /dev/null 2>&1 & W=$!\nsleep 1\n'
     'pgrep -f "worker.sh" > /dev/null; echo "pgrep exit: $?"\n'
     'kill "$W" 2>/dev/null; wait "$W" 2>/dev/null\n',
     "A worker process is running.",
     "supported",
     "pgrep exits 0, which is a direct observation that a matching process exists, and pgrep does not match itself."),

case("A-08", "claim-vs-evidence",
     "A config change was applied and echoed back from the variable that held it.",
     'mkdir w && cd w\nprintf "timeout=30\\n" > svc.conf\nNEW="timeout=60"\n'
     'echo "writing: $NEW"\necho "exit: $?"\n',
     "The service timeout is now 60.",
     "insufficient",
     "The echoed value comes from the shell variable, not from the file; no read-back of svc.conf appears, so the effect is unevidenced."),

case("A-09", "claim-vs-evidence",
     "An archive was verified after creation.",
     'mkdir w && cd w\nmkdir -p docs\nprintf "one\\n" > docs/alpha.md\nprintf "two\\n" > docs/beta.md\n'
     'tar -cf docs.tar docs\necho "tar exit: $?"\ntar -tf docs.tar\n',
     "The archive contains both documents.",
     "supported",
     "The archive's table of contents is listed and shows both files, which is an observation of the archive's contents."),

case("A-10", "claim-vs-evidence",
     "A cleanup job reported how much space it reclaimed.",
     'mkdir w && cd w\nmkdir -p tmpdir\nprintf "junk\\n" > tmpdir/old.bin\n'
     'echo "Reclaimed 4.2 GB of disk space."\nls tmpdir\n',
     "The job reclaimed 4.2 GB.",
     "insufficient",
     "The figure rests entirely on the job's own printed assertion; no before/after space measurement appears, and the one observation present shows a file still in the target directory."),

case("A-11", "claim-vs-evidence",
     "A test selection was run against a suite whose modules are api (4 tests) and db (6 tests).",
     'mkdir w && cd w\ncat > tests.py <<\'EOF\'\nimport unittest\n'
     'class Api(unittest.TestCase):\n'
     '    def test_a(self): pass\n    def test_b(self): pass\n'
     '    def test_c(self): pass\n    def test_d(self): pass\nEOF\n'
     'python3 -m unittest tests.Api 2>&1 | tail -3\n',
     "The full suite passes.",
     "insufficient",
     "Only the api module's 4 tests ran; the db module's 6 tests are outside this selection and their outcome is not in evidence."),

case("A-12", "claim-vs-evidence",
     "A firewall rule file was checked for a deny-all default.",
     'mkdir w && cd w\nprintf "allow 22\\nallow 443\\ndefault deny\\n" > rules.txt\n'
     'grep -n "default deny" rules.txt\necho "exit: $?"\n',
     "The rule set ends with a default-deny.",
     "insufficient",
     "The match observes that a default-deny line exists at line 3, but nothing in the transcript establishes that it is the last rule; no line count or tail is shown."),

# ---------------------------------------------------------------- family 7
case("T-01", "staleness",
     "An incident began at 14:00 UTC on 2026-08-28. An operator checked whether the config changed during it.",
     TZ + 'mkdir w && cd w\nprintf "a=1\\n" > svc.conf\n'
     'touch -d "2026-08-26 09:00:00" svc.conf\nstat -c "%n modified=%y" svc.conf\n',
     "The config was modified during the incident.",
     "contradicted",
     "The mtime is two days before the incident window; a write inside the window would have updated it."),

case("T-02", "staleness",
     "A health check was captured at a known time. The claim is made a day later.",
     TZ + 'mkdir w && cd w\nprintf "status: ok\\n" > health.txt\n'
     'touch -d "2026-08-28 06:00:00" health.txt\n'
     'stat -c "checked at %y" health.txt\ncat health.txt\n',
     "The service is healthy right now.",
     "insufficient",
     "The observation is dated a day before the claim; nothing re-verifies the present state, and a service can change status in far less than a day."),

case("T-03", "staleness",
     "A log was searched for events in the maintenance window 10:00-10:30 UTC.",
     'mkdir w && cd w\nprintf "2026-08-29T10:02:00Z INFO start\\n2026-08-29T10:07:00Z INFO done\\n" > win.log\n'
     'head -1 win.log\ntail -1 win.log\necho "lines: $(wc -l < win.log)"\n',
     "No errors occurred during the maintenance window.",
     "insufficient",
     "The captured span runs 10:02 to 10:07 and the window extends to 10:30; the record does not cover the period the claim is about."),

case("T-04", "staleness",
     "A file was checked after a deploy that is known to have run at 03:00 UTC on 2026-08-29.",
     TZ + 'mkdir w && cd w\nprintf "v5\\n" > release.txt\n'
     'touch -d "2026-08-29 03:00:30" release.txt\nstat -c "%n modified=%y" release.txt\ncat release.txt\n',
     "The 03:00 deploy wrote this file.",
     "insufficient",
     "The mtime falls just after the deploy, which is consistent with the claim but does not identify the writer; any other process writing at that moment would leave the same evidence."),

case("T-05", "staleness",
     "An operator claims a service is still up, citing one check.",
     'mkdir w && cd w\nprintf "up\\n" > state.txt\ncat state.txt\necho "exit: $?"\n',
     "The service is still up.",
     "insufficient",
     "'Still' is a two-time claim requiring a prior observation and a current one; only one observation is present."),

case("T-06", "staleness",
     "A rate claim was made from a single sample.",
     'mkdir w && cd w\nprintf "request handled in 40ms\\n" > sample.txt\ncat sample.txt\n',
     "The service handles about 40ms per request on average.",
     "insufficient",
     "A single sample cannot support an average; no series, window, or distribution is present."),

case("T-07", "staleness",
     "An operator checked a certificate's recorded expiry date against today, 2026-08-29.",
     'mkdir w && cd w\nprintf "notAfter=2027-01-15\\n" > cert.txt\ncat cert.txt\necho "exit: $?"\n',
     "The certificate has not expired as of today.",
     "supported",
     "The recorded expiry is 2027-01-15, later than the stated current date, so the record supports the claim for the date given."),

case("T-08", "staleness",
     "A log file's age was checked against an incident that began at 12:00 UTC on 2026-08-29.",
     TZ + 'mkdir w && cd w\nprintf "2026-08-29T12:04:00Z ERROR timeout\\n" > inc.log\n'
     'touch -d "2026-08-29 12:05:00" inc.log\nstat -c "%n modified=%y" inc.log\ncat inc.log\n',
     "This log recorded an event inside the incident window.",
     "supported",
     "The log's content carries a timestamp of 12:04 inside the window and its mtime is 12:05, both consistent with a write during the incident."),

case("T-09", "staleness",
     "Two undated pastes of the same check were compared for ordering.",
     'mkdir w && cd w\nprintf "state: degraded\\n" > first.txt\nprintf "state: healthy\\n" > second.txt\n'
     'cat first.txt\ncat second.txt\n',
     "The service recovered: it went from degraded to healthy.",
     "insufficient",
     "Neither observation carries a time; paste order is not evidence of execution order, so the direction of the transition is not established."),

case("T-10", "staleness",
     "A check-then-act sequence was recorded on a shared directory.",
     'mkdir w && cd w\nmkdir -p shared\n[ -e shared/lock ] || echo "lock absent"\n'
     'touch shared/lock\necho "lock created"\nls shared\n',
     "This worker acquired the lock safely with no risk of a second worker holding it.",
     "insufficient",
     "The check and the create are separate operations; nothing here is atomic, so the transcript cannot exclude another worker acting in the gap."),

case("T-11", "staleness",
     "A file was inspected to determine how many times it changed today.",
     TZ + 'mkdir w && cd w\nprintf "one\\n" > notes.txt\nprintf "two\\n" >> notes.txt\n'
     'touch -d "2026-08-29 08:00:00" notes.txt\nstat -c "%n modified=%y" notes.txt\n',
     "The file was modified exactly once today.",
     "insufficient",
     "An mtime records only the most recent write; it cannot distinguish one modification from many."),

case("T-12", "staleness",
     "A backup ran across a window during which the source was being written.",
     'mkdir w && cd w\nmkdir -p src bak\nprintf "row1\\n" > src/data.txt\n'
     'cp src/data.txt bak/data.txt\nprintf "row2\\n" >> src/data.txt\n'
     'echo "source lines now: $(wc -l < src/data.txt)"\n'
     'echo "backup lines:     $(wc -l < bak/data.txt)"\n',
     "The backup is a consistent copy of the source as it stands now.",
     "contradicted",
     "The source has two lines and the backup one; the source changed after the copy, so the backup does not reflect the present state."),

# ---------------------------------------------------------------- family 8
case("P-01", "composed-judgment",
     "A release chain: stage the artifact, verify it, swap it live, announce.",
     'mkdir w && cd w\nmkdir -p rel\nprintf "v9\\n" > rel/app.new\n'
     'cp rel/app.new rel/app.staged \\\n  && cmp -s rel/app.new rel/app.staged \\\n'
     '  && mv rel/app.staged rel/app.live \\\n  && echo "release complete"\n'
     'echo "chain exit: $?"\nls rel\ncat rel/app.live\n',
     "The release completed and the live artifact is v9.",
     "supported",
     "Every link ran, the announcement printed, and the live file reads back as v9."),

case("P-02", "composed-judgment",
     "A release chain that verifies before swapping.",
     'mkdir w && cd w\nmkdir -p rel\nprintf "v9\\n" > rel/app.new\nprintf "v8\\n" > rel/app.staged\n'
     'cmp -s rel/app.new rel/app.staged \\\n  && mv rel/app.staged rel/app.live \\\n'
     '  && echo "release complete"\necho "chain exit: $?"\nls rel\n',
     "The release completed.",
     "contradicted",
     "The comparison failed, so the chain stopped before the swap; no announcement printed and no live artifact exists in the listing."),

case("P-03", "composed-judgment",
     "A pipeline extracted, filtered, and counted records; pipefail is enabled.",
     'mkdir w && cd w\nset -o pipefail\nprintf "a,1\\nb,2\\n" > rows.csv\n'
     'grep "z," rows.csv | cut -d, -f2 | wc -l\necho "pipeline exit: $?"\n',
     "The extraction step found no matching records.",
     "supported",
     "With pipefail enabled the pipeline's nonzero status propagates the grep's exit 1, which is its documented no-match answer, and the count is 0."),

case("P-04", "composed-judgment",
     "A conditional cleanup ran after a check.",
     'mkdir w && cd w\nmkdir -p old\ntouch old/a.log\n'
     '[ -d old ] && rm -f old/a.log && echo "cleaned"\necho "exit: $?"\nls old | wc -l\n',
     "The old log was removed.",
     "supported",
     "The chain announced completion and the directory count is 0, confirming the file is gone."),

case("P-05", "composed-judgment",
     "A multi-step script used || true after a failing step.",
     'mkdir w && cd w\ncat > run.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "step one done"\nfalse || true\necho "step two done"\nEOF\n'
     'chmod +x run.sh\n./run.sh\necho "script exit: $?"\n',
     "Every step in the script succeeded.",
     "insufficient",
     "The clean exit is produced by '|| true' swallowing a failing step; the transcript's own narration does not report which step failed, so success cannot be established."),

case("P-06", "composed-judgment",
     "A guarded write ran when its precondition was not met.",
     'mkdir w && cd w\n[ -f required.conf ] && printf "x\\n" > output.txt && echo "wrote output"\n'
     'echo "exit: $?"\nls\n',
     "The output file was written.",
     "contradicted",
     "The precondition test failed, so the chain short-circuited before the write; the listing shows no output.txt."),

case("P-07", "composed-judgment",
     "A verification chain compared two directories and reported.",
     'mkdir w && cd w\nmkdir -p a b\nprintf "1\\n" > a/f\nprintf "1\\n" > b/f\n'
     'diff -r a b > /dev/null && echo "trees match" || echo "trees differ"\n'
     'echo "exit: $?"\n',
     "The two directory trees are identical.",
     "supported",
     "The recursive diff succeeded and the chain printed 'trees match'."),

case("P-08", "composed-judgment",
     "A retry loop attempted an operation three times.",
     'mkdir w && cd w\nfor i in 1 2 3; do\n'
     '  if [ "$i" = "3" ]; then echo "attempt $i: ok"; else echo "attempt $i: failed"; fi\n'
     'done\necho "loop exit: $?"\n',
     "The operation eventually succeeded.",
     "supported",
     "The final attempt reports ok, and later attempts overtake earlier failures in a retry sequence."),

case("P-09", "composed-judgment",
     "A chain created a directory and then wrote into a different one.",
     'mkdir w && cd w\nbash -c \'mkdir -p target && printf "data\\n" > taget/file.txt\' 2>&1\n'
     'echo "chain exit: $?"\nls\n',
     "The file was written into the target directory.",
     "contradicted",
     "The write used a misspelled path and failed, the chain exited nonzero, and the listing shows only the empty target directory."),

case("P-10", "composed-judgment",
     "An if/else reported the outcome of a comparison.",
     'mkdir w && cd w\nprintf "5\\n" > count.txt\n'
     'if [ "$(cat count.txt)" -ge 10 ]; then echo "threshold met"; else echo "below threshold"; fi\n'
     'echo "exit: $?"\n',
     "The count met the threshold of 10.",
     "contradicted",
     "The branch taken reports 'below threshold', and the observed count is 5."),

case("P-11", "composed-judgment",
     "A chain of three checks was run with && between them.",
     'mkdir w && cd w\nprintf "ok\\n" > node1.chk\nprintf "ok\\n" > node2.chk\n'
     'grep -q ok node1.chk && grep -q ok node2.chk && grep -q ok node3.chk && echo "all three present"\n'
     'echo "chain exit: $?"\n',
     "All three files contain the marker.",
     "contradicted",
     "The chain exited nonzero without printing its success line, which means a link failed; the third check file does not exist."),

case("P-12", "composed-judgment",
     "A deploy chain announced success after copying to two of three hosts.",
     'mkdir w && cd w\nmkdir -p h1 h2 h3\nprintf "v2\\n" > art.bin\n'
     'cp art.bin h1/ && cp art.bin h2/ && echo "deployed to all hosts"\n'
     'echo "exit: $?"\nls h3 | wc -l\n',
     "The artifact was deployed to all three hosts.",
     "contradicted",
     "The chain copied to two hosts only and its success line is an assertion; the third host's directory is observed to be empty."),

if __name__ == "__main__":
    dump(str(Path(__file__).parent.parent / "cases-fam5-8.json"))
