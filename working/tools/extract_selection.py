"""Replace a stage's generated output with the selected directories."""

from collections.abc import Iterable
from pathlib import Path
from shutil import copytree, rmtree
from tempfile import mkdtemp


def extract_directories(stage: Path, sources: Iterable[Path]) -> None:
    stage = stage.resolve(strict=True)
    output = stage / "output"
    if output.resolve() != output:
        raise ValueError(f"Expected a local output directory: {output}")
    staging = Path(mkdtemp(prefix=".extract-", dir=stage)).resolve(strict=True)
    if staging.parent != stage:
        raise ValueError(f"Unexpected staging directory: {staging}")
    candidate = staging / "new"
    previous = staging / "previous"
    try:
        candidate.mkdir()
        for source in sources:
            copytree(source, candidate / source.name, symlinks=True)
        if output.exists():
            output.rename(previous)
        try:
            candidate.rename(output)
        except OSError:
            if previous.exists():
                previous.rename(output)
            raise
        if previous.exists():
            rmtree(previous)
    finally:
        if not previous.exists():
            rmtree(staging)
