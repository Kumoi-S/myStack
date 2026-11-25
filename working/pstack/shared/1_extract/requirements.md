# Stage 1 — Extract the pstack Claude Code snapshot

## Goal

Produce a reproducible pstack Claude Code snapshot in `./output/` for Stage 2. Keep `./extract.py` alongside it as the reusable tool for producing and refreshing the snapshot.

## Context & Inputs

- **Target snapshot.** Use `harness/pstack/claude-code/` from the `sources/cursor-plugins/` submodule. The gitlink recorded in the parent repository's index selects the upstream commit.
- **Previous snapshot.** Use `output/` committed in the parent repository's `HEAD` to decide whether an existing snapshot can be safely replaced.
- **Upstream update.** After checking out a newer commit in the submodule, stage its gitlink from the parent repository root with `git add -- sources/cursor-plugins`.

Run the extraction tool from the repository root.

```powershell
uv run --locked working/pstack/shared/1_extract/extract.py
```

## Constrain

- Require the submodule's checked-out `HEAD` to match the selected commit. Check the entire submodule for staged changes, unstaged changes, and non-ignored untracked files. Stop if the revision differs or any such changes exist.
- Extract the committed subtree as-is. Reject a missing or empty source subtree, links, and unsupported entries.
- Build each new snapshot in a temporary directory. Verify the complete path set and exact file bytes against the selected Git subtree. On Unix-like systems, also verify executable bits.
- Recheck the selected commit and submodule cleanliness before installing the candidate. Preserve any output that appeared or changed during extraction. If installation fails after moving existing output aside, restore it. If restoration fails, report the backup path.

After validating the source, apply the first matching case.

| State of `output/` | Required behavior |
| --- | --- |
| Matches the target tree | Reuse it in place. |
| Is missing or empty | Install the target snapshot. |
| Matches the snapshot committed in the parent repository's `HEAD` | Reuse it if the committed snapshot already matches the target. Otherwise install the target snapshot. |
| Any other nonempty output | Stop and report local changes. Preserve the directory. |

Accept normal Git checkout line-ending conversions when comparing the working copy with the committed snapshot.

## Done Check

- A successful run leaves the complete verified subtree directly in `./output/`, including the Claude Code adapter used in Stage 4 of the [generic fork](../../forks/generic/4_cursor_replacement_generalization/requirements.md) and the [Codex fork](../../forks/codex/4_cursor_replacement_generalization/requirements.md).
- An unchanged rerun reuses the snapshot. A clean upstream update with a staged gitlink replaces a clean older snapshot.
- A rejected source or output validation returns a nonzero exit and preserves any existing output.

## Proof to Show

- Show the extraction command, selected commit, and reported outcome. For a new or refreshed snapshot, include the extracted file count and the result of comparing the installed tree with the selected Git subtree.
- For a rejected run, show the reason, the nonzero exit status, and the check that the existing output was preserved.
