#!/usr/bin/env python3
"""Test book-4 listings under gate conditions; print each with its transcript."""
import subprocess, tempfile, sys
from pathlib import Path

def run(name, script):
    with tempfile.TemporaryDirectory(prefix="tfq-ch-") as tmp:
        sp = Path(tmp)/"listing.sh"; sp.write_text(script)
        r = subprocess.run(["bash", str(sp)], cwd=tmp, text=True, timeout=25,
                           env={"PATH":"/usr/bin:/bin","HOME":tmp},
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(f"##### {name} (rc={r.returncode})")
        print(r.stdout.rstrip("\n"))
        print()

for f in sorted(Path(sys.argv[1]).glob("*.sh")):
    run(f.name, f.read_text())
