# CSC 582 Assignment 2 — Options market object model

**Shazan Ansar — 213063554.** Take-home deadline: October 23, 2026, 5:30 PM.
This repository contains Mermaid diagrams and Markdown prose, with no market
simulation. Significant assistance and verification are recorded in AI_USAGE.md.

Start with OPTIONS-MARKETS.md. Its original prose is preserved; added notes
mark variation, fixed rules, impossible cases, assumptions and design implications.
Then read the canonical diagrams and their rationale:

| File | Purpose |
|---|---|
| design/model.md | One class diagram: ownership, terms, payoff, lifecycle, clearing and construction. |
| design/expiry.md | Automatic call exercise, with both accounts, physical delivery, strike cash and one assignment. |
| design/put-value.md | Pre-expiry put valuation through state and payoff delegation. |
| design/rationale.md | Eight required explanations, rejected alternatives, invariants and misfits. |
| design/traceability.md | Maps source requirements to model responsibilities and sequence evidence. |
| design/audit.md | Reviews operations, lifecycle permissions and failure obligations. |
| design/validation.md | Records diagram parsing, rendering and operation checks. |
| design/study-guide.md | Preparation explanations tied to this model. |
| PROGRESS.md | Verified checkpoints and remaining actions. |

The three canonical diagram files each contain one Mermaid block. View them
in GitHub's rendered Markdown and zoom the class diagram for detail. The supplied
design/README.md remains distribution guidance with illustrative notation.

The model separates reusable listed definitions from individually issued units.
Position holds either Stock or OptionContract through Asset. A composed state
authorizes resolution, Payoff supplies financial behavior, and one ledger operation
commits balanced ownership, delivery, assignment and lifecycle effects. The
rationale explains the costs, including unit granularity and assignment re-pairing.

Run unchanged python3 munger.py from this root, select 1, and use student ID
213063554. Inspect the generated take-home text file and actual git history.
Only the supplied PDF and figures should appear under FILES NOT BUNDLED.
Generated bundles and macOS metadata are ignored by Git. Student review and
successful delivery of the bundle remain separate from file preparation.
