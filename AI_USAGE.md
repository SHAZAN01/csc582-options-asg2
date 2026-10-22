# AI Usage Disclosure

## Tools used

- ChatGPT

## Summary

I used ChatGPT to review the assignment requirements, guide repository setup,
inspect my rehearsal bundle, and draft the temporary Mermaid sketches below.
ChatGPT also drafted this disclosure. The final domain model and rationale
have not yet been developed.

## Log

### Entry 1 — Setup and Mermaid rehearsal

- **Date:** 2026-10-21
- **Tool:** ChatGPT
- **Related commits:** 6b8215d for initial setup; the commit containing this
  entry records the disclosure and temporary diagram sketches.
- **What I asked for:** Step-by-step help understanding and completing the
  assignment, checking the package, creating my repository, and bundling it.
- **What it produced:** A requirements checklist, Terminal instructions,
  a review of the rehearsal bundle, and temporary Mermaid sketches.
- **What I changed, rejected, or had to fix:** I used Shazan Ansar as my
  submission name. These sketches are format rehearsals, not my final model.
- **What I verified myself, and how:** I ran the package checksum command;
  every listed file reported OK. I ran the bundler and opened its output.
  Visual verification of the temporary Mermaid sketches is pending.

## Where the agent was wrong

No modelling errors have been identified yet. This section will be updated
if later review reveals an error in an AI suggestion.

### Entry 2 — Mermaid importer troubleshooting

- **Date:** 2026-10-21
- **Tool:** ChatGPT
- **Related commits:** The commit containing this entry records the workaround.
- **What I asked for:** Help importing and rendering the practice diagrams.
- **What it produced:** Revised sequence script using simple participant names.
- **What changed:** Removed participant aliases and the rehearsal note.
  Named the final return totalValue; it represents quantity times stock price.
- **Verification:** Imported the revised sequence script and exported its
  rendered image. The Preview showed three participants and four messages
  without a rendering error.
- **Remaining issue:** The class diagram's visual import omitted operations
  and relationship details. Full class-diagram verification is still pending.
  The original class Mermaid source is retained.
