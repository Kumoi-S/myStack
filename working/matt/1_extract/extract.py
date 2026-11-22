"""Extract Matt Pocock's published skills into the sibling output directory."""

import io
import json
import stat
import subprocess
import sys
import tarfile
from hashlib import file_digest, sha256
from pathlib import Path, PurePosixPath
from shutil import rmtree
from tempfile import TemporaryDirectory, mkdtemp


CACHE_FILE = Path(".extract-state.json")


def entry_mode(path: Path) -> int:
    info = path.lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    if stat.S_ISLNK(info.st_mode) or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f"Unexpected filesystem link: {path}")
    return info.st_mode


def file_sha256(path: Path) -> str:
    if not stat.S_ISREG(entry_mode(path)):
        raise ValueError(f"Expected a regular file: {path}")
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def inventory(directory: Path) -> dict[Path, str | None]:
    if not stat.S_ISDIR(entry_mode(directory)):
        raise ValueError(f"Expected a directory: {directory}")

    entries = {}
    for child in directory.iterdir():
        name = Path(child.name)
        if stat.S_ISDIR(entry_mode(child)):
            entries[name] = None
            entries.update({name / path: digest for path, digest in inventory(child).items()})
        else:
            entries[name] = file_sha256(child)
    return entries


def tree_sha256(entries: dict[Path, str | None]) -> str:
    ordered = sorted((path.as_posix(), digest) for path, digest in entries.items())
    return sha256(json.dumps(ordered).encode("ascii")).hexdigest()


def git_directory(upstream: Path) -> Path:
    dot_git = upstream / ".git"
    if dot_git.is_dir():
        return dot_git.resolve(strict=True)
    prefix, _, location = dot_git.read_text(encoding="utf-8").strip().partition(":")
    if prefix != "gitdir" or not location.strip():
        raise ValueError(f"Invalid Git directory pointer: {dot_git}")
    return (upstream / location.strip()).resolve(strict=True)


def git(upstream: Path, *args: str) -> bytes:
    result = subprocess.run(
        [
            "git", "--no-replace-objects", "--literal-pathspecs",
            f"--git-dir={git_directory(upstream)}", f"--work-tree={upstream}", *args,
        ],
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode(encoding="utf-8", errors="replace").strip()
        raise OSError(f"git {args[0]} failed: {detail}")
    return result.stdout


def head_commit(upstream: Path) -> str:
    return git(upstream, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()


def read_release(upstream: Path, commit: str) -> tuple[str, dict[str, PurePosixPath]]:
    manifest_path = ".claude-plugin/plugin.json"
    manifest = json.loads(git(upstream, "show", f"{commit}:{manifest_path}"))
    if not isinstance(manifest, dict):
        raise ValueError(f"Invalid release manifest: {manifest_path}")
    version = manifest.get("version")
    published = manifest.get("skills")
    if not isinstance(version, str) or not version or not isinstance(published, list) or not published:
        raise ValueError(f"Expected a version and a nonempty skills list in {manifest_path}")

    skills = {}
    names = {"license", CACHE_FILE.name.casefold()}
    for item in published:
        if not isinstance(item, str):
            raise ValueError(f"Invalid skill path: {item!r}")
        relative = PurePosixPath(item)
        if (
            len(relative.parts) < 2
            or relative.parts[0] != "skills"
            or ".." in relative.parts
            or "\\" in item
            or ":" in item
        ):
            raise ValueError(f"Expected a path under skills/: {item}")

        name = relative.name
        if name.casefold() in names:
            raise ValueError(f"Conflicting output name: {name}")
        skills[name] = relative
        names.add(name.casefold())
    return version, skills


def existing_output(output: Path) -> dict[Path, str | None]:
    try:
        output.lstat()
    except FileNotFoundError:
        return {}
    return inventory(output)


def build_output(
    upstream: Path, commit: str, skills: dict[str, PurePosixPath], scratch: Path
) -> Path:
    paths = [path.as_posix() for path in skills.values()]
    archive = git(upstream, "archive", "--format=tar", commit, "--", "LICENSE", *paths)
    sources = scratch / "sources"
    sources.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        members = tar.getmembers()
        for member in members:
            if (
                not (member.isdir() or member.isfile())
                or "\\" in member.name
                or ":" in member.name
            ):
                raise ValueError(f"Unexpected archive entry: {member.name}")
        tar.extractall(sources, members, filter="data")

    candidate = scratch / "output"
    candidate.mkdir()
    license_path = sources / "LICENSE"
    if not license_path.is_file():
        raise ValueError(f"Missing LICENSE in {commit}")
    license_path.rename(candidate / "LICENSE")
    for name, path in skills.items():
        source = sources.joinpath(*path.parts)
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing SKILL.md in {commit}: {path}")
        source.rename(candidate / name)
    return candidate


def install_output(candidate: Path, output: Path, original: dict[Path, str | None]) -> None:
    if not output.exists(follow_symlinks=False):
        if original:
            raise ValueError(f"Output changed during extraction: {output}")
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
        if inventory(previous) != original:
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


def extract(upstream: Path, output: Path) -> str:
    commit = head_commit(upstream)
    current = existing_output(output)
    previous_commit = None
    if CACHE_FILE in current:
        cache = json.loads((output / CACHE_FILE).read_text(encoding="utf-8"))
        if not isinstance(cache, dict) or not isinstance(cache.get("commit"), str):
            raise ValueError(f"Invalid extraction cache in {output}")
        payload = {path: digest for path, digest in current.items() if path != CACHE_FILE}
        if cache.get("tree_sha256") != tree_sha256(payload):
            raise ValueError(f"Output has local changes. Move it aside before extracting: {output}")
        previous_commit = cache["commit"]
        if previous_commit == commit:
            return f"Using cached output for {commit[:12]}: {output}"

    version, skills = read_release(upstream, commit)
    with TemporaryDirectory(prefix=".extract-", dir=output.parent) as staging:
        scratch = Path(staging).resolve(strict=True)
        if scratch.parent != output.parent:
            raise ValueError(f"Unexpected staging location: {scratch}")
        candidate = build_output(upstream, commit, skills, scratch)
        payload = inventory(candidate)
        if previous_commit is None and current and current != payload:
            raise ValueError(f"Output differs from the release. Move it aside before extracting: {output}")
        cache = {"commit": commit, "tree_sha256": tree_sha256(payload)}
        (candidate / CACHE_FILE).write_text(json.dumps(cache, indent=2) + "\n", encoding="utf-8")
        if head_commit(upstream) != commit:
            raise ValueError("Matt's HEAD changed during extraction. Run the script again.")
        install_output(candidate, output, current)

    action = "Extracted"
    if previous_commit is not None:
        action = "Updated"
    elif current:
        action = "Cached"
    return f"{action} {len(skills)} skills from v{version} ({commit[:12]}): {output}"


def main() -> int:
    stage = Path(__file__).resolve().parent
    upstream = stage.parents[2] / "sources" / "mattpocock-skills"
    output = stage / "output"
    try:
        message = extract(upstream, output)
    except (OSError, ValueError, tarfile.TarError) as error:
        print(f"Extraction failed: {error}", file=sys.stderr)
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
