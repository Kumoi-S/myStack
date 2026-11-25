"""Extract Matt's published skills and the three selected writing skills."""

import json
import sys
from pathlib import Path

STAGE = Path(__file__).resolve().parent
WORKING = STAGE.parents[1]
sys.path.insert(0, str(WORKING / "tools"))
from extract_selection import extract_directories

WRITING_SKILLS = ("writing-beats", "writing-fragments", "writing-shape")


def main() -> None:
    upstream = WORKING.parent / "sources" / "mattpocock-skills"
    skills = upstream / "skills"
    manifest = json.loads((upstream / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    published = [upstream / item for item in manifest["skills"]]
    if not published:
        raise ValueError("The published skills list is empty")
    published_names = {path.name.casefold() for path in published}
    selected = published + [
        skills / "in-progress" / name for name in WRITING_SKILLS if name not in published_names
    ]
    for path in selected:
        if not path.resolve().is_relative_to(skills) or not (path / "SKILL.md").is_file():
            raise ValueError(f"Invalid skill directory: {path}")
    if len({path.name.casefold() for path in selected}) != len(selected):
        raise ValueError("Selected skills have conflicting directory names")
    extract_directories(STAGE, selected)
    print(f"Extracted {len(selected)} skills to {STAGE / 'output'}")


if __name__ == "__main__":
    main()
