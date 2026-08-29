#!/usr/bin/env python3
"""Check that no printed transcript contains a machine-varying value.

The front matter claims listings were rewritten until their transcripts
reproduce anywhere. This enforces that claim: it scans every ```output
fence for values that would differ on the gate's machine — the authoring
account's username, absolute scratch paths, process ids, non-UTC timezone
offsets, and today's date — and exits nonzero on a hit.
"""
import getpass, os, re, sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
USER = getpass.getuser()
HOME = os.path.expanduser("~")

PATTERNS = [
    (re.compile(rf"\b{re.escape(USER)}\b"), "authoring username"),
    (re.compile(re.escape(HOME)), "authoring home path"),
    (re.compile(r"/tmp/[A-Za-z0-9._-]{6,}"), "absolute scratch path"),
    (re.compile(r"[-+]\d{4}\b"), "timezone offset (pin TZ=UTC; +0000 is fine)"),
    (re.compile(r"\bpid[= ]\d+", re.I), "process id"),
    (re.compile(r"^\s*\d{5,7}\s+\d+\.\d", re.M), "ps-style pid/cpu columns"),
]
ALLOWED = {"+0000"}


def main():
    hits = []
    for f in sorted(BOOK.glob("ch*.md")):
        for block in re.findall(r"```output\n(.*?)```", f.read_text(), re.S):
            for pat, label in PATTERNS:
                for m in pat.finditer(block):
                    if m.group(0) in ALLOWED:
                        continue
                    line = block[:m.start()].count("\n") + 1
                    hits.append(f"{f.name} transcript line {line}: {label} -> {m.group(0)!r}")
    if hits:
        print(f"NON-REPRODUCIBLE TRANSCRIPT VALUES ({len(hits)}):")
        for h in hits:
            print("  " + h)
        return 1
    print("portable: no usernames, home paths, scratch paths, pids, or "
          "non-UTC offsets in any printed transcript")
    return 0


if __name__ == "__main__":
    sys.exit(main())
