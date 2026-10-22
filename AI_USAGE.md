# AI Usage Disclosure

## Tools used

- ChatGPT

## Summary

I used ChatGPT to review the assignment requirements, guide repository setup,
inspect my rehearsal bundle, draft temporary Mermaid sketches, and prepare
AI-assisted annotations of the domain document. ChatGPT also drafted this
disclosure and the progress checklist. A complete candidate class diagram,
two sequence diagrams and rationale were installed and pushed as d237bcc.
The generated bundle was inspected. A later review strengthens the settlement
trace and simplifies state responsibilities. Student understanding and final
delivery confirmation remain unverified.

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
  At that checkpoint the original class Mermaid source was retained.
  **Later status:** the final diagrams were rendered directly and the
  temporary practice sources were removed in d237bcc.

### Entry 3 — Complete annotated document and installation package

- **Date:** 2026-10-22
- **Tool:** ChatGPT with read-only GitHub access and local file preparation
- **Related commits:** Repository checkpoint fa741a9 preceded this update.
  The installed annotation package was committed and pushed as 2004e79.
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
- **At that checkpoint:** The notes did not choose the final hierarchy.
  Lifecycle, construction, valuation and settlement were subsequently
  diagrammed in d237bcc and revised in Entry 5.

### Entry 4 — Candidate model, rationale and review package

- **Date:** 2026-10-22
- **Tool:** ChatGPT, read-only GitHub checks, and local Mermaid validation
- **Related commits:** Installed and pushed as d237bcc, verified on GitHub.
  The first generated bundle containing this model was also inspected.
- **What I asked for:** Check the installed annotations and guide the next
  assignment stage with complete, usable files.
- **What it produced:** One Mermaid class diagram in Markdown, the two
  required sequence diagrams, an eight-part rationale, a coverage and
  operation audit, a study guide, a validation record, and updated README,
  disclosure and progress files.
- **Assistant modelling decisions:** Asset interface; individually issued
  contracts distinct from listed definitions; a private signed payoff
  coefficient; rejecting default lifecycle states; exchange threshold
  policy; an owning ledger for atomic paired changes; deterministic
  eligible writer selection with unit re-pairing; a registry boundary.
- **Alternatives rejected:** Right-enum switches outside construction;
  duplicate CallOption/PutOption operations; universal Asset lifecycle;
  independent balance updates; multiple inheritance for has-a relations.
- **What the assistant corrected during preparation:** Mermaid treats
  semicolons in sequence notes as statement separators, so they were
  replaced with commas. Long method declarations were shortened to
  parameter names, with the types documented beneath the class diagram.
  A definition cache was added so equivalent listings share assignment pools.
- **Assistant verification:** Parsed and rendered all three Mermaid blocks;
  reviewed renderings; checked that every sequence call names an operation
  in the class model with the matching argument count; checked all eight
  rationale headings and the archive contents. No market simulation was
  written or executed.
- **Additional formula reference:** MIT OpenCourseWare standard call/put
  expressions were consulted only to check that the proposed signed BSM
  expression can avoid a kind switch. Requirements still come from the
  assignment domain document; the source gap is explicitly recorded.
- **Student verification and changes:** Pending. The architecture, diagrams
  and rationale were drafted by ChatGPT. The student must understand,
  review and, where necessary, revise them before submission. The record
  does not claim independent student design choices or completed exam practice.
- **Material limitations:** Individual-unit rather than bulk contracts;
  restricted feasible re-pairing policy; no netting or failed delivery;
  on-time expiry assumed; chosen threshold and day count. These are
  explained in rationale.md rather than hidden.

### Entry 5 — Rubric review and explicit settlement revision

- **Date:** 2026-10-22
- **Tool:** ChatGPT with source review and local Mermaid validation
- **Related commits:** d237bcc is the verified installed checkpoint. The
  commit containing this entry records the revised package after installation.
- **Request:** Assess the actual bundle against the rubric and strengthen
  weak areas. The student asked for a higher mark.
- **Produced:** Revised class model and expiry sequence, consistent rationale
  and audit, current progress/disclosure, and expanded explanation practice.
- **Changes:** Account position/cash changes and assignment recording are
  explicit sequence messages. OptionContract coordinates resolution; state
  objects supply authorization and valuation. All financial effects remain
  one indivisible ledger operation. No market simulation is supplied.
- **Rejected:** Fabricating reading history, backdating commits, claiming
  student understanding without evidence, or guaranteeing a grade.
- **Verification:** The validation record reports parsing, rendering and
  sequence-to-class operation checks for this revision.
- **Student review:** Still required. These are assistant-authored changes
  and preparation explanations, not evidence of an unaided design or defense.
- **Submission issue:** The assistant checked the published take-home form
  and found identity fields and a checklist but no file-upload question.
  A checklist response alone does not establish delivery of the bundle.
  Instructor confirmation of the delivery route remains necessary.

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

