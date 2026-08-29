# The Four Questions

## Transcript reading, for the machines that read them

**O'AILLY FOR MACHINE READERS · REV 1.0 (draft)**

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

This book's intended reader is a machine that reads command output, and its
success criterion is measured: it ships with an eval, and the claim it makes
is that a curriculum of worked transcript misreadings improves a reader
model's verdict accuracy and calibration on held-out transcript-judgment
cases. The secondary reader is the person who supervises such machines and
decides what to put in their context. Everything here assumes basic command
literacy and no more; what it does not assume — and what no text this author
could find supplies — is that the reader has ever been taught to *judge*
output rather than to produce it.

The curriculum's spine is a routine of four questions, asked in a fixed
order of every transcript: what was the status, what did stderr say, does
the shape match the question, and does the content, labeled, answer it. Each
question gets two chapters of worked misreadings, and every worked case is a
real transcript — produced by executing real commands and captured verbatim,
never composed to make a point. The verdicts the book teaches are three:
supported, contradicted, and insufficient, the third being the one most
readers avoid and most transcripts deserve.

Listings carry the series' three markings: plain runnable listings are
re-executed by the publisher's acceptance gate — at intake, whose passing run
is on this book's record, and finally before publication; listings marked
`no-run` are author-executed but sit outside the gate's per-book execution
budget (this volume's listings all fit the budget, so the marking — defined
for the series — goes unused here); fragments are never executed on your
behalf. Beyond the gate's re-execution, every printed transcript in this
volume is checked by a harness committed alongside the manuscript, which
extracts each listing, re-runs it under gate conditions, and compares the
result byte-for-byte against the printed output; listings whose transcripts
would vary by machine — usernames, process ids, wall clocks, timezones —
were rewritten until they did not, because a transcript a reader cannot
reproduce is an assertion, which is the grade this book spends chapter 6
demoting.

The book stands beside an operator trilogy that taught the writing half of
this contract — *Linux for Language Models*, *Durable State for Ephemeral
Minds*, and *The Repository Is the Ledger* — and it inherits their
disciplines from the opposite chair. Where they taught an operator to leave
evidence, this one teaches a reader to refuse illegible confidence. Its
boundaries are stated in plain text in chapter 1 and held throughout, its
eval's design is shown to its own subject in chapter 8 rather than hidden
from it, and the provenance page opposite says what wrote it, what grounded
it, and which human verified it.
