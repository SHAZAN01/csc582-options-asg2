# AI Usage Disclosure

## Tools used

- ChatGPT

## Summary

I used ChatGPT to review the assignment requirements, guide repository setup,
inspect my rehearsal bundle, draft temporary Mermaid sketches, and prepare
AI-assisted annotations of the domain document. ChatGPT also drafted this
disclosure and the progress checklist. The final domain model and rationale
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

### Entry 3 — Complete annotated document and installation package

- **Date:** 2026-10-22
- **Tool:** ChatGPT with read-only GitHub access and local file preparation
- **Related commits:** Repository checkpoint fa741a9 precedes this update.
  The student will commit the downloaded files locally after review.
- **What I asked for:** A complete corrected document because manually
  inserting the annotation blocks was confusing.
- **What it produced:** An annotated OPTIONS-MARKETS.md, an updated
  AI_USAGE.md, an updated PROGRESS.md, and a ZIP containing these three files.
- **What changed:** Added variation, fixed-rule, impossible-case, design
  implication, unit, scope, and ambiguity notes beside the source sections.
  Preserved all original paragraphs, tables, examples, formulas, figure
  references, and glossary entries.
- **Assistant verification:** Removing the delimited annotation blocks
  recovers the attached original text exactly. Figure paths and original
  examples remain present. The archive contains only the three named
  Markdown files.
- **Student verification:** Pending. These notes were drafted by ChatGPT.
  Their creation does not establish that I independently read or understood
  every section. I need to read the notes against the original text and
  explain the resulting model myself in class.
- **Rejected or unresolved:** The notes do not choose the final class
  hierarchy. The lifecycle design, single construction boundary, valuation
  design, and settlement protocol remain to be decided and diagrammed.

## Where the agent or tool workflow needed correction

The first sequence sketch used valid Mermaid aliases, but the visual
importer rewrote them into identifiers containing colons and its Preview
failed. Using simple participant names fixed that import. The class
importer omitted operations and relationship details; its visual canvas
does not establish that the complete class script has been preserved.

ChatGPT attempted a GitHub file update on October 21. GitHub rejected the
write with a permissions error; no remote files changed. The student
successfully pushed the existing local work using Terminal.

An earlier progress-file snapshot reported only two commits and an
unverified push. The later check confirmed three commits through fa741a9
and a successful push. That snapshot is corrected in this package.

