# Walk-through: setting up, and testing your submission before submission day

Do this **on day one**, not the night before. The point is to prove the whole pipeline works —
repository, Mermaid, bundle — while it's still cheap to discover that something doesn't. Budget
half an hour.

You write no code that simulates the market: the only code you write is Mermaid script, which
generates your UML diagrams. So there is no build, no test framework, and no docs generator, and the
toolchain to prove is a short one: **git, Mermaid that renders, and the munger.** That's what these
steps do.

Commands are shown for Linux/macOS; on Windows use PowerShell or WSL and adjust paths.

---

## Step 0 — Verify your copy of the munger

`munger.py` is what turns your project into the single file you submit, and **it must not be
modified** (§10 of the handout). Check that your copy is the one that was distributed:

```
sha256sum munger.py
```

macOS:

```
shasum -a 256 munger.py
```

Compare the output against the digest in `CHECKSUMS.txt` and in §10 of the assignment PDF. They
must match exactly. If they don't, re-download the package — don't try to fix it by hand.

To check the whole package at once, from the package directory:

```
sha256sum -c CHECKSUMS.txt        # Linux
shasum -a 256 -c CHECKSUMS.txt    # macOS
```

Every line should say `OK` — except `OPTIONS-MARKETS.md` once you've started marking it up, which
is expected and is the point (rubric item 1).

## Step 1 — Make your own git repository

Copy the package files into a fresh working directory of your own — **not** a clone of the package
repository, whose history is the package's rather than yours — then:

```
cd ~/csc582-options        # wherever you're working
git init
git add .
git commit -m "Initial commit: distributed package"
```

That's your first commit. You need at least twenty, spread over at least seven distinct days
(rubric item 7) — two weeks gives you room, so use it. A local repository is all you need: no
GitHub account, no remote.

## Step 2 — Do a dry run of the munger, right now

Before you've written a single word of your own, run the bundler on the package as it stands:

```
python3 munger.py
```

It asks three things — your student ID, your name, and which submission this is. Answer **1**
(take-home) for this rehearsal. It then writes `<ID>_<Name>_takehome_bundle.txt` into the current
directory. Type your student ID exactly as you will type it in the exam form later: your bundles
are found by it. That file is your whole take-home submission; it goes to the take-home form (the
URL is in §10 of the assignment PDF). Answer **2** only at the end of the in-class session (Step 7).

This is a rehearsal — the output isn't worth submitting yet, but running it now tells you whether
Python works on your machine, whether you're in the right directory, and what the bundle actually
looks like.

## Step 3 — Read the bundle you just produced

Open the `.txt` file in an editor. You should see five sections in order:

```
STUDENT NAME: Ada Lovelace
STUDENT ID: 12345
SUBMISSION: take-home (due at the start of class)

MUNGER SHA-256: ...                    <- must match Step 0
========================================

GIT COMMIT HISTORY:                     <- your commits, newest first
c8495d2  2026-10-06  Ada Lovelace  Initial commit: distributed package

(1 commits)

========================================

PROJECT STRUCTURE:                      <- your directory tree
├── AI_USAGE.template.md
├── CHECKSUMS.txt
├── Fa26-CSC582-Assignment2.pdf
├── OPTIONS-MARKETS.md
├── README.md
├── WALKTHROUGH.md
├── design
│   └── README.md
├── figures
│   ├── long-call.svg
│   ├── long-put.svg
│   └── short-call.svg
└── munger.py

========================================

FILES NOT BUNDLED:                      <- only the package's own PDF and figures
  Fa26-CSC582-Assignment2.pdf                             134.7 KB
  figures/long-call.svg                                     3.2 KB
  figures/long-put.svg                                      3.4 KB
  figures/short-call.svg                                    3.3 KB
  ...

========================================

SOURCE FILES:                           <- the contents of each file, in full

--- START FILE: AI_USAGE.template.md ---
...
```

**Check these four things**, because they're the same four things that matter on submission day:

1. **The commit history is there.** If it says no `.git` directory was found, you ran the script
   from the wrong directory — run it from your repository root.
2. **Your files are actually in the `SOURCE FILES` section**, not just listed in the tree. The
   tree lists everything; only text files get their contents bundled.
3. **The digest at the top matches Step 0.**
4. **The `FILES NOT BUNDLED` section** lists the package's PDF and the three figures in
   `figures/`, and nothing else. Those are expected — they are the handout and the domain
   document's pictures, not your work. If one of *your* files ever appears there, such
   as a diagram exported as an image, it is not graded (§6 of the handout). Commit it as Mermaid
   script and re-run.

