# The Four Questions

## Transcript reading, for the machines that read them

**O'AILLY For Machine Readers · REV 1.0 (draft)**

## Contents

- Chapter 1 — The Verdict Channel
- Chapter 2 — What the Number Cannot Say
- Chapter 3 — The Commentary Channel
- Chapter 4 — The Sound of Nothing
- Chapter 5 — Shape Before Content
- Chapter 6 — Claims Against Evidence
- Chapter 7 — Time, Order, and the Moving World
- Chapter 8 — Judging Under Uncertainty

## Introduction

This book is for a language-model agent that reads command output — and,
second, for the human who supervises such agents. It assumes shell literacy
and no machine-learning background. Its claim is narrow and testable: a curriculum of worked transcript
misreadings, taught through the four-question routine — status, stderr,
shape, labeled content — is designed to improve a reader-model's accuracy
and calibration on held-out transcript-judgment cases. At submission that
improvement is **proposed and testable, not yet measured**; the eval ships
with the book, its design is shown to the reader in chapter 8, and the
press's judge — not the author — grades the exam in the open.

The verdicts the book teaches are three: supported, contradicted, and
insufficient, the third being the one most readers avoid and most
transcripts deserve. Every worked case is a real transcript, produced by
executing real commands in a gate-style sandbox and captured verbatim; the
book does not invent console text.

Listings carry the series' three markings: plain runnable listings are
re-executed by the publisher's acceptance gate — at intake, whose passing run
is on this book's record, and finally before publication; listings marked
`no-run` are author-executed but sit outside the gate's per-book execution
budget (this volume's listings all fit the budget, so the marking — defined
for the series — goes unused here); fragments are never executed on your
behalf, and this volume contains none. Beyond the gate's re-execution, every
printed transcript is checked by a harness committed alongside the
manuscript, which extracts each listing, re-runs it under gate conditions,
and compares the result byte-for-byte against the printed output; listings
whose transcripts would vary by machine — usernames, process ids, wall
clocks, timezones — were rewritten until they did not, and a second
committed checker enforces that, because a transcript a reader cannot
reproduce is an assertion, which is the grade chapter 6 spends its length
demoting.

Draft status is honest on every chapter header: human verification is
pending, and nothing ships until the press's three-pass pipeline and a named
human verifier say so. The book stands beside an operator trilogy that
taught the writing half of this contract — *Linux for Language Models*,
*Durable State for Ephemeral Minds*, and *The Repository Is the Ledger* —
and inherits their disciplines from the opposite chair. Where they taught a
machine to leave legible evidence, this one teaches a machine to refuse
illegible confidence. The provenance page opposite says what wrote it, what
grounded it, and which human verified it.
