#!/usr/bin/env python3
"""Scorer for the-four-questions eval. Stdlib only, per the gate sandbox.

Task: given (context, transcript, claim), the model under test outputs a
verdict in {supported, contradicted, insufficient} and a 0-100 confidence.

Modes
  --endpoint URL   query an OpenAI-compatible chat endpoint per case
  --answers FILE   score pre-collected answers (JSON: {case_id: {"verdict":..,
                   "confidence":..}}) -- no network; how the smoke test runs
  --dry-run        print the prompts that would be sent, send nothing

Conditions (--condition): none (baseline), compact (prepends compact.md),
book (prepends book.md). Treatment files live beside this script; missing
treatment file is an error, not a silent fallback.

Metrics: verdict accuracy (overall and per-family) and a Brier score on the
stated confidence, taken as the forecast probability that one's own verdict
is correct: (confidence/100 - correct)^2, mean over cases. Lower is better;
a coin-flipping reader that knows it is coin-flipping beats a confident one.
"""
import argparse, json, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERDICTS = ("supported", "contradicted", "insufficient")

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


def load_cases(path):
    data = json.loads(Path(path).read_text())
    cases = data["cases"]
    for c in cases:
        assert c["gold"] in VERDICTS, f"{c['id']}: bad gold {c['gold']!r}"
    return cases


def build_prompt(case, condition):
    body = PROMPT.format(**case)
    if condition == "none":
        return body
    treatment = HERE / ("compact.md" if condition == "compact" else "book.md")
    if not treatment.exists():
        sys.exit(f"treatment file missing: {treatment} (authored with the book; "
                 "no silent fallback to the baseline condition)")
    return treatment.read_text() + "\n\n---\n\n" + body


def parse_answer(text):
    """Take the LAST verdict/confidence pair in the reply.

    Reasoning models routinely restate the option list, or think aloud and
    revise, before committing. Reading the first match scores the menu
    rather than the answer — which would understate a verbose model and
    silently favour terse ones, an artifact of the harness rather than the
    treatment.
    """
    vs = re.findall(r"verdict:\s*(supported|contradicted|insufficient)", text, re.I)
    cs = re.findall(r"confidence:\s*(\d{1,3})", text)
    if not vs:
        return None, None
    conf = min(100, int(cs[-1])) if cs else 50
    return vs[-1].lower(), conf


def query(endpoint, model, prompt, timeout=120):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps({"model": model, "temperature": 0,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(HERE / "cases-seed.json"))
    ap.add_argument("--condition", choices=("none", "compact", "book"), default="none")
    ap.add_argument("--endpoint")
    ap.add_argument("--model", default="model-under-test")
    ap.add_argument("--answers")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", help="write per-case results JSON here")
    args = ap.parse_args()

    cases = load_cases(args.cases)
    if args.dry_run:
        for c in cases:
            print(f"===== {c['id']} =====\n{build_prompt(c, args.condition)}\n")
        return

    answers = {}
    if args.answers:
        answers = json.loads(Path(args.answers).read_text())
    elif not args.endpoint:
        sys.exit("need --endpoint, --answers, or --dry-run")

    results = []
    for c in cases:
        if args.answers:
            a = answers.get(c["id"])
            verdict, conf = (a.get("verdict"), a.get("confidence", 50)) if a else (None, None)
        else:
            verdict, conf = parse_answer(query(args.endpoint, args.model,
                                               build_prompt(c, args.condition)))
        correct = verdict == c["gold"]
        results.append(dict(id=c["id"], family=c["family"], gold=c["gold"],
                            verdict=verdict, confidence=conf, correct=correct,
                            brier=None if conf is None else (conf / 100 - correct) ** 2))

    scored = [r for r in results if r["verdict"] is not None]
    unparsed = [r["id"] for r in results if r["verdict"] is None]
    n = len(results)
    acc = sum(r["correct"] for r in results) / n  # unparsed count as wrong
    brier = (sum(r["brier"] for r in scored) / len(scored)) if scored else float("nan")

    fams = {}
    for r in results:
        fams.setdefault(r["family"], []).append(r["correct"])

    print(f"condition={args.condition}  cases={n}  accuracy={acc:.3f}  brier={brier:.3f}")
    if unparsed:
        print(f"unparsed (scored as wrong): {', '.join(unparsed)}")
    for fam in sorted(fams):
        ok = fams[fam]
        print(f"  {fam:24s} {sum(ok)}/{len(ok)}")
    if args.out:
        Path(args.out).write_text(json.dumps(
            dict(condition=args.condition, accuracy=acc, brier=brier,
                 results=results), indent=2) + "\n")


if __name__ == "__main__":
    main()
