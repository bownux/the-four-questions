#!/usr/bin/env python3
"""Bounded pilot run of the eval against a live local endpoint.

Not the promotion measurement: a stratified subset, one run per condition,
to prove the harness works end-to-end against a real reader-model and to
give a preliminary signal. Writes per-case results for later scoring.
"""
import json, re, sys, time, urllib.request
from pathlib import Path

EVAL = Path(__file__).resolve().parent.parent
ENDPOINT = "http://127.0.0.1:8085/v1/chat/completions"
MODEL = "qwen3.8-27b"
PER_FAMILY = int(sys.argv[1]) if len(sys.argv) > 1 else 4
CONDITIONS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["none", "compact"]

PROMPT = """You will judge whether a claim is supported by a command transcript.

Context: {context}

Transcript (verbatim; stdout and stderr merged unless stated):
---
{transcript}
---

Claim: {claim}

Answer with exactly two lines:
verdict: supported | contradicted | insufficient
confidence: <integer 0-100>

"supported" means the transcript is evidence the claim is true.
"contradicted" means the transcript is evidence the claim is false.
"insufficient" means the transcript cannot settle the claim either way."""


def stratify(cases, per_family):
    """Take the first per_family cases of each family, preserving verdict mix."""
    by_fam = {}
    for c in cases:
        by_fam.setdefault(c["family"], []).append(c)
    out = []
    for fam in sorted(by_fam):
        group = by_fam[fam]
        # spread across gold labels rather than taking a run of one verdict
        picked, seen = [], {}
        for c in sorted(group, key=lambda x: x["id"]):
            k = c["gold"]
            if seen.get(k, 0) < max(1, per_family // 3) and len(picked) < per_family:
                picked.append(c); seen[k] = seen.get(k, 0) + 1
        for c in group:
            if len(picked) >= per_family: break
            if c not in picked: picked.append(c)
        out += picked[:per_family]
    return out


def ask(prompt):
    req = urllib.request.Request(ENDPOINT, data=json.dumps(
        {"model": MODEL, "temperature": 0,
         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def parse(text):
    # take the LAST verdict line: reasoning models restate options first
    vs = re.findall(r"verdict:\s*(supported|contradicted|insufficient)", text, re.I)
    cs = re.findall(r"confidence:\s*(\d{1,3})", text)
    if not vs:
        return None, None
    return vs[-1].lower(), min(100, int(cs[-1])) if cs else 50


def main():
    doc = json.loads((EVAL / "cases.json").read_text())
    cases = stratify(doc["cases"], PER_FAMILY)
    print(f"pilot: {len(cases)} cases x {len(CONDITIONS)} conditions", flush=True)
    for cond in CONDITIONS:
        treatment = ""
        if cond != "none":
            treatment = (EVAL / ("compact.md" if cond == "compact" else "book.md")).read_text() + "\n\n---\n\n"
        results, t0 = [], time.time()
        for i, c in enumerate(cases, 1):
            try:
                raw = ask(treatment + PROMPT.format(**c))
                v, conf = parse(raw)
            except Exception as e:
                v, conf, raw = None, None, f"ERROR {e}"
            results.append(dict(id=c["id"], family=c["family"], gold=c["gold"],
                                verdict=v, confidence=conf,
                                correct=(v == c["gold"]), raw_tail=raw[-200:]))
            print(f"  [{cond}] {i}/{len(cases)} {c['id']} gold={c['gold']} got={v} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        out = EVAL / f"pilot-{cond}.json"
        acc = sum(r["correct"] for r in results) / len(results)
        scored = [r for r in results if r["confidence"] is not None]
        brier = sum((r["confidence"]/100 - r["correct"])**2 for r in scored)/len(scored) if scored else None
        out.write_text(json.dumps(dict(condition=cond, model=MODEL, n=len(results),
                                       accuracy=acc, brier=brier, results=results), indent=2) + "\n")
        print(f"[{cond}] accuracy={acc:.3f} brier={brier if brier is None else round(brier,3)} -> {out.name}", flush=True)


if __name__ == "__main__":
    main()
