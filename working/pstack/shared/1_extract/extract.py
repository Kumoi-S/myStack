"""Extract the pinned pstack Claude Code harness into the sibling output directory.

The parent index selects the source commit. The committed output is the
baseline for deciding whether an older snapshot can be replaced.
"""

import io
import stat
import subprocess
import sys
import tarfile
from hashlib import new as new_hash
from json import dumps
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory, mkdtemp


SOURCE = "sources/cursor-plugins"
HARNESS = "harness/pstack/claude-code"

type Inventory = dict[str, tuple[str, str]]


def git(worktree: Path, *args: str, stdin: bytes | None = None) -> bytes:
    gitdir = worktree / ".git"
    if gitdir.is_file():
        prefix, _, location = gitdir.read_text(encoding="utf-8").strip().partition(":")
        if prefix != "gitdir" or not location.strip():
            raise ValueError(f"Invalid Git directory pointer: {gitdir}")
        gitdir = worktree / location.strip()
    if not gitdir.is_dir():
        raise ValueError(f"Missing Git checkout at {worktree}")
    result = subprocess.run(
        [
            "git", "--no-replace-objects", "--literal-pathspecs", "--no-optional-locks",
            f"--git-dir={gitdir.resolve()}", f"--work-tree={worktree}", *args,
        ],
        cwd=worktree,
        capture_output=True,
        input=stdin,
    )
    if result.returncode:
        detail = result.stderr.decode(encoding="utf-8", errors="replace").strip()
        raise OSError(f"git {args[0]} failed at {worktree}: {detail}")
    return result.stdout


def clean_source_commit(root: Path, upstream: Path) -> str:
    entry = git(root, "ls-files", "--stage", "-z", "--", SOURCE)
    metadata, _, path = entry.partition(b"\t")
    fields = metadata.split()
    if path != SOURCE.encode() + b"\0" or len(fields) != 3 or fields[0] != b"160000" or fields[2] != b"0":
        raise ValueError(f"Expected a submodule commit for {SOURCE} in the parent Git index")

    pinned = fields[1].decode("ascii")
    checked_out = git(upstream, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    if checked_out != pinned:
        raise ValueError(f"{SOURCE} HEAD is {checked_out[:12]}, but the parent index pins {pinned[:12]}")
    diff = ("diff", "--no-ext-diff", "--no-textconv", "--name-status", "--ignore-submodules=none")
    changes = (
        git(upstream, *diff, "--cached")
        + git(upstream, *diff)
        + git(upstream, "ls-files", "--others", "--exclude-standard")
    )
    if changes:
        raise ValueError(f"{SOURCE} has local changes:\n{changes.decode('utf-8', errors='replace').rstrip()}")
    return pinned


def tree_inventory(worktree: Path, tree: str) -> Inventory:
    entries = {}
    for entry in git(worktree, "ls-tree", "-rtz", tree).split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, _, oid = metadata.decode("ascii").split()
        name = path.decode("utf-8")
        if mode == "040000":
            entries[name] = (mode, "")
        elif mode in {"100644", "100755"}:
            entries[name] = (mode if sys.platform != "win32" else "", oid)
        else:
            raise ValueError(f"Unsupported Git entry in {tree}: {name} ({mode})")
    return entries


def disk_inventory(directory: Path, object_format: str) -> Inventory:
    def scan(path: Path) -> tuple[str, str]:
        info = path.lstat()
        attributes = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Unexpected filesystem link: {path}")
        if stat.S_ISDIR(info.st_mode):
            for child in path.iterdir():
                entries[child.relative_to(directory).as_posix()] = scan(child)
            return "040000", ""
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"Expected a regular file: {path}")
        content = path.read_bytes()
        digest = new_hash(object_format, f"blob {len(content)}\0".encode("ascii"))
        digest.update(content)
        mode = "100755" if info.st_mode & stat.S_IXUSR else "100644"
        return mode if sys.platform != "win32" else "", digest.hexdigest()

    entries: Inventory = {}
    if scan(directory)[0] != "040000":
        raise ValueError(f"Expected a directory: {directory}")
    return entries


