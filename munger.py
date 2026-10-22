"""Bundles your repository into a single .txt file for submission.

Run this from the ROOT of your project repository:

    python3 munger.py

It asks for your student ID, your name, and which submission this is, then
writes <ID>_<Name>_takehome_bundle.txt or <ID>_<Name>_inclass_bundle.txt
containing your git commit history, your project tree, and the contents of
every Markdown, Mermaid, and notes file it finds.

The take-home and in-class submissions go to DIFFERENT Google Forms. Upload
each bundle through the form for that submission.

DO NOT MODIFY THIS FILE. Every bundle records the SHA-256 of the script that
produced it, and that digest is checked against the published one when your
submission is graded. A modified munger is treated as a submission integrity
problem, not a clever workaround.

Files that are not readable as text - images, PDFs, drawing-tool exports - are
listed by name under FILES NOT BUNDLED rather than included. A class diagram
that exists only as an image cannot be graded: commit it as Mermaid script.

It is still your responsibility to open the bundle and confirm your work is in
it before you upload. If this script misses something your project needs
included, email the instructor - do not edit the script.
"""

import hashlib
import os
import re
import subprocess

# Configure what to include/exclude
ALLOWED_EXTENSIONS = {
    # C / C++
    '.h', '.hpp', '.hh', '.c', '.cpp', '.cc', '.cxx',
    # JVM
    '.java', '.kt', '.kts', '.gradle',
    # Python
    '.py', '.toml', '.cfg',
    # JavaScript / TypeScript
    '.js', '.mjs', '.cjs', '.ts',
    # .NET
    '.cs', '.csproj',
    # Swift
    '.swift',
    # notes, design, config - this is a design repository, but a stray
    # scratch file in any of these languages still belongs in the bundle
    # if you put one in your repo
    '.md', '.txt', '.json', '.xml', '.yml', '.yaml',
    '.mmd', '.puml', '.uml', '.dot', '.pseudo',
}

IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 'bin', 'obj', 'out', 'build', 'node_modules',
    '__pycache__', 'target', '.gradle', 'cmake-build-debug', 'cmake-build-release',
    '.pytest_cache', '.mypy_cache', '.ruff_cache', 'venv', '.venv', 'env',
    'dist', '_build', 'coverage', '.tox', 'Debug', 'Release',
}


def clean_string(text):
    """Removes special characters to create a safe filename."""
    return re.sub(r'[^a-zA-Z0-9]', '_', text.strip())


def is_bundle(filename):
    """True for any bundle this script has produced.

    Matches previous runs as well as the current one, so that the in-class
    bundle does not end up containing the whole take-home bundle.

    @param filename a bare filename, not a path
    @return whether the file is a munger bundle
    """
    return filename.endswith('_bundle.txt')


def generate_tree(dir_path, prefix=""):
    """Recursively builds a string representation of the directory structure."""
    tree_str = ""
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return ""

    # Filter out hidden files, ignored directories, and any bundle files
    items = [i for i in items if not i.startswith('.') and not is_bundle(i) and not (os.path.isdir(os.path.join(dir_path, i)) and i in IGNORE_DIRS)]

    for i, item in enumerate(items):
        path = os.path.join(dir_path, item)
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "

        tree_str += f"{prefix}{connector}{item}\n"

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            tree_str += generate_tree(path, prefix + extension)
    return tree_str


def classify_files(root_dir):
    """Walks the project once, splitting files into bundled and not-bundled.

    Anything whose extension is not a known text type - images, PDFs, drawing-
    tool files - cannot go into a text bundle. Those are reported by name and
    size instead of being silently dropped, so a diagram that exists only as a
    PNG is visible as a problem rather than as an absence.

    @param root_dir the project root to walk
    @return a (to_bundle, skipped) pair; to_bundle holds (path, relative path)
            and skipped holds (relative path, size in bytes)
    """
    to_bundle, skipped = [], []

    for current_dir, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = sorted(d for d in dirs
                         if not d.startswith('.') and d not in IGNORE_DIRS)

        for file in sorted(files):
            if file.startswith('.') or is_bundle(file):
                continue
            filepath = os.path.join(current_dir, file)
            rel_path = os.path.relpath(filepath, root_dir)

            if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                to_bundle.append((filepath, rel_path))
            else:
                try:
                    size = os.path.getsize(filepath)
                except OSError:
                    size = 0
                skipped.append((rel_path, size))

    return to_bundle, skipped


