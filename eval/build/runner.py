#!/usr/bin/env python3
"""Shared capture harness for the eval corpus.

Every case's transcript is produced by really running its script in a
gate-style sandbox (PATH=/usr/bin:/bin, fresh HOME, merged streams) and
captured verbatim. Nothing here composes output by hand.
"""
import subprocess, tempfile, json, sys
from pathlib import Path

CASES = []


def case(cid, family, context, script, claim, gold, rationale):
    """Run script, capture the real transcript, append the case."""
    with tempfile.TemporaryDirectory(prefix="tfq-corpus-") as tmp:
        sp = Path(tmp) / "case.sh"
        sp.write_text(script)
        r = subprocess.run(["bash", str(sp)], cwd=tmp, text=True, timeout=30,
                           env={"PATH": "/usr/bin:/bin", "HOME": tmp},
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    CASES.append(dict(id=cid, family=family, context=context,
                      transcript=r.stdout.rstrip("\n"), claim=claim,
                      gold=gold, rationale=rationale))


def dump(path):
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    counts = {}
    for c in CASES:
        counts.setdefault(c["family"], {}).setdefault(c["gold"], 0)
        counts[c["family"]][c["gold"]] += 1
    Path(path).write_text(json.dumps(CASES, indent=2) + "\n")
    print(f"wrote {len(CASES)} cases -> {path}")
    for fam in sorted(counts):
        row = counts[fam]
        print(f"  {fam:24s} " + "  ".join(f"{k}={v}" for k, v in sorted(row.items())))
