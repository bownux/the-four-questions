#!/usr/bin/env python3
"""Extract each ```bash listing, run gate-style, diff against its ```output fence."""
import re, subprocess, tempfile, sys
from pathlib import Path

fails = 0
for ch in sorted(Path(".").glob("ch*.md")):
    text = ch.read_text()
    blocks = re.findall(r"```bash\n(.*?)```\n+```output\n(.*?)```", text, re.S)
    for i, (script, printed) in enumerate(blocks, 1):
        with tempfile.TemporaryDirectory(prefix="tfq-v-") as tmp:
            sp = Path(tmp)/"listing.sh"; sp.write_text(script)
            r = subprocess.run(["bash", str(sp)], cwd=tmp, text=True, timeout=30,
                               env={"PATH":"/usr/bin:/bin","HOME":tmp},
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            real = r.stdout.rstrip("\n")
            want = printed.rstrip("\n")
            if real != want or r.returncode != 0:
                fails += 1
                print(f"MISMATCH {ch.name} listing {i} (rc={r.returncode})")
                print("-- printed:"); print(want)
                print("-- real:"); print(real)
            else:
                print(f"ok {ch.name} listing {i}")
print("FAILURES:", fails)
sys.exit(1 if fails else 0)
