#!/usr/bin/env python3
"""Balance batch: supported/insufficient cases for the contradicted-heavy
families, so no single-verdict strategy beats a third of the corpus."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from runner import case, dump

case("V-13", "verdict-channel",
     "A packaging step wrote an archive and the operator checked its exit status.",
     'mkdir w && cd w\nmkdir -p pkg\nprintf "content\\n" > pkg/file.txt\n'
     'tar -cf pkg.tar pkg\necho "exit: $?"\ntar -tf pkg.tar | wc -l\n',
     "The archive was created successfully.",
     "supported",
     "tar exited 0 and its table of contents lists entries, so the archive exists and is readable."),

case("V-14", "verdict-channel",
     "A script's exit status was captured after an intervening echo.",
     'mkdir w && cd w\nprintf "x\\n" > f.txt\ngrep "zzz" f.txt\n'
     'echo "checking status now"\necho "exit: $?"\n',
     "The search command exited nonzero.",
     "insufficient",
     "The printed status belongs to the echo that ran immediately before it, not to grep; $? was overwritten, so the search's own status is not in the record."),

case("C-13", "commentary-channel",
     "A data loader ran; streams are merged.",
     'mkdir w && cd w\ncat > load.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "loading from cache" >&2\necho "loaded 12 records"\nEOF\n'
     'chmod +x load.sh\n./load.sh\necho "exit: $?"\n',
     "Twelve records were loaded.",
     "supported",
     "The stdout line reports the count and the exit status is 0; the stderr line is an informational notice that does not bear on the count."),

case("C-14", "commentary-channel",
     "A job's output was captured with stderr sent to a separate file that is not shown.",
     'mkdir w && cd w\ncat > job.sh <<\'EOF\'\n#!/bin/sh\n'
     'echo "deprecated option in use" >&2\necho "job finished"\nEOF\n'
     'chmod +x job.sh\n./job.sh 2> err.log\necho "exit: $?"\n',
     "The job ran without any deprecation notices.",
     "insufficient",
     "stderr was redirected away from this capture, so the transcript cannot establish whether notices were emitted."),

case("S-13", "success-shaped-failure",
     "A file was truncated to a fixed size and the result checked.",
     'mkdir w && cd w\nprintf "0123456789\\n" > blob.bin\ntruncate -s 4 blob.bin\n'
     'echo "exit: $?"\nwc -c < blob.bin\n',
     "The file is now 4 bytes.",
     "supported",
     "The byte count is read back from the file and printed as 4, matching the claim exactly."),

case("S-14", "success-shaped-failure",
     "A directory was synchronized by copying newer files into it.",
     'mkdir w && cd w\nmkdir -p a b\nprintf "1\\n" > a/x.txt\ncp -u a/x.txt b/\n'
     'echo "exit: $?"\n',
     "A newer version of x.txt was copied into b/.",
     "insufficient",
     "cp -u copies only when the source is newer, and exits 0 either way; without a listing or comparison the transcript cannot show whether a copy occurred."),

case("H-13", "shape-mismatch",
     "An operator counted distinct users appearing in an access log.",
     'mkdir w && cd w\nprintf "ann\\nbob\\nann\\n" > users.log\n'
     'wc -l < users.log\necho "exit: $?"\nsort -u users.log | wc -l\n',
     "Two distinct users appear in the log.",
     "supported",
     "The deduplicated count is 2, which is the figure the claim is about; the raw line count of 3 answers a different question."),

case("A-13", "claim-vs-evidence",
     "A quota check was run and its output compared against a stated limit of 100.",
     'mkdir w && cd w\nprintf "used=42\\n" > quota.txt\ncat quota.txt\necho "exit: $?"\n',
     "The account is under its quota of 100.",
     "supported",
     "The observed usage of 42 is below the limit stated in the context, and the value is read from the file rather than asserted."),

if __name__ == "__main__":
    dump(str(Path(__file__).parent.parent / "cases-balance.json"))