Delete the dry-run bundle when you're done looking at it. Re-running the script overwrites it
anyway.

## Step 4 — Prove your Mermaid renders, before it matters

Every diagram you submit is **Mermaid script** (§6 of the handout) — no other diagram language, and
never an image. Prove it renders *before* you have real content in it: the thing you submit is the
script, and a script with a typo in it renders as nothing — and rubric item 6 is Mermaid that
parses.

Mermaid needs no install. Either:

- put a `mermaid` code block in a Markdown file and preview it in an editor that renders Mermaid
  (VS Code does, with a Mermaid preview extension); or
- open <https://free.mermake.online>, paste your script, and see it drawn. It is also the one
  diagram tool permitted in the in-class session, so time spent in it now is rehearsal.

Now make a **deliberately tiny** class diagram — five or six boxes is plenty — and a tiny sequence
diagram — three participants, three messages. Commit them, and confirm you can see both rendered and
readable before you close the editor. `design/README.md` has a notation sketch for each.

```
# put the diagrams in design/ as script, e.g. design/model.mmd and design/expiry.mmd
git add design/
git commit -m "Prove the Mermaid toolchain: minimal class and sequence diagrams"
```

This is a throwaway. Its job is to surface, on day one, every way the format can fail you: a
preview extension that isn't installed, a site you can't reach from the lab machines, a syntax
error you can't yet read. Discover those now, not in week two with a real model in the file.

Keep the sketch until the real diagram replaces it, then delete it.

## Step 5 — Start reading the domain document

`OPTIONS-MARKETS.md` is the assignment's real input. Read it the way its own §0 tells you to —
with a commit after each reading pass, not once at the end. Your marked-up copy of it is itself
graded (rubric item 1), and its commit history is the evidence that the reading was done as
reading, not reconstructed the night before.

From here the work is the assignment proper: model, write the rationale, commit as you go.

## Step 6 — Submission day

Before you run the munger, check your repository against this list:

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

Then:

```
git add -A
git commit -m "..."          # your last commit before submitting
python3 munger.py            # answer 1 - take-home
```

Open the bundle one more time and re-check the four things from Step 3. Then upload
`<ID>_<Name>_takehome_bundle.txt` to the take-home form — the URL is in §10 of the assignment
PDF — by the start of class on the day of the in-class session.

That's the whole take-home submission: nothing else to hand in, nothing to push anywhere.

## Step 7 — In-class session day

Bring a laptop with your repository on it, with Python working. You answer questions in an exam
form, opened at the start, with AI assistants off, and at the end you upload a second bundle.

- **Part A** is where your take-home is assessed: in-class questions about the model *you*
  submitted, with your answers graded together with your take-home bundle against rubric items 1–8. The
  take-home's 75% is earned here, in the room. Know your own design.
- **Part B** (25%) is one design task, sized for two hours, that extends your model. You answer in
  prose plus a Mermaid class diagram typed into an answer box; no sequence diagram is asked for in
  class. One diagram tool is permitted, named on the task sheet you'll be given.
- **The in-class bundle.** At the end of the in-class session, commit again and re-run `munger.py`, this
  time answering **2**. That writes `<ID>_<Name>_inclass_bundle.txt`, which goes to a **separate
  in-class form** handed out during the in-class session, before time is called.

---

## If something goes wrong

**"No .git directory found here"** — you're not in your repository root. `cd` to the directory
containing `.git` and re-run.

**Your commit history shows commits you didn't make** — you are working inside a clone of the
package repository. Copy your files into a fresh directory, `git init` there, and commit your work
again (Step 1). Do it early: the history is graded.

**You uploaded the wrong file** — tell me as soon as you notice. The take-home bundle's name ends
in `_takehome_bundle.txt` and goes to the take-home form; the in-class bundle's name ends in
`_inclass_bundle.txt` and goes to the in-class form.

**Bundled 0 files** — you're either in the wrong directory or your files use extensions the script
doesn't recognize. Check the tree section: if your files aren't listed there either, it's the
directory. If they're in the tree but not bundled, email me — **do not edit the script**, it is
checksummed.

**Your diagram tool exports a file type that isn't bundled** — don't submit the export; commit the
Mermaid *script* (a `.mmd` file, or a `mermaid` code block in a `.md` file). Exports are for your
eyes only.

**Your bundle is enormous** — expect well under 200 KB: this is a repository of Markdown and
Mermaid, not code. Much past that means something generated got swept in: check the tree for a
directory that shouldn't be there, and tell me what it is; the exclusion list may need one more
entry.
