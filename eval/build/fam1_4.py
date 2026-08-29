#!/usr/bin/env python3
"""Corpus families 1-4: verdict-channel, success-shaped-failure,
commentary-channel, empty-output. All fixtures held out from the book's
worked examples (different tools, domains, and data)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from runner import case, dump, CASES

# ---------------------------------------------------------------- family 1
# verdict-channel: what the exit status does and does not say
case("V-01", "verdict-channel",
     "An operator checked whether the deny-list file contains the entry 'legacy-api'.",
     'mkdir w && cd w\nprintf "old-portal\\nbeta-ui\\n" > denylist.txt\n'
     'grep -x "legacy-api" denylist.txt\necho "exit: $?"\n',
     "The deny-list check errored out and must be re-run.",
     "contradicted",
     "grep exit 1 is the documented 'no lines selected' answer; the check ran and answered no. An error would be exit 2 with a diagnostic."),

case("V-02", "verdict-channel",
     "Two build manifests were compared before promoting a release.",
     'mkdir w && cd w\nprintf "pkg-a 1.2\\npkg-b 3.4\\n" > staging.txt\n'
     'printf "pkg-a 1.2\\npkg-b 3.5\\n" > production.txt\n'
     'diff staging.txt production.txt\necho "exit: $?"\n',
     "The two manifests are identical.",
     "contradicted",
     "diff exit 1 with a printed hunk means the inputs differ; pkg-b is 3.4 in staging and 3.5 in production."),

case("V-03", "verdict-channel",
     "A maintenance script tried to invoke the cluster CLI.",
     'mkdir w && cd w\nbash -c "clusterctl get nodes" 2>&1\necho "exit: $?"\n',
     "The cluster has no nodes registered.",
     "contradicted",
     "Exit 127 is command-not-found: the CLI was never located, so no query about nodes was performed. The transcript says nothing about the cluster."),

case("V-04", "verdict-channel",
     "A data export was run under a time limit.",
     'mkdir w && cd w\ntimeout 1 sleep 5\necho "exit: $?"\n',
     "The export finished within its time limit.",
     "contradicted",
     "Exit 124 is timeout's documented report that the command outlived its allowance and was killed."),

case("V-05", "verdict-channel",
     "A helper script was executed as part of a nightly job.",
     'mkdir w && cd w\nprintf "#!/bin/sh\\necho ok\\n" > helper.sh\n'
     'bash -c "./helper.sh" 2>&1\necho "exit: $?"\n',
     "The helper script is missing from the job directory.",
     "contradicted",
     "Exit 126 means the file was found but could not be executed (no execute permission); 127 would mean missing. The file exists."),

case("V-06", "verdict-channel",
     "A worker process was stopped by the supervisor during a drain.",
     'mkdir w && cd w\nbash -c \'kill -TERM $$\' 2>&1\necho "exit: $?"\n',
     "The worker exited on its own after finishing its queue.",
     "contradicted",
     "Exit 143 is 128+15: the process was terminated by SIGTERM, not by completing and exiting on its own."),

case("V-07", "verdict-channel",
     "A configuration file was checked for a required setting.",
     'mkdir w && cd w\nprintf "tls_enabled = true\\nmin_version = 1.2\\n" > tls.conf\n'
     'grep -n "tls_enabled = true" tls.conf\necho "exit: $?"\n',
     "TLS is enabled in this configuration file.",
     "supported",
     "grep exit 0 with the matching line printed at its line number directly evidences the setting."),

case("V-08", "verdict-channel",
     "An integrity check compared a downloaded artifact against its reference copy.",
     'mkdir w && cd w\nprintf "payload-v4\\n" > artifact.bin\ncp artifact.bin reference.bin\n'
     'cmp artifact.bin reference.bin\necho "exit: $?"\n',
     "The downloaded artifact matches the reference byte for byte.",
     "supported",
     "cmp exit 0 with no output is the documented 'files are identical' answer."),

case("V-09", "verdict-channel",
     "A pipeline extracted matching records and counted them. The shell's pipefail option is not set anywhere in this session.",
     'mkdir w && cd w\nprintf "alpha\\nbeta\\n" > names.txt\n'
     'grep "gamma" names.txt | wc -l\necho "pipeline exit: $?"\n',
     "The extraction step ran without error.",
     "insufficient",
     "The printed status belongs to wc, the pipeline's last member. Without pipefail or PIPESTATUS the upstream grep's status is not in the record; the count 0 shows it selected nothing but cannot distinguish no-match (exit 1) from an error (exit 2)."),

case("V-10", "verdict-channel",
     "A cleanup command was run against a scratch directory.",
     'mkdir w && cd w\nmkdir cache\ntouch cache/a.bin cache/b.bin\n'
     'find cache -name "*.cache" -delete\necho "exit: $?"\n',
     "The cache files were deleted.",
     "insufficient",
     "find exits 0 for a completed traversal whether or not anything matched, and the transcript shows no listing before or after. Nothing here evidences that any file was removed."),

case("V-11", "verdict-channel",
     "A search for a hard-coded credential pattern was run over a source directory.",
     'mkdir w && cd w\nmkdir -p src\nprintf "int main(void){return 0;}\\n" > src/main.c\n'
     'grep -rn "AKIA" src missing_dir\necho "exit: $?"\n',
     "The credential scan completed over both requested paths.",
     "contradicted",
     "grep exit 2 with a stderr diagnostic means an input could not be read: missing_dir was never scanned, so the scan did not complete over both paths."),

case("V-12", "verdict-channel",
     "A JSON config was validated before deployment.",
     'mkdir w && cd w\nprintf \'{"replicas": 3}\\n\' > cfg.json\n'
     'python3 -m json.tool cfg.json > /dev/null\necho "exit: $?"\n',
     "The configuration is valid JSON.",
     "supported",
     "The parser exited 0, which is exactly the claim's scope: well-formedness. Nothing wider is claimed."),

# ---------------------------------------------------------------- family 2
# success-shaped-failure: clean statuses, dead task
case("S-01", "success-shaped-failure",
     "An operator intended to archive the reports directory into reports.tar.",
     'mkdir w && cd w\nmkdir reports\nprintf "q1\\n" > reports/q1.txt\n'
     'tar -cf reports.tar reprots 2>&1\necho "tar exit: $?"\nls\n',
     "reports.tar now contains the reports directory.",
     "contradicted",
     "The source path was misspelled; tar reported it could not stat 'reprots' and exited 2. An empty reports.tar appears in the listing because tar creates its output file before reading inputs, so its presence is not evidence the directory was archived."),

case("S-02", "success-shaped-failure",
     "An operator intended to change the log level to debug.",
     'mkdir w && cd w\nprintf "loglevel=info\\nworkers=4\\n" > app.ini\n'
     'sed -i "s/log_level=info/log_level=debug/" app.ini\necho "sed exit: $?"\n'
     'cat app.ini\n',
     "The log level is now debug.",
     "contradicted",
     "sed exited 0 but its pattern (log_level) does not match the file's spelling (loglevel); the read-back shows loglevel=info unchanged."),

case("S-03", "success-shaped-failure",
     "An operator intended to move all PDF invoices into the archive directory.",
     'mkdir w && cd w\nmkdir -p archive\ntouch invoice1.pdf invoice2.pdf notes.txt\n'
     'mv *.PDF archive/ 2>&1\necho "mv exit: $?"\nls\nls archive\n',
     "Both invoices were moved into archive/.",
     "contradicted",
     "The uppercase glob matched nothing, mv reported the failure, and the listings show both invoices still in the working directory and archive/ empty."),

case("S-04", "success-shaped-failure",
     "A deployment script created the target directory before copying.",
     'mkdir w && cd w\nmkdir -p /tmp/does-not-matter\nmkdir -p releases/v3\n'
     'echo "mkdir exit: $?"\nls releases\n',
     "The releases/v3 directory was newly created by this run.",
     "insufficient",
     "mkdir -p is a goal-state command: exit 0 means the directory exists now, not that this run created it. Nothing in the transcript shows prior absence."),

case("S-05", "success-shaped-failure",
     "A cleanup step ran against a lock path before starting work.",
     'mkdir w && cd w\nrm -f /tmp/nonexistent-lock-file-xyz\necho "rm exit: $?"\n',
     "The cleanup step deleted a leftover lock from a previous run.",
     "insufficient",
     "rm -f succeeds whether or not the file existed; the transcript is equally consistent with there having been no lock file at all."),

case("S-06", "success-shaped-failure",
     "A backup routine copied two config files into a backup directory that it created first.",
     'mkdir w && cd w\nprintf "a\\n" > one.conf\nprintf "b\\n" > two.conf\n'
     'mkdir -p bak\ncp one.conf two.conf bak/\necho "copy exit: $?"\n'
     'ls bak\ncmp -s one.conf bak/one.conf && cmp -s two.conf bak/two.conf\n'
     'echo "both compare equal: $?"\n',
     "Both config files are backed up correctly.",
     "supported",
     "The destination is enumerated and both files are compared byte-for-byte against their sources with a printed exit 0."),

case("S-07", "success-shaped-failure",
     "A database dump was written to a file.",
     'mkdir w && cd w\nprintf "id,name\\n1,alice\\n" > dump.csv\n'
     'cp dump.csv dump.csv.bak\necho "exit: $?"\nls -1\n',
     "The dump was copied to a backup file.",
     "supported",
     "The copy exited 0 and the listing shows both dump.csv and dump.csv.bak present."),

case("S-08", "success-shaped-failure",
     "A script normalized a data file in place using a redirect.",
     'mkdir w && cd w\nprintf "c\\na\\nb\\n" > items.txt\n'
     'echo "lines before: $(wc -l < items.txt)"\n'
     'sort items.txt > items.txt\necho "sort exit: $?"\n'
     'echo "lines after:  $(wc -l < items.txt)"\n',
     "The items file was sorted in place.",
     "contradicted",
     "The redirect truncated items.txt before sort read it; the after-count is 0, so the data was destroyed rather than sorted."),

case("S-09", "success-shaped-failure",
     "A loop validated three input files; one of them does not exist.",
     'mkdir w && cd w\nprintf "ok\\n" > in1.txt\nprintf "ok\\n" > in2.txt\n'
     'for f in in1.txt in2.txt in3.txt; do\n'
     '  if grep -q ok "$f" 2>/dev/null; then echo "$f ok"; else echo "$f FAILED"; fi\n'
     'done\necho "loop exit: $?"\n',
     "All three input files validated successfully.",
     "contradicted",
     "The loop prints 'in3.txt FAILED'; the clean loop status only reflects the last echo, not the validation outcome."),

case("S-10", "success-shaped-failure",
     "A permissions fix was applied to a config file.",
     'mkdir w && cd w\ntouch secret.env\nchmod 600 secret.env\n'
     'echo "chmod exit: $?"\nstat -c "%a %n" secret.env\n',
     "secret.env is now mode 600.",
     "supported",
     "The mode is read back from the file itself and printed as 600, which is the claim's exact content."),

case("S-11", "success-shaped-failure",
     "A record count was checked after an import.",
     'mkdir w && cd w\nprintf "1,a\\n2,b\\n3,c\\n" > imported.csv\n'
     'wc -l < imported.csv\necho "exit: $?"\n',
     "All 500 source records were imported.",
     "contradicted",
     "The imported file holds 3 lines, which contradicts a claim of 500 records regardless of what the source contained."),

case("S-12", "success-shaped-failure",
     "A symlink was pointed at the current release.",
     'mkdir w && cd w\nmkdir -p rel-1 rel-2\nln -sfn rel-1 current\n'
     'ln -sfn rel-2 current\necho "ln exit: $?"\nreadlink current\n',
     "The current symlink points at rel-2.",
     "supported",
     "readlink observes the link's target directly and prints rel-2."),

# ---------------------------------------------------------------- family 3
# commentary-channel: stderr reading
case("C-01", "commentary-channel",
     "A migration tool was run; stdout and stderr are merged in this transcript.",
     'mkdir w && cd w\ncat > migrate.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "WARNING: column created_at has no index; migration will be slow" >&2\n'
     'echo "migrated 250 rows"\nEOF\nchmod +x migrate.sh\n./migrate.sh\necho "exit: $?"\n',
     "The migration completed with no warnings.",
     "contradicted",
     "A warning about the missing index is present in the merged output; the run succeeded but 'no warnings' is false."),

case("C-02", "commentary-channel",
     "A package installer was run; streams are merged.",
     'mkdir w && cd w\ncat > install.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "notice: using cached index from 2026-08-01" >&2\necho "installed 4 packages"\nEOF\n'
     'chmod +x install.sh\n./install.sh\necho "exit: $?"\n',
     "Four packages were installed.",
     "supported",
     "The stdout line reports the installation and the exit status is 0; the stderr line is a notice about index freshness, which does not contradict the count."),

case("C-03", "commentary-channel",
     "A retrying uploader was run against a flaky endpoint; streams are merged.",
     'mkdir w && cd w\ncat > upload.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "error: connection refused (attempt 1)" >&2\n'
     'echo "error: connection refused (attempt 2)" >&2\n'
     'echo "uploaded backup.tar (attempt 3)"\nEOF\n'
     'chmod +x upload.sh\n./upload.sh\necho "exit: $?"\n',
     "The upload failed.",
     "contradicted",
     "The error lines describe two failed attempts that were overtaken by a successful third; the final line reports the upload completing and the status is 0."),

case("C-04", "commentary-channel",
     "A batch job processed a list of records; streams are merged.",
     'mkdir w && cd w\ncat > batch.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "record 3: parse error, skipped" >&2\necho "processed 9 of 10 records"\nEOF\n'
     'chmod +x batch.sh\n./batch.sh\necho "exit: $?"\n',
     "Every record in the batch was processed.",
     "contradicted",
     "Both channels agree that one record was skipped: stderr names the parse error and stdout reports 9 of 10."),

case("C-05", "commentary-channel",
     "A checksum tool was run over two files; streams are merged.",
     'mkdir w && cd w\nprintf "data\\n" > present.bin\n'
     'sha256sum present.bin absent.bin\necho "exit: $?"\n',
     "Both files were checksummed successfully.",
     "contradicted",
     "The stderr diagnostic reports absent.bin could not be read and the exit status is nonzero; only one file was checksummed."),

case("C-06", "commentary-channel",
     "A tool wrote its result to stdout and its progress to a separate file. Only the stdout capture is shown.",
     'mkdir w && cd w\ncat > run.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "step 1/2" >&2\necho "step 2/2" >&2\necho "result: 42"\nEOF\n'
     'chmod +x run.sh\n./run.sh 2> progress.log\necho "exit: $?"\n',
     "The tool emitted no warnings during the run.",
     "insufficient",
     "stderr was redirected to progress.log and is not shown, so this capture cannot establish the presence or absence of warnings."),

case("C-07", "commentary-channel",
     "A linter was run over a source tree; streams are merged.",
     'mkdir w && cd w\ncat > lint.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "style: line 42 exceeds 100 columns" >&2\nexit 0\nEOF\n'
     'chmod +x lint.sh\n./lint.sh\necho "exit: $?"\n',
     "The linter found no issues.",
     "contradicted",
     "A style finding is printed on stderr; the clean exit reflects the linter's contract of not failing on style findings, not an absence of them."),

case("C-08", "commentary-channel",
     "A timing measurement was taken of a short command.",
     'mkdir w && cd w\n{ time sleep 0.1 ; } 2>&1 | grep -c "real"\necho "exit: $?"\n',
     "The timing output was captured in this transcript.",
     "supported",
     "The count of 1 shows a 'real' timing line was produced and captured; the shell's time keyword writes to stderr, which this capture merged."),

case("C-09", "commentary-channel",
     "A tool was run with its error output discarded.",
     'mkdir w && cd w\nls /nonexistent-path-abc 2>/dev/null\necho "exit: $?"\n',
     "The path was listed without problems.",
     "contradicted",
     "The nonzero exit status shows the listing failed even though the diagnostic was discarded by the redirection."),

case("C-10", "commentary-channel",
     "A deprecation-carrying build was run; streams are merged.",
     'mkdir w && cd w\ncat > build.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "DEPRECATION: --legacy-resolver is removed in 3.0 (this build uses it)" >&2\n'
     'echo "build succeeded in 12s"\nEOF\nchmod +x build.sh\n./build.sh\necho "exit: $?"\n',
     "This build will keep working after the 3.0 upgrade.",
     "contradicted",
     "The deprecation warning states the flag this build uses is removed in 3.0, which is evidence against the claim rather than for it."),

case("C-11", "commentary-channel",
     "A service reload was attempted; streams are merged.",
     'mkdir w && cd w\ncat > reload.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "config test successful"\necho "reloading" \nEOF\n'
     'chmod +x reload.sh\n./reload.sh\necho "exit: $?"\n',
     "The configuration passed its syntax test.",
     "supported",
     "The tool's own output reports the config test succeeding and the run exited 0."),

case("C-12", "commentary-channel",
     "A copy ran with a warning about preserving attributes; streams are merged.",
     'mkdir w && cd w\nprintf "x\\n" > src.txt\ncat > copy.sh <<\'EOF\'\n#!/bin/sh\n'
     'cp src.txt dst.txt\necho "warning: could not preserve ownership" >&2\nEOF\n'
     'chmod +x copy.sh\n./copy.sh\necho "exit: $?"\ncmp -s src.txt dst.txt; echo "contents equal: $?"\n',
     "The file contents were copied correctly.",
     "supported",
     "The byte comparison exits 0; the ownership warning concerns metadata, not contents, so it does not bear on this claim."),

# ---------------------------------------------------------------- family 4
# empty-output: the five silences
case("E-01", "empty-output",
     "An operator checked whether any core dumps were left in the crash directory.",
     'mkdir w && cd w\nmkdir crash\ntouch crash/readme.txt\n'
     'find crash -name "core.*"\necho "exit: $?"\nfind crash -type f | wc -l\n',
     "There are no core dumps in the crash directory.",
     "supported",
     "The traversal completed (exit 0), the directory is shown to be inhabited by one file, and no core.* entries were found."),

case("E-02", "empty-output",
     "An operator searched the August billing directory for failed charges.",
     'mkdir w && cd w\nmkdir -p billing/2026-07 billing/2026-08\n'
     'printf "charge 91 FAILED\\n" > billing/2026-07/log.txt\n'
     'grep -rn "FAILED" billing/2026-08\necho "exit: $?"\nfind billing -type f\n',
     "No charges failed in the billing records.",
     "contradicted",
     "The searched directory is empty; the only billing file lives under 2026-07 and contains a FAILED charge, which the search never examined."),

case("E-03", "empty-output",
     "An operator searched a restricted directory for key files.",
     'mkdir w && cd w\nmkdir -p keys\ntouch keys/id_rsa\nchmod 000 keys\n'
     'find keys -name "id_*" 2>/dev/null\necho "exit: $?"\nchmod 755 keys\n',
     "There are no private key files in the keys directory.",
     "insufficient",
     "find's nonzero exit shows the traversal was obstructed and its diagnostic was discarded by the redirection; the silence covers a directory that could not be read, so it settles nothing either way."),

case("E-04", "empty-output",
     "An operator searched an application log for warnings.",
     'mkdir w && cd w\nprintf "2026-08-29 Warn: cache miss rate high\\n" > app.log\n'
     'grep "WARN" app.log\necho "exit: $?"\ngrep -ci "warn" app.log\n',
     "The application logged no warnings.",
     "contradicted",
     "The case-sensitive pattern missed the file's spelling; a case-insensitive count finds 1 warning line."),

case("E-05", "empty-output",
     "An operator checked whether the error log recorded anything during the incident window.",
     'mkdir w && cd w\n: > error.log\ngrep -c "" error.log\necho "exit: $?"\nwc -c error.log\n',
     "The service ran without errors during the window.",
     "insufficient",
     "The log is zero bytes, so it cannot distinguish 'no errors occurred' from 'nothing was ever written to this file'."),

case("E-06", "empty-output",
     "The program emit.py contains exactly these three lines: 'import os', "
     "'print(\"total: 128\")', 'os._exit(0)'. It was run with its output piped to cat.",
     'mkdir w && cd w\ncat > emit.py <<\'EOF\'\nimport os\nprint("total: 128")\nos._exit(0)\nEOF\n'
     'python3 emit.py | cat\necho "exit: $?"\n',
     "The program produced no output.",
     "contradicted",
     "The stated source prints a total; os._exit terminates without flushing the block-buffered pipe, so the line was produced and lost in the capture rather than never produced."),

case("E-07", "empty-output",
     "An operator listed the quarantine directory after a scan.",
     'mkdir w && cd w\nmkdir quarantine\nls quarantine\necho "exit: $?"\nls -A quarantine | wc -l\n',
     "The quarantine directory is empty.",
     "supported",
     "ls completed successfully and the explicit count of entries, including hidden ones, is 0."),

case("E-08", "empty-output",
     "An operator searched for TODO markers across a source directory.",
     'mkdir w && cd w\nmkdir -p src\nprintf "def main():\\n    return 0\\n" > src/main.py\n'
     'grep -rn "TODO" src\necho "exit: $?"\nfind src -type f | wc -l\n',
     "There are no TODO markers in the source directory.",
     "supported",
     "The scope is shown to contain one file, the search completed, and grep's exit 1 is the documented not-found answer."),

case("E-09", "empty-output",
     "A monitoring channel produced no alerts overnight.",
     'mkdir w && cd w\n: > alerts.log\ngrep -c "" alerts.log\necho "exit: $?"\n'
     'wc -c alerts.log\n',
     "The fleet was healthy overnight because no alerts fired.",
     "insufficient",
     "An empty alert log cannot distinguish a healthy fleet from a dead reporting channel; nothing here evidences that the channel was alive."),

case("E-10", "empty-output",
     "An operator checked for running containers with a name filter.",
     'mkdir w && cd w\nprintf "web-1 running\\napi-2 running\\n" > containers.txt\n'
     'grep "^worker-" containers.txt\necho "exit: $?"\nwc -l < containers.txt\n',
     "No containers whose names start with worker- are running.",
     "supported",
     "The source listing is shown to be non-empty and the anchored pattern selected no lines, which is grep's exit-1 answer for this scope."),

case("E-11", "empty-output",
     "An operator diffed a deployed config against the repository copy.",
     'mkdir w && cd w\nprintf "a=1\\n" > deployed.conf\ncp deployed.conf repo.conf\n'
     'diff deployed.conf repo.conf\necho "exit: $?"\n',
     "The deployed config matches the repository copy.",
     "supported",
     "diff printed nothing and exited 0, which is its documented 'inputs are the same' answer."),

case("E-12", "empty-output",
     "An operator grepped a log that had just been rotated.",
     'mkdir w && cd w\nprintf "2026-08-29 ERROR upstream timeout\\n" > svc.log\n'
     'mv svc.log svc.log.1\n: > svc.log\ngrep -c "ERROR" svc.log\necho "exit: $?"\nls\n',
     "There were no upstream failures during the shift.",
     "contradicted",
     "The searched file is a freshly created empty log; the rotated sibling svc.log.1 shown in the listing holds the error the claim denies."),

if __name__ == "__main__":
    dump(str(Path(__file__).parent.parent / "cases-fam1-4.json"))
