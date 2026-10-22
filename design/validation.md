# Candidate package validation

Checked on October 22, 2026. This record covers the revised downloadable
files; it does not certify a later edit or the student's eventual bundle.

| Check | Result |
|---|---|
| Mermaid engine | 11.17.2 |
| Class diagram | Parsed and rendered; 22 classes in five namespaces |
| Expiry sequence | Parsed and rendered; 5 participants; 18 calls matched to class operation names and argument counts |
| Put valuation sequence | Parsed and rendered; 5 participants; 6 calls matched to class operation names and argument counts |
| Required rationale questions | All eight numbered headings present |
| Alternatives and misfits | Present and specific to this model |
| Diagram format | Exactly one Mermaid block in each of the three canonical diagram files |
| File types in update | Markdown only |
| munger.py in update | Absent; existing distributed script is preserved |

Local SVG renderings were inspected. The class model is a large relationship
map and needs zooming to read; namespaces group ownership, terms/payoffs,
lifecycle, clearing and the entry boundary. The sequence diagrams each have
at most five participants. Holder and Writer resolve to the Account class.
The expiry sequence has explicit option closure, stock delivery, strike cash,
assignment recording and terminal transition inside one critical fragment.
The revised state interface supplies permission and valuation while the
contract coordinates resolution. Both sequences match that responsibility split. No browser visual-import round trip is needed.

The matching-call check verifies source consistency, not financial semantics
or a future implementation. The no-kind-tests reasoning and the atomic
settlement contracts are reviewed in audit.md and rationale.md. These are
model specifications, not claims of executable enforcement or a market test
suite. Human review and rendering in the student's final viewing environment
remain necessary before submission.

The delivered revision was checked to contain the three root Markdown files and seven
files under design/. Temporary validation scripts, images, dependencies,
student bundles and the distribution PDF are not part of this update.
