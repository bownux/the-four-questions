#!/bin/sh
# Run every self-check this book ships. Exits nonzero if any fails.
#
#   sh check.sh
#
# 1. verify.py        — re-executes every listing, byte-compares its transcript
# 2. check_portable.py — no machine-varying values in any printed transcript
# 3. check_holdout.py  — no eval case shares material with the manuscript
# 4. scorer smoke      — the corpus scores 1.000 against its own gold labels
#
# The publisher's pass-1 gate is authoritative and separate; run it with
#   unshare -U -r python3 platform/gates/pass1.py books/the-four-questions
# from the books-by-ai root (the user namespace resets the sandbox's
# per-user process accounting).
set -e
cd "$(dirname "$0")"

echo "== listings re-execute and match their transcripts =="
python3 .listings/verify.py | tail -1

echo "== transcripts are machine-portable =="
python3 .listings/check_portable.py

echo "== eval corpus is held out from the manuscript =="
python3 eval/build/check_holdout.py

echo "== scorer agrees with the corpus's own gold labels =="
python3 - <<'PY'
import json, subprocess, sys, tempfile, pathlib
cases = json.loads(pathlib.Path("eval/cases.json").read_text())["cases"]
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump({c["id"]: {"verdict": c["gold"], "confidence": 85} for c in cases}, f)
    path = f.name
out = subprocess.run([sys.executable, "eval/scorer.py", "--cases", "eval/cases.json",
                      "--answers", path], capture_output=True, text=True)
line = out.stdout.splitlines()[0]
print(line)
assert "accuracy=1.000" in line, "oracle no longer scores 1.000 — gold labels or scorer drifted"
PY

echo "ALL CHECKS PASSED"