def self_digest():
    """SHA-256 of this script, so a grader can confirm it wasn't modified."""
    try:
        with open(os.path.abspath(__file__), 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        return f"[could not hash munger.py: {e}]"


def get_git_log(root_dir):
    """Returns this repo's commit history, or a note explaining why it can't."""
    if not os.path.isdir(os.path.join(root_dir, '.git')):
        return ("[No .git directory found here. Run this script from your repository\n"
                " root. If you didn't use git, your commit history is a graded\n"
                " component and cannot be credited.]\n")
    try:
        result = subprocess.run(
            ['git', 'log', '--date=short', '--pretty=format:%h  %ad  %an  %s'],
            cwd=root_dir, capture_output=True, text=True, timeout=30
        )
        log = result.stdout.strip()
        if not log:
            return "[Git repository found, but it has no commits.]\n"
        count = len(log.splitlines())
        return f"{log}\n\n({count} commits)\n"
    except Exception as e:
        return f"[Could not read git history: {e}]\n"


def ask_submission_kind():
    """Asks which of the two submissions this bundle is for.

    The take-home and in-class bundles go to DIFFERENT Google Forms and are
    graded against different parts of the exam, so they must be
    distinguishable from the filename alone.

    @return a (slug, description) pair, or None if the answer was unusable
    """
    print("\nWhich submission is this?")
    print("  1. Take-home  - the model you built for the take-home, due at the start of class")
    print("  2. In-class   - Part B, the extension you designed during the in-class session")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        return ("takehome", "take-home (due at the start of class)")
    if choice == "2":
        return ("inclass", "in-class Part B (due before the in-class session ends)")
    return None


def main():
    print("=== CSC 582 Submission Bundler ===")
    student_id = input("Enter your Student ID: ").strip()
    student_name = input("Enter your First and Last Name: ").strip()

    if not student_id or not student_name:
        print("Error: Name and ID are required.")
        return

    kind = ask_submission_kind()
    if kind is None:
        print("Error: enter 1 for the take-home submission or 2 for the in-class one.")
        return
    slug, description = kind

    safe_id = clean_string(student_id)
    safe_name = clean_string(student_name)
    output_filename = f"{safe_id}_{safe_name}_{slug}_bundle.txt"

    root_dir = os.getcwd()
    to_bundle, skipped = classify_files(root_dir)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        # 1. Write the metadata header
        outfile.write(f"STUDENT NAME: {student_name}\n")
        outfile.write(f"STUDENT ID: {student_id}\n")
        outfile.write(f"SUBMISSION: {description}\n")
        outfile.write(f"MUNGER SHA-256: {self_digest()}\n")
        outfile.write("=" * 40 + "\n\n")

        # 2. Write the commit history (evidence of incremental work)
        outfile.write("GIT COMMIT HISTORY:\n")
        outfile.write(get_git_log(root_dir))
        outfile.write("\n" + "=" * 40 + "\n\n")

        # 3. Write the directory tree
        outfile.write("PROJECT STRUCTURE:\n")
        outfile.write(generate_tree(root_dir))
        outfile.write("\n" + "=" * 40 + "\n\n")

        # 4. Say plainly what could NOT be bundled, so a missing deliverable is
        #    visible rather than merely absent
        outfile.write("FILES NOT BUNDLED:\n")
        if skipped:
            for rel_path, size in skipped:
                outfile.write(f"  {rel_path:<52} {size / 1024:>8.1f} KB\n")
            outfile.write(
                "\nThese files are in the project but are not readable as text, so their\n"
                "contents are not included. If a graded deliverable is listed above - your\n"
                "class diagram, for example - it cannot be graded. Commit diagrams as\n"
                "Mermaid script: a .mmd file, or a mermaid code block in a .md file.\n")
        else:
            outfile.write("  (none - every file in the project was bundled)\n")
        outfile.write("\n" + "=" * 40 + "\n\n")

        # 5. Write the file contents
        outfile.write("SOURCE FILES:\n\n")

        for filepath, rel_path in to_bundle:
            outfile.write(f"--- START FILE: {rel_path} ---\n")
            try:
                # errors='replace' prevents crashes on weird character encodings
                with open(filepath, 'r', encoding='utf-8', errors='replace') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"[Error reading file: {e}]\n")
            outfile.write(f"\n--- END FILE: {rel_path} ---\n\n")

    own_files = [r for _, r in to_bundle if r != os.path.basename(__file__)]

    print(f"\nBundled {len(to_bundle)} files, plus git history and project tree.")
    print(f"Output saved to: {output_filename}")

    if skipped:
        print(f"\n{len(skipped)} file(s) could NOT be bundled (not readable as text):")
        for rel_path, _ in skipped[:8]:
            print(f"  {rel_path}")
        if len(skipped) > 8:
            print(f"  ... and {len(skipped) - 8} more")
        if any(r.replace('\\', '/').startswith('design/') for r, _ in skipped):
            print("\n  ^ Some of these are in design/. Diagrams submitted only as images")
            print("    cannot be graded. Commit them as Mermaid script.")

    if not own_files:
        print("\nWARNING: this bundle contains none of your work - only munger.py itself.")
        print("Are you in your project's root directory, and do your files use")
        print("extensions this script knows about? Do not submit this bundle.")
    else:
        form = "TAKE-HOME" if slug == "takehome" else "IN-CLASS"
        print("Open it, skim it, confirm your work is actually in there, then")
        print(f"upload it through the {form} submission Google Form.")
        print("The two submissions use different forms - check you have the right one.")


if __name__ == "__main__":
    main()