def install_output(candidate: Path, output: Path, original: Inventory | None, object_format: str) -> None:
    if original is None:
        if output.exists(follow_symlinks=False):
            raise ValueError(f"Output appeared during extraction: {output}")
        candidate.rename(output)
        return

    backup = Path(mkdtemp(prefix=".extract-previous-", dir=output.parent)).resolve(strict=True)
    if backup.parent != output.parent:
        raise ValueError(f"Unexpected backup location: {backup}")
    previous = backup / output.name
    try:
        output.rename(previous)
    except OSError:
        backup.rmdir()
        raise
    try:
        if disk_inventory(previous, object_format) != original:
            raise ValueError(f"Output changed during extraction: {output}")
        candidate.rename(output)
    except BaseException:
        try:
            previous.rename(output)
        except OSError as error:
            raise OSError(f"Could not restore output. Previous files are at {previous}") from error
        backup.rmdir()
        raise
    rmtree(backup)


def extract(root: Path, output: Path) -> str:
    upstream = root / SOURCE
    commit = clean_source_commit(root, upstream)
    tree = f"{commit}:{HARNESS}"
    object_format = git(upstream, "rev-parse", "--show-object-format").decode("ascii").strip()
    expected = tree_inventory(upstream, tree)
    if not expected:
        raise ValueError(f"Empty harness tree: {tree}")

    current = disk_inventory(output, object_format) if output.exists(follow_symlinks=False) else None
    if current == expected:
        return f"Using existing output for {commit[:12]}: {output}"

    if current:
        relative = output.relative_to(root).as_posix()
        previous = tree_inventory(root, f"HEAD:{relative}") if git(root, "ls-tree", "HEAD", "--", relative) else {}
        if current != previous:
            same_paths_and_modes = current.keys() == previous.keys() and all(
                entry[0] == previous[path][0] for path, entry in current.items()
            )
            if not same_paths_and_modes:
                raise ValueError(f"Output has local changes: {output}")
            # Compare through Git's clean filters for checkouts with converted line endings.
            changed = [path for path in current if current[path] != previous[path]]
            paths = "".join(dumps(f"{relative}/{path}", ensure_ascii=False) + "\n" for path in changed)
            hashes = git(root, "hash-object", "--stdin-paths", stdin=paths.encode("utf-8")).decode("ascii").splitlines()
            if hashes != [previous[path][1] for path in changed]:
                raise ValueError(f"Output has local changes: {output}")
        if previous == expected:
            return f"Using existing output for {commit[:12]}: {output}"

    archive = git(upstream, "archive", "--format=tar", tree)
    with TemporaryDirectory(prefix=".extract-", dir=output.parent) as staging:
        scratch = Path(staging).resolve(strict=True)
        if scratch.parent != output.parent:
            raise ValueError(f"Unexpected staging location: {scratch}")
        candidate = scratch / "output"
        candidate.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
            members = tar.getmembers()
            for member in members:
                if not (member.isdir() or member.isfile()) or "\\" in member.name or ":" in member.name:
                    raise ValueError(f"Unexpected archive entry: {member.name}")
            tar.extractall(candidate, members, filter="data")
        if disk_inventory(candidate, object_format) != expected:
            raise ValueError(f"Archive differs from its committed Git tree: {tree}")
        if clean_source_commit(root, upstream) != commit:
            raise ValueError(f"{SOURCE} changed during extraction. Run the script again.")
        install_output(candidate, output, current, object_format)

    file_count = sum(mode != "040000" for mode, _ in expected.values())
    return f"Extracted {file_count} files from {commit[:12]}: {output}"


def main() -> int:
    stage = Path(__file__).resolve().parent
    try:
        print(extract(stage.parents[3], stage / "output"))
    except (OSError, ValueError, tarfile.TarError) as error:
        print(f"Extraction failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
