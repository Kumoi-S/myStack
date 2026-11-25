"""Extract pstack's Claude Code agents and skills."""

import sys
from pathlib import Path

STAGE = Path(__file__).resolve().parent
WORKING = STAGE.parents[1]
sys.path.insert(0, str(WORKING / "tools"))
from extract_selection import extract_directories


def main() -> None:
    source = WORKING.parent / "sources/cursor-plugins/harness/pstack/claude-code"
    extract_directories(STAGE, [source / "agents", source / "skills"])
    print(f"Extracted agents and skills to {STAGE / 'output'}")


if __name__ == "__main__":
    main()
