# CSC 582 Assignment 2 — Options market object model

Student submission name: **Shazan Ansar**. Take-home deadline: **October 23,
2026, 5:30 PM**. This repository contains Mermaid diagrams and Markdown prose;
it contains no executable market simulation.

Read `OPTIONS-MARKETS.md` first. Its original domain text is preserved and
AI-assisted annotations mark variation, fixed rules, impossible cases and
ambiguities. Significant assistance is disclosed in `AI_USAGE.md`.

| File | Purpose |
|---|---|
| `design/model.md` | The single class diagram, with terms, ownership, payoff behaviour, lifecycle, clearing and construction. |
| `design/expiry.md` | Automatic exercise of one in-the-money call, including physical delivery and assignment. |
| `design/put-value.md` | A put's value before expiry through state and payoff delegation. |
| `design/rationale.md` | All eight rationale questions, rejected alternatives, assumptions and misfits. |
| `design/audit.md` | Coverage, operation and lifecycle review. |
| `design/study-guide.md` | Explanations and open-ended preparation questions. |
| `PROGRESS.md` | Verified checkpoints and remaining work. |

Each diagram file contains one Mermaid code block and renders in GitHub's
Markdown view. The Markdown source is the graded artifact. Temporary
`toolchain-*.mmd` sketches should be removed once these replacements are installed.

The model distinguishes listed definitions from individually issued contracts.
Each issued unit has paired ownership and its own state. The rationale explains
the costs of that choice. This is an AI-assisted design draft requiring student
review, not a claim that every course/process requirement is complete.

Run the unchanged `python3 munger.py` from this repository root to generate the
take-home bundle, answering `1`. Inspect its metadata, history and source files
before uploading it. Generated bundles are ignored by Git. The supplied handout
and figures remain in the repository; their binary contents are expected to be
listed under FILES NOT BUNDLED.
