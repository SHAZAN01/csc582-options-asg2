# CSC 582 — Assignment #2: Modelling an Unfamiliar System Through Abstraction — The Options Market (Fall 2026)

Take a domain you have probably never worked in — options, and the contracts built out of them —
described in ordinary prose, and turn it into an object model. **You write no code that simulates
the market.** The only code you write is Mermaid script, which generates your UML diagrams: a class
diagram and two sequence diagrams. You also write a design rationale, and you defend all of it in a
monitored in-class session.

> [!IMPORTANT]
> **You are not expected to be perfect.** Asg2 grades are curved to a class average of 75 (Asg1
> grades were not). Your grade depends on how carefully and thoroughly you carry out each part,
> compared with your classmates.

**Everything your model is based on is in [`OPTIONS-MARKETS.md`](OPTIONS-MARKETS.md)**, the domain
description in this repository. The handout cites its sections as "doc §5"; a plain "§5" is a
section of the handout.

**Start here:** [`Fa26-CSC582-Assignment2.pdf`](Fa26-CSC582-Assignment2.pdf) — the assignment itself:
rubric, what you have to model, the one rule the whole design rests on, policies, and how to submit.
Read all of it before drawing anything; the no-kind-tests rule and the design rationale are easy to
design yourself into a corner on.

Then do [`WALKTHROUGH.md`](WALKTHROUGH.md) on day one. It takes half an hour and proves your whole
pipeline works — repository, Mermaid, bundle — while it's still cheap to find out it doesn't.

## What's in this package

| | |
|---|---|
| [`Fa26-CSC582-Assignment2.pdf`](Fa26-CSC582-Assignment2.pdf) | The assignment. Rubric first, then the domain, the rule, policies, and how to submit. |
| [`OPTIONS-MARKETS.md`](OPTIONS-MARKETS.md) | The domain description — the "requirements document" you model. **You mark this up in place as you read it** (rubric item 1). |
| [`figures/`](figures/) | The diagrams that `OPTIONS-MARKETS.md` shows. |
| [`WALKTHROUGH.md`](WALKTHROUGH.md) | Day-one setup: verify the munger, make your repo, dry-run a bundle, prove your Mermaid renders. |
| [`design/`](design/) | Where your class diagram and two sequence diagrams (Mermaid) and your design rationale (Markdown) go. |
| [`AI_USAGE.template.md`](AI_USAGE.template.md) | Rename to `AI_USAGE.md` in your repo and keep it current (rubric item 8). |
| [`munger.py`](munger.py) | Run from your repo root to bundle your project into the single file you submit. **Do not modify it.** |
| [`CHECKSUMS.txt`](CHECKSUMS.txt) | SHA-256 of every file in this package, so you can confirm your copy is unmodified. |

## Getting a copy

Use **Code → Download ZIP** on this page, or clone the repository. Either way you need the files on
your own machine, because your work lives in a git repository of your own —
[`WALKTHROUGH.md`](WALKTHROUGH.md) step 1 sets it up. If you clone, copy the
files out into a fresh directory rather than working inside the clone: the clone's history is this
package's, and your commit history is graded as yours.

## Mermaid, and prose

Everything you submit is one of two kinds:

- **Mermaid script — required for every diagram.** Your class diagram is a Mermaid `classDiagram`
  and your two sequence diagrams are `sequenceDiagram`s, committed in `design/` as `.mmd` files or
  `mermaid` code blocks in Markdown files. Not images, and not another diagram language. In the
  in-class session, Part B's class diagram is Mermaid too, typed into the exam's answer box.
- **Prose, in Markdown — everything else:** your design rationale, `AI_USAGE.md`, your `README.md`,
  and your marked-up copy of `OPTIONS-MARKETS.md`.

## Checklist: what your repository must contain

Go through this before you run `munger.py` on submission day. The names of the diagram files are
up to you; the contents are not.

- [ ] `OPTIONS-MARKETS.md` — your marked-up copy, at the top of the repository
- [ ] `README.md` — half a page: how to read your repository
- [ ] `AI_USAGE.md` — renamed from `AI_USAGE.template.md`, and up to date
- [ ] your class diagram, as Mermaid script in `design/` (a `.mmd` file, or a `mermaid` block in a
      `.md` file)
- [ ] your two sequence diagrams, as Mermaid script in `design/`: exercise at expiry, and the value
      of a put
- [ ] `design/rationale.md` — the eight questions, at least two rejected alternatives, and your
      misfits
- [ ] at least 20 commits, on at least 7 different days, each with a real message
- [ ] none of *your* files under `FILES NOT BUNDLED` in the bundle — only the handout PDF and
      `figures/` belong there
- [ ] the **same student ID** in `munger.py` and in the exam form: your bundle is found by it

## Verifying this package

Every file here is checksummed. From this directory:

```
sha256sum -c CHECKSUMS.txt        # Linux
shasum -a 256 -c CHECKSUMS.txt    # macOS
```

Every line should report `OK`. On Windows PowerShell, check a single file with
`Get-FileHash munger.py -Algorithm SHA256` and compare against the entry in `CHECKSUMS.txt`.

Two different reasons to run this:

- **`munger.py` must never change.** Its digest is recorded in every bundle you produce and is
  checked when your submission is graded. If it doesn't match, re-download the package — don't
  patch it. If the bundler doesn't handle something your project needs, email the instructor.
- **`OPTIONS-MARKETS.md` is the one file you are *supposed* to change.** Its checksum describes the
  copy as distributed; your marked-up copy will differ from it, which is the point (rubric item 1).
  Everything else should stay as it is, apart from renaming `AI_USAGE.template.md`.

## The short version

- **Individual work.** No teams this term.
- **No code that simulates the market**, in any language: no build, no tests. The only code you
  write is Mermaid script, for your UML diagrams; everything else is prose in Markdown.
- **Two weeks** for the take-home.
- **You are not expected to be perfect.** Asg2 grades are curved to a class average of 75 (Asg1
  grades were not).
- **AI assistants are allowed** during the take-home, and must be disclosed in `AI_USAGE.md`. An
  assistant can produce a plausible class diagram of this domain in seconds; what it cannot do is
  answer for that diagram in the in-class session, where it is off.
- **Every mark comes from questions answered in the in-class session.** Your take-home is assessed
  there by **Part A** — in-class questions about your model, graded together with the bundle you
  submitted, against rubric items 1–8 (75%). **Part B** has you design an extension of your own
  model during the in-class session (25%); you commit it and upload a second, in-class bundle at the
  end. An answer that does not match your bundles scores zero.
- **Submit the take-home by running `munger.py`** and uploading the resulting
  `<ID>_<Name>_takehome_bundle.txt` through the take-home form, by the start of class on the day of
  the in-class session: **TAKEHOME-FORM-PENDING** *(the form is not ready yet; its link will be
  added here)*. No GitHub account or hosted repo is required; a local git repo is (its history rides
  along in the bundle — rubric item 7). The in-class bundle goes to a separate form, given out in
  the in-class session.

## Getting started

1. Read the assignment PDF — the rubric is on page 1, and §5's rule will shape every line you draw.
2. Work through [`WALKTHROUGH.md`](WALKTHROUGH.md).
3. Read `OPTIONS-MARKETS.md` the way §0 of that document tells you to, marking it up as you go and
   committing as you read.
4. Model: draw the class diagram and the two sequence diagrams in Mermaid, write the design
   rationale, keep them in `design/`, and commit early and often — at least twenty commits over at
   least seven days.
5. Run `python3 munger.py` and upload the bundle to the take-home form.
