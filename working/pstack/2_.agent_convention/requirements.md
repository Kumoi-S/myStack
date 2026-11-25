# Stage 2 — pstack `.agent/` paths

Read `../1_extract_and_pick/output/` and write `./output/`. Resolve `.agent/` paths from the target checkout root.

| Workflow | Current path | New default |
| --- | --- | --- |
| [Decision log](../1_extract_and_pick/output/skills/show-me-your-work/SKILL.md) · [guide](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/guide/07-overnight.md) | `decisions.tsv` or `.audit/<task-slug>.tsv` | `.agent/decisions.tsv` or `.agent/audit/<task-slug>.tsv`. Use the same log on pickup. |
| [Hillclimb](../1_extract_and_pick/output/skills/poteto-mode/playbooks/hillclimb.md) | `decision.tsv` | `.agent/decision.tsv` |
| [Pause and resume](../1_extract_and_pick/output/skills/poteto-mode/playbooks/pause-safely.md) | `/tmp/<slug>-resume.md` | `<os.tmpdir>/<slug>-resume.md` |
| [Arena](../1_extract_and_pick/output/skills/arena/SKILL.md) | Worktree or `/tmp/arena-<slug>/candidate-<n>/` | Worktree first, then `<os.tmpdir>/arena-<slug>/candidate-<n>/` |
| [Prototype](../1_extract_and_pick/output/skills/poteto-mode/playbooks/prototype.md) | Isolated scratch directory | `.agent/prototype/` for standalone prototypes. Use a separate Git worktree when the prototype needs the project's source layout, build, or runtime. |
| [Verification](../1_extract_and_pick/output/skills/maintain-verification-skill/SKILL.md) | Scratch notes, disposable data, and proof at skill-defined paths | Notes and proof in `.agent/verify-<app>/<run-id>/`. Use `<os.tmpdir>/notes-verify-$RUN_ID` for Notes example data. Keep proof through teardown. |
| [Statechart](../1_extract_and_pick/output/skills/statechart/SKILL.md) | Scratch directory outside the repo | `<os.tmpdir>/statechart-<run-id>/`. Honor `--out`. |
| [Ketchup video](../1_extract_and_pick/output/skills/ketchup-video/SKILL.md) | Render outside the repo | `<os.tmpdir>/ketchup-video-<run-id>/` |

## Examples

| Source | Original | Replacement |
| --- | --- | --- |
| [Decision log](../1_extract_and_pick/output/skills/show-me-your-work/SKILL.md) | Keep it at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once, and leave it out of git. | Keep it at `.agent/decisions.tsv`, or `.agent/audit/<task-slug>.tsv` when several efforts run at once, and leave it out of git. |
| [Pause and resume](../1_extract_and_pick/output/skills/poteto-mode/playbooks/pause-safely.md) | For the compaction trigger write it to a file like `/tmp/<slug>-resume.md`. | For the compaction trigger write it to a file like `<os.tmpdir>/<slug>-resume.md`. |
| [Prototype](../1_extract_and_pick/output/skills/poteto-mode/playbooks/prototype.md) | Build throwaway in an isolated scratch dir, separate from production source. | Build a standalone prototype in an isolated directory under `.agent/prototype/`. Use a separate Git worktree when the prototype needs the project's source layout, build, or runtime. |
