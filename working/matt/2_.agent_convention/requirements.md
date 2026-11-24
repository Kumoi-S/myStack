# Stage 2 — Matt Pocock `.agent/` paths

Read `../1_extract/output/` and write `./output/`. Resolve `.agent/` paths from the target checkout root. Update readers, templates, and pointers together. Read existing project docs as references and honor explicit output destinations.

| Workflow | Current path | New default |
| --- | --- | --- |
| [Handoff](../1_extract/output/handoff/SKILL.md) | OS temp directory | `<os.tmpdir>/` |
| [Architecture report](../1_extract/output/improve-codebase-architecture/SKILL.md) · [report guide](../1_extract/output/improve-codebase-architecture/HTML-REPORT.md) | OS temp directory | `<os.tmpdir>/architecture-review-<timestamp>.html` |
| [Prototype](../1_extract/output/prototype/SKILL.md) | Near the module or page being prototyped | `.agent/prototype/` for standalone prototypes. Use a separate Git worktree when the prototype needs the project's source layout, build, or runtime. Capture the prototype on its branch. |
| [One-off wizard](../1_extract/output/wizard/SKILL.md) | Scratch directory or `scripts/` | `.agent/wizard/` |
| [Standalone diagnosis harness](../1_extract/output/diagnosing-bugs/SKILL.md) | Scratch location | `.agent/diagnosing-bugs/` |
| [Implementation exploration notes](../1_extract/output/implement-spec/SKILL.md) | Shared location | `.agent/implement-spec/` when workers can read it |
| [Local Markdown tracker](../1_extract/output/setup-matt-pocock-skills/issue-tracker-local.md) · [setup](../1_extract/output/setup-matt-pocock-skills/SKILL.md) | `.scratch/<feature>/` | `.agent/scratch/<feature>/` for new setups. Existing projects use their configured tracker path. |
| [Skill setup docs](../1_extract/output/setup-matt-pocock-skills/SKILL.md) | `docs/agents/{issue-tracker,domain,triage-labels}.md` | `.agent/{issue-tracker,domain,triage-labels}.md` |
| [Glossary and context map](../1_extract/output/domain-modeling/GLOSSARY-FORMAT.md) | Root `GLOSSARY.md` or `GLOSSARY-MAP.md` with `src/<context>/GLOSSARY.md` | `.agent/GLOSSARY.md` or `.agent/GLOSSARY-MAP.md` with `.agent/contexts/<context>/GLOSSARY.md` |
| [ADRs](../1_extract/output/domain-modeling/ADR-FORMAT.md) | `docs/adr/` and `src/<context>/docs/adr/` | `.agent/adr/` and `.agent/contexts/<context>/adr/` |
| [Research notes](../1_extract/output/research/SKILL.md) | Existing repo notes location or a path chosen by the agent | `.agent/research/` |

## Examples

| Source | Original | Replacement |
| --- | --- | --- |
| [Local Markdown tracker](../1_extract/output/setup-matt-pocock-skills/issue-tracker-local.md) | One feature per directory: `.scratch/<feature-slug>/` | Use one directory per feature at `.agent/scratch/<feature-slug>/`. |
| [Glossary](../1_extract/output/domain-modeling/GLOSSARY-FORMAT.md) | One `GLOSSARY.md` at the repo root. | One glossary at `.agent/GLOSSARY.md`. |
| [Prototype](../1_extract/output/prototype/SKILL.md) | Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. | Put standalone prototype code in `.agent/prototype/` and give it a name that identifies it as a prototype. Use a separate Git worktree when the prototype needs the project's source layout, build, or runtime. |
