"""Remove .gitkeep placeholders from directories Git can retain through other files."""

import argparse
import os
import subprocess
from pathlib import Path

MARKER = ".gitkeep"


def git_paths(*args: str) -> set[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z", *args])
    return {Path(os.fsdecode(name)) for name in output.split(b"\0") if name}


def redundant_markers(paths: set[Path]) -> set[Path]:
    markers = {path for path in paths if path.name == MARKER}
    populated = {
        parent for path in paths for parent in path.parents
        if path.name != MARKER or parent != path.parent
    }
    return {marker for marker in markers if marker.parent in populated}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="also clean the pending commit")
    args = parser.parse_args()

    root = Path(os.fsdecode(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).rstrip(b"\n\r")))
    os.chdir(root)
    indexed = git_paths("--cached")
    worktree = (indexed - git_paths("--deleted")) | git_paths("--others", "--exclude-standard")
    remove = redundant_markers(worktree)
    if args.staged:
        staged = redundant_markers(indexed)
        # An unstaged sibling cannot keep this directory in the pending commit.
        remove -= indexed - staged
        if staged:
            paths = b"".join(os.fsencode(path.as_posix()) + b"\0" for path in sorted(staged))
            subprocess.run(
                ["git", "--literal-pathspecs", "rm", "--cached", "--force", "--quiet",
                 "--pathspec-from-file=-", "--pathspec-file-nul"],
                input=paths, check=True,
            )

    for path in sorted(remove):
        if path.parent.resolve() == root / path.parent and (path.is_symlink() or path.is_file()):
            path.unlink()
            print(f"Removed {path.as_posix()}")


if __name__ == "__main__":
    main()
